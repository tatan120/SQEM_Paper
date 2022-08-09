# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:38:32 2022

@author: sebas
"""

Wd=[]
DV=[]

out_matrixE=pd.DataFrame(columns=["comuna1","comuna","Exento","L","w","PI","f","ip","welfare"])


for s in [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,33]:
    DV.append(s)
    csvFA = pd.read_csv('G:\Mi unidad\SQEM_FCM\datos\db_gem1_2022.csv')
    #csvFA.dropna(how='any', inplace=True)
    if s<10:
        csvFA["h_exento"]=csvFA["h_e_0"+str(s)]
        csvFA["tax_base"]=csvFA["tax_0"+str(s)]
    else:
        csvFA["h_exento"]=csvFA["h_e_"+str(s)]
        csvFA["tax_base"]=csvFA["tax_"+str(s)]
    #taxbasse2017 taxbase2018
    
    csvFA = csvFA[['comuna1','comuna','w_mean','L','L_workers','r_all',
    'impterritorial', 'patentescom', 'percirculacion','IP','IPP','pobres','h_exento','h_all','tax_base','v_arriendo']]
    #csvFA["L"]=csvFA["L_workers"]
    csvFA["v_arriendo"].fillna((csvFA["v_arriendo"].mean()),inplace=True)
    
    barN=len(csvFA["L"])
    csvFA["w_mean"]=csvFA["w_mean"]*12
    #csv = np.genfromtxt('G:\Mi unidad\SQEM_FCM\datos\dmatrix2022.csv', delimiter=",")
    #no_zeros=np.array(np.zeros(barN))
    #for i in range(0,barN):
    #    no_zeros[i]=csv[i+1,i+1]
    #print("La matriz de distancia tienen " + str(np.mean(no_zeros))
    #      + " comunas incorrectas")
    
    #Matriz de distancia
    #R=csv[1:,1:]
    #R1=R.copy()
    #R1[R1==0]=1
    #tau=np.exp(t*R/np.max(R))
    #Phat=np.dot((R1**-1.5),np.array(csvFA["v_arriendo"]).reshape(barN,1))-np.array(csvFA["v_arriendo"]).reshape(barN,1)
    #csvFA["Phat"]=Phat
    #csvFA.loc[csvFA["v_arriendo"]==0,["v_arriendo"]]=csvFA["Phat"]
    #csvFA.loc[csvFA["comuna"]=="VIÑA DEL MAR",["comuna"]]="VINA DEL MAR"
    #csvFA.loc[csvFA["comuna"]=="MAIPÚ",["comuna"]]="MAIPU"
    
    
    ############################################################################################################################################
    #Creating additional variables##############################################################################################################
    csvFA['h_all']=csvFA['h_all'].astype('float')
    csvFA["delta2"]=np.zeros((barN,1))
    csvFA.loc[csvFA["comuna"]=="SANTIAGO",["delta2"]]=0.55
    csvFA.loc[csvFA["comuna"]=="PROVIDENCIA",["delta2"]]=0.65
    csvFA.loc[csvFA["comuna"]=="LAS CONDES",["delta2"]]=0.65
    csvFA.loc[csvFA["comuna"]=="VITACURA" ,["delta2"]]=0.65
    delta2=np.array(csvFA["delta2"])
    #csvFA.loc[csvFA["comuna"]=="SANTIAGO",["patentescom"]]=csvFA["patentescom"]*(1/0.45) #es igual a 1/0.45      
    #csvFA.loc[csvFA["comuna"]=="PROVIDENCIA",["patentescom"]]=csvFA["patentescom"]*(1/0.35) #es igual a 1/0.35
    #csvFA.loc[csvFA["comuna"]=="LAS CONDES",["patentescom"]]=csvFA["patentescom"]*(1/0.35) #es igual a 1/0.35
    #csvFA.loc[csvFA["comuna"]=="VITACURA",["patentescom"]]=csvFA["patentescom"]*(1/0.35) #es igual a 1/0.35
    #csvFA["percirculacion"]=csvFA["percirculacion"]*2.666
    csvFA["patentescom"]=1000*csvFA["patentescom"]
    csvFA["percirculacion"]=1000*csvFA["percirculacion"]
    csvFA['impterritorial']=1000*csvFA['impterritorial']
    csvFA['IPP']=1000*csvFA['IPP']
    csvFA['IP']=1000*csvFA['IP']
    poor=np.array(csvFA['pobres'])
    exen=np.array(csvFA['h_exento'])
    rexen=22300000/np.sum(np.array(csvFA["w_mean"]))
    Pob=np.sum(csvFA['L'])
    Pat=np.array(csvFA["patentescom"])/np.sum(np.array(csvFA["w_mean"]))
    Pat=Pat/sum(csvFA["L"])
    Per=np.array(csvFA["percirculacion"])/np.sum(np.array(csvFA["w_mean"]))
    Per=Per/sum(csvFA["L"])#COnfirmar con Alicia la métrica de las patentes y permisos.
    r_all=np.array(csvFA["r_all"])/np.sum(np.array(csvFA["w_mean"]))
    h_all=np.array(csvFA["h_all"])/np.sum(np.array(csvFA["h_all"]))
    #Omega cero
    #csvFA['Omega0']=np.zeros(barN,dtype=object)
    #csvFA.loc[csvFA['r_all']>rexen*np.sum(np.array(csvFA["w_mean"])),'Omega0']=iota*(csvFA['r_all']-rexen*np.sum(np.array(csvFA["w_mean"])))*csvFA['h_all']
    csvFA['Omega0']=iota*csvFA['tax_base']
    Omega0=np.array(csvFA['Omega0'])/np.sum(csvFA['w_mean'])
    Omega0=Omega0/np.sum(csvFA['L'])
    #Lambda cero
    csvFA['Lambda0']=csvFA['patentescom']
    Lambda0=np.array(csvFA['Lambda0'])/np.sum(csvFA['w_mean'])
    Lambda0=Lambda0/np.sum(csvFA['L'])
    #Pi cero
    csvFA['Pi0']=csvFA['percirculacion']
    Pi0=np.array(csvFA['Pi0'])/np.sum(csvFA['w_mean'])
    Pi0=Pi0/np.sum(csvFA['L'])
    #Fondo enviado
    csvFA['FCM_sent']=delta1*csvFA['Omega0']+csvFA['delta2']*csvFA['Lambda0']+delta3*csvFA['Pi0']
    FCM=np.sum(np.array(csvFA['FCM_sent']))
    #IPP
    csvFA['IPP_0']=(1-delta1)*csvFA['Omega0']+(1-csvFA['delta2'])*csvFA['Lambda0']+(1-delta3)*csvFA['Pi0']
    f=FCM*Pfcm(csvFA['L'],poor,csvFA['IPP_0'],exen,csvFA['h_all'])
    csvFA['E0']=csvFA['w_mean']*csvFA['L']
    csvFA['E1']=csvFA['E0']+f
    csvFA['E2']=csvFA['E1']-csvFA['delta2']*csvFA['Lambda0']-delta3*csvFA['Pi0']
    csvFA['Etotal']=csvFA['E2']/(1+gamma3*(delta1*iota-1))
    #prueba
    # IPI=0.25*np.ones(len(csvFA['L']),dtype=object)/len(csvFA['L'])
    # IPC=0.1*poor/np.sum(poor)
    # alfa=np.multiply(exen**2/np.sum(exen),np.power(csvFA['h_all'],-1))
    
    
    
    
    GA=np.power(gamma1,gamma1)*np.power(gamma3,gamma3)
    
    csvFA["test"]=np.zeros((barN,1))
    
    for i in range(0,barN):
        csvFA.loc[csvFA["comuna"]==csv[1:,0],["test"]]=1
    print("La matriz de distancia y la matriz de datos tienen " + str(np.mean(csvFA["test"]))
          + " comunas incorrectas")
        
    
    #Recovering A_bar and U_bar#################################################################################################################
    #Abar=np.ones(barN,dtype=object)/barN
    #Ubar=np.ones(barN,dtype=object)/barN
    
    params1=[t,delta1,delta2,delta3,iota,alpha,gamma1,gamma2,gamma3,beta,eta,sigma,barN]
    arg1=[csvFA["L"]/sum(csvFA["L"]),csvFA["w_mean"]/sum(csvFA["w_mean"]),Ubar,Abar,h_all,r_all,GA,tau,Omega0,Lambda0,Pi0,np.array(csvFA["pobres"]), np.array(csvFA["h_exento"]),sum(csvFA["L"]),np.array(csvFA["h_all"]),np.array(csvFA['L'])]
    [Lf,wf,RR,RR1,RR2,RR3]=Recover_Lw(arg1,params1,Abar,Ubar,e1,e2,e3)
    Arg1=[Lf,wf,Ubar,Abar,h_all,r_all,GA,tau,Omega0,Lambda0,Pi0,np.array(csvF["pobres"]), np.array(csvF["h_exento"]),sum(csvF["L"]),np.array(csvF["h_all"]),np.array(csvF["L"])]
    W,PI,P,f,IP=welfare(Arg1,params1,e1,e2,e3)
    #Guardar variables#
    out_df['Wel_exen_'+str(s)]=np.array(W)
    delta_m=(s)*np.ones(len(np.array(W)))
    Wnew=out_df['Wel_exen_'+str(s)].mean()
    Wd.append((Wnew-Wold)*100/Wold)
    out_df['Pob_exen_'+str(s)] = Lf*sum(csvF["L"])
    out_df['Sal_exen_'+str(s)] = wf*sum(csvF["w_mean"])
    out_df['PI_exen_'+str(s)] = PI
    out_df['fondo_exen_'+str(s)] = f
    out_df['IP_exen_'+str(s)] = IP
    
    data1={"comuna1":csvF["comuna1"],"comuna":csvF["comuna"],"Exento":delta_m,"L":Lf*sum(csvF["L"]),"w":wf*sum(csvF["w_mean"]),"PI":PI,"PI_Wr":P,"f":f,"ip":IP,"welfare":np.array(W)}
    out_matrix_m=pd.DataFrame(data1)
    if s==0:
        out_matrixE=out_matrix_m
    else:
        out_matrixE=out_matrixE.append(out_matrix_m,ignore_index=True)
        
    print(Wd)
dataExen={"Valor Exento":DV, "Porcentual Welfare Changes":Wd}
deltaExen_PC=pd.DataFrame(dataExen)
deltaExen_PC.to_csv(r'ResultadosExentos.csv')
out_matrixE.to_csv(r'Exen_Resultados.csv')