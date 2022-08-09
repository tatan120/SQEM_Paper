#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Importing packages#########################################################################################################################
import random as rn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys
from IPython import get_ipython #Use pip install Ipython if not installed
from Recover_AU import Recover_AU
from Recover_Lw import Recover_Lw
from welfare import welfare 
from Pfcm import Pfcm
############################################################################################################################################

get_ipython().magic("reset -sf")

#Setting parameters#########################################################################################################################
t=0.5*(-1.1)
delta1=0.6
delta3=0.625
iota=0.0098
alpha=0.05   #Productivity Force
gamma1=0.207 #Public Goods Elasticity
gamma2=0.65  #Consumption Elasticity
gamma3=0.143  #Housing Elasticity
beta=0.16 #Amenity
eta=1  #Rivarly parameter
sigma=1.7 #Substitution elasticity
e1=0
e2=0
e3=0.
#Simulation control variable: Default YN=1
YN=1
if YN==0:
    exec(open("loading_data.py").read())
else:
    exec(open("loading_data_2.py").read())

#Recovering Amenities and productivity ###################################################################################################################
[Ubar,Abar]=Recover_AU(arg,params,e1,e2,e3)
csvF["Ubar"]=Ubar
csvF["Abar"]=Abar

#Recovering Population and wages for double checking #####################################################################################################
[L_01,w_01,L_t,E_t,L_t0,w_t0]=Recover_Lw(arg,params,Abar,Ubar,e1,e2,e3)
csvF["L_final"]=L_01*sum(csvF["L"])
csvF["w_Final"]=w_01*sum(csvF["w_mean"])
csvF['L_t']=L_t
csvF['L_t0']=L_t0
csvF['w_t0']=w_t0*np.sum(csvF["w_mean"])
csvF['E_t']=E_t
print(csvF["L_final"]-csvF["L"])

#Recovering welfare###################################################################################################################
Arg=[np.array(csvF["L_final"])/sum(csvF["L"]),np.array(csvF["w_Final"])/sum(csvF["w_mean"]),Ubar,Abar,h_all,r_all,GA,tau,Omega0,Lambda0,Pi0,np.array(csvF["pobres"]), np.array(csvF["h_exento"]),sum(csvF["L"]),np.array(csvF["h_all"]),np.array(csvF["L"])]
W,PI,P,f,IP=welfare(Arg,params,e1,e2,e3)
csvF["Welfare"]=W
print(W)

#Contrafactual###################################################################################################################
exec(open("Delta1.py").read())
exec(open("Delta3.py").read())
exec(open("Delta2.py").read())
exec(open("Delta2_B.py").read())

if YN==0:
   exec(open("Exen.py").read())
else:
   exec(open("Exen_2.py").read())
out_df.to_csv(r'MatrizResultadosTotales.csv')

#Final Database###################################################################################################################

AU_df=out_df[["comuna1","comuna","Ubar","Abar","L","w_mean"]]
AU_df.to_csv(r'AU_DataBase.csv')

