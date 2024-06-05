from aidds_buy.sys import config as cfg
from aidds_buy.sys.utils import app_exception
from aidds_buy.sys.utils import modeling_logs as logs
from aidds_buy.sys.utils import get_cleaning_data
from aidds_buy.sys.utils import save_data
from aidds_buy.modeling import preprocess_module as ppm


class ModelingPreprocessing:
    """ Main preprocessing class for modeling section. """
    
    def __init__(self, cd_dict=None):
        try:
            self._logs = logs(code='preprocessing')
            # Cleaning Dataframe DICTionary
            self._cd_dict = cd_dict
            # PreProcessing DataFrame
            self.ppdf = None
            self._run()
        except Exception as e:
            raise app_exception(e)
        finally:
            if hasattr(self, '_logs'):
                self._logs.stop()
        
    def _run(self):
        try:
            if not self._cd_dict:
                self._cd_dict = get_cleaning_data()
            # Preprocessing CONS Dataset
            self._cons()
            # Preprocessing Facility Dataset
            for pkey in cfg.type.pds[1:]:
                self._facility_data(pkey=pkey)
            # Preprocessing complete:
            # - Final NaN handling, Save column info, Save preprocessing df
            self._complete()
        except Exception as e:
            raise app_exception(e)
        
    def _cons(self):
        """ Preprocessing CONS dataset for modeling section. """
        _logs = logs(code='preprocessing.cons')
        try:
            cons_df = self._cd_dict[cfg.type.pds[0]]
            _logs.mid(code='source', value=cons_df.shape)
            # Preprocessing CONS dataset using common modules
            cons_df = ppm.cons(cons_df=cons_df)
            
            # Generate and save a list of office_codes
            # to be used for preprocessing in the service section.
            office_codes = cons_df.office_cd.unique().tolist()
            save_data(data=office_codes, code='pickle.office_codes')
            # Generate office_id using office_codes(index value)
            office_ids = [office_codes.index(cd) for cd in cons_df.office_cd]
            # Add 'office_id' column
            cons_df['office_id'] = office_ids
            # Remove 'office_cd' column
            cons_df.drop(columns=['office_cd'], inplace=True)
            _logs.mid(code='result', value=cons_df.shape)
            
            # Calculate the number of facility
            self.ppdf = ppm.calculate(cons_df=cons_df, cd_dict=self._cd_dict)
            _logs.mid(code='calculate', value=self.ppdf.shape)
        except Exception as e:
            raise app_exception(e)
        finally:
            _logs.stop()
        
    def _facility_data(self, pkey=None):
        """ Preprocessing facility dataset for modeling section. """
        _logs = logs(code=f'preprocessing.{pkey}')
        try:
            # Get facility dataset
            pds_df = self._cd_dict[pkey]
            # Preprocessing facility dataset using common modules
            pds_df = eval(f'ppm.{pkey}({pkey}_df=pds_df)')
            _logs.mid(code='one_hot', value=pds_df.shape)
            
            # Saving modeling columns 
            # to be used for preprocessing in the service section.
            cols = pds_df.columns.tolist()
            save_data(data=cols, code=f'pickle.{pkey}_one_hot_cols')
            
            # Add aggregated facility data to the preprocessing dataframe
            # - add all columns except 'acc_no(index 0)'
            sum_cols = pds_df.columns.tolist()[1:]
            self.ppdf = ppm.aggregation_by_facility(
                pds_df=pds_df, cols=sum_cols, pp_df=self.ppdf)
            _logs.mid(code='result', value=self.ppdf.shape)
        except Exception as e:
            raise app_exception(e)
        finally:
            _logs.stop()
        
    def _complete(self):
        """ Preprocessing complete:
            - Final NaN handling, Save column info, Save preprocessing df """
        try:
            # Preprocessing final missing values handling
            self.ppdf = self.ppdf.fillna(0)
            
            # Save column info in the modeling section to ensure consistency
            # between datafram column info in the modeling and service section
            # - Column positions may change due to operations like one-hot encoding,
            #   requiring column rearrangement at the service section.
            save_cols = self.ppdf.columns.tolist()
            save_data(data=save_cols, code='pickle.last_pp_cols')
            
            # Save preprocessing data
            save_data(data=self.ppdf, code='data.pp.last')
            # Save data without pold for test
            # - Of these, 7 have line and 30 not line
            save_data(self.ppdf[self.ppdf.pole_cnt==0], 'data.pp.zero')
        except Exception as e:
            raise app_exception(e)
        
        