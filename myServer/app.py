from flask import Flask, jsonify
from flask_cors import CORS
import csv
import json
import numpy as np
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['JSON_AS_ASCII'] = False
# enable CORS
CORS(app)


def Normalize(_data):
    dataMin=_data.min(axis=0)
   
    dataMax=_data.max(axis=0)
    data=(_data-dataMin)/(dataMax-dataMin)
    return data,dataMin,dataMax

def _Normalize(_data,dataMin,dataMax):
    new_data=(_data-dataMin)/(dataMax-dataMin)
    return new_data



@app.route('/getraw20', methods=['GET'])
def GetRaw20():
    json_data = [json.dumps(d,ensure_ascii=False) for d in csv.DictReader(open('data.csv'))]
    
    return jsonify(json_data)

@app.route('/reconstructRaw', methods=['GET'])
def GetReconstructRaw():
    raw=np.load('raw.npy')
    dim2=np.load('dim2_reconnstruct.npy')
    dim4=np.load('dim4_reconnstruct.npy')
    dim6=np.load('dim6_reconnstruct.npy')
    dim8=np.load('dim8_reconnstruct.npy')
    List={'r':raw.tolist(),'d2':dim2.tolist(),'d4':dim4.tolist(),'d6':dim6.tolist(),'d8':dim8.tolist()}
    return jsonify(List)






if __name__ == '__main__':
    app.run()
