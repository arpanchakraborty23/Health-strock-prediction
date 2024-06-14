import os,sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier
from xgboost import XGBClassifier

from src.config_manager.config_manger import ModelTrainConfig
from src.utils.utils import model_evaluatuion,save_obj
from src.logging.logger import logging
from src.exception.exception import CustomException

class ModelTrain:
    def __init__(self,config=ModelTrainConfig) -> None:
        self.config=config

    def initate_model_train(self):
        try:
            train_array=np.load(self.config.train_arr)
            test_array=np.load(self.config.test_arr)

            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                'LogisticRegression':LogisticRegression(),
                'KNeighborsClassifier': KNeighborsClassifier(),
                'DesisionTree':DecisionTreeClassifier(),
                'RandomForest':RandomForestClassifier(),
                'BaggingClf':BaggingClassifier(),
                'Xgboost':XGBClassifier()
            }

            params = {
                'LogisticRegression': {
                    'C': [1, 5, 10],
                    'penalty': ['l1', 'l2'],
                    'solver': ['lbfgs', 'liblinear', 'newton-cg', 'sag', 'saga']
                },
                'KNeighborsClassifier': {
                    'n_neighbors': [1, 3, 5, 10],
                    'weights': ['uniform', 'distance'],
                    'metric': ['euclidean', 'manhattan']
                },
                'DesisionTree': {
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [None, 10, 20, 30],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                },
                'RandomForest': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [None, 10, 20, 30],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                },
                'BaggingClf': {
                    'n_estimators': [50, 100, 200],
                    'max_samples': [0.5, 0.7, 0.9]
                },
                'Xgboost': {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 0.2, 0.3],
                    'max_depth': [3, 5, 7, 9],
                    'subsample': [0.6, 0.8, 1.0],
                    'colsample_bytree': [0.6, 0.8, 1.0]
                }
            }
            report:dict=model_evaluatuion(x_train,y_train,x_test,y_test,models,params)

            print(report)
            logging.info(f'Model Report : {report}')

            print('\n====================================================================================\n')

            # 6. Find the best model
            best_model_score=max(sorted(report.values()))

            
            best_model_name = list(report.keys())[
                list(report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            print(f'Best Model Found , Model Name : {best_model_name} , Score : {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found , Model Name : {best_model_name} , Score : {best_model_score}')


            save_obj(
                file_path=self.config.model,
                obj=best_model
            )
            return self.config.model
            
        except CustomException as e:
            logging.info(f'Error cooured {str(e)}')
            raise CustomException(sys,e)  