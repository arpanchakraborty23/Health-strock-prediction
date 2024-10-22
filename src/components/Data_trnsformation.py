import numpy as np
import sys
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.logging.logger import logging
from src.exception.exception import CustomException
from src.entity.config_entity import DatatranformationConfig
from src.utils.utils import save_obj

class DataTransformation:
    def __init__(self,config=DatatranformationConfig) -> None:
        self.config=config

    def get_preprocesser_obj(self):
        try:
            preproces_obj=Pipeline(
                steps=[
                    ('Impute',SimpleImputer(strategy='median')),
                    ('Scaler',StandardScaler())
                ]
            )

            return preproces_obj

        except Exception as e:
            logging.info(f'error {str(e)}')
            raise CustomException(sys,e)
        
    def initate_data_transformation(self):
        try:
            logging.info(' Data Transformation started')

            train_df=pd.read_csv(self.config.train_data)
            test_df=pd.read_csv(self.config.test_data)

            print(train_df.columns)
            print(test_df.head())

            Target_col=self.config.target_col
            
          

            # x_train
            input_cols_train_df=train_df.drop(columns=[Target_col,'Unnamed: 0'],axis=1)

            print(input_cols_train_df)

            # y_train
            target_col_train_df=train_df[Target_col]

            #  X_test
            input_cols_test_df=test_df.drop(columns=[Target_col,'Unnamed: 0'],axis=1)

            # y_test
            target_col_test_df=test_df[Target_col]

            scaler=self.get_preprocesser_obj()

            input_cols_train_arr=scaler.fit_transform(input_cols_train_df)
            input_cols_test_arr=scaler.transform(input_cols_test_df)

            logging.info(input_cols_train_arr)

            train_arr=np.c_[input_cols_train_arr,np.array(target_col_train_df)]
            test_arr=np.c_[input_cols_test_arr,np.array(target_col_test_df)]
            
            np.save(self.config.train_arr,train_arr)
            np.save(self.config.test_arr,test_arr)

            save_obj(
                file_path=self.config.preprocess_obj,
                obj=scaler
            )

            return (
                train_arr,
                test_arr
            )



        except Exception as e:
            logging.info(f'error {str(e)}')
            raise CustomException(sys,e)
            
