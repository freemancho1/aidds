import sys
import pandas as pd
from typing import Type
from sklearn.model_selection import train_test_split

import aidds.sys.config as cfg 
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.exception import AppException
from aidds.sys.utils.evaluation import regression_evals, calculate_mape
from aidds.sys.utils.data_io import save_data, get_scaling_data, read_data


class Learning:
    """ Training 9 models and saving the best-performing model """

    def __init__(self, scaling_df_dict=None) -> Type['Learning']:
        try:
            self._logs = Logs(code='learning')
            self._sd_dict = scaling_df_dict
            self._tds = None
            self._modeling_cols = None
            self._best = {
                'model': None, 
                'score': -sys.float_info.max, 
                'mape': 0, 
                'model_key': ''
            }
            self._run()
        except Exception as e:
            raise AppException(e)
        finally:
            if hasattr(self, '_logs'):
                self._logs.stop()
                
    def _run(self) -> None:
        try:
            if not self._sd_dict:
                self._sd_dict = get_scaling_data()
            # Training dataset(train_x, test_x, train_y, test_y) + x, y
            self._tds = {
                tkey: self._sd_dict[tkey] for tkey in ['x','y']+cfg.type.tds
            }
            self._modeling_cols = self._sd_dict[cfg.modeling.cols]
                
            # Train the model while extracting the best data
            for idx in range(cfg.modeling.best.cnt):
                value = f'Index: {idx+1}, Total{self._tds["x"].shape}' \
                        f'train_x{self._tds["train_x"].shape}, ' \
                        f'test_x{self._tds["test_x"].shape}'
                self._logs.mid(code='size', value=value)
                
                for mkey in cfg.models.key:
                    self._ml_fit_and_evals(mkey=mkey)
                # Generating new optimal data
                self._gen_optimal_data()
                
            # Save best model and data
            save_data(data=self._best['model'], code='model.best')
            save_data(data=self._tds['x'], code='data.scaling.best')
            ppdf = read_data(code='data.pp.last')
            save_data(ppdf[ppdf.acc_no.isin(self._tds['x'].acc_no)],'data.pp.best')
        except Exception as e:
            raise AppException(e)
        
    def _ml_fit_and_evals(self, mkey=None) -> None:
        """ Creating and evaluating models using the given algorithm 
            and saving the best model."""
        try:
            train_x = self._tds['train_x']
            train_y = self._tds['train_y'].to_numpy()
            test_x = self._tds['test_x']
            test_y = self._tds['test_y'].to_numpy()
            
            # Get model algorithm
            model = eval(f'cfg.models.ml.{mkey}')
            model.fit(train_x[self._modeling_cols], train_y)
            pred_y = model.predict(test_x[self._modeling_cols])
            evals, _ = regression_evals(y=test_y, p=pred_y, verbose=1)
            if self._best['score'] < evals[1]:  # r2_score
                self._best = {
                    'score': evals[1], 'mape': evals[0], 
                    'model': model, 'model_key': mkey
                }
                self._logs.mid(code='best', value=self._best)
            # Save models
            save_data(data=model, code=f'model.{mkey}')
        except Exception as e:
            raise AppException(e)
        
    def _gen_optimal_data(self) -> None:
        try:
            # Predict all data using the optimal model
            test_x = self._tds['x']
            test_y = self._tds['y'].to_numpy().reshape(-1)
            model = self._best['model']
            pred_y = model.predict(test_x[self._modeling_cols])
            
            check_df = pd.DataFrame({
                'acc_no': test_x['acc_no'],
                'test': test_y,
                'pred': pred_y
            })
            check_df['mape'] = calculate_mape(check_df.test, check_df.pred)
            # Remove the bottom 15% with low accuracy(mape)
            threshold = check_df['mape'].quantile(cfg.modeling.best.per)
            check_df['best'] = check_df['mape']\
                .apply(lambda x: '*' if x < threshold else '')
            best_cond = check_df.best == '*'
            # Re-split
            self._tds['x'] = self._tds['x'][best_cond]
            self._tds['y'] = self._tds['y'][best_cond]
            self._tds['train_x'], self._tds['test_x'], \
                self._tds['train_y'], self._tds['test_y'] = \
                    train_test_split(self._tds['x'], self._tds['y'],
                                     test_size=cfg.modeling.test_size)
        except Exception as e:
            raise AppException(e)
        
