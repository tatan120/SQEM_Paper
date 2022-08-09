#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:03:15 2021

@author: dusanparedes
"""
import pandas as pd
import numpy as np
from Pfcm import Pfcm

def welfare(arg,params,e1,e2,e3):
    L_01=arg[0]
    w_01=arg[1]
    Ubar=arg[2]
    Abar=arg[3]
    h_all_nor=arg[4]
    r_all=arg[5]
    GA=arg[6]
    tau=arg[7]
    Omega0=arg[8]
    Lambda0=arg[9]
    Pi0=arg[10]
    poor=arg[11]
    exen=arg[12]
    Pob=arg[13]
    h_all=arg[14]
    L=arg[15]
    

        
    delta1=params[1]
    delta2=params[2]
    delta3=params[3]
    iota=params[4]
    alpha=params[5]
    gamma1=params[6] 
    gamma2=params[7]
    gamma3=params[8]
    beta=params[9]
    eta=params[10]
    sigma=params[11] 
    barN=params[12] 
    
    #e1=0.5
    #e2=0.5
    #e3=0.5  


    #csvF2 = pd.read_csv('db_gem.csv')
    
    #poor=csvF2["pobres"]
    #exen=csvF2["h_exentos"]
    #f=0.25*FCM*np.ones(barN,dtype=object)/barN
    #f=f+0.1*FCM*(np.array(poor))/(sum(poor))
    #f=f+0.3*FCM*(np.array(exen))/(sum(exen))
    #IPP_PC=np.multiply(IPP,np.power(L_01,-1))  
    #f=f+0.35*np.multiply(FCM/(barN-1),(np.ones(barN,dtype=object)-IPP_PC/np.sum(IPP_PC)))
    #f=FCM*Pfcm(L_01,poor,IPP,exen,htotal)
    #E=(np.multiply(w_01,L_01)+f-np.multiply(delta2,Pat)-delta3*Per)
    #AR=np.power((np.ones(barN,dtype=object)+gamma3*(delta1*iota-np.ones(barN,dtype=object))),-1)
    #E=np.multiply(E,AR)
    
    
    Omega=Omega0*(L_01*Pob/L)**e1
    Lambda=Lambda0*(L_01*Pob/L)**e2
    Pi=Pi0*(L_01*Pob/L)**e3
    FCM_sent=delta1*Omega+delta2*Lambda+delta3*Pi
    IPP=(1-delta1)*Omega+np.multiply((np.ones(barN)-delta2),Lambda)+(1-delta3)*Pi
    FCM=np.sum(FCM_sent)
    f=FCM*Pfcm(L_01,poor,IPP,exen,h_all)
    E=(np.multiply(w_01,L_01)+f-delta1*Omega-np.multiply(delta2,Lambda)-delta3*Pi)
    E=E/(1-gamma3)
        #f=FCM*Pfcm(L_01,poor,IPP,exen,htotal)
        #E=(np.multiply(w_01,L_01)+f-np.multiply(delta2,Pat)-delta3*Per)
    #AR=np.power((np.ones(barN,dtype=object)+gamma3*(delta1*iota-np.ones(barN,dtype=object))),-1)
    #E=np.multiply(E,AR)
    
    
    
    #Computing P
    P=np.multiply(np.multiply(tau, w_01.reshape(barN,1)),np.power(np.multiply(Abar,np.power(L_01,alpha)).reshape(barN,1),-1))
    P=np.power(np.sum(np.power(P,1-sigma),0),1/(1-sigma))
    
    #Joint price index
    PI=(P**(gamma1+gamma2))*(r_all**gamma3) 
    Pmean=np.mean(PI)
    PI=PI/Pmean
    
    #Computing Welfare
    U=np.multiply(Ubar,np.power(L_01,-beta))
    W=np.multiply(np.multiply(U*GA,np.power(E,gamma1+gamma3)),np.power(IPP+f,gamma2))
    W=np.multiply(np.multiply(np.multiply(W,np.power(P,-gamma1-gamma2)),np.power(r_all,-gamma3)),np.power(L_01,-gamma1-eta*gamma2-gamma3))
    return W,PI,P,f,IPP