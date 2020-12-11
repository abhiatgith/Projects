from wsgiref import simple_server
import json
from flask import Flask, request, Response, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from training_main import Train_processing
from model_training import train_model
from prediction_main import pred_validation
from predictfrommodel import Prediction
import os
from werkzeug.utils import secure_filename
from flask import flash, redirect, send_file

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "Prediction_Batch_Files"

@app.route("/", methods=["GET", "POST"])
def upload_predict():
    #filesToRemove = [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER)]
    #for f in filesToRemove:
    #    os.remove(f)
    if request.method == "POST":
        csv_file = request.files["csvfile"]
        if csv_file:
            csv_location = os.path.join(UPLOAD_FOLDER, csv_file.filename)
            csv_file.save(csv_location)
            pred_folder, pred_file = predict(UPLOAD_FOLDER)
            return send_from_directory(pred_folder, pred_file, as_attachment=True)
    return render_template("index.html")


# @app.route("/predict", methods=['POST'])
# @cross_origin()
def predict(predfile_loc):
    try:
        if predfile_loc is not None:
            # Object Initialization for prediction
            predict_Val = pred_validation(predfile_loc)
            # Calling the prediction validation function
            predict_Val.prediction_validation()
            # initialising object for prediction class
            pred = Prediction(predfile_loc)
            # predicting for dataset present in database
            path_folder, path_file = pred.predictionFromModel()
            return path_folder, path_file
        else:
            print('Nothing Matched')
    except ValueError:
        raise ValueError
    except KeyError:
        raise KeyError
    except Exception as e:
        raise e


#port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    #print("This application has started to run")
    app.run(debug=True)
    #host = '0.0.0.0'
    #port = 5000
    #httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    #httpd.serve_forever()
