#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 11:47:49 2021

@author: dusanparedes
"""

#Importing packages#########################################################################################################################
import random as rn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from IPython import get_ipython #Use pip install Ipython if not installed
from Recover_AUV16_12_2021_fcm import Recover_AU
from Recover_LwV16_12_2021_fcm import Recover_Lw
from welfareV16_12_2021_fcm import welfare 
from Pfcm import Pfcm

from time import sleep
from progress.bar import Bar
#prueba github
f=89
############################################################################################################################################

get_ipython().magic("reset -sf")

#Setting parameters#########################################################################################################################
t=0.5
delta1=0.6
delta3=0.625
iota=0.0098
alpha=0.05   #Fuerza de la productividad
gamma1=0.2  #Peso de los bienes públicos
gamma2=0.65  #Peso de consumo privado
gamma3=0.15  #Peso de housing
beta=0.6  #Amenidad
eta=0.5  #Parámetro de rivalidad de bienes públicos
sigma=5 #Elasticidad de sustitución 
e1=0.01
e2=0.01
e3=0.03

exec(open("loading_dataV16_12_21.py").read())

[Ubar,Abar]=Recover_AU(arg,params,e1,e2,e3)
csvF["Ubar"]=Ubar
csvF["Abar"]=Abar

[L_01,w_01,L_t,E_t,L_t0,w_t0]=Recover_Lw(arg,params,Abar,Ubar,e1,e2,e3)
csvF["L_final"]=L_01*sum(csvF["L"])
csvF["w_Final"]=w_01*sum(csvF["w_mean"])
csvF['L_t']=L_t
csvF['L_t0']=L_t0
csvF['w_t0']=w_t0*np.sum(csvF["w_mean"])

csvF['E_t']=E_t

print(csvF["L_final"]-csvF["L"])

Arg=[np.array(csvF["L_final"])/sum(csvF["L"]),np.array(csvF["w_Final"])/sum(csvF["w_mean"]),Ubar,Abar,h_all,r_all,GA,tau,Omega0,Lambda0,Pi0,np.array(csvF["pobres"]), np.array(csvF["h_exento"]),sum(csvF["L"]),np.array(csvF["h_all"]),np.array(csvF["L"])]
W=welfare(Arg,params,e1,e2,e3)
csvF["Welfare"]=W
print(W)


#exec(open("delta1V16_12_21.py").read())
Wold=np.mean(W)
RE=np.zeros((1000,5))
i=-1
for s in np.linspace(1,10,3):
    for e1 in np.linspace(0.1,1,3):
        for e2 in np.linspace(0.1,1,3):
            for e3 in np.linspace(0.1,1,3):
                arg1=arg[:] 
                params1=params[:]
                #FCM=(s/10)*iota*np.multiply(r33,H33)
                #FCM=FCM+np.multiply(delta2,Pat)
                #FCM=FCM+delta3*Per
                #FCM=np.sum(FCM)
                #IPP=(1-s/10)*iota*np.multiply(r33,H33)+np.multiply(np.ones(318,dtype=object)-delta2,Pat)+(1-delta3)*Per
                #arg1[6]=np.array(IPP)
                #arg1[9]=np.array(FCM)
                params1[1]=s/10
                #DV.append(s/10)
                [Lf,wf,RR,RR1,RR2,RR3]=Recover_Lw(arg1,params1,Abar,Ubar,e1,e2,e3)
                Arg1=[Lf,wf,Ubar,Abar,h_all,r_all,GA,tau,Omega0,Lambda0,Pi0,np.array(csvF["pobres"]), np.array(csvF["h_exento"]),sum(csvF["L"]),np.array(csvF["h_all"]),np.array(csvF["L"])]
                W=welfare(Arg1,params1,e1,e2,e3)
                #if e1==0.1 and e2==0.1 and e3=0.1:
                #    Wold=np.mean(W)
                #Guardar variables#
                Wnew=np.mean(W)
                i=i+1
                RE[i,:]=[s/10,e1,e2,e3,(Wnew-Wold)*100/Wold]
                print([s/10,e1,e2,e3])


arr = np.genfromtxt("dat.csv", delimiter=",")

# exec(open("delta3V09_12_21.py").read())


# #exec(open("delta2.py").read())

# #exec(open("delta3.py").read())
# #exec(open("delta_simulations.py").read())

# #exec(open("iota_simulations.py").read())

# #exec(open("HR_simulations.py").read())
# #
# #exec(open("EJ.py").read())