# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 17:32:40 2019

@author: rocco
"""

#%%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

usrs=pd.read_pickle('Usuarios')
repre=pd.read_pickle('Repreguntas')

fork8 = usrs.where(usrs['fork']==8)

fork8.dropna(how='all',inplace=True)

a = list(fork8.index)
id_ctrl = np.array([])

for row in repre.iterrows():
    if row[1][0] in a:
        id_ctrl = np.append(id_ctrl,row[0])  ##id_ctrl es el índice de repre de las repreguntas de usuarios control

#for x in a :
varActrl = repre.loc[id_ctrl]['variacion agreement']
varCctrl = repre.loc[id_ctrl]['variacion confianza']

#plt.hist(varActrl, density=True) #histograma de variacion de agreement en control

plt.hist(varCctrl, density=True, bins=np.linspace(min(varCctrl),max(varCctrl),101))

#%%
asd = repre.where((repre['manipulada']==1) & (repre['deteccion']==0))

asd.dropna(how='all', inplace=True)

plt.hist(asd['variacion agreement'],density=True,bins=np.linspace(min(varCctrl),max(varCctrl),101))
        
        


        
        
        

