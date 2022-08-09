
from sklearn import linear_model  
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn
#import seaborn as sns



htotal=np.array(csvF["h_all"])


#Creación de nueva base de datos
out_df=csvF[["comuna1","comuna","Ubar","Abar","L","w_mean","Welfare","h_all"]]
out_matrix1=pd.DataFrame(columns=["comuna1","comuna","delta1","L","w","PI","f","ip","welfare"])
Wold=out_df["Welfare"].mean()
out_df["REG"]=np.zeros(barN)
for i in range(1,16):
    out_df.loc[round(out_df["comuna1"]/1000,0)==i,["REG"]]=i
    
out_df["MR"]=np.zeros(barN)
out_df.loc[out_df["REG"]==13,["MR"]]=1

Wd=[]
DV=[]
prueba=9
# #################################################################################################
# #Iteración sobre delta ,3,4,5,6,7,8,9,10
for s in np.linspace(0,1000,20):
    arg1=arg[:] 
    params1=params[:]
    params1[1]=s/1000
    DV.append(s/1000)
    [Lf,wf,RR,RR1,RR2,RR3]=Recover_Lw(arg1,params1,Abar,Ubar,e1,e2,e3)
    Arg1=[Lf,wf,Ubar,Abar,h_all,r_all,GA,tau,Omega0,Lambda0,Pi0,np.array(csvF["pobres"]), np.array(csvF["h_exento"]),sum(csvF["L"]),np.array(csvF["h_all"]),np.array(csvF["L"])]
    W,PI,P,f,IP=welfare(Arg1,params1,e1,e2,e3)
    #Guardar variables#
    out_df['Wel33_delta'+str(10*s)]=np.array(W)
    delta_m=(s/1000)*np.ones(len(np.array(W)))
    Wnew=out_df['Wel33_delta'+str(10*s)].mean()
    Wd.append((Wnew-Wold)*100/Wold)
    out_df['Pob33_delta'+str(10*s)] = Lf*sum(csvF["L"])
    out_df['Sal33_delta'+str(10*s)] = wf*sum(csvF["w_mean"])
    out_df['PI33_delta'+str(10*s)] = PI
    out_df['fondo33_delta'+str(10*s)] = f
    out_df['IP33_delta'+str(10*s)] = IP
    data1={"comuna1":csvF["comuna1"],"comuna":csvF["comuna"],"delta1":delta_m,"L":Lf*sum(csvF["L"]),"w":wf*sum(csvF["w_mean"]),"PI":PI,"PI_Wr":P,"f":f,"ip":IP,"welfare":np.array(W)}
    out_matrix_m=pd.DataFrame(data1)
    if s==0:
        out_matrix1=out_matrix_m
    else:
        out_matrix1=out_matrix1.append(out_matrix_m,ignore_index=True)
    print(Wd)
data1={"Delta 1":DV, "Porcentual Welfare Changes":Wd}
delta1_PC=pd.DataFrame(data1)
delta1_PC.to_csv(r'ResultadosDelta1.csv')
out_matrix1.to_csv(r'Delta1_Resultados.csv')