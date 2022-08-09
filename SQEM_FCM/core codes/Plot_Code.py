# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:43:04 2022

@author: sebas
"""

# #################################################################################################
# #welfare plot####
# ################
Wd2=np.array(Wd).real
fig, ax = plt.subplots(figsize=(10,10))
ax.plot(DV,Wd2,linewidth=0.6, marker="o",mfc='none')
ax.margins(x=0, tight=True)
ax.spines['top'].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlabel("$\delta_1$", fontsize=16)
ax.set_ylabel("Welfare change (%)", fontsize=16)
ax.set_title("Welfare change for $\delta_1$ simulations", fontsize=16)
ax.plot(np.linspace(0,1,100),np.zeros(100),color="red",linestyle ="--",linewidth=2, alpha=0.2)
ax.margins(x=0, tight=True)
ax.set_ylim(bottom=-7, top=2)
ax.set_xlim(left=0.1, right=1)
threshold = 5
ax.fill_between(DV, Wd2, 0, alpha=0.04, where = Wd2 >= 0.0000, color='blue')
ax.fill_between(DV, Wd2, 0, alpha=0.04, where = Wd2 < 0.08105224658103674, color='red' )
#ax.set_title('We')
ax.text(0.45,1, 'Welfare gain', fontsize=12, c='r')
ax.text(0.82,-1.4, 'Welfare loss', fontsize=12, c='r')
ax.text(0.12,-1.4, 'Welfare loss', fontsize=12, c='r')
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.vlines(x=0.6, ymin=-7, ymax=0, colors='r', ls=':', lw=2, label='vline_single')
plt.savefig('Plots/Welfare_delta1')
plt.show()

#################################################################################################
###Convergence betas ###############################################################


for s in [1,2,3,4,5,6,7,8,9,10]:
    out_df['growth'+str(10*s)]=(out_df['Pob33_delta'+str(10*s)]-(out_df["L"]))/(out_df["L"])*100
    
data2=pd.DataFrame(out_df,columns=['L','growth10','growth20','growth30','growth40','growth50','growth60','growth70',
'growth80','growth90','growth100','Sal33_delta10','Sal33_delta100','REG'], dtype=np.float64)
betas=np.zeros((10,3))
for s in [1,2,3,4,5,6,7,8,9,10]:
    m,b=np.polyfit(data2["L"],data2['growth'+str(10*s)],1)
    betas[s-1,0]=s/10
    betas[s-1,1]=b
    betas[s-1,2]=m
print(betas)

fig1 = plt.figure(figsize=(20,20))
ax10 = fig1.add_subplot(111)
ax10.plot(betas[:,0], betas[:,2], color ="red", linewidth=0.6, marker="o",mfc='none')
ax10.plot(np.linspace(0,1,100),np.zeros(100),linestyle ="--",linewidth=2, alpha=0.2,c='r')
ax10.set_xlabel("$\delta_1$", fontsize=22)
ax10.set_ylabel("Beta convergence", fontsize=22)
ax10.set_title("Beta convergence for $\delta_1$ simulations", fontsize=24)
ax10.spines['top'].set_visible(False)
ax10.spines['right'].set_visible(False) 
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
ax10.margins(x=0, tight=True)
ax10.set_xlim(left=0, right=1)
plt.show()

# ###Convergence plot###############################################################

fig1 = plt.figure(figsize=(20,20))
fig1.suptitle('Population convergende for $\delta_1$ simulations', fontsize=16)
ax10 = fig1.add_subplot(221)
ax40 = fig1.add_subplot(222)
ax70 = fig1.add_subplot(223)
ax90 = fig1.add_subplot(224)
Names=[ax10,ax40,ax70,ax90]
Vals=[10,40,70,90]
# out_df['growth10']=(out_df['Pob33_delta10']-(out_df["L"]))/(out_df["L"])*100
# out_df['growth40']=(out_df['Pob33_delta40']-(out_df["L"]))/(out_df["L"])*100
# out_df['growth70']=(out_df['Pob33_delta70']-(out_df["L"]))/(out_df["L"])*100
# out_df['growth90']=(out_df['Pob33_delta90']-(out_df["L"]))/(out_df["L"])*100
pop_limit = 300000
#data2=pd.DataFrame(out_df,columns=['L', 'Pob33_delta10','Pob33_delta40','Pob33_delta70','Pob33_delta90','growth10','growth40','growth70','growth90'], dtype=np.float64)

colors={}
for i in range(1,16):
    if i==13:
        colors[i]="red"
    else:
        colors[i]="orange"
for AX in Names:
    d=Vals[Names.index(AX)]
    AX.scatter(data2["L"],data2['growth'+str(d)],s=10,marker = 'x',c=data2["REG"].map(colors))
    AX.plot(np.linspace(0,750000,100),np.zeros(100),linestyle ="--",linewidth=2, alpha=0.2,c='r')
    AX.set_xlabel("Observed population")
    AX.set_ylabel("Population growth")
    AX.set_title("Population convergence for $\delta_1$ ="+str(d))
    AX.margins(x=0, tight=True)
    csvF["label"]=np.zeros((barN,1))
    csvF.loc[csvF["L"]>pop_limit,["label"]]=csvF["comuna"]
    csvF.loc[csvF["label"]==0,["label"]]=""
    label=csvF["label"]
    for x_pos, y_pos, label in zip(out_df["L"], out_df["growth"+str(d)], label):
        AX.annotate(label,             # The label for this point
        xy=(x_pos, y_pos), # Position of the corresponding point
        xytext=(7, 0),     # Offset text by 7 points to the right
        textcoords='offset points', # tell it to use offset points
        ha='left',         # Horizontally aligned to the left
        va='center')       # Vertical alignment is centered
    XA=np.linspace(0,10,1000)
    m,b=np.polyfit(data2['L'],data2['growth'+str(d)],1)
    ploy_delta10=AX.plot(data2['L'],m*data2['L']+b, linewidth=0.4, color='g')
    AX.legend([ploy_delta10[0]], ['Beta convergence'], frameon=False, bbox_to_anchor=(0.7,0.09))
    #AX.text(590000,40, r'$\beta$ =' +str(round(m,5)), fontsize=13, c='r')
    AX.spines['top'].set_visible(False)
    AX.spines['right'].set_visible(False) 

colors2 = {'Metropolitan Region':'gold', 'No Metropolitan Region':'orange'}         
labels = list(colors2.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors2[label]) for label in labels]
plt.savefig('Plots/convergence_delta1')
plt.show()




# #################################################################################################
# #####Simulated population
fig = plt.figure(figsize=(32,32))
ax1 = fig.add_subplot(221)
ax1.set_xlim(left=0, right=720000)
ax1.set_ylim(bottom=0, top=900000)
ax2 = fig.add_subplot(222)
ax2.set_xlim(left=0, right=720000)
ax2.set_ylim(bottom=0, top=900000)
ax3 = fig.add_subplot(223)
ax3.set_xlim(left=0, right=720000)
ax3.set_ylim(bottom=0, top=900000)
ax4 = fig.add_subplot(224)
ax4.set_xlim(left=0, right=720000)
ax4.set_ylim(bottom=0, top=900000)

#Delta10####################################################################
ax1.scatter(out_df["L"],out_df["Pob33_delta10"])
XA=np.linspace(0,720000,1000)
linea45=ax1.plot(XA,XA,color="r",linestyle ="--",linewidth=2, alpha=0.2)
ax1.legend([linea45[0]], ['Simulated=Observed ($\delta_1$ = 0.6)'],bbox_to_anchor=(0.56,0.09), frameon=False, prop={'size': 12})
ax1.set_title('$\delta_1$ = 0.1')
ax1.set_xlabel('Observed population')
ax1.set_ylabel('Simulated population')
csvF["label"]=np.zeros((barN,1))
csvF.loc[csvF["L"]>pop_limit,["label"]]=csvF["comuna"]
csvF.loc[csvF["label"]==0,["label"]]=""
label=csvF["label"]
for x_pos, y_pos, label in zip(out_df["L"], out_df["Pob33_delta10"], label):
    ax1.annotate(label,             # The label for this point
    xy=(x_pos, y_pos), # Position of the corresponding point
    xytext=(7, 0),     # Offset text by 7 points to the right
    textcoords='offset points', # tell it to use offset points
    ha='left',         # Horizontally aligned to the left
    va='center')       # Vertical alignment is centered
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False) 

#Delta40####################################################################
ax2.scatter(out_df["L"],out_df["Pob33_delta40"])
XA=np.linspace(0,720000,1000)
ax2.plot(XA,XA,color="r",linestyle ="--",linewidth=2, alpha=0.2)
ax2.set_title('$\delta_1$ = 0.4')
ax2.set_xlabel('Observed population')
ax2.set_ylabel('Simulated population')
csvF["label"]=np.zeros((barN,1))
csvF.loc[csvF["L"]>pop_limit,["label"]]=csvF["comuna"]
csvF.loc[csvF["label"]==0,["label"]]=""
label=csvF["label"]
for x_pos, y_pos, label in zip(out_df["L"], out_df["Pob33_delta40"], label):
    ax2.annotate(label,             # The label for this point
    xy=(x_pos, y_pos), # Position of the corresponding point
    xytext=(7, 0),     # Offset text by 7 points to the right
    textcoords='offset points', # tell it to use offset points
    ha='left',         # Horizontally aligned to the left
    va='center')       # Vertical alignment is centered
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)   

#Delta70####################################################################
ax3.scatter(out_df["L"],out_df["Pob33_delta70"])
XA=np.linspace(0,720000,1000)
ax3.plot(XA,XA,color="r",linestyle ="--",linewidth=2, alpha=0.2)
ax3.set_title('$\delta_1$ = 0.7')
ax3.set_xlabel('Observed population')
ax3.set_ylabel('Simulated population')
csvF["label"]=np.zeros((barN,1))
csvF.loc[csvF["L"]>pop_limit,["label"]]=csvF["comuna"]
csvF.loc[csvF["label"]==0,["label"]]=""
label=csvF["label"]
for x_pos, y_pos, label in zip(out_df["L"], out_df["Pob33_delta70"], label):
    ax3.annotate(label,             # The label for this point
    xy=(x_pos, y_pos), # Position of the corresponding point
    xytext=(7, 0),     # Offset text by 7 points to the right
    textcoords='offset points', # tell it to use offset points
    ha='left',         # Horizontally aligned to the left
    va='center')       # Vertical alignment is centered
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

#Delta90####################################################################

ax4.scatter(out_df["L"],out_df["Pob33_delta90"])
XA=np.linspace(0,720000,1000)
ax4.plot(XA,XA,color="r",linestyle ="--",linewidth=2, alpha=0.2)
ax4.set_title('$\delta_1$ = 0.9')
ax4.set_xlabel('Observed population')
ax4.set_ylabel('Simulated population')
csvF["label"]=np.zeros((barN,1))
csvF.loc[csvF["L"]>pop_limit,["label"]]=csvF["comuna"]
csvF.loc[csvF["label"]==0,["label"]]=""
label=csvF["label"]
for x_pos, y_pos, label in zip(out_df["L"], out_df["Pob33_delta90"], label):
    ax4.annotate(label,             # The label for this point
    xy=(x_pos, y_pos), # Position of the corresponding point
    xytext=(7, 0),     # Offset text by 7 points to the right
    textcoords='offset points', # tell it to use offset points
    ha='left',         # Horizontally aligned to the left
    va='center')   
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
colors = {'Metropolitan Region':'red', 'No Metropolitan Region':'orange'}         
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels,bbox_to_anchor=(0.5,0.8), prop={'size': 12}, frameon=False)
plt.savefig('Plots/pop_simulated_delta1')
plt.show()












# #################################################################################################
# #################################################################################################
# #Bar plots with population differential
import numpy as np

out_df['Diff_pop_delta_90']=out_df["Pob33_delta90"]-out_df["L"]
fig, ax = plt.subplots(figsize=(20,15))
colors = {'Metropolitan Region':'gold', 'No Metropolitan Region':'orange'}         
labels = list(colors.keys())
ppp = out_df[(out_df['Diff_pop_delta_90']>15000) | (out_df['Diff_pop_delta_90']<-15000)]
ppp.sort_values('Diff_pop_delta_90',inplace=True)
ax.bar(ppp['comuna'], ppp['Diff_pop_delta_90'],color="orange",alpha=0.8)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')


plt.rcParams['axes.edgecolor']='#333F4B'
plt.rcParams['axes.linewidth']=0.8
plt.rcParams['xtick.color']='#333F4B'
plt.rcParams['ytick.color']='#333F4B'
plt.xticks(rotation='vertical', size = 12)

plt.yticks(np.arange(-200000, 200000, 10000), size = 8)

ax.spines['right'].set_color('none')
ax.spines["left"].set_position(("axes", .52))
ax.spines["bottom"].set_position(("axes", .499))

ax.set_ylim(bottom=-200000, top=200000)

ax.spines['top'].set_color('none')
plt.xticks( rotation='vertical', size = 12)
ax.margins(y=0, tight=True)
colors = {'Metropolitan Region':'gold', 'No Metropolitan Region':'orange'}         
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
#plt.legend(handles, labels,bbox_to_anchor=(0.8,0.4), prop={'size': 12})
plt.axhline(y=80000,color="r",linestyle ="--",linewidth=2, alpha=0.2)
plt.axhline(y=-80000,color="r",linestyle ="--",linewidth=2, alpha=0.2)

plt.savefig("neg_pos")
plt.show()




# #######################################
df7=out_df.copy()
df=out_df.copy()
delta = np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]) # (N,) array-like

####################################################3
from collections import defaultdict
import seaborn as sns
from scipy import stats
from scipy import interpolate
#sns.set_style("ticks")

def add_widths(x, y, width=0.1):
    """ Adds flat parts to widths """
    new_x = []
    new_y = []
    for i,j in zip(x,y):
        new_x += [i-width, i, i+width]
        new_y += [j, j, j]
    return new_x, new_y

def bumpsplot(dataframe, color_dict=defaultdict(lambda: "k"), 
                          linewidth_dict=defaultdict(lambda: 1),
                          labels=[]):
    r = dataframe.rank(method="first")
    r = (r - r.max() + r.max().max()).fillna(0) # Sets NAs to 0 in rank
    for i in r.index:
        x = np.arange(r.shape[1])
        y = r.loc[i].values
        color = color_dict[i]
        lw = linewidth_dict[i]
        x, y = add_widths(x, y, width=0.1)
        xs = np.linspace(0, x[-1], num=1024)
        plt.plot(xs, interpolate.PchipInterpolator(x, y)(xs), color=color, linewidth=lw, alpha=0.5)
        if i in labels:
            plt.text(x[0] - 0.1, y[0]+0.1, s=i, horizontalalignment="right", verticalalignment="center", color=color,fontsize=15)
            plt.text(x[-1] + 0.1, y[-1], s=i, horizontalalignment="left", verticalalignment="center", color=color,fontsize=15)
    plt.xticks(np.arange(r.shape[1]), dataframe.columns)
####################################################3

##DESCENDING####
#df4=pd.DataFrame([],columns=("comuna","Poblacion","delta"))
for s in delta:
    if s>0.1:
        df4=df5
    df5=pd.DataFrame(df["comuna"])
    df5["Poblacion"]=df['Pob33_delta'+str(int(100*s))]
    df5["delta"]=int(100*s)
    if s>0.1:
        df5=pd.concat([df4, df5])
df5 = df5.groupby(["comuna", "delta"])["Poblacion"].sum().unstack()
df6=df5.copy()
df6["TOT"]=df6[100]-df6[60]
df6=df6.sort_values(["TOT"],ascending=True)

winter_colors = defaultdict(lambda: "grey")
lw = defaultdict(lambda: 1)
top_comunas = df6.iloc[0:10, 0].index
df5=df5.sort_values([100],ascending=True)
df5=df5.loc[df5[100]>80000]

for i,c in enumerate(top_comunas):
    winter_colors[c] = sns.color_palette("husl", n_colors=len(top_comunas))[i]
    lw[c] = 4
plt.figure(figsize=(18,12))
plt.axes(frameon=False)
bumpsplot(df5, color_dict=winter_colors, linewidth_dict=lw, labels=top_comunas)
plt.gca().get_yaxis().set_visible(False)
plt.grid()
plt.xlabel("$\delta$ (%)", fontsize=16)
#plt.xticks(df5.shape[1])
#plt.xticks([10,20,30,40,50,60,70,80,90,100])
plt.xticks(fontsize=20)
plt.title('Municipalities ranking with population reduction over 80.000 inhabitants for $\delta_1$ simulations (comparison with $\delta_1$=0.6)', fontsize=18)

plt.savefig('descending.pdf')
plt.show()

##ASCENDING####
#df4=pd.DataFrame([],columns=("comuna","Poblacion","delta"))
for s in delta:
    if s>0.1:
        df4=df5
    df5=pd.DataFrame(df["comuna"])
    df5["Poblacion"]=df['Pob33_delta'+str(int(100*s))]
    df5["delta"]=int(100*s)
    if s>0.1:
        df5=pd.concat([df4, df5])
df5 = df5.groupby(["comuna", "delta"])["Poblacion"].sum().unstack()
df6=df5.copy()
df6["TOT"]=df6[100]-df6[60]
df6=df6.sort_values(["TOT"],ascending=False)

winter_colors = defaultdict(lambda: "grey")
lw = defaultdict(lambda: 1)
top_comunas = df6.iloc[0:10, 0].index
df5=df5.sort_values([100],ascending=False)
df5=df5.loc[df5[100]>80000]

for i,c in enumerate(top_comunas):
    winter_colors[c] = sns.color_palette("husl", n_colors=len(top_comunas))[i]
    lw[c] = 4
plt.figure(figsize=(18,12))
plt.axes(frameon=False)
bumpsplot(df5, color_dict=winter_colors, linewidth_dict=lw, labels=top_comunas)
plt.gca().get_yaxis().set_visible(False)
plt.grid()
plt.xlabel("$\delta$ (%)", fontsize=16)
plt.title('Municipalities ranking with population increment over 80.000 inhabitants for $\delta_1$ simulations (comparison with $\delta_1$=0.6)', fontsize=18)
#plt.xticks(df5.shape[1])
#plt.xticks([10,20,30,40,50,60,70,80,90,100])
plt.xticks(fontsize=20)
plt.savefig('ascending.pdf')
plt.show()

# #Wd=[]
# #DV=[]
