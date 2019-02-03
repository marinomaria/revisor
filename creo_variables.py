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
import variables as v
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
df_users['edad'] = v.crear_edad(df_N)
df_users['genero'] = v.crear_genero(df_N)
df_users['genero'] = df_users['genero'].map({1: 'fem', 2: 'masc'})

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
for repregunta in repreguntas:
    statements = np.append(statements, v.buscar_statement(df_N, repregunta))
    variacion_agreement = np.append(variacion_agreement, v.crear_variacion_de_agreement(df_N, repregunta))
    treatment = np.append(treatment, v.crear_variable_treatment(df_N, repregunta))
    deteccion = np.append(deteccion, v.crear_deteccion(df_N, repregunta))
    
for repregunta, statement in zip(repreguntas, statements):
    variacion_confianza = np.append(variacion_confianza, v.crear_variacion_de_confianza(df_N, repregunta, statement))
    distancia = np.append(distancia, v.crear_distancia(repregunta, statement))
    

genero = df_users['genero']
edad = df_users['edad']
polarizacion = df_users['polarizacion']
