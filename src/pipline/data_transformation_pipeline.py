import sys,os
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.config_manager.config_manger import ConfigManager
from src.components.Data_trnsformation import DataTransformation

class DataTransformationPipline:
    def __init__(self) -> None:
        pass
    def TransformationPipline(self):
        try:
            config=ConfigManager()
            data_transform_config=config.get_data_transformation_config()
            data_transform=DataTransformation(config=data_transform_config)
            data_transform.initate_data_transformation()

        except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise CustomException(sys,e)
        
if __name__=='__main__':
    try:
        logging.info(f'<<<<<<<<<<<<<<<< Data_Transformation  Started >>>>>>>>>>>>>>>>>')
        object=DataTransformationPipline()
        object.TransformationPipline()
        logging.info(f'>>>>>>>>>>>>>>>>>> Data_Transformation  completed >>>>>>>>>>>>>>>>>>')
    except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise CustomException(sys,e) 