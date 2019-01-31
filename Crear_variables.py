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

dicc2 = np.array(['id', 'completo', 'orientacion_politica', 'polarizacion', 'zero'])
df_users = pd.DataFrame(data = Us, columns = dicc2)
df_users.set_index('id', inplace = True)
df_users.index = df_users.index.astype(int, copy = False)
del df_users['completo']
del df_users['zero']
#%%
repreguntas = np.array(np.where(df_N['es_repr'] == 1))[0] #Array de repreguntas

statements = np.array([])
variacion_confianza = np.array([])
variacion_agreement = np.array([])
treatment = np.array([])
distancia = np.array([])
deteccion = np.array([])
#timer = np.array([])
#%%
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
    
def crear_distancia(repregunta, statement):
    return repregunta - statement

def crear_deteccion(index_repregunta):
    if df_N.loc[index_repregunta]['answer_repr'] != -1:
        return True
    else: return False
    
def crear_genero():
    return np.array(df_N.loc[np.where(df_N['qst_id'] == 29)[0]]['answer'])

def crear_edad():
    return np.array(df_N.loc[np.where(df_N['qst_id'] == 30)[0]]['answer'])

#def crear_timer(index_repregunta):
#    if df_N.loc[index_repregunta]['timer'] != 0:
#        return df_N.loc[index_repregunta]['timer']
#    else: return np.nan   
#%%   
for repregunta in repreguntas:
    statements = np.append(statements, buscar_statement(repregunta))
    variacion_agreement = np.append(variacion_agreement, crear_variacion_de_agreement(repregunta))
    treatment = np.append(treatment, crear_variable_treatment(repregunta))
    deteccion = np.append(deteccion, crear_deteccion(repregunta))
    
for repregunta, statement in zip(repreguntas, statements):
    variacion_confianza = np.append(variacion_confianza, crear_variacion_de_confianza(repregunta, statement))
    distancia = np.append(distancia, crear_distancia(repregunta, statement))
    
df_users['genero'] = crear_genero()
df_users['genero'] = df_users['genero'].map({1: 'fem', 2: 'masc'})
genero = df_users['genero']

edad = crear_edad()
df_users['edad'] = edad

polarizacion = df_users['polarizacion']