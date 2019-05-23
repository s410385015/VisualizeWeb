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

@app.route('/reconstructDiff', methods=['GET'])
def GetReconstructDiff():
    raw=np.load('raw.npy')
    dim2=np.load('dim2_reconnstruct.npy')
    dim4=np.load('dim4_reconnstruct.npy')
    dim6=np.load('dim6_reconnstruct.npy')
    dim8=np.load('dim8_reconnstruct.npy')
    tags=np.load('tags.npy')
    len=(int)(raw.shape[0]/100)
    
    r2=[]
    tmp=np.abs(dim2/raw-1)
    for i in range(0,raw.shape[0],len):
        r2.append(np.array(tmp[i:i+len,:].sum(axis=0)/len))
    r2=np.array(r2)

    r4=[]
    tmp=np.abs(dim4/raw-1)
    for i in range(0,raw.shape[0],len):
        r4.append(np.array(tmp[i:i+len,:].sum(axis=0)/len))
    r4=np.array(r4)
    
    r6=[]
    tmp=np.abs(dim6/raw-1)
    for i in range(0,raw.shape[0],len):
        r6.append(np.array(tmp[i:i+len,:].sum(axis=0)/len))
    r6=np.array(r6)
    
    r8=[]
    tmp=np.abs(dim8/raw-1)
    for i in range(0,raw.shape[0],len):
        r8.append(np.array(tmp[i:i+len,:].sum(axis=0)/len))
    r8=np.array(r8)

    List={'len':raw.shape[0],'dim':raw.shape[1],'r2':r2.tolist(),'r4':r4.tolist(),'r6':r6.tolist(),'r8':r8.tolist(),'tags':tags.tolist()}
    return jsonify(List)


@app.route('/reconstructDiffSub', methods=['GET'])
def GetReconstructDiffSub():
    raw,rmin,rmax=Normalize(np.load('raw.npy'))
    dim2=_Normalize(np.load('dim2_reconnstruct.npy'),rmin,rmax)
    dim4=_Normalize(np.load('dim4_reconnstruct.npy'),rmin,rmax)
    dim6=_Normalize(np.load('dim6_reconnstruct.npy'),rmin,rmax)
    dim8=_Normalize(np.load('dim8_reconnstruct.npy'),rmin,rmax)
    tags=np.load('tags.npy')
    len=(int)(raw.shape[0]/100)
    
    r2=[]
    tmp=dim2-raw
    for i in range(0,raw.shape[0],len):
        r2.append(np.array(tmp[i:i+len,:].sum(axis=0)/len))
    r2=np.round(np.array(r2),decimals=2)

    r4=[]
    tmp=dim4-raw
    for i in range(0,raw.shape[0],len):
        r4.append(np.array(tmp[i:i+len,:].sum(axis=0)/len))
    r4=np.round(np.array(r4),decimals=2)
    
    r6=[]
    tmp=dim6-raw
    for i in range(0,raw.shape[0],len):
        r6.append(np.array(tmp[i:i+len,:].sum(axis=0)/len))
    r6=np.round(np.array(r6),decimals=2)
    
    r8=[]
    tmp=dim8-raw
    for i in range(0,raw.shape[0],len):
        r8.append(np.array(tmp[i:i+len,:].sum(axis=0)/len))
    r8=np.round(np.array(r8),decimals=2)

    List={'len':r2.shape[0],'dim':raw.shape[1],'r2':r2.tolist(),'r4':r4.tolist(),'r6':r6.tolist(),'r8':r8.tolist(),'tags':tags.tolist()}
    return jsonify(List)



if __name__ == '__main__':
    app.run(host= '0.0.0.0',port='5000')
