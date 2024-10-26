import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import traceback
import os
import sys
import numpy as np
from pathlib import Path
from urllib.parse import urlparse
from sklearn.metrics import accuracy_score, precision_score, recall_score,classification_report

from src.logging.logger import logging
from src.exception.exception import CustomException
from src.utils.utils import save_json, load_obj
from src.config_manager.config_manger import ConfigManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ['MLFLOW_TRACKING_URI'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['MLFLOW_TRACKING_USERNAME'] = os.getenv('MLFLOW_TRACKING_USERNAME')
os.environ['MLFLOW_TRACKING_PASSWORD'] = os.getenv('MLFLOW_TRACKING_PASSWORD')


class ModelEval:
    def __init__(self, config):
        self.config = config
    
    def eval_metrics(self, y_actual, y_pred):
        """Evaluate performance metrics: accuracy, precision, and recall."""
        try:
            accuracy = accuracy_score(y_actual, y_pred) * 100
            precision = precision_score(y_actual, y_pred) * 100
            recall = recall_score(y_actual, y_pred) * 100
            clf_report=classification_report(y_actual,y_pred)

            return accuracy, precision, recall,clf_report

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

            # Set MLflow tracking URI
            mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI'))

            # Infer the signature for the model
            sig = infer_signature(x_test, y_test)

            # Start MLflow run for logging
            with mlflow.start_run():
                # Make predictions
                predict = model.predict(x_test)

                # Calculate evaluation metrics (accuracy, precision, recall)
                accuracy, precision, recall,clf_report = self.eval_metrics(y_actual=y_test, y_pred=predict)
                scores = {'accuracy': accuracy, 'precision': precision, 'recall': recall,"classification report":clf_report}

                # Save metrics as JSON
                save_json(filename='model_eval_metrics.json', data=scores)

                # Log metrics to MLflow
                mlflow.log_metric('Accuracy', accuracy)
                mlflow.log_metric('Precision', precision)
                mlflow.log_metric('Recall', recall)

                mlflow.log_text(clf_report,'classsification_report.txt')

                # Log the model with signature
                tracking_uri_type_store = urlparse(mlflow.get_tracking_uri()).scheme
                if tracking_uri_type_store != 'file':
                    mlflow.sklearn.log_model(model, 'model', registered_model_name='best_model')
                else:
                    mlflow.sklearn.log_model(model, 'model', signature=sig)

        except Exception as e:
            logging.error(f'Error in Model evaluation: {e}')
            logging.error(traceback.format_exc())
            raise CustomException(f'Error in model evaluation: {e}')
