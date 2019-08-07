import torch
import torch.optim as optim
import torch.utils.data as Data
import torch.nn.functional as F
import numpy as np
from torch.autograd import Variable
import pandas as pd
import math
from sklearn import preprocessing
import torch
import torch.nn as nn
import torch.nn.functional as F
import pylab
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd 
from colour import Color

def Loader(path):
    data=np.genfromtxt(path,delimiter=',')
    #delete the first column of the data
    #first column is date info
  
    df=pd.DataFrame(data[:,0])
    data=np.delete(data,0,1)
        
    
    #get rid of the tags
    data=data[1:]
    return data

def _Normalize(_data):
    dataMin=_data.min(axis=0)
   
    dataMax=_data.max(axis=0)
    data=(_data-dataMin)/(dataMax-dataMin)
    return data,dataMin,dataMax

def Normalize(_data,dataMin,dataMax):
    new_data=(_data-dataMin)/(dataMax-dataMin)
    return new_data

def Denormalize(data,dataMin,dataMax):

    return data*(dataMax-dataMin)+dataMin

def NormalizeMeanZero(_data):
    return preprocessing.scale(_data,axis=0)

def FindClosePoint(dim,expect):
    tmp=np.array(_data)
   
    if expect>=0:
        tmp[:,dim]=tmp[:,dim]-expect
        tmp[:,dim]=tmp[:,dim]**2
    else:
        tmp[:,dim]=tmp[:,dim]*0
    
    tmp=np.sum(tmp,axis=1)
    idx=tmp.argmin()

def FindClosePoint(new_data,dim):
    match=[]
    for j in range(new_data.shape[0]):
        tmp=np.array(_data)
        expect=-np.ones(dim_size)
        expect[dim]=new_data[j,dim]      
        for i in range(expect.shape[0]):
            if expect[i]>=0:
                tmp[:,i]=tmp[:,i]-expect[i]
                tmp[:,i]=tmp[:,i]**2
            else:
                tmp[:,i]=tmp[:,i]*0
        tmp=np.sum(tmp,axis=1)

        idx=tmp.argmin()
       
        match.append(_data[idx])
    match=np.array(match)
    return match

def FindMatchLatent(latent,dim,re_data):
    
    test_x=Variable(torch.FloatTensor(latent),requires_grad=True)
   
    loss_func=nn.L1Loss()
    test_opt=optim.Adam([test_x],lr=0.1)
    for i in range(100):
        test_output=model.decoder(test_x)  
       
        cost=torch.FloatTensor([[0]])
        
        #print(str(epoch)+" "+str(test_output[0,0])+" "+str(re_data[0,0]))
        cost+=loss_func(test_output[:,dim],re_data[:,dim])
        test_opt.zero_grad()
        cost.backward()
        test_opt.step()
        if cost <1e-5:
            #print(i,cost)
            return test_output
        #print(test_x)
        #print("Epoch: [%3d], Loss: %.5f" %(epoch + 1, cost.data))
    #print(i,cost)
    return test_output


def MatchAE(labels_tags):
    
    raw_data=Loader('Plastics_and_Chemicals_Macro.csv')
    _raw_data=torch.Tensor(raw_data[:,spilt_L:spilt_H])
    data,_min,_max=_Normalize(raw_data)
    spilt_L=14
    spilt_H=30
    raw_dataset=Data.TensorDataset(_raw_data,_raw_data)
    raw_loader=Data.DataLoader(dataset=raw_dataset,batch_size=64,shuffle=False)
    labels_tags=np.load('tags.npy')
    
    model=torch.load('AE.pkl')
    model.eval()

    factor=1.1
    dim=spilt_H-spilt_L
    test_min=_min[spilt_L:spilt_H]
    test_max=_max[spilt_L:spilt_H]

    Container=[]
    Container_r=[]
    for i in range(dim):
        re=[]
        for index,(x,_) in enumerate(raw_loader):
        
            expect=x.data.numpy()
            x=Normalize(x.data.numpy(),test_min,test_max)
            x=np.array(x)
            expect[:,i]*=factor
            expect=Normalize(expect,test_min,test_max)
            #match=FindClosePoint(expect,i)
        
            encoded,decoded=model(torch.FloatTensor(x))
        
            output=FindMatchLatent(encoded,i,torch.FloatTensor(expect))
            #output=decoded
            

            for k in range(output.shape[0]):
                re.append(output[k].data.numpy())
            
        
        print(str(i)+" is processing...")
        
    
        re=Denormalize(re,test_min,test_max)
        
        #df=pd.DataFrame(re)
        #df.to_csv(".\\new\\re-50"+str(i)+".csv",header=None,index=None)
        d=(re/raw_data[:,spilt_L:spilt_H])-1
        
        d[:,i]=factor-1
        d=np.array(d,dtype=float)
        
        plt.figure()
        plt.rcParams['font.family']='Arial Unicode MS' 
        plt.xticks(rotation=90)
        plt.xticks(range(tags.shape[1]),labels_tags,fontsize=12)
        plt.imshow(d, aspect='auto',cmap='bwr',vmin=-1, vmax=1)
        #plt.imshow(np.abs(d), aspect='auto')
        #c1=plt.pcolor(np.abs(d),cmap='Reds')
        plt.colorbar()
        plt.savefig("dim"+str(i)+".png",dpi=600)
        plt.show()
        Container.append(d)
        Container_r.append(re)

        np.save('container.npy',Container)
    
def DrawDim(selectDim):
    Container=np.load('container.npy')
    raw_data=np.load('raw_data.npy')
    labels_tags=np.load('tags.npy')
    b=np.array(Container)
    #b=np.abs(b)
    b=b.sum(axis=1)
    b/=raw_data.shape[0]
    fig=plt.figure(figsize=(20,10))
    fig.patch.set_facecolor('#f2f4f7')
    #fig.patch.set_facecolor('xkcd:mint green')
    plt.rcParams['font.family']='Arial Unicode MS' 
    plt.xticks(rotation=90)
    plt.xticks(range(labels_tags.shape[0]),labels_tags,fontsize=12)
    plt.yticks(range(labels_tags.shape[0]),labels_tags,fontsize=12)
    plt.imshow(b, aspect='auto',cmap='bwr',vmin=-0.5, vmax=0.5)
    #c=plt.pcolor(b,cmap='Reds')
    #plt.imshow(b)
    plt.gca().set_aspect('equal', adjustable='box')
    if(selectDim!=-1):
        plt.gca().get_yticklabels()[selectDim].set_color('red') 
    plt.colorbar()
    plt.savefig("dimall.png",bbox_inches='tight',dpi=300,facecolor=fig.get_facecolor())
    plt.close()

