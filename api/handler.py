import pickle
import pandas as pd
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann

# loads model
model = pickle.load(open('/Users/brunokatekawa/Desktop/Data Science/DataScienceProducao/Curso_DS_Prod/model/model_rossmann.pkl', 'rb'))

# initializes API
app = Flask(__name__)

# creates the endpoint
@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predcit():
    # gets json that comes from API
    test_json = request.get_json()
    
    # checks if json exists
    if test_json:   
        # unique example
        if isinstance(test_json, dict):
            test_raw = pd.DataFrame(test_json, index=[0])
            
        #multiple examples
        else:
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
        
        
        # instantiates Rossmann class
        pipeline = Rossmann()
        
        # data cleaning
        df1 = pipeline.data_cleaning(test_raw)
        
        # feature engineering
        df2 = pipeline.feature_engineering(df1)
        
        # data preparation
        df3 = pipeline.data_preparation(df2)
        
        # prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)
        
        return df_response
        
    else:
        return Response('{}', status=200, mimetype='application/json')

# checks if there is main in the class
if __name__ == '__main__':
    app.run('0.0.0.0')