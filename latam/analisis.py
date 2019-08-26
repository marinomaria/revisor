# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 20:15:06 2019

@author: Casa
"""
#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import funciones as v
#%%
df_repr = pd.read_csv('Repreguntas.csv',index_col=0)
df_users = pd.read_csv('Usuarios.csv',index_col=0)


#%%
df_repr['confianza inicial'].describe()
sub_repr = df_repr.drop(['question id', 'statement index', 'orden', 'distancia', 'timer'], axis = 1)
for i in range(10):
    group_nm = sub_repr.where((sub_repr['confianza inicial']  >= 10*i) & (sub_repr['confianza inicial'] <= 10*(i+1)) & (sub_repr['manipulada']==0)).dropna(how = 'all')
    group_md = sub_repr.where((sub_repr['confianza inicial']  >= 10*i) & (sub_repr['confianza inicial'] <= 10*(i+1)) & (sub_repr['manipulada']==1) & (sub_repr['deteccion']==1)).dropna(how = 'all')
    group_mnd = sub_repr.where((sub_repr['confianza inicial']  >= 10*i) & (sub_repr['confianza inicial'] <= 10*(i+1)) & (sub_repr['manipulada']==1) & (sub_repr['deteccion']==0)).dropna(how = 'all')
    
    vc_nm = np.mean(group_nm['variacion confianza'])
    vc_md = np.mean(group_md['variacion confianza'])
    vc_mnd = np.mean(group_mnd['variacion confianza'])
    
    
    print(np.mean(group_md['variacion confianza']),i,'md')
    print(np.mean(group_nm['variacion confianza']),i,'nm')
    print(np.mean(group_mnd['variacion confianza']),i,'mnd')
     
    plt.xlabel('Confianza Inicial')
    plt.ylabel('Variacion confianza promedio')
    plt.plot(i*10+5,vc_nm,'b.')
    plt.plot(i*10+5,vc_md,'r.')
    plt.plot(i*10+5,vc_mnd,'g.')
#%%   
ALi = np.abs(sub_repr['agreement inicial'] - 50) * 2
sub_repr['ALi'] = ALi
#%%
for i in range(10):
    group_nm = sub_repr.where((sub_repr['ALi']  >= 10*i) & (sub_repr['ALi'] <= 10*(i+1)) & (sub_repr['manipulada']==0)).dropna(how = 'all')
    group_md = sub_repr.where((sub_repr['ALi']  >= 10*i) & (sub_repr['ALi'] <= 10*(i+1)) & (sub_repr['manipulada']==1) & (sub_repr['deteccion']==1)).dropna(how = 'all')
    group_mnd = sub_repr.where((sub_repr['ALi']  >= 10*i) & (sub_repr['ALi'] <= 10*(i+1)) & (sub_repr['manipulada']==1) & (sub_repr['deteccion']==0)).dropna(how = 'all')
    
    vc_nm = group_nm['variacion confianza']
    vc_md = group_md['variacion confianza']
    vc_mnd = group_mnd['variacion confianza']
    
    
    print(np.mean(group_md['variacion confianza']),i,'md')
    print(np.mean(group_nm['variacion confianza']),i,'nm')
    print(np.mean(group_mnd['variacion confianza']),i,'mnd')
    
    plt.xlabel('ALi')
    plt.ylabel('Variacion confianza promedio')
    plt.plot(i*10+4,np.mean(vc_nm),'b.')
    plt.errorbar(i*10+4,np.mean(vc_nm),yerr=np.std(vc_nm)/np.sqrt(len(vc_nm)),color='black')
    plt.plot(i*10+5,np.mean(vc_md),'r.')
    plt.errorbar(i*10+5,np.mean(vc_md),yerr=np.std(vc_md)/np.sqrt(len(vc_md)),color='black')
    plt.plot(i*10+6,np.mean(vc_mnd),'g.')
    plt.errorbar(i*10+6,np.mean(vc_mnd),yerr=np.std(vc_mnd)/np.sqrt(len(vc_mnd)),color='black')
    
    #%%
   #Dropeo algunas columnas que no voy a usar para que el algoritmo itere mas rapido.
sub_repr = df_repr.drop(['question id', 'statement index', 'orden', 'distancia', 'timer'], axis = 1) 
sub_users = df_users.drop(['fork', 'genero', 'pais', 'nivel educativo'], axis = 1)
# Defino una lista de strings con las variables de usuarios que se cuantifican de 0 a 100 (orientacion politica,
# polarizacion, edad, religiosidad, conservador/liberal)
variables = list(sub_users.columns) 


#Hago un for adentro de otro for para plotear todo a la vez. el primer for define la variable de users.
# el segundo for lo voy a usar para partir a la poblacion en subgrupos segun esa variable, en grupos de 0 a 10, 10 a 20, etc.
# Una vez elegido var e i, el algoritmo arma el subgrupo, se queda con los id de los que estan en ese subgrupo
# y luego vuelve a separar el subgrupo segun nm, md, mnd. Por ultimo calcula la media de varconf en cada subgrupo y plotea.

for var in variables:
    for i in range(10):
        subgrupo = sub_users.where((sub_users[var] >= 10*i) & (sub_users[var] <= 10*(i+1))).dropna(how = 'all')
        repr_subgrupo = sub_repr[sub_repr['user id'].isin(subgrupo.index)] #el index de subgrupo son los user id.
        
        
        repr_subgrupo_nm = repr_subgrupo[repr_subgrupo['manipulada']==0]
        repr_subgrupo_md = repr_subgrupo[(repr_subgrupo['manipulada']==1) & (repr_subgrupo['deteccion']==1)]
        repr_subgrupo_mnd = repr_subgrupo[(repr_subgrupo['manipulada']==1) & (repr_subgrupo['deteccion']==0)]
        
        varconf_nm = np.mean(repr_subgrupo_nm['variacion confianza'])
        varconf_md = np.mean(repr_subgrupo_md['variacion confianza'])
        varconf_mnd = np.mean(repr_subgrupo_mnd['variacion confianza'])
        
        
        plt.xlabel(var)
        plt.ylabel('Variacion confianza promedio')
        plt.plot(i*10+5,varconf_nm,'b.')
        plt.plot(i*10+5,varconf_md,'r.')
        plt.plot(i*10+5,varconf_mnd,'g.')  
    plt.show()
    plt.clf()