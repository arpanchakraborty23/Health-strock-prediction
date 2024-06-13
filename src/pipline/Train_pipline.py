import sys
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.config_manager.config_manger import ConfigManager
from src.components.Data_ingestion import DataIngestion
from src.components.Data_trnsformation import DataTransformation


class TrainPipline:
    def __init__(self) -> None:
        pass

    def pipline(self):
        try:
            logging.info('<<<<<<<<<<<<<<<< Data_Ingestion >>>>>>>>>>>>>>>>>>')
            config=ConfigManager()
            data_ingestion_config=config.get_data_ingestion_config()
            data_ingestion=DataIngestion(config=data_ingestion_config)
            data_ingestion.initate_data_ingestion()
            logging.info('<<<<<<<<<<<<<<<< Data_Ingestion_completed >>>>>>>>>>>>>>>>>>')

            logging.info('<<<<<<<<<<<<<<<< Data_Transformation >>>>>>>>>>>>>>>>>>')

            config=ConfigManager()
            data_transform_config=config.get_data_transformation_config()
            data_transform=DataTransformation(config=data_transform_config)
            data_transform.initate_data_transformation()

            logging.info('<<<<<<<<<<<<<<<< Data_Transformation Complete >>>>>>>>>>>>>>>>>>')


            
        except Exception as e:
            logging.info(f'Error cooured {str(e)}')
            raise CustomException(sys,e)   
        

if __name__ == '__main__':
    try:
        logging.info(f'********************Train Pipline**********************')
        obj = TrainPipline()
        obj.pipline()
        logging.info('******************** Train Pipline Completed **********************')
    except Exception as e:
        logging.exception(e)
        raise e      