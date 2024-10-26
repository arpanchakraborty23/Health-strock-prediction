import sys,os
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.config_manager.config_manger import ConfigManager
from src.components.Data_ingestion import DataIngestion

class DataIngestionTrainPipline:
    def __init__(self) -> None:
       pass

    def IngestionPipline(self):
        
        try:
            config=ConfigManager()
            data_ingestion_config=config.get_data_ingestion_config()
            data_ingestion=DataIngestion(config=data_ingestion_config)
            data_ingestion.initate_data_ingestion()
          
            
        except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise CustomException(sys,e)
        
if __name__=='__main__':
    try:
        logging.info(f'<<<<<<<<<<<<<<<< Data Ingestion Started >>>>>>>>>>>>>>>>>')
        object=DataIngestionTrainPipline()
        object.IngestionPipline()
        logging.info(f'>>>>>>>>>>>>>>>>>> Data Ingestion completed >>>>>>>>>>>>>>>>>>')
    except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise CustomException(sys,e)    