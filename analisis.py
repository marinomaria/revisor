# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 20:15:06 2019

@author: Casa
"""
#%%
import numpy as np
import pandas as pd
import funciones as v
#%%
df_repr = pd.read_pickle('Repreguntas')


#%%
df_repr['confianza inicial'].describe()
asd = df_repr.where((df_repr['confianza inicial']  > 79) & (df_repr['confianza inicial'] < 91)).dropna(how = 'all')


 
