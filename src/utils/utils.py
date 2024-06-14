import os
import sys
import yaml,json
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV
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

def model_evaluatuion(x_train,y_train,x_test,y_test,models,prams):
    try:
            logging.info(' model evaluation started')
            report={}
            for i in range(len(models)):
                model = list(models.values())[i]
                param=prams[list(models.keys())[i]]
                #prams=prams[list(models.keys())[i]]
                print(f"Training {model}...")
                gs=GridSearchCV(model,param_grid=param,cv=5,verbose=3,refit=True,scoring='neg_mean_squared_error',n_jobs=-1)

            
                gs.fit(x_train,y_train)

                model.set_params(**gs.best_params_)

                # Train model
                model.fit(x_train,y_train)

                

                # Predict Testing data
                y_test_pred =model.predict(x_test)

                
                test_model_score = accuracy_score(y_test,y_test_pred)*100

                report[list(models.keys())[i]] =  test_model_score

               

                # Calculate the ROC curve
                fpr, tpr, thresholds = roc_curve(y_test, y_test_pred)

                # Calculate the AUC (Area Under the Curve)
                roc_auc = auc(fpr, tpr)

                # Plot the ROC curve
                plt.figure()
                plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
                plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
                plt.xlim([0.0, 1.0])
                plt.ylim([0.0, 1.05])
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title(f'Receiver Operating Characteristic {list(models.keys())[i]}')
                plt.legend(loc="lower right")
                plt.show()

            return report
        
    except Exception as e:
        logging.info(f' Error {str(e)}')
        raise CustomException(sys,e)
    
def load_obj(file_path):
    with open(file_path,'rb') as f:
        data=pickle.load(f)

    return data

