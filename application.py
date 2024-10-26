from flask import Flask,render_template,request,send_file,jsonify
from src.exception.exception import CustomException
from src.logging.logger import logging
from src.pipline.Prediction_pipline import PredictionPipline
from src.config_manager.config_manger import PredictionConfigManager

import sys,os

application= Flask(__name__)
app=application

@app.route("/")
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST', 'GET'])
def upload():
    try:
        config=PredictionConfigManager()
        pred_config=config.get_prediction_config()

        logging.info('prediction started')
        if request.method=='POST':
            prediction_pipeline = PredictionPipline(config=pred_config)

            # prediction_pipeline.prediction_file_path
            prediction_file_detail= prediction_pipeline.run_pipline()

            logging.info('Prediction Completed Download file')

            return send_file(prediction_pipeline.prediction_file_path,
                download_name=prediction_file_detail.prediction_file_name,
                as_attachment=True)



        else:
            return render_template('upload.html')

    except Exception as e:
        logging.info(f'error in bulk app prediction {str(e)}')
        raise CustomException(sys,e) from e 
    



if __name__=="__main__":
    app.run(host="0.0.0.0")