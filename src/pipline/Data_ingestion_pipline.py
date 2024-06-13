import sys
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.config_manager.config_manger import ConfigManager
from src.components.Data_ingestion import DataIngestion

STAGE_NAME='Data Ingestion'
class TrainPipline:
    def __init__(self) -> None:
        pass

    def pipline(self):
        try:
            config=ConfigManager()
            data_ingestion_config=config.data_ingestion_config()
            data_ingestion=DataIngestion(config=data_ingestion_config)
            data_ingestion.initate_data_ingestion()

            
        except Exception as e:
            logging.info(f'Error cooured {str(e)}')
            raise CustomException(sys,e)   
        

if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = TrainPipline()
        obj.pipline()
        logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logging.exception(e)
        raise e      