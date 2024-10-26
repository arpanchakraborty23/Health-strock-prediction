from src.config_manager.config_manger import ConfigManager
from src.components.model_evaluation import ModelEval
from src.logging.logger import logging
from src.exception.exception import CustomException

import sys,os



class EvaluationPipline:
    def __init__(self) -> None:
        
        pass
    def main(self):
        try:
            config=ConfigManager()
            model_eval_config=config.get_model_eval_config()
            model_eval=ModelEval(model_eval_config)
            model_eval.initiating_model_eval()

          

        except Exception as e:
            logging.info(f'Error occured {str(e)}')
            raise CustomException(sys,e)
        
if __name__ == '__main__':
    try:
        logging.info(f"*******************")
        logging.info(f"<<<<<<<<<<<<<<<< Model Eval Started >>>>>>>>>>>>>>>>>")
        obj = EvaluationPipline()
        obj.main()
        logging.info(f"<<<<<<<<<<<<<<<< Model Eval Started >>>>>>>>>>>>>>>>>")
    except Exception as e:
        logging.info(e)
        raise CustomException(sys,e)