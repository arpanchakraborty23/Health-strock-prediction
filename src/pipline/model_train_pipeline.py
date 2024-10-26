import sys,os
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.config_manager.config_manger import ConfigManager
from src.components.model_train import ModelTrain

class ModelTrainPipline:
    def __init__(self) -> None:
        pass
    def ModelPipline(self):
        try:
            config=ConfigManager()
            data_transform_config=config.get_model_train_config()
            data_transform=ModelTrain(config=data_transform_config)
            data_transform.initate_model_train()

        except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise CustomException(sys,e)
        
if __name__=='__main__':
    try:
        logging.info(f'<<<<<<<<<<<<<<<< Model Train  Started >>>>>>>>>>>>>>>>>')
        object=ModelTrainPipline()
        object.ModelPipline()
        logging.info(f'>>>>>>>>>>>>>>>>>> Model Train  completed >>>>>>>>>>>>>>>>>>')
    except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise CustomException(sys,e) 