# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 15:33:25 2019

@author: rocco
"""

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
import funciones as v

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
dicc = np.array(['id','pais','user_id','fork','qst_id','qst_type','answer','es_repr','answer_repr','valor_presentado','comm','confianza','omit','tester','timer','fecha'])
df_N = pd.DataFrame(data = N, columns = dicc)
# Borro las columnas irrelevantes para el análisis
del df_N['comm']
del df_N['omit']
del df_N['tester']
del df_N['id']
#%%
repreguntas = np.array(np.where(df_N['es_repr'] == 1))[0] #Array de repreguntas

statements = np.array([])
varC = np.array([])
varA = np.array([])
treatment = np.array([])

def buscar_statement(repregunta):
    return np.where((df_N['qst_id'] == df_N.loc[repregunta]['qst_id']) & (df_N['user_id'] == df_N.loc[repregunta]['user_id']) & (df_N['es_repr'] == 0))

def crear_variacion_de_confianza(index_repregunta, index_statement):
    return abs(df_N.loc[index_repregunta]['confianza'] - df_N.loc[index_statement]['confianza'])
    
def crear_variacion_de_agreement(index_repregunta):
    if df_N.loc[index_repregunta]['answer_repr'] != -1:
        return abs(df_N.loc[index_repregunta]['answer'] - df_N.loc[index_repregunta]['answer_repr'])
    
def crear_variable_treatment(index_repregunta):
    if df_N.loc[index_repregunta]['answer'] != df_N.loc[index_repregunta]['valor_presentado']:
        return True
    else: return False
 #%%   
for repregunta in repreguntas:
    statements = np.append(statements, buscar_statement(repregunta))
    varA = np.append(varA, crear_variacion_de_agreement(repregunta))
    treatment = np.append(treatment, crear_variable_treatment(repregunta))
    
for repregunta, statement in zip(repreguntas, statements):
    varC = np.append(varC, crear_variacion_de_confianza(repregunta, statement))

#%%
RCl = []
RCo = []
RMx = []

PrCl = np.array(np.where((df_N['qst_id']==52) & (df_N['pais']=='Chile'))[0]) ##array de prguntas CL

for i in PrCl:
    RCl += [df_N.loc[i,'answer']]
    
PrCo = np.array(np.where((df_N['qst_id']==52) & (df_N['pais']=='Colombia'))[0]) ##array de prguntas Co

for i in PrCo:
    RCo += [df_N.loc[i,'answer']]
    
PrMx = np.array(np.where((df_N['qst_id']==52) & (df_N['pais']=='Mexico'))[0]) ##array de prguntas Mx

for i in PrMx:
    RMx += [df_N.loc[i,'answer']]

#%%
# A partir de aca liberal es 0 y conservador 100:
LCCl = 100 - np.array(RCl)
LCCo = 100 - np.array(RCo)
LCMx = 100 - np.array(RMx)

normalizoCl = []
normalizoCo = []
normalizoMx = []

v.normalizacion_lineal(LCCl,normalizoCl)
v.normalizacion_lineal(LCCo,normalizoCo)
v.normalizacion_lineal(LCMx,normalizoMx)


nLC=[normalizoCl,normalizoCo,normalizoMx]
#%%
#plt.hist(RCl,bins=range(1,101))