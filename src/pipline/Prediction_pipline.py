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
            input_df=pd.read_csv(input_csv)
            logging.info(f'Input csv file: {input_df.head()}')
            
        

            drop_cols=['Unnamed: 0']

            Target_col='Target'

        
        

            print(input_df.head())

            # if drop_cols in input_df:
            #     input_df.drop(columns=[drop_cols,Target_col],axis=1,inplace=True)
            # else:
            #     input_df.drop(columns=[Target_col],axis=1,inplace=True)

            input_df.drop(columns=[Target_col],axis=1)

            logging.info(f'input dataframe columns: {input_df.columns}')

            prediction=self.predict(input_df)

            input_df['Target']=[pred for pred in prediction]

            input_df['Target']=input_df['Target'].map({'Dropout':0 ,'Graduate':1 ,'Enrolled':2 })
            
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
    

class FormPredictionPipeline:
    def __init__(self,config=PredictionConfig):
        self.config=config
        
        logging.info('form prediction config')
        

    def predict(self,features):
        
        model=load_obj(self.config.model)
        scaler=load_obj(self.config.preprocess_obj)

        trnsform=scaler.transform(features)
        pred=model.predict(trnsform)

        return pred
    
class CustomData:
    def __init__(self,
                id:int,
                gender:int, 
                age:float,
                hypertension:int,
                heart_disease:int,
                ever_married:int,
                work_type:int,
                Residence_type:int,
                avg_glucose_level:float,
                bmi:float,
                smoking_status:int) -> None:
        
                self.id=id
                self.gender=gender
                self.age=age
                self.hypertension=hypertension
                self.heart_disease=heart_disease
                self.ever_married=ever_married
                self.work_type=work_type
                self.Residence_type=Residence_type
                self.avg_glucose_level=avg_glucose_level
                self.bmi=bmi
                self.smoking_status=smoking_status

    def get_custom_df(self):
        custom_input_data={
            'id':[self.id],
                'gender':[self.gender],
                'age':[self.age],
                'hypertension':[self.hypertension],
                'heart_disease':[self.heart_disease],
                'ever_married':[self.ever_married],
                'work_type':[self.work_type],
                'Residence_type':[self.Residence_type],
                'avg_glucose_level':[self.avg_glucose_level],
                'bmi':[self.bmi],
                'smoking_status':[self.smoking_status]
        }
        df=pd.DataFrame(custom_input_data)

        return df
        
        