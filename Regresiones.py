# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 17:21:51 2019

@author: rocco
"""


#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import statsmodels.api as sm

#%%
#%%
#Levanto los datos y los mergeo
Datos = np.load('MatrizLimpiaConCerosmx.npz')
MX = Datos['N'] 
UsMX = Datos['Us']

Datos = np.load('MatrizLimpiaConCeroscl.npz')
CL = Datos['N'] 
UsCL = Datos['Us']

Datos = np.load('MatrizLimpiaConCerosco.npz')
Co = Datos['N'] 
UsCo = Datos['Us']

CL[:,2] = CL[:,2] + MX[len(MX)-1,2]
UsCL[:,0] = UsCL[:,0] + UsMX[len(UsMX)-1,0]

Co[:,2] = Co[:,2] + CL[len(CL)-1,2]
UsCo[:,0] = UsCo[:,0] + UsCL[len(UsCL)-1,0]

N = np.vstack((MX, CL, Co))
Us = np.vstack((UsMX, UsCL, UsCo))

#%%Los convierto en un df
dicc = np.array(['id','Pais','uid','f','qid','tp','ans','es_re','Vre','Vpp','comm','c','omit','tester','timer','fecha'])
df_N = pd.DataFrame(data = N, columns = dicc)
# Borro las columnas irrelevantes para el análisis
del df_N['comm']
del df_N['omit']
del df_N['tester']


