import os,sys
import pandas as pd
from sklearn.model_selection import train_test_split

from src.logging.logger import logging
from src.exception.exception import CustomException
from src.entity.config_entity import DataIngestonConfig

class DataIngestion:
    def __init__(self,config=DataIngestonConfig) -> None:
        self.config=config

    def initate_data_ingestion(self):
        try:
            logging.info('Data Ingestion Started')
            df=pd.read_csv('Datasets\clean_dataset.csv')

            logging.info('Data read completed')

            logging.info(df.head())

            df.to_csv(self.config.raw_data)

            train_data,test_data=train_test_split(df,test_size=0.29,random_state=0)

            train_data.to_csv(self.config.train_data)
            test_data.to_csv(self.config.test_data)

            logging.info('data Ingestion Compelted')

            return (
                self.config.train_data,
                self.config.test_data
            )
        except Exception as e:
            logging.info(f'Error cooured {str(e)}')
            raise CustomException(sys,e)     