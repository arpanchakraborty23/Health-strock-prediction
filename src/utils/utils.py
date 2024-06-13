import os
import sys
import yaml,json
from pathlib import Path
from ensure import ensure_annotations
from box import ConfigBox
from src.logging.logger import logging
from src.exception.exception import CustomException

@ensure_annotations
def read_yaml(file_path:Path):
    try:
        with open(file_path) as f:
            file=yaml.safe_load(f)
        return ConfigBox(file)
    except Exception as e:
        logging.info(f'error in {str(e)}')
        raise CustomException(sys,e)


@ensure_annotations   
def create_dir(file_path:list,verbose=True):
    try:
        for path in file_path:
            os.makedirs(path,exist_ok=True)
            if verbose:
                logging.info(f"created directory at: {path}")    
    except Exception as e:
        raise CustomException(sys,e) 