import os,sys
import pickle
from flask import request
import pandas as pd
from src.utils.utils import load_obj
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.config_manager.config_manger import PredictionConfigManager
from src.entity.config_entity import PredictionConfig

class PredictionPipline:
    def __init__(self,config=PredictionConfig) -> None:
        self.config=config
        self.prediction_file_path=os.path.join(self.config.prediction_output_dirname,self.config.prediction_file_name)

    def save_input_file(self):
        prediction_file_dir='prdiction_artifacts'

        os.makedirs(prediction_file_dir,exist_ok=True)

        input_csv_file=request.files['file']

        pred_file_path=os.path.join(prediction_file_dir,input_csv_file.filename)

        input_csv_file.save(pred_file_path)

        return pred_file_path
    
    def predict(self,features):
        
        model=load_obj(self.config.model)
        scaler=load_obj(self.config.preprocess_obj)

        trnsform=scaler.transform(features)
        pred=model.predict(trnsform)

        return pred
    
    def get_pred_as_df(self,input_csv):
        
        input_df=pd.read_csv(input_csv)
       

        drop_cols=['Unnamed: 0','Unnamed: 0.1']

        Target_col='stroke'

       
      

        print(input_df.head())
        
        input_df= input_df.drop(columns=[Target_col,'Unnamed: 0','Unnamed: 0.1'],axis=1)
        print(f'x_test  {input_df.head()}')

        prediction=self.predict(input_df)

        input_df['Target']=[pred for pred in prediction]

        input_df['Target']=input_df['Target'].map({'bad':1,'Good':0})
        
        os.makedirs(
            self.config.prediction_output_dirname,exist_ok=True
        )


        input_df.to_csv(self.prediction_file_path)


    def run_pipline(self):
        input_csv=self.save_input_file()

        self.get_pred_as_df(input_csv)

        return self.config