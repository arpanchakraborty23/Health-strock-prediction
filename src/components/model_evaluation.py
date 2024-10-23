import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import traceback
import os
import sys
import numpy as np
from pathlib import Path
from urllib.parse import urlparse
from sklearn.metrics import accuracy_score, precision_score, recall_score

from src.logging.logger import logging
from src.exception.exception import CustomException
from src.utils.utils import save_json, load_obj
from src.config_manager.config_manger import ModelEvalConfig

class ModelEval:
    def __init__(self, config):
        self.config = config
    
    def eval_metrics(self, y_actual, y_pred):
        """Evaluate performance metrics: accuracy, precision, and recall."""
        try:
            accuracy = accuracy_score(y_actual, y_pred) * 100
            precision = precision_score(y_actual, y_pred) * 100
            recall = recall_score(y_actual, y_pred) * 100

            return accuracy, precision, recall

        except Exception as e:
            logging.info(f'Error in Model evaluation metrics: {str(e)}')
            raise CustomException(sys, e)

    def initiating_model_eval(self):
        """Initiate model evaluation process."""
        try:
            logging.info('Model evaluation started')

            # Load test data and model
            test_arr = np.load(self.config.test_arr)
            model = load_obj(self.config.model)

            x_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]

            # Infer the signature for the model
            sig = infer_signature(x_test, y_test)

            # Start MLflow run for logging
            with mlflow.start_run():
                # Make predictions
                predict = model.predict(x_test)

                # Calculate evaluation metrics (accuracy, precision, recall)
                accuracy, precision, recall = self.eval_metrics(y_actual=y_test, y_pred=predict)
                scores = {'accuracy': accuracy, 'precision': precision, 'recall': recall}

                # Save metrics as JSON
                save_json(filename='model_eval_metrics.json', data=scores)

                # Log metrics to MLflow
                mlflow.log_metric('Accuracy', accuracy)
                mlflow.log_metric('Precision', precision)
                mlflow.log_metric('Recall', recall)

                # Log the model with signature
                try:
                    mlflow.sklearn.log_model(model, 'model', signature=sig)
                    logging.info('Model logged successfully with signature.')
                except Exception as e:
                    logging.error(f'Failed to log model with signature: {e}')
                    logging.error(traceback.format_exc())

        except Exception as e:
            logging.error(f'Error in Model evaluation: {e}')
            logging.error(traceback.format_exc())
            raise CustomException(f'Error in model evaluation: {e}')
