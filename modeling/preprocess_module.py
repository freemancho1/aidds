import pandas as pd

from aidds import config as cfg, app_exception


class PreprocessModule:
    """ Data preprocessing(shared modeling and service) module """
    
    @staticmethod
    def cons(cons_df=None) -> pd.DataFrame:
        """ Common module for CONS dataset preprocessing """
        try:
            df = cons_df.copy()
            
            # Handling missing values
            df.fillna(0, inplace=True)
            
            ##
            # Currently only handling missing values,
            # but leaving room for future additions.
            
            return df
        except Exception as e:
            raise app_exception(e)
        
    @staticmethod
    def calculate(cons_df=None, cd_dict=None) -> pd.DataFrame:
        """ Common module for adding the number of facilities to
            preprocessed CONS dataframe

        Args:
            cons_df (pd.DataFrame, required): Preprocessing cons dataframe.
            cd_dict (dict, required): Cleaning Dataframe DICTionary

        Returns:
            pd.DataFrame: Dataframe with the number of facilities added 
                to the preprocessed CONS dataframe
        """
        try:
            ppdf = cons_df.copy()
            
            # Add the number of facilities to the preprocessed CONS df
            for pkey in cfg.type.pds[1:]:
                pds_df = cd_dict[pkey].copy()
                # Calculate the number of facilities per acc_no
                try:
                    cnt_per_acc_no = pds_df[cfg.cols.join].value_counts()
                    col_name = f'{pkey}_cnt'
                    # Add
                    ppdf = pd.merge(
                        ppdf, cnt_per_acc_no.rename(col_name), how='left',
                        left_on=cfg.cols.join, right_on=cnt_per_acc_no.index,
                    )
                    # Handling missing values
                    ppdf[col_name] = ppdf[col_name].fillna(0)
                # Skip if there is no pole or line data.
                # - Future columns will be created in batches later.
                except KeyError:
                    return ppdf
                
            # Constraints based on the number of facilities
            # - 0 to 10 for POLE/LINE data count
            # - 1 for SL
            modeling_rows = \
                (ppdf.pole_cnt >= cfg.constraints.min_pole_cnt) & \
                (ppdf.pole_cnt <= cfg.constraints.max_pole_cnt) & \
                (ppdf.line_cnt >= cfg.constraints.min_line_cnt) & \
                (ppdf.line_cnt <= cfg.constraints.max_line_cnt) & \
                (ppdf.sl_cnt   == cfg.constraints.sl_cnt)
            ppdf = ppdf[modeling_rows].reset_index(drop=True)
            return ppdf
        except Exception as e:
            raise app_exception(e)
    
    @staticmethod
    def pole(pole_df=None) -> pd.DataFrame:
        """ Common module for POLE dataset preprocessing """
        try:
            df = pole_df.copy()
            # Handling missing values
            df = df.fillna(0)
            
            try:
                # One-hot encoding for categorical columns
                # Target columns
                cols = ['pole_shape_cd', 'pole_type_cd', 'pole_spec_cd']
                # Prefix is used by removing the last 3 letters('_cd')
                # from each item in the cols list
                prefix = [item[:-3] for item in cols]
                # Standardizing numerical values(converting non-float values to float)
                # 1 and 1.0 are treated as separate columns in One-hot encoding
                if df.pole_spec_cd.dtype != 'float64':
                    df.pole_spec_cd = df.pole_spec_cd.astype(float)
                # One-hot encoding
                df = pd.get_dummies(df, columns=cols, prefix=prefix)
                # Converting True, False to 1, 0
                df = df.apply(
                    lambda item: int(item) if isinstance(item, bool) else item
                )
            # Skip if there is no pole or line data.
            # - Future columns will be created in batches later.
            except AttributeError:
                pass
            
            return df
        except Exception as e:
            raise app_exception(e)
        
    @staticmethod
    def line(line_df=None) -> pd.DataFrame:
        """ Common module for LINE dataset preprocessing """
        try:
            df = line_df.copy()
            
            try:
                # One-hot encoding for categorical columns
                # Target columns
                cols = [
                    'wiring_scheme', 'line_type_cd', 'line_spec_cd', 
                    'line_phase_cd', 'neutral_type_cd', 'neutral_spec_cd'
                ]
                # Prefix is used by removing the last 3 letters('_cd')
                # from each item in the cols list
                # However, exclude 'wiring_scheme' as it does not end with '_cd'
                prefix = [cols[0]] + [item[:-3] for item in cols[1:]]
                # Standardizing numerical values(converting non-float values to float)
                # 1 and 1.0 are treated as separate columns in One-hot encoding
                if df.line_spec_cd.dtype != 'float64':
                    df.line_spec_cd = df.line_spec_cd.astype(float)
                # Neutral wire specification code contains both 0.0 and NaN
                # - Replace NaN with 999.0 to differentiate
                df.neutral_spec_cd = df.neutral_spec_cd.fillna(999.0)
                # Convert NaN values in Neutral wire type code to the string 'NaN'
                df.neutral_type_cd = df.neutral_type_cd.fillna('NaN')
                # Add total wire length = Span length * Number of wires(phase_cd)
                df.loc[:, 'line_length'] = df.span * df.line_phase_cd
                
                # Handling missing values for the remaining columns,
                # considering there's separate treatment for missing values above.
                df = df.fillna(0)
                
                # One-hot encoding
                df = pd.get_dummies(df, columns=cols, prefix=prefix)
                # Converting True, False to 1, 0
                df = df.apply(
                    lambda item: int(item) if isinstance(item, bool) else item
                )
            # Skip if there is no pole or line data.
            # - Future columns will be created in batches later.
            except AttributeError:
                pass
            
            return df
        except Exception as e:
            raise app_exception(e)
        
    @staticmethod
    def sl(sl_df=None) -> pd.DataFrame:
        """ Common module for SL dataset preprocessing """
        try:
            df = sl_df.copy()
            # Handling missing values
            df = df.fillna(0)
            
            # One-hot encoding for categorical columns
            # Target columns
            cols = ['sl_type_cd', 'sl_spec_cd']
            # Prefix is used by removing the last 3 letters('_cd')
            # from each item in the cols list
            prefix = [item[:-3] for item in cols]
            # Standardizing numerical values(converting non-float values to float)
            # 1 and 1.0 are treated as separate columns in One-hot encoding
            if df.sl_spec_cd.dtype != 'float64':
                df.sl_spec_cd = df.sl_spec_cd.astype(float)
            # Add total wire length = Span length * Number of wires(phase_cd)
            df.loc[:, 'sl_length'] = df.sl_span * df.sl_phase
            
            # One-hot encoding
            df = pd.get_dummies(df, columns=cols, prefix=prefix)
            # Converting True, False to 1, 0
            df = df.apply(
                lambda item: int(item) if isinstance(item, bool) else item
            )
            
            return df
        except Exception as e:
            raise app_exception(e)
        
    @staticmethod
    def aggregation_by_facility(pds_df=None, cols=None, pp_df=None):
        """ Aggregation the count of columns that have been one-hot encoded 
            for each facility. """
        try:
            unique_acc_no = pds_df[cfg.cols.join].unique()
            acc_no_sums = []
            # Sum by acc_no
            for acc_no in unique_acc_no:
                conditions = pds_df[cfg.cols.join] == acc_no
                sum_values = pds_df[conditions][cols].sum().values.tolist()
                acc_no_sums.append([acc_no] + sum_values)
            # Create a dataframe aggregated by acc_no
            sums_df = pd.DataFrame(acc_no_sums, columns=[cfg.cols.join]+cols)
            # Merge sums_df with pp_df
            ppdf = pd.merge(pp_df, sums_df, on=cfg.cols.join, how='left')
            return ppdf
        except Exception as e:
            raise app_exception(e)
    
    
    
    