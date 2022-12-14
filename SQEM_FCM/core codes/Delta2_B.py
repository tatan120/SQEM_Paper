# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:31:46 2022

@author: sebas
"""

Wd=[]
DV=[]

out_matrix2b=pd.DataFrame(columns=["comuna1","comuna","delta2","L","w","PI","f","ip","welfare"])


# #################################################################################################
# #Iteración sobre delta2 solo 4 pagan
for s in np.linspace(625,1000,20):
    arg1=arg[:] 
    params1=params[:]
    params1[2]=(s/1000)*np.ceil(params1[2])
    DV.append(s/1000)
    [Lf,wf,RR,RR1,RR2,RR3]=Recover_Lw(arg1,params1,Abar,Ubar,e1,e2,e3)
    Arg1=[Lf,wf,Ubar,Abar,h_all,r_all,GA,tau,Omega0,Lambda0,Pi0,np.array(csvF["pobres"]), np.array(csvF["h_exento"]),sum(csvF["L"]),np.array(csvF["h_all"]),np.array(csvF["L"])]
    W,PI,P,f,IP=welfare(Arg1,params1,e1,e2,e3)
    #Guardar variables#
    out_df['Wel33_delta2B_'+str(10*s)]=np.array(W)
    delta_m=(s/1000)*np.ones(len(np.array(W)))
    Wnew=out_df['Wel33_delta2B_'+str(10*s)].mean()
    Wd.append((Wnew-Wold)*100/Wold)
    out_df['Pob33_delta2B_'+str(10*s)] = Lf*sum(csvF["L"])
    out_df['Sal33_delta2B_'+str(10*s)] = wf*sum(csvF["w_mean"])
    out_df['PI33_delta2B_'+str(10*s)] = PI
    out_df['fondo33_delta2B_'+str(10*s)] = f
    out_df['IP33_delta2B_'+str(10*s)] = IP
    
    data1={"comuna1":csvF["comuna1"],"comuna":csvF["comuna"],"delta2":delta_m,"L":Lf*sum(csvF["L"]),"w":wf*sum(csvF["w_mean"]),"PI":PI,"PI_Wr":P,"f":f,"ip":IP,"welfare":np.array(W)}
    out_matrix_m=pd.DataFrame(data1)
    if s==0:
        out_matrix2b=out_matrix_m
    else:
        out_matrix2b=out_matrix2b.append(out_matrix_m,ignore_index=True)
    print(Wd)
    
    
    print(Wd)
data2B={"Delta 2":DV, "Porcentual Welfare Changes":Wd}
delta2B_PC=pd.DataFrame(data2B)
delta2B_PC.to_csv(r'ResultadosDelta2B.csv')
out_matrix2b.to_csv(r'Delta2b_Resultados.csv')

# #################################################################################################
