# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 10:30:16 2021

@author: sebas
"""

import pandas as pd
import numpy as np


for s in [10,12,14,16,18,20,22,24,26,28,30,32]:

#Loading data###############################################################################################################################
csvF2 = pd.read_csv('db_gem1_1412021.csv')
csvF2.dropna(how='any', inplace=True)
csvF2["h_exento"]=csvF["h_e_"+str(s)]
csvF2["tax_base"]=csvF["tax_"+str(s)]

csvF2 = csvF2[['comuna1','comuna','w_mean','L','L_workers','r_all',
'impterritorial', 'patentescom', 'percirculacion','IP','IPP','pobres','h_exento','h_all','tax_base']]
#csvF["L"]=csvF["L_workers"]

8+
csvF2['h_all']=csvF2['h_all'].astype('float')
  .0csvF2.loc[csvF2["comuna"]=="SANTIAGO",["delta2"]]=0.55
csvF2.loc[csvF2["comuna"]=="PROVIDENCIA",["delta2"]]=0.65
csvF2.loc[csvF2["comuna"]=="LAS CONDES",["delta2"]]=0.65
csvF2.loc[csvF2["comuna"]=="VITACURA" ,["delta2"]]=0.65
delta2=np.array(csvF2["delta2"])
#csvF.loc[csvF["comuna"]=="SANTIAGO",["patentescom"]]=csvF["patentescom"]*(1/0.45) #es igual a 1/0.45      
#csvF.loc[csvF["comuna"]=="PROVIDENCIA",["patentescom"]]=csvF["patentescom"]*(1/0.35) #es igual a 1/0.35
#csvF.loc[csvF["comuna"]=="LAS CONDES",["patentescom"]]=csvF["patentescom"]*(1/0.35) #es igual a 1/0.35
#csvF.loc[csvF["comuna"]=="VITACURA",["patentescom"]]=csvF["patentescom"]*(1/0.35) #es igual a 1/0.35
#csvF["percirculacion"]=csvF["percirculacion"]*2.666
csvF["patentescom"]=1000*csvF["patentescom"]
csvF["percirculacion"]=1000*csvF["percirculacion"]
csvF['impterritorial']=1000*csvF['impterritorial']
csvF['IPP']=1000*csvF['IPP']
csvF['IP']=1000*csvF['IP']
poor=np.array(csvF['pobres'])
exen=np.array(csvF['h_exento'])
rexen=22300000/np.sum(np.array(csvF["w_mean"]))
Pob=np.sum(csvF['L'])
Pat=np.array(csvF["patentescom"])/np.sum(np.array(csvF["w_mean"]))
Pat=Pat/sum(csvF["L"])
Per=np.array(csvF["percirculacion"])/np.sum(np.array(csvF["w_mean"]))
Per=Per/sum(csvF["L"])#COnfirmar con Alicia la métrica de las patentes y permisos.
r_all=np.array(csvF["r_all"])/np.sum(np.array(csvF["w_mean"]))
h_all=np.array(csvF["h_all"])/np.sum(np.array(csvF["h_all"]))
#Omega cero
#csvF['Omega0']=np.zeros(barN,dtype=object)
#csvF.loc[csvF['r_all']>rexen*np.sum(np.array(csvF["w_mean"])),'Omega0']=iota*(csvF['r_all']-rexen*np.sum(np.array(csvF["w_mean"])))*csvF['h_all']
csvF['Omega0']=iota*csvF['tax_base']
Omega0=np.array(csvF['Omega0'])/np.sum(csvF['w_mean'])
Omega0=Omega0/np.sum(csvF['L'])
#Lambda cero
csvF['Lambda0']=csvF['patentescom']
Lambda0=np.array(csvF['Lambda0'])/np.sum(csvF['w_mean'])
Lambda0=Lambda0/np.sum(csvF['L'])
#Pi cero
csvF['Pi0']=csvF['percirculacion']
Pi0=np.array(csvF['Pi0'])/np.sum(csvF['w_mean'])
Pi0=Pi0/np.sum(csvF['L'])
#Fondo enviado
csvF['FCM_sent']=delta1*csvF['Omega0']+csvF['delta2']*csvF['Lambda0']+delta3*csvF['Pi0']
FCM=np.sum(np.array(csvF['FCM_sent']))
#IPP
csvF['IPP_0']=(1-delta1)*csvF['Omega0']+(1-csvF['delta2'])*csvF['Lambda0']+(1-delta3)*csvF['Pi0']
f=FCM*Pfcm(csvF['L'],poor,csvF['IPP_0'],exen,csvF['h_all'])
csvF['E0']=csvF['w_mean']*csvF['L']
csvF['E1']=csvF['E0']+f
csvF['E2']=csvF['E1']-csvF['delta2']*csvF['Lambda0']-delta3*csvF['Pi0']
csvF['Etotal']=csvF['E2']/(1+gamma3*(delta1*iota-1))
#prueba
# IPI=0.25*np.ones(len(csvF['L']),dtype=object)/len(csvF['L'])
# IPC=0.1*poor/np.sum(poor)
# alfa=np.multiply(exen**2/np.sum(exen),np.power(csvF['h_all'],-1))



#Matriz de distancia
R=csv[1:,1:]
tau=np.exp(t*R/np.max(R))
GA=np.power(gamma1,gamma1)*np.power(gamma3,gamma3)

csvF["test"]=np.zeros((barN,1))

for i in range(0,barN):
    csvF.loc[csvF["comuna"]==csv[1:,0],["test"]]=1
print("La matriz de distancia y la matriz de datos tienen " + str(np.mean(csvF["test"]))
      + " comunas incorrectas")
    

#Recovering A_bar and U_bar#################################################################################################################
Abar=np.ones(barN,dtype=object)/barN
Ubar=np.ones(barN,dtype=object)/barN

params=[t,delta1,delta2,delta3,iota,alpha,gamma1,gamma2,gamma3,beta,eta,sigma,barN]
arg=[csvF["L"]/sum(csvF["L"]),csvF["w_mean"]/sum(csvF["w_mean"]),Ubar,Abar,h_all,r_all,GA,tau,Omega0,Lambda0,Pi0,np.array(csvF["pobres"]), np.array(csvF["h_exento"]),sum(csvF["L"]),np.array(csvF["h_all"]),np.array(csvF['L'])]

