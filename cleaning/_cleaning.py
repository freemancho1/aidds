import pandas as pd

from aidds import config as cfg
from aidds import modeling_logs as logs
from aidds import AppException
from aidds.sys import get_provide_data, save_data


class Cleaning:
    """ Extract only the necessary columns and rows for modeling """
    def __init__(self):
        try:
            self._logs = logs(code='cleaning')
            # cd_dict: cleaning data dictionary
            self._cd_dict = {}
            # pd_dict: provided data dictionary
            self._pd_dict = get_provide_data()
            self._run()
        except Exception as e:
            raise AppException(e)
        finally:
            if hasattr(self, '_logs'):
                self._logs.stop()
                
    def _run(self):
        try:
            # Get CONS dataset
            pkey = cfg.type.pds[0]
            cons_df = self._pd_dict[pkey]
            
            # Handling constraints on rows
            modeling_rows = \
                (cons_df.acc_type_name == cfg.constraints.acc_type_name) & \
                (cons_df.cont_cap       < cfg.constraints.max_cont_cap) & \
                (cons_df.cons_cost      < cfg.constraints.max_total_cons_cost)
            cons_df = cons_df[modeling_rows].reset_index(drop=True)
            
            # Add columns: 'cont_type', 'sup_type'
            # - Columns to be added in future data updates.
            cons_df['cont_type'] = '1'
            cons_df['sup_type'] = '1'
            
            # Change office-name to office-cd
            office_names = cons_df.office_name.unique().tolist()
            office_codes = []
            for name in cons_df.office_name:
                # Assigning office_codes like AAAA, BBBB...
                # based on the order of unique office_names
                code = f'{chr(ord("A") + office_names.index(name)) * 4}'
                office_codes.append(code)
            # Add office_cd column to cons_df 
            cons_df['office_cd'] = office_codes
            
            # Extracting modeling columns from cons_df
            self._cd_dict[pkey] = cons_df[cfg.cols.cons.pp]
            
            # Remove records from the facility data 
            # where there is no acc_no in cons_df
            for pkey in cfg.type.pds[1:]:
                pds_df = self._pd_dict[pkey]
                conditions = pds_df[cfg.cols.join].isin(cons_df[cfg.cols.join])
                pds_df = pds_df[conditions]
                # Extracting modeling columns from facility_df
                self._cd_dict[pkey] = pds_df[eval(f'cfg.cols.{pkey}.pp')]
                
            # Save cleaning data
            for pkey in cfg.type.pds:
                save_data(self._cd_dict[pkey], code=f'data.cleaning.{pkey}')
                self._logs.mid(code=pkey, value=self._cd_dict[pkey].shape)
        except Exception as e:
            raise AppException(e)