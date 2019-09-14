# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 14:39:41 2019

@author: Milt
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%% Manipulados y no manipulados fork 1 y 3
sw = pd.read_csv('SWperez.csv', index_col = 0)
plt.figure(1)
plt.title('Manipulados')
plt.plot(np.mean([sw.A1[(sw.fork == 1) | (sw.fork == 3)],sw.A2[(sw.fork == 1) | (sw.fork == 3)]],axis = 0), np.mean([sw.A3[(sw.fork == 1) | (sw.fork == 3)],sw.A4[(sw.fork == 1) | (sw.fork == 3)]],axis = 0),'o')
plt.figure(2)
plt.title('No manipulados')
plt.plot(np.mean([sw.B1[(sw.fork == 1) | (sw.fork == 3)],sw.B2[(sw.fork == 1) | (sw.fork == 3)]],axis = 0), np.mean([sw.B3[(sw.fork == 1) | (sw.fork == 3)],sw.B4[(sw.fork == 1) | (sw.fork == 3)]],axis = 0),'o')

#%% Manipulados y no manipulados fork 1 y 3 promedio por decenas
Ai = np.mean([sw.A1[(sw.fork == 1) | (sw.fork == 3)], sw.A2[(sw.fork == 1) | (sw.fork == 3)]],axis = 0)
Af = np.mean([sw.A3[(sw.fork == 1) | (sw.fork == 3)], sw.A4[(sw.fork == 1) | (sw.fork == 3)]],axis = 0)
Bi = np.mean([sw.B1[(sw.fork == 1) | (sw.fork == 3)], sw.B2[(sw.fork == 1) | (sw.fork == 3)]],axis = 0)
Bf = np.mean([sw.B3[(sw.fork == 1) | (sw.fork == 3)], sw.B4[(sw.fork == 1) | (sw.fork == 3)]],axis = 0)

hist = np.zeros(10)
k = np.zeros(10)

histNM = np.zeros(10)
kNM = np.zeros(10)

for i in range(len(Af)):
    hist[int(Ai[i]/11)] = hist[int(Ai[i]/11)] + Af[i]
    k[int(Ai[i]/11)] = k[int(Ai[i]/11)] + 1       
    
    histNM[int(Bi[i]/11)] = histNM[int(Bi[i]/11)] + Bf[i]
    kNM[int(Bi[i]/11)] = kNM[int(Bi[i]/11)] + 1  

hist = hist/k
histNM = histNM/kNM

plt.figure()
plt.xlabel('Opening questions agreement')
plt.ylabel('Final questions agreement')
plt.title('All topics')
plt.scatter(['0-10','11-20','21-30','31-40','41-50','51-60','61-70','71-80','81-90','91-100'],hist, label = 'Non manipulated')
plt.scatter(['0-10','11-20','21-30','31-40','41-50','51-60','61-70','71-80','81-90','91-100'],histNM, label = 'Manipulated')
plt.legend()