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
#Creo el DataFrame de usuarios
dicc2 = np.array(['id', 'completo', 'orientacion_politica', 'polarizacion', 'zero'])
df_users = pd.DataFrame(data = Us, columns = dicc2)
df_users.set_index('id', inplace = True) #Uso los ID de usuarios como index
df_users.index = df_users.index.astype(int, copy = False)
del df_users['completo'] #Borro columnas irrelevantes
del df_users['zero']
df_users['edad'] = v.crear_edad(df_N)
df_users['genero'] = v.crear_genero(df_N) #Agrego columnas género, edad, religiosidad
df_users['genero'] = df_users['genero'].map({1: 'fem', 2: 'masc'}) #Reemplazo 1 por 'fem' y 2 por 'masc'
df_users['religiosidad'] = v.crear_religiosidad(df_N)

#%% Inicializo las variables
repreguntas = np.array(np.where(df_N['es_repr'] == 1))[0] #Array de repreguntas

statements = np.array([])
variacion_confianza = np.array([])
variacion_agreement = np.array([])
manipulada = np.array([])
distancia = np.array([])
deteccion = np.array([])
religiosidad = np.array([])
confianza_inicial = np.array([])
agreement_inicial = np.array([])
ed_lvl = np.array([])
timer = np.array([])
#%% For's que iteran sobre repreguntas y statements, llenando las variables para el análisis  
for repregunta in repreguntas:
    statements = np.append(statements, v.buscar_statement(df_N, repregunta))
    variacion_agreement = np.append(variacion_agreement, v.crear_variacion_de_agreement(df_N, repregunta))
    manipulada = np.append(manipulada, v.crear_variable_manipulada(df_N, repregunta))
    deteccion = np.append(deteccion, v.crear_deteccion(df_N, repregunta))
    agreement_inicial = np.append(agreement_inicial, v.crear_agreement_inicial(df_N, repregunta))
    timer = np.append(timer, v.crear_timer(df_N, repregunta))
    
for repregunta, statement in zip(repreguntas, statements):
    variacion_confianza = np.append(variacion_confianza, v.crear_variacion_de_confianza(df_N, repregunta, statement))
    distancia = np.append(distancia, v.crear_distancia(repregunta, statement))
    confianza_inicial = np.append(confianza_inicial, v.crear_confianza_inicial(df_N, statement))
#%%    
#Defino variables derivadas de columas de df_users
genero = df_users['genero']
edad = df_users['edad']
polarizacion = df_users['polarizacion']
religiosidad = df_users['religiosidad']
v.colapsar_educacion(df_N, ed_lvl)

#Creo el DataFrame de repreguntas, donde el index = index de la repregunta
dicc3 = np.array(['statements', 'manipulada', 'deteccion', 'distancia', 'variacion agreement', 'variacion confianza'])
df_repr = pd.DataFrame(data = [statements, manipulada, deteccion, distancia, variacion_agreement, variacion_confianza])
df_repr = df_repr.T
df_repr.index = repreguntas
df_repr.columns = dicc3
df_repr['confianza inicial'] = confianza_inicial
df_repr['agreement inicial'] = agreement_inicial

#%% Guardo el df Repregunta

#df_repr.to_pickle('Repreguntas')
#Cuando lo quiera levantar uso df_repr = pd.read_pickle('Repreguntas')

