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
df_repr = pd.read_pickle('Repreguntas')


#%%
df_repr['confianza inicial'].describe()
sub_repr = df_repr.drop(['user id', 'question id', 'statement index', 'orden', 'distancia', 'timer'], axis = 1)
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
    
    vc_nm = np.mean(group_nm['variacion confianza'])
    vc_md = np.mean(group_md['variacion confianza'])
    vc_mnd = np.mean(group_mnd['variacion confianza'])
    
    
    print(np.mean(group_md['variacion confianza']),i,'md')
    print(np.mean(group_nm['variacion confianza']),i,'nm')
    print(np.mean(group_mnd['variacion confianza']),i,'mnd')
    
    plt.xlabel('ALi')
    plt.ylabel('Variacion confianza promedio')
    plt.plot(i*10+5,vc_nm,'b.')
    plt.plot(i*10+5,vc_md,'r.')
    plt.plot(i*10+5,vc_mnd,'g.')