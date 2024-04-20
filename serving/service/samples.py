import json
import random

import aidds.sys.config as cfg 
from aidds.sys.utils.exception import AppException
from aidds.sys.utils.logs import service_logs as logs
from aidds.sys.utils.data_io import read_data, get_cleaning_data


class Samples:
    """ Generate sample data to be used for 
        web service testing from cleaned data 
    
        * Singleton service 
    """
    def __init__(self) -> None:
        try:
            self._source_df = read_data(
                code='data.scaling.best', dtype={cfg.cols.join: str})
            self._acc_nos = self._source_df[cfg.cols.join].tolist()
            self._cd_dict = get_cleaning_data()
            logs(code='samples.main')
        except Exception as e:
            raise AppException(e)
        
    def get(self, recommend_count=3) -> json:
        """ Returns 1 sample data(JSON) for service testing 
            - Sample data is a single JSON consisting of the number
              of recommended(suggested) route data.
        """
        try:
            # Extract acc_no to be used in the sample as recommend_count
            sample_acc_nos = random.sample(self._acc_nos, k=recommend_count)
            logs(code='samples.get', value=sample_acc_nos)
            
            # Generate sample data(JSON)
            sample_dict = {}
            for acc_no in sample_acc_nos:
                recommend_dict = {}
                for pkey in cfg.type.pds:
                    df = self._cd_dict[pkey]
                    df = df[df[cfg.cols.join] == acc_no]
                    recommend_dict[pkey] = df
                # Add recommended route to sample data
                # - Here, the acc_nos are different(independent)
                sample_dict[acc_no] = recommend_dict
                
            # Convert extracted sample data to JSON
            # The acc_no is unified as the first acc_no 
            # and a different recommendation number is assigned
            sample_json = self._sample_to_json(sample=sample_dict)
            return sample_json
        except Exception as e:
            raise AppException(e)
        
    def _sample_to_json(self, sample=None) -> json:
        """ Convert sample data to JSON data """
        try:
            # Cleaned sample data to be converted to JSON
            cleaning_dict = {}
            sample_dict = sample
            # 'acc_no' to represent sample data(use the acc_no that comes first)
            acc_no = None
            # Recommended route number(from 1 to len(sample_dict))
            pred_seq = 1
            
            for idx, row in sample_dict.items():
                if not acc_no:
                    acc_no = idx
                pred_no = f'pred_{pred_seq}'
                cleaning_dict[pred_no] = {}
                
                # Data cleaning
                # - Add acc_no(unified), pred_no, pred_type for each recommend route
                # - Initially as follows
                #             acc_no  cons_cost office_cd  cont_cap  sup_type
                # 3219  476920214453    2969453      CCCC         3         1
                cons_dict = row[cfg.type.pds[0]].to_dict(orient='records')[0]
                # Change acc_no, add pred_no, pred_type
                cons_dict.update({
                    cfg.cols.join: acc_no,
                    'pred_no': pred_no, 'pred_type': pred_no
                })
                cleaning_dict[pred_no][cfg.type.pds[0]] = cons_dict
                
                # Extract facility-specific details from recommend route number
                for pkey in cfg.type.pds[1:]:
                    cleaning_dict[pred_no][pkey] = {}
                    pds_df = row[pkey].copy()
                    detail_dict = {}
                    seq = 1
                    for _, detail_row in pds_df.iterrows():
                        detail = detail_row.to_dict()
                        # Change the acc_no of each facility details to first acc_no
                        detail[cfg.cols.join] = acc_no
                        detail_dict[f'{pkey}_{seq}'] = detail
                        seq += 1
                    cleaning_dict[pred_no][pkey] = detail_dict
                pred_seq += 1
            
            # Convert the cleaned sample dictionary to JSON
            sample_json = json.dumps(cleaning_dict, ensure_ascii=False) 
            return sample_json
        except Exception as e:
            raise AppException(e)
    
                
        
    