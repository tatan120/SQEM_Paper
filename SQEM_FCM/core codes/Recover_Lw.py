#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 12:48:39 2021

@author: dusanparedes
"""
import pandas as pd
import numpy as np
from Pfcm import Pfcm

def Recover_Lw(arg,params,Abar,Ubar,e1,e2,e3):
   
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
    
    #e1=0.01
    #e2=0.01
    #e3=0.03

    #Solving for w and L########################################################################################################################
    L_01=np.ones(barN,dtype=object)/barN
    w_01=np.ones(barN,dtype=object)/barN
    
    #Convergence parameters
    update=0.25
    tol = 1e-15
    maxi= 15000
    diff= 1
    it  = 0
    
    #Numerical approximation to get L and w
    
    while (diff>tol and it<maxi):
        L_t0=L_01
        w_t0=w_01
        
        #f=0.25*FCM*np.ones(barN,dtype=object)/barN
        #f=f+0.10*FCM*(np.array(poor))/(sum(poor))
        #f=f+0.30*FCM*(np.array(exen))/(sum(exen))
        #IPP_PC=np.multiply(IPP,np.power(L_01*Pob/np.sum(L_01),-1))    
        #f=f+0.35*np.multiply(FCM/(barN-1),(np.ones(barN,dtype=object)-IPP_PC/np.sum(IPP_PC)))
        Omega=Omega0*(L_01*Pob/L)**e1
        Lambda=Lambda0*(L_01*Pob/L)**e2
        #print((L_01*Pob/L)**e2)
        Pi=Pi0*(L_01*Pob/L)**e3
        FCM_sent=delta1*Omega+delta2*Lambda+delta3*Pi
        IPP=(1-delta1)*Omega+(1-delta2)*Lambda+(1-delta3)*Pi
        FCM=np.sum(FCM_sent)
        f=FCM*Pfcm(L_01,poor,IPP,exen,h_all)
        E=(np.multiply(w_01,L_01)+f-delta1*Omega-np.multiply(delta2,Lambda)-delta3*Pi)
        #f=FCM*Pfcm(L_01,poor,IPP,exen,htotal)
        #E=(np.multiply(w_01,L_01)+f-np.multiply(delta2,Pat)-delta3*Per)
        #AR=np.power((np.ones(barN,dtype=object)+gamma3*(delta1*iota-np.ones(barN,dtype=object))),-1)
        E=E/(1-gamma3)
    
    #Solving equation for L
        aux1_1=np.power(tau,1-sigma)
        aux1_2=np.multiply(np.multiply(np.power(w_01,1-sigma),np.power(Abar,sigma-1)),np.power(L_01,(sigma-1)*alpha))
        aux1_3=((GA)**((sigma-1)/(1-gamma3)))*np.sum(np.multiply(aux1_1,aux1_2.reshape(barN,1)),0)
        aux1_4=np.multiply(aux1_3,np.power(r_all,gamma3*(1-sigma)/(1-gamma3)))
        aux1_5=np.multiply(aux1_4,np.power(IPP+f,gamma2*(sigma-1)/(1-gamma3)))
        aux1_6=np.multiply(aux1_5,np.power(E,(gamma1+gamma3)*(sigma-1)/(1-gamma3)))
        aux1_7=np.multiply(aux1_6,np.power(Ubar,(sigma-1)/(1-gamma3)))
        L_1=np.power(aux1_7,(1-gamma3)/((1-sigma)*(-beta-gamma1-gamma3-eta*gamma2)))
    
    #Solving equation for w
        aux2_1=np.power(L_01,-gamma1-gamma3-eta*gamma2)
        aux2_2=np.multiply(aux2_1,np.power(r_all,-gamma3))
        aux2_3=np.multiply(aux2_2,np.power(IPP+f,gamma2))
        aux2_4=np.multiply(aux2_3,np.power(E,gamma1+gamma3))
        aux2_5=np.multiply(aux2_4,np.multiply(Ubar,np.power(L_01,-beta)))
        aux2_6=np.power(GA*aux2_5,(sigma-1)/(1-gamma3))
        aux2_7=(gamma1+gamma2)*np.multiply(aux2_6,E)
        aux2_8=np.sum(np.multiply(aux1_1,aux2_7.reshape(barN,1)),1)
        aux2_9=np.multiply(np.power(Abar,sigma-1),np.power(L_01,-1+alpha*(sigma-1)))
        w_1=np.power(np.multiply(aux2_8,aux2_9),1/sigma)
        L_t=L_1
        
    #Setting convergence
        L_1=L_1/(sum(L_1))
        w_1=w_1/(sum(w_1))
        for i in range(barN):
            L_1[i]=L_1[i].real
            w_1[i]=w_1[i].real
        diff=np.linalg.norm(L_1-L_01,2)+np.linalg.norm(w_1-w_01,2)
        L_01=update*L_1+(1-update)*L_01
        w_01=update*w_1+(1-update)*w_01
        for i in range(barN):
            L_01[i]=L_01[i].real
            w_01[i]=w_01[i].real
        L_01=L_01/np.sum(L_01)
        w_01=w_01/np.sum(w_01)
        it=it+1
    return L_01,w_01,L_t,E,L_t0*Pob,w_t0
