import pandas as pd
import numpy as np

#Loading data###############################################################################################################################
csvF = pd.read_csv('db_gem1_2022.csv')
#csvF.dropna(how='any', inplace=True)
csvF["h_exento"]=csvF["h_e_22"]
csvF["tax_base"]=csvF["tax_22"]
#taxbasse2017 taxbase2018

csvF = csvF[['comuna1','comuna','w_mean','L','L_workers','r_all',
'impterritorial', 'patentescom', 'percirculacion','IP','IPP','pobres','h_exento','h_all','tax_base','v_arriendo']]
csvF["v_arriendo"].fillna((csvF["v_arriendo"].mean()),inplace=True)

barN=len(csvF["L"])
csvF["w_mean"]=csvF["w_mean"]*12
csv = np.genfromtxt('dmatrix2022.csv', delimiter=",")
no_zeros=np.array(np.zeros(barN))
for i in range(0,barN):
    no_zeros[i]=csv[i+1,i+1]
print("La matriz de distancia tienen " + str(np.mean(no_zeros))
      + " comunas incorrectas")

#Distance matrix###########################################################################################################################
R=csv[1:,1:]
tau=np.exp(t*R/np.max(R))

############################################################################################################################################
#Creating additional variables##############################################################################################################
csvF['h_all']=csvF['h_all'].astype('float')
csvF["delta2"]=np.zeros((barN,1))
csvF.loc[csvF["comuna"]=="SANTIAGO",["delta2"]]=0.55
csvF.loc[csvF["comuna"]=="PROVIDENCIA",["delta2"]]=0.65
csvF.loc[csvF["comuna"]=="LAS CONDES",["delta2"]]=0.65
csvF.loc[csvF["comuna"]=="VITACURA" ,["delta2"]]=0.65
delta2=np.array(csvF["delta2"])
csvF["fix"]=np.ones((barN,1))
csvF.loc[csvF["comuna"]=="SANTIAGO",["delta2"]]=1/0.55
csvF.loc[csvF["comuna"]=="PROVIDENCIA",["delta2"]]=1/0.65
csvF.loc[csvF["comuna"]=="LAS CONDES",["delta2"]]=1/0.65
csvF.loc[csvF["comuna"]=="VITACURA" ,["delta2"]]=1/0.65
fix=np.array(csvF["fix"])

csvF["patentescom"]=1000*np.multiply(csvF["patentescom"],fix)
csvF["percirculacion"]=1000*(1/delta3)*csvF["percirculacion"]
csvF['impterritorial']=1000*(1/delta1)*csvF['impterritorial']
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


GA=np.power(gamma1,gamma1)*np.power(gamma3,gamma3)

csvF["test"]=np.zeros((barN,1))

for i in range(0,barN):
    csvF.loc[csvF["comuna"]==csv[1:,0],["test"]]=1
print("La matriz de distancia y la matriz de datos tienen " + str(np.mean(csvF["test"]))
      + " comunas incorrectas")
    

#Recovering A_bar and U_bar arguments#################################################################################################################
Abar=np.ones(barN,dtype=object)/barN
Ubar=np.ones(barN,dtype=object)/barN

params=[t,delta1,delta2,delta3,iota,alpha,gamma1,gamma2,gamma3,beta,eta,sigma,barN]
arg=[csvF["L"]/sum(csvF["L"]),csvF["w_mean"]/sum(csvF["w_mean"]),Ubar,Abar,h_all,r_all,GA,tau,Omega0,Lambda0,Pi0,np.array(csvF["pobres"]), np.array(csvF["h_exento"]),sum(csvF["L"]),np.array(csvF["h_all"]),np.array(csvF['L'])]

