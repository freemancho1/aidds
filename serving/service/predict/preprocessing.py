import pandas as pd
from typing import Type

from aidds import config as cfg 
from aidds import service_logs as logs
from aidds import app_exception
from aidds.modeling import PreprocessModule as ppm


class PredictPreprocessing:
    def __init__(self, in_json=None, pkl=None) -> Type['PredictPreprocessing']:
        try:
            self._in_json = in_json
            self._pkl = pkl
            self._cleaning_df = {}
            # Preprocessing Datafram dict(Generate as many recommended counts)
            self.ppdf = {}
            # Return JSON data dict(Generate as many recommended counts)
            self.return_json = {}
            self._run()
        except Exception as e:
            raise app_exception(e)
    
    def _run(self) -> None:
        try:
            self._json_to_dataframe()
            # pnid = Predict Number ID
            for pnid in self._cleaning_df.keys():
                # Preprocessing CONS dataset
                self._cons(pnid=pnid)
                # Preprocessing facility dataset
                for pkey in cfg.type.pds[1:]:
                    self._facility_data(pnid=pnid, pkey=pkey)
                self._complete(pnid=pnid)
        except Exception as e:
            raise app_exception(e)
    
    def _json_to_dataframe(self) -> None:
        # Using the input JSON data dictionary
        # 1. Create a dataframe dictionary to be used for prediction
        # 2. Create a JSON data dictionary to return prediction results.
        try:
            # 'in_json': Temp data used in this function
            # 'self.return_json': in_json + predicted cost(added later)
            in_json = self.return_json = self._in_json.copy()
            # Get the first acc_no value 
            # (can be used in lists, dictionaries, and JSON)
            first_key = next(iter(in_json))
            acc_no = in_json[first_key][cfg.type.pds[0]][cfg.cols.join]
            # Display the number of recommended routes for the requested JSON
            value = f'{cfg.cols.join}={acc_no}, size={len(in_json)}'
            logs(code='predict.json_size', value=value)
            
            # Convert JSON data for each recommendation number(predict number id)
            # into a data frame to be used for prediction
            # pnid = Predict Number ID
            for pnid in in_json.keys():
                self._cleaning_df[pnid] = {}
                for pkey in cfg.type.pds:
                    json_data = in_json[pnid][pkey]
                    # CONS data exception handling
                    if pkey == cfg.type.pds[0]:
                        # Add dimensions to make it a dataframe
                        pds_df = pd.DataFrame([json_data])
                        # Remove unused pred_no/type columns from predictions
                        pds_df.drop(
                            columns=['pred_no', 'pred_type'], inplace=True)
                        # Remove unnecessary columns from return JSON data
                        # - Only CONS data, not in facility data
                        # - Remove except join, cons_cost, pred_no, pred_type
                        for col in cfg.cols.cons.source.service[4:]:
                            self.return_json[pnid][pkey].pop(col, None)
                    else:
                        # Convert equipment data in JSON format to a list
                        list_data = [value for _, value in json_data.items()]
                        pds_df = pd.DataFrame(list_data)
                    # Save dataframe
                    self._cleaning_df[pnid][pkey] = pds_df
        except Exception as e:
            raise app_exception(e)
    
    def _cons(self, pnid=None) -> None: 
        try:
            pds_df = self._cleaning_df[pnid][cfg.type.pds[0]]
            # Common module 
            pds_df = ppm.cons(cons_df=pds_df)
            
            # Create a office_id using the office_cds(pickle)
            office_ids = []
            for code in pds_df.office_cd:
                office_ids.append(self._pkl['office_codes'].index(code))
            pds_df['office_id'] = office_ids
            pds_df.drop(columns=['office_cd'], inplace=True)
            
            # Calculate the number of facility
            pds_df = ppm.calculate(
                cons_df=pds_df, cd_dict=self._cleaning_df[pnid])
            self.ppdf[pnid] = pds_df
        except Exception as e:
            raise app_exception(e)
    
    def _facility_data(self, pnid=None, pkey=None) -> None:
        try:
            pds_df = self._cleaning_df[pnid][pkey]
            
            # Preprocessing of common modules for each facility
            # - One-hot encoding is performed here
            pds_df = eval(f'ppm.{pkey}({pkey}_df=pds_df)')
            
            # Add a service data columns 
            # using the column info used in the modeling section.
            cols = self._pkl[f'{pkey}_one_hot_cols']
            pds_columns = pds_df.columns.tolist()
            append_cols = [col for col in cols if col not in pds_columns]
            # The column order is later aligned with the modeling section.
            pds_df.loc[:, append_cols] = 0
            
            # Add aggregated facility data to the preprocessing dataframe
            # - add all columns except 'acc_no(index 0)'
            sum_cols = pds_df.columns.tolist()[1:]
            self.ppdf[pnid] = ppm.aggregation_by_facility(
                pds_df=pds_df, cols=sum_cols, pp_df=self.ppdf[pnid])
        except Exception as e:
            raise app_exception(e)
        
    def _complete(self, pnid=None) -> None:
        """ Preprocessing complete:
            - Final NaN handling, Match the column order """
        try:
            # Match the column order of the service section
            # with the modeling section.
            self.ppdf[pnid] = self.ppdf[pnid].reindex(
                columns=self._pkl['last_pp_cols'])
            # Preprocessing final missing values handling
            self.ppdf[pnid] = \
                self.ppdf[pnid].fillna(0).infer_objects(copy=False)
        except Exception as e:
            raise app_exception(e)
        