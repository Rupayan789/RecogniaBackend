import flask
import pandas as pd
from flask_cors import CORS, cross_origin
import joblib
import numpy as np
from flask import Flask,render_template,request,jsonify
from inputdataframe import url_Lexical_Features
import pickle
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
scaler = pickle.load(open('scaler.pkl', 'rb'))
model2 = joblib.load('./moodel.pkl')
@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
   
    url = request.get_json(force=True)['url']
    print(url)
    df=pd.DataFrame({
        "url":[url]
    })
    df2=url_Lexical_Features(df,'url')
    df3=df2.drop(['host_name','get_tld','url'],axis=1)
    df4 = df3.copy()
    df4.url_scheme = df4.url_scheme.map({'http':0,'https':1})
    for i in df4.select_dtypes('bool').columns:
        df4[i] = df4[i].map({True:1,False:0})
    df5 = pd.DataFrame(scaler.transform(df4),columns=df4.columns)
    result = model2.predict(df5)
    response = jsonify({"response":int(result[0])})
    return response

if __name__ == '__main__':
    app.run(debug=True)