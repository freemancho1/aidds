from typing import Type
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split

import aidds.sys.config as cfg 
from aidds.sys.utils.exception import AppException
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.data_io import read_data, save_data


class Scaling:
    """ Scaling class for modeling section. """
    
    def __init__(self, pp_df=None) -> Type['Scaling']:
        try:
            self._logs = Logs(code='scaling')
            self._ppdf = pp_df 
            # Source data dictionary before scaling 
            self._data = {}
            # Scaling data + modeling_cols dictionary
            self.sdata = {}
            self._run()
        except Exception as e:
            raise AppException(e)
        finally:
            if hasattr(self, '_logs'):
                self._logs.stop()

    def _run(self) -> None:
        try:
            if self._ppdf is None:
                self._ppdf = read_data('data.pp.last', dtype={'acc_no': str})
            
            # Not to split the data by the number of poles, omitted this part.
            #
            # # Add keys for storing data in self._data and self.sdata
            # # - Generate self._data['x']={}, 'y'={}, 'train_x'={}....
            # self._data = {tkey: {} for tkey in ['x', 'y'] + cfg.type.tds}
            # self.sdata = {tkey: {} for tkey in cfg.type.tds}
            
            # Split x, y
            y = self._ppdf.pop(cfg.cols.target)
            x = self._ppdf
            self._logs.mid(code='source_x', value=x.shape)
            
            # Save modeling columns      
            # to be used for scaling in the service section.
            modeling_cols = x.columns.tolist()[1:]
            self.sdata[cfg.modeling.cols] = modeling_cols
            save_data(data=modeling_cols, code='pickle.modeling_cols')

            # Split train_x, test_x, train_y, test_y
            train_x, test_x, train_y, test_y = \
                train_test_split(x, y, test_size=cfg.modeling.test_size)
            value = f'Train{train_x.shape}, Test{test_x.shape}'
            self._logs.mid(code='split', value=value)
            
            # Save x, y, train_x, test_x, train_y, test_y
            # In the code below, the 'x' series data is scaled, so save here
            for tkey in ['x', 'y'] + cfg.type.tds:
                self._data[tkey] = eval(tkey)
                save_data(data=eval(tkey), code=f'data.split.{tkey}')
                
            # Scaling without acc_no
            scaler = StandardScaler()
            train_x[modeling_cols] = scaler.fit_transform(train_x[modeling_cols])
            test_x[modeling_cols] = scaler.transform(test_x[modeling_cols])
            # Scaling the all data to find rows with high prediction accuracy.
            x[modeling_cols] = scaler.transform(x[modeling_cols])
            
            # Save scaling data with acc_no
            for tkey in ['x', 'y'] + cfg.type.tds:
                self.sdata[tkey] = eval(tkey)
                save_data(data=eval(tkey), code=f'data.scaling.{tkey}')
                
            # Save scaler
            save_data(data=scaler, code='pickle.scaler')
        except Exception as e:
            raise AppException(e)
