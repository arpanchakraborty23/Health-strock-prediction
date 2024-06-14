from flask import Flask,render_template,request,send_file,jsonify
from src.exception.exception import CustomException
from src.logging.logger import logging
from src.pipline.Prediction_pipline import PredictionPipline,FormPredictionPipeline,CustomData
from src.config_manager.config_manger import PredictionConfigManager

import sys,os

app= Flask(__name__)

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
    
@app.route('/form',methods=['POST','GET'])
def predict_form():
    try:
        if request.method=='GET':
            return render_template('form.html')
        else:
            
            data=CustomData(
                    id=int(request.form.get('id')),
                    gender=int(request.form.get('gender')),
                    age=float(request.form.get('age')),
                    hypertension=int(request.form.get('hypertension')),
                    heart_disease=int(request.form.get('heart_disease')),
                    ever_married=int(request.form.get('ever_married')),
                    work_type=int(request.form.get('work_type')),
                    Residence_type=int(request.form.get('Residence_type')),
                    avg_glucose_level=float(request.form.get('avg_glucose_level')),
                    bmi=float(request.form.get('bmi')),
                    smoking_status=int(request.form.get('smoking_status'))
            )
            
            new_data=data.get_custom_df()


            config=PredictionConfigManager()
            pred_config=config.get_prediction_config()

            pred_pipline=FormPredictionPipeline(config=pred_config)

            pred=pred_pipline.predict(new_data)
            result=round(pred[0],2)
            
           
            

            return render_template('form.html',final_result=result)
    except Exception as e:
            logging.info(f'error in bulk app prediction {str(e)}')
            raise CustomException(sys,e) from e 

if __name__=="__main__":
    app.run(debug=True,port=5000)