import os,sys
import pickle
from flask import request
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from src.utils.utils import load_obj,input_csv_to_db
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.config_manager.config_manger import PredictionConfigManager
from src.entity.config_entity import PredictionConfig

class PredictionPipline:
    def __init__(self,config=PredictionConfigManager) -> None:
        self.config=config
        self.prediction_file_path=os.path.join(self.config.prediction_output_dirname,self.config.prediction_file_name)

        logging.info('Prediction Pipline Started')

    def save_input_file(self):
        try:
            prediction_file_dir='prdiction_artifacts'

            os.makedirs(prediction_file_dir,exist_ok=True)

            input_csv_file=request.files['file']

            pred_file_path=os.path.join(prediction_file_dir,input_csv_file.filename)

            input_csv_file.save(pred_file_path)

           

            return pred_file_path
        except Exception as e:
            logging.info(f'Error cooured {str(e)}')
            raise CustomException(sys,e)
    
    def predict(self,features):
        try:
            model=load_obj(self.config.model)
            scaler=load_obj(self.config.preprocess_obj)

            trnsform=scaler.transform(features)
            pred=model.predict(trnsform)

            return pred
        except Exception as e:
            logging.info(f'Error cooured {str(e)}')
            raise CustomException(sys,e)
    
    def get_pred_as_df(self,input_csv):
        try:
            # read input csv
            input_df=pd.read_csv(input_csv)
            logging.info(f'Input csv file: {input_df.head()}')
            
            # Target col
            Target_col='stroke'

            # store input data to DataBase
            input_csv_to_db(
                input_csv=input_df,
                url=os.getenv('MongoDB'),
                db=os.getenv('input_csv_db'),
                collection=os.getenv('input_csv_collection')
            )

            print(input_df.head())
            if 'Unnamed: 0' in input_df.columns:
                input_df = input_df.drop(columns=['Unnamed: 0', Target_col])
            else:
                input_df = input_df.drop(columns=[Target_col])

            

            logging.info(f'input dataframe columns: {input_df.columns}')

            prediction=self.predict(input_df)

            input_df['Target']=[pred for pred in prediction]

            
            os.makedirs(
                self.config.prediction_output_dirname,exist_ok=True
            )


            input_df.to_csv(self.prediction_file_path)
        except Exception as e:
            logging.info(f'Error cooured {str(e)}')
            raise CustomException(sys,e)


    def run_pipline(self):
        input_csv=self.save_input_file()

       

        self.get_pred_as_df(input_csv)

        return self.config
    


