import os
import sys
import yaml,json
import pickle
from pathlib import Path
from ensure import ensure_annotations
from box import ConfigBox
from sklearn.metrics import roc_auc_score,accuracy_score
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
    
def save_obj(file_path,obj):
    with open(file_path,'wb') as f:
        pickle.dump(obj,f)

def model_evaluatuion(x_train,y_train,x_test,y_test,models):
    report={}
    for i in range(len(models)):
        model=list(models.values())[i]

        model.fit(x_train,y_train)

        y_pred=model.predict(x_test)

        accuracy=accuracy_score(y_test,y_pred)*100
        report[list(models.keys())[i]] =[
                f'Accuracy: {accuracy:.2f}% '   
            ]

        return report

