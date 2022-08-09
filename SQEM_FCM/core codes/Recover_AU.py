#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 12:05:56 2021

@author: dusanparedes
"""
import pandas as pd
import numpy as np
from Pfcm import Pfcm

def Recover_AU(arg,params,e1,e2,e3):
    #Convergence parameters
    update=0.25
    tol = 1e-15
    maxi= 15000
    diff= 1
    it  = 0
    
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
    
    #e1=0.01
    #e2=0.01
    #e3=0.03

    #Initial wage and population
    L_01=np.array(L_01)/np.sum(np.array(L_01))
    w_01=np.array(w_01)/np.sum(np.array(w_01))
        
    while (diff>tol and it<maxi):   
        #f=0.25*FCM*np.ones(barN,dtype=object)/barN
        #f=f+0.10*FCM*(np.array(poor))/(sum(poor))
        #f=f+0.30*FCM*(np.array(exen))/(sum(exen))
        #IPP_PC=np.multiply(IPP,np.power(L_01*Pob,-1))
        #f=f+0.35*np.multiply(FCM/(barN-1),(np.ones(barN,dtype=object)-IPP_PC/np.sum(IPP_PC)))
        Omega=Omega0*(L_01*Pob/L)**e1
        Lambda=Lambda0*(L_01*Pob/L)**e2
        Pi=Pi0*(L_01*Pob/L)**e3
        FCM_sent=delta1*Omega+delta2*Lambda+delta3*Pi
        IPP=(1-delta1)*Omega+(1-delta2)*Lambda+(1-delta3)*Pi
        FCM=np.sum(FCM_sent)
        f=FCM*Pfcm(L_01,poor,IPP,exen,h_all)
        E=(np.multiply(w_01,L_01)+f-delta1*Omega-np.multiply(delta2,Lambda)-delta3*Pi)
        #AR=np.power((np.ones(barN,dtype=object)+gamma3*(delta1*iota-np.ones(barN,dtype=object))),-1)
        E=E/(1-gamma3)
    
    #Solving equation for U_bar
        aux1_1=np.power(tau,1-sigma)
        aux1_2=np.multiply(np.multiply(np.power(w_01,1-sigma),np.power(Abar,sigma-1)),np.power(L_01,(sigma-1)*alpha))
        aux1_3=((GA)**((sigma-1)/(1-gamma3)))*np.sum(np.multiply(aux1_1,aux1_2.reshape(barN,1)),0)
        aux1_4=np.multiply(aux1_3,np.power(r_all,gamma3*(1-sigma)/(1-gamma3)))
        aux1_5=np.multiply(aux1_4,np.power(IPP+f,gamma2*(sigma-1)/(1-gamma3)))
        aux1_6=np.multiply(aux1_5,np.power(E,(gamma1+gamma3)*(sigma-1)/(1-gamma3)))
        aux1_7=np.multiply(aux1_6,np.power(L_01,(sigma-1)*(-beta-gamma1-gamma3-eta*gamma2)/(1-gamma3)))
        Ubar_1=np.power(aux1_7,(1-gamma3)/(1-sigma))
    
    #Solving equation for A_bar
        aux2_1=np.power(L_01,-gamma1-gamma3-eta*gamma2)
        aux2_2=np.multiply(aux2_1,np.power(r_all,-gamma3))
        aux2_3=np.multiply(aux2_2,np.power(IPP+f,gamma2))
        aux2_4=np.multiply(aux2_3,np.power(E,gamma1+gamma3))
        aux2_5=np.multiply(aux2_4,np.multiply(Ubar,np.power(L_01,-beta)))
        aux2_6=np.power(GA*aux2_5,(sigma-1)/(1-gamma3))
        aux2_7=(gamma1+gamma2)*np.multiply(aux2_6,E)
        aux2_8=np.sum(np.multiply(aux1_1,aux2_7.reshape(barN,1)),1)
        aux2_9=np.multiply(np.power(w_01,-sigma),np.power(L_01,-1+alpha*(sigma-1)))
        Abar_1=np.power(np.multiply(aux2_8,aux2_9),1/(1-sigma))
        
    #Setting convergence
        su=sum(Ubar_1)
        au=sum(Abar_1)
        Ubar_1=Ubar_1/(sum(Ubar_1))
        Abar_1=Abar_1/(sum(Abar_1))
        diff=np.linalg.norm(Ubar_1-Ubar,2)+np.linalg.norm(Abar_1-Abar,2)
        Ubar=update*Ubar_1+(1-update)*Ubar
        Abar=update*Abar_1+(1-update)*Abar
        for i in range(barN):
            Ubar[i]=Ubar[i].real
            Abar[i]=Abar[i].real
        Ubar=Ubar/np.sum(Ubar)
        Abar=Abar/np.sum(Abar)
        it=it+1
        
    #Recovering U_bar and A_bar in levels and adding to database
  
    
    Ubar2=Ubar*su
    Abar2=Abar*au
    return Ubar,Abar