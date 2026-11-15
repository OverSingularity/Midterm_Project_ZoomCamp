from flask import Flask, jsonify, request
import pickle
import xgboost as xgb
import pandas as pd

#Function for taking data (json), changing type to DMatrix and prediction output
def TakingDMatrix(dane: dict)-> xgb.DMatrix:
    dt = pd.DataFrame([dane]) # changing format of data into pandas DataFrame
    # changing dtypes inside DataFrame
    CAT_FEATURES = ['Gender', 'Country', 'City', 'Payment_Method_Diversity', 'Signup_Quarter']
    dt[CAT_FEATURES] = dt[CAT_FEATURES].astype('str').astype('category')
    # formating into DMatrix
    DM = xgb.DMatrix(dt, enable_categorical = True)
    return DM

def MakingPrediction(dm: xgb.DMatrix, classificator):
    churn = classificator.predict(dm)
    return churn
# loading model
## declaring model file name
model_file =  'final_model.bin' # using pickle model was saved with binary format .bin
## loading model
with open(model_file, 'rb') as file_input:
    model = pickle.load(file_input)
# declaring ppp 
web_app = Flask('churning')
#declaring app route and methods of request
@web_app.route('/prediction', methods = ['POST'])
# function of our mapp
def Prediction():
    # Our application will get data from json file:
    dane = request.get_json() # the json file is transform to python dictionary 
   
    DM = TakingDMatrix(dane)

    answer = MakingPrediction(DM, model) ## for xgbmodel !

    result = {'churn_prediction:': float(answer[0])} 

    return jsonify(result)
if __name__ == "__main__":
    web_app.run(debug=True, host = '0.0.0.0', port = 9696)
