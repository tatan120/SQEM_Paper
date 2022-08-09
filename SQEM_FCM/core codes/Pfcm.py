import numpy as np
import pandas as pd

def Pfcm(L,poor,IPP1,hexen,htotal):
  IPI=0.25*np.ones(len(L),dtype=object)/len(L)
  IPC=0.1*poor/np.sum(poor)
  alfa=np.multiply(hexen**2/np.sum(hexen),np.power(htotal,-1))
  IXC=0.3*alfa/np.sum(alfa)
  #M=np.sqrt((hexen/htotal)*(rexen/rtotal))
  #P=np.sqrt((np.sum(hexen)/np.sum(htotal))*(np.sum(rexen)/np.sum(rtotal)))
  IPPh=IPP1/L
  IPPhP=np.sum(IPP1)/np.sum(L)
  IIP=np.zeros(len(L),dtype=object)
  S=0
  for i in range(len(IPPh)):
    if IPPh[i]<IPPhP:
      IIP[i]=0.35*L[i]*(IPPhP-IPPh[i])
      S=S+L[i]*(IPPhP-IPPh[i])
  if np.abs(S)<10**(-15):
      IIP=0.35*np.ones(len(L),dtype=object)/len(L)
  else:
      IIP=IIP/S    
  return IIP+IXC+IPC+IPI