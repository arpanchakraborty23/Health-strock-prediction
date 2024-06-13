import os,sys
import yaml
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.entity.config_entity import DataIngestonConfig
from src.constant.yaml_path import *
from src.utils.utils import read_yaml,create_dir


class ConfigManager:
    def __init__(self,config_file_path=Config_file_path,pram_file_path=param_file_path) -> None:
        self.config=read_yaml(config_file_path)
        self.param=read_yaml(pram_file_path)

        create_dir([self.config.Artifacts_root])

    def data_ingestion_config(self):
        try:
            config=self.config.Data_Ingestion
            create_dir([config.dir])

            data_ingestion_config=DataIngestonConfig(
                dir=config.dir,
                raw_data=config.raw_data,
                train_data=config.train_data,
                test_data=config.test_data
            )

            return data_ingestion_config

        except Exception as e:
            logging.info(f'error {str(e)}')
            raise CustomException(sys,e)