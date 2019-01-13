# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 16:44:57 2018

@author: Milton
"""

#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import statsmodels.api as sm


#%%
#Carga la matriz nueva para un solo pais
Datos = np.load('MatrizLimpiaConCeroscl.npz')
N = Datos['N'] 
Us= Datos['Us']


#%%
#Creo la matriz Conjunta
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

#%%
#Calculo las variables para la regresion abs(Af - Ai) ~ M + Demo + M:Demo + ALi + F + O + O:F + sign(ALi - ALf) + Tipo:CL y la variación de confianza
#Demo: Gen, Pol, SocEc, Ed, Rel
#Datos = np.load('MatrizLimpiaConCeros.npz')
#N = Datos['N'] 
#Us= Datos['Us']

varA = np.array([]) #Variación de agreement
varC = np.array([]) #Variación de confianza
M = np.array([]) #Treatment, si está manipulado es uno, si no es 0
ALi = np.array([]) #Agreement level inicial
F = np.array([]) #Fork, control es 0, tratamiento es 1
O1 = np.array([]) #número de repregunta
O2 = np.array([])
O3 = np.array([])
ALf = np.array([]) #Agreement level final
Coinc = np.array([]) #Coincidencia, si es 1 es porque la afirmación y el usuario eran conservadores o liberales. Si es 0 es porque el tipo de pregunta no coincide con el usuario
Gm = np.array([]) #Genero
Pol = np.array([]) #Polarización
SocEc = np.array([]) #Nivel socioeconómico
Rel = np.array([]) #Nivel de religiosidad
Ed = np.array([]) #Nivel educativo (colapsado en alto/bajo)
CL = np.array([]) #Conservador o Liberal
CLsm = np.array([]) #Conservador o liberal según mí)
OfOp = np.array([])
CamLad = np.array([])
Edad = np.array([]) 
Paisa = np.array([])
Paisb = np.array([])
Intera = np.array([]) #Interés en política
Interb = np.array([])
Interc = np.array([])
Interd = np.array([])
Conv = np.array([]) #Qué tan convencido está de su posición política
Freca = np.array([]) #frecuencia de participación en elecciones
Frecb = np.array([])
Frecc = np.array([])
Frecd = np.array([])
Prob = np.array([]) #Probailidad de participacion en las proximas elecciones
Vote = np.array([]) #Votó en las elecciones anteriores
Prim = np.array([]) #Votó en las elecciones primarias
#Alina = np.array([]) #Alineación política 
#Alinb = np.array([])
#VotAnt = np.array([])#Si el voto anterior coincide o no con el actual
Sort = np.array([])
Ci = np.array([])
Cf = np.array([])
qstID16 = np.array([])
qstID17 = np.array([])
qstID18 = np.array([])
qstID19 = np.array([])
qstID20 = np.array([])
qstID21 = np.array([])
qstID22 = np.array([])
qstID23 = np.array([])
qstID39 = np.array([])
qstID40 = np.array([])
qstID41 = np.array([])
usrID = np.array([])
#Timer = np.array([])
D = np.array([])
dist = np.array([])

A = np.where(N[:,7]==1)[0].astype(int) #Tomo los indices de las repreguntas
for i in A:
    
    U = np.where(N[:,2]==N[i,2])[0].astype(int)
    I = np.where(N[:,4]==N[i,4])[0].astype(int) #indices de todas las preguntas con el mismo número
    j = I[np.where(I==i)[0][0].astype(int)-1] #busco el indice de la pregunta anterior a la que estoy ubicado ahora en i, esto busca la pregunta inicial a partir de la repregunta
    
    P11 = np.where(N[U,4] == 11)[0].astype(int)    
    P12 = np.where(N[U,4] == 12)[0].astype(int)
    P29 = np.where(N[U,4] == 29)[0].astype(int)
    P44 = np.where(N[U,4] == 44)[0].astype(int)
    P50 = np.where(N[U,4] == 50)[0].astype(int)
    P51 = np.where(N[U,4] == 51)[0].astype(int)
    P31 = np.where(N[U,4] == 31)[0].astype(int)
    P52 = np.where(N[U,4] == 52)[0].astype(int)
    P13 = np.where(N[U,4] == 13)[0].astype(int)
    P30 = np.where(N[U,4] == 30)[0].astype(int)
    P45 = np.where(N[U,4] == 45)[0].astype(int)
    P48 = np.where(N[U,4] == 48)[0].astype(int)
    P7 = np.where(N[U,4] == 7)[0].astype(int) 
    P8 = np.where(N[U,4] == 8)[0].astype(int) 
    P42 = np.where(N[U,4] == 42)[0].astype(int) 
    
    # len(P7) > 0 and  not pd.isnull(N[i,14]) and N[i,14] > 0 and 
    
    if   np.sum(N[U,7])==4 and  len(P29) > 0 and len(P45) > 0 and  len(P50) > 0 and len(P51) > 0 and len(P44) > 0 and len(P31) > 0 and len(P52) > 0 and len(P13) > 0 and len(P30)>0 and N[U[P50[0]],6] < 9 and len(P11) > 0:
        
        if N[i,8] != -1:
            varA = np.append(varA, abs(N[i,6]-N[i,8]))
            ALf = np.append(ALf, 2*abs(50 - N[i,8]))
            CamLad = np.append(CamLad, int((N[i,8]-50)*(N[i,6]-50) < 0))
        else:
            varA = np.append(varA, abs(N[i,6] - N[i,9]))
            ALf = np.append(ALf, 2*abs(50 - N[i,9]))
            CamLad = np.append(CamLad, int((N[i,9]-50)*(N[i,6]-50) < 0))
            
        varC = np.append(varC,N[j,11]-N[i,11])
        
        Ci = np.append(Ci, N[j,11])
        
        Cf = np.append(Cf, N[i,11])
        
        if N[i,6] != N[i,9]:
            M = np.append(M, 1)
            if (N[i,8]-50)*(N[i,9]-50) < 0 and N[i,8] != -1:
                D = np.append(D,1)
            else:
                D = np.append(D,0)
        else:
            M = np.append(M,0)
            
        ALi = np.append(ALi, 2*abs(50 - N[i,6])) 
        
        F = np.append(F, abs(N[i,3]-8)) #1 si es tratamiento 0 si es control
        
        u = np.where(N[:(i+1),2]==N[i,2])[0].astype(int)
        
        O1 = np.append(O1, int(np.sum(N[u,7]) == 1)) #En la repregunta 1 O1 vale 1
        O3 = np.append(O3, int(np.sum(N[u,7]) == 3)) #En la repregunta 3 O3 vale 1
        O2 = np.append(O2, int(np.sum(N[u,7]) == 2)) #En la repregunta 2 O2 vale 1
        
        Gm = np.append(Gm, int(N[U[P29[0]],6] == 1)) #Si es Mujer Gm vale 1
            
        Pol = np.append(Pol, Us[np.where(Us[:,0] == N[i,2])[0].astype(int), 3])
        
        dist = np.append(dist, i - j)
        
#        Timer = np.append(Timer, N[i,14])
        
        if N[i,1] == 'Chile':
            SocEc = np.append(SocEc, int(N[U[P50[0]],6] < 3))
            
            Paisa = np.append(Paisa,1)
            Paisb = np.append(Paisb,0)
            
            OfOp = np.append(OfOp, N[U[P13[0]],6] - 1)
            
            Ed = np.append(Ed, int(N[U[P31[0]],6] <= 3))  #Para Mexico 6 es posgrado mientras que para Chile 1 es Posgrado
            
#            Prim = np.append(Prim, N[U[P7[0]],6])
            
#            if N[P7[0],6] == 1 and N[P13[0],6] < 3  and 2*N[P13[0],6] == N[P8[0],6]  and int(N[P42[0],6]/51) + 1 == N[P13[0],6]: #Votaste las dos veces al partido con el que te sentís más afín
#                Alina = np.append(Alina, 1)
#                Alinb = np.append(Alinb, 0)
#            else:
#                if (N[P7[0],6] != 1 and N[P13[0],6] < 3  and int(N[P42[0],6]/51) + 1 == N[P13[0],6]) or (N[P7[0],6] == 1 and N[P13[0],6] >= 3 and 2*(int(N[P42[0],6]/51) + 1) == N[P8[0],6]) or (N[P7[0],6] == 1 and N[P13[0],6] < 3  and ((N[P13[0],6] == int(N[P42[0],6]/51) + 1 and N[P8[0],6] != 2*int(N[P42[0],6]/51) + 1) or (N[P13[0],6] != int(N[P42[0],6]/51) + 1 and N[P8[0],6] == 2*(int(N[P42[0],6]/51) + 1)) or (2*N[P13[0],6] == N[P8[0],6] and N[P8[0],6] != 2*(int(N[P42[0],6]/51) + 1)))):
#                    #Votaste 1 vez al partido con el que te sentís más afín o votaste las dos veces al partido con el que te sentís menos afín
#                    Alina = np.append(Alina, 0)
#                    Alinb = np.append(Alinb, 1)
#                else:
#                    #Una vez no votaste y la otra votaste al partido en el que te sentís menos afín
#                    Alina = np.append(Alina, 0)
#                    Alinb = np.append(Alinb, 0)
#            if  N[P7[0],6] == 1 and N[P13[0],6] < 3 and 2*N[P13[0],6] == N[P8[0],6]:
#                VotAnt = np.append(VotAnt, 1)
#            else:
#                VotAnt = np.append(VotAnt, 0)
            
        if N[i,1]== 'Colombia':
            SocEc = np.append(SocEc, int(N[U[P50[0]],6] > 3))
            
            Paisa = np.append(Paisa,0)
            Paisb = np.append(Paisb,1)
            
            OfOp = np.append(OfOp,1)

            Ed = np.append(Ed, int(N[U[P31[0]],6] <= 3))  #Para Mexico 6 es posgrado mientras que para Chile 1 es Posgrado
            
#            Prim = np.append(Prim, N[U[P7[0]],6])
            
#            if N[P7[0],6] == 1 and N[P13[0],6] < 3 and N[P13[0],6] == N[P8[0],6]-2 and int(N[P42[0],6]/51) + 1 == N[P13[0],6]: #Votaste las dos veces al partido con el que te sentís más afín
#                Alina = np.append(Alina, 1)
#                Alinb = np.append(Alinb, 0)            
#            else:
#                if (N[P7[0],6] != 1 and N[P13[0],6] < 3  and int(N[P42[0],6]/51) + 1 == N[P13[0],6]) or (N[P7[0],6] == 1 and N[P13[0],6] >= 3 and int(N[P42[0],6]/51) + 1 == N[P8[0],6]-2) or (N[P7[0],6] == 1 and N[P13[0],6] < 3  and ((N[P13[0],6] == int(N[P42[0],6]/51) + 1 and N[P8[0],6]-2 != int(N[P42[0],6]/51) + 1) or (N[P13[0],6] != int(N[P42[0],6]/51) + 1 and N[P8[0],6]-2 == int(N[P42[0],6]/51) + 1) or (N[P13[0],6] == N[P8[0],6]-2 + 1 and N[P8[0],6]-2 != int(N[P42[0],6]/51) + 1))):
#                    #Votaste 1 vez al partido con el que te sentís más afín o votaste las dos veces al partido con el que te sentís menos afín
#                    Alina = np.append(Alina, 0)
#                    Alinb = np.append(Alinb, 1)
#                else:
#                    #Una vez no votaste y la otra votaste al partido en el que te sentís menos afín
#                    Alina = np.append(Alina, 0)
#                    Alinb = np.append(Alinb, 0)
#            
#            if  N[P7[0],6] == 1 and N[P13[0],6] < 3 and N[P13[0],6] == N[P8[0],6]-2:
#                VotAnt = np.append(VotAnt, 1)
#            else:
#                VotAnt = np.append(VotAnt, 0)                    
#        
        if N[i,1]== 'Mexico':
            SocEc = np.append(SocEc, int(N[U[P50[0]],6] > 4))
            
            Paisa = np.append(Paisa,0)
            Paisb = np.append(Paisb,0)
            
            OfOp = np.append(OfOp, int(N[U[P13[0]],6] != 2))
            
            Ed = np.append(Ed, int(N[U[P31[0]],6] >= 6))  #Para Mexico 6 es posgrado mientras que para Chile 1 es Posgrado
            

            
        Rel = np.append(Rel, N[U[P51[0]],6])

        Edad = np.append(Edad, N[U[P30[0]],6])    

        CL = np.append(CL, int(N[U[P52[0]],6]/51)) #0 si es de izquierda, 1 si es de derecha
        CLsm = np.append(CLsm, Us[np.where(Us[:,0] == N[i,2])[0].astype(int), 2])
        Sort = np.append(Sort, int(int(N[U[P52[0]],6]/51) == int(Us[np.where(Us[:,0] == N[i,2])[0].astype(int), 2]/51)))
        
        Coinc = np.append(Coinc, int(int(N[U[P52[0]],6]/51) + 1 == int(N[j,5]))) 
        
        Intera = np.append(Intera, int(N[U[P11[0]],6] == 1))
        Interb = np.append(Interb, int(N[U[P11[0]],6] == 2))
        Interc = np.append(Interc, int(N[U[P11[0]],6] == 3))
        Interd = np.append(Interd, int(N[U[P11[0]],6] == 4))
        
        Conv = np.append(Conv, N[U[P12[0]],6])
        
        Freca = np.append(Freca, int(N[U[P44[0]],6] == 1))
        Frecb = np.append(Frecb, int(N[U[P44[0]],6] == 2))
        Frecc = np.append(Frecc, int(N[U[P44[0]],6] == 4))
        Frecd = np.append(Frecd, int(N[U[P44[0]],6] == 5))        
        
        Prob = np.append(Prob, int(N[U[P44[0]],6] < 3)) #1 si es más probable que participe, 0 si es más probable que no participe
        
        Vote = np.append(Vote, int(N[U[P48[0]],6] < 3)) #1 si votó, 0 si no
        
        qstID16 = np.append(qstID16, int(N[i,4]==16))
        qstID17 = np.append(qstID17, int(N[i,4]==17))        
        qstID18 = np.append(qstID18, int(N[i,4]==18))
        qstID19 = np.append(qstID19, int(N[i,4]==19))        
        qstID20 = np.append(qstID20, int(N[i,4]==20))
        qstID21 = np.append(qstID21, int(N[i,4]==21))
        qstID22 = np.append(qstID22, int(N[i,4]==22))
        qstID23 = np.append(qstID23, int(N[i,4]==23))
        qstID39 = np.append(qstID39, int(N[i,4]==39))
        qstID40 = np.append(qstID40, int(N[i,4]==40))
        qstID41 = np.append(qstID41, int(N[i,4]==41))
        
        usrID = np.append(usrID, N[i,2])
        
        
        
        
        #Falta agregar Perfil
        
        
S = (np.sign(ALf-ALi)+1)/2 #1 se te polarizaste 0 si no

#,[y for y in Alina],[y for y in Alinb],[y for y in VotAnt],[y for y in Prim]
#'Alina','Alinb','VotAnt','Prim',
data = np.array([[y for y in varA],[y for y in M],[y for y in usrID],[y for y in varC],[y for y in ALi],[y for y in F],[y for y in O1],[y for y in O3],[y for y in O2],[y for y in Coinc],[y for y in Gm],[y for y in Pol],[y for y in Rel],[y for y in Ed],[y for y in CL],[y for y in CLsm],[y for y in S],[y for y in SocEc],[y for y in OfOp],[y for y in CamLad],[y for y in Edad],[y for y in Paisa],[y for y in Paisb],[y for y in Intera],[y for y in Interb],[y for y in Interc],[y for y in Interd],[y for y in Conv],[y for y in Freca],[y for y in Frecb],[y for y in Frecc],[y for y in Frecd],[y for y in Prob],[y for y in Vote],[y for y in Sort],[y for y in Ci],[y for y in dist],[y for y in qstID16],[y for y in qstID17],[y for y in qstID18],[y for y in qstID19],[y for y in qstID20],[y for y in qstID21],[y for y in qstID22],[y for y in qstID23],[y for y in qstID39],[y for y in qstID40],[y for y in qstID41]])

df = pd.DataFrame(data = data.T, columns = ['varA','M','usrID','varC','ALi','F','O1','O2','O3','Coinc','Gm','Pol','Rel','Ed','CL','CLsm','S','SocEc','OfOp','CamLad','Edad','Paisa','Paisb','Intera','Interb','Interc','Interd','Conv','Freca','Frecb','Frecc','Frecd','Prob','Vote','Sort','Ci','dist','qstID16','qstID17','qstID18','qstID19','qstID20','qstID21','qstID22','qstID23','qstID39','qstID40','qstID41'])

#estos no dieron significativos:  + SocEc + Gm + F + Paisa + Paisb + F + Pol:M + SocEc + Sort + Vote + OfOp + Coinc + CLsm:Coinc + CLsm + Prob + O1:F +  O3:F + O3 + CL + O1 + Interd + Interb + Interc + Conv:Intera + Intera + Conv + Conv:Interd + SocEc + Pol:M + Ed + SocEc:M + Conv:Interc + Rel + Frecc + Frecd + dist + Gm + O2 + O2:F + Ci + Ci:M + Pol + S + Edad + M + varA + varA:M + ALi+ ALi:M + SocEc + Gm + F + CLsm
#Analisis de mediacion:   + varA + varA:M + ALi+ ALi:M
#Variables que van si o si aunque no sean significativas: + varA + M + varA:M + Ci + Ci:M + SocEc + Gm + F + CLsm + O3 + O3:F
est = sm.MixedLM.from_formula("varC ~ qstID16 + qstID17 + qstID18 + qstID19 + qstID20 + qstID21 + qstID22 + qstID23 + qstID39 + qstID40 + qstID41 + Pol + Edad + M + varA + varA:M + ALi + ALi:M + SocEc + Gm + F + Pol:M + O3 + O3:F + dist", df, groups = df["usrID"]).fit()
est.summary()

#%%
#Este modulo es para hacer varias regresiones distintas una atrás de la otra
formula = ["varC ~ qstID16 + qstID17 + qstID18 + qstID19 + qstID20 + qstID21 + qstID22 + qstID23 + qstID39 + qstID40 + qstID41 + Pol +  Edad + M + varA + varA:M + ALi+ ALi:M", "varC ~ qstID16 + qstID17 + qstID18 + qstID19 + qstID20 + qstID21 + qstID22 + qstID23 + qstID39 + qstID40 + qstID41 + Pol + Edad + M + varA + varA:M + ALi+ ALi:M + SocEc + Gm + F","varC ~ qstID16 + qstID17 + qstID18 + qstID19 + qstID20 + qstID21 + qstID22 + qstID23 + qstID39 + qstID40 + qstID41 + Pol + Edad + M + varA + varA:M + ALi+ ALi:M + SocEc + Gm + F + O3 + O3:F"]    
textopre = ['Variables significativas', 'Agrego variables teóricamente importantes', 'Agrego interaccion pregunta tres con fork']
for i in range(len(formula)):
    est = sm.MixedLM.from_formula(formula[i], df, groups = df["usrID"]).fit()
    print(textopre[i])
    print(est.summary())
    
#%%
#Histogramas de las variables importantes
Vars = [Pol, Ci, Edad, varA, ALi, dist, varC]
NVars = ['Pol', 'Ci', 'Edad', 'varA', 'ALi', 'dist','varC']
Dtr = [[[],[]]]*len(Vars)
for i in range(len(Vars)):
    OrdV = sorted(Vars[i])
    Dtr[i] = [[],[]]
    while sum(Dtr[i][1]) < len(OrdV): #Esto tarda mucho
        Dtr[i][0].append(OrdV[sum(Dtr[i][1])])
        Dtr[i][1].append(OrdV.count(OrdV[sum(Dtr[i][1])]))
    
    plt.figure()
    plt.title(NVars[i])
    plt.bar(Dtr[i][0],Dtr[i][1])
    plt.savefig(NVars[i])
    
    j=0
    
    while sum(Dtr[i][1][:j])/sum(Dtr[i][1]) < 0.1:
        j = j + 1
    
    print('The ' + str(100 - sum(Dtr[i][1][:(j-1)])*100/sum(Dtr[i][1])) + '% of the sample, is over ' + str(Dtr[i][0][j]))

    z=len(Dtr[i][1])-2
    
    while sum(Dtr[i][1][(len(Dtr[i][1])-1):z:-1])/sum(Dtr[i][1]) < 0.1:
        z = z -1 
    
    print('The ' + str(100 - sum(Dtr[i][1][(len(Dtr[i][1])-1):(z+1):-1])*100/sum(Dtr[i][1])) + '% of the sample, is under ' + str(Dtr[i][0][z]))

        
#%%
#Grafico las variables importantes para ver cuales hay que linealizar (graficadas en grupos de 0 a 100)

de0a100 = [0, 11 , 21 ,31,41,51,61,71,81,91]

viv = [varA, ALi , Pol, Rel, CLsm, Conv, Ci, Edad] #Acá van las variables que quiero linealizar
nomVar = ['varA', 'ALi' , 'Pol', 'Rel', 'CLsm', 'Conv', 'Ci','Edad'] #Acá va el nombre de la variable

for j in range(len(viv)): #Grafico todas las variables que van de 0 a 100

    VCfin = np.zeros(10)
    k = np.zeros(10)

    for i in range(len(varC)):
        VCfin[int(viv[j][i]/11)] = VCfin[int(viv[j][i]/11)] + varC[i]
        k[int(viv[j][i]/11)] = k[int(viv[j][i]/11)] + 1       
        
    VCfin = VCfin/k
    
    plt.figure(j)
    plt.xlabel(nomVar[j])
    plt.ylabel('Variation of Confidence')
    plt.title(nomVar[j])
    plt.scatter(de0a100, VCfin, zorder = 2)
    m,b,r,p,stderr = stats.stats.linregress(viv[j],varC)
    x = np.linspace(0,100,1000)
    plt.plot(x, m*x+b, zorder = 3)
    plt.text(x=0,y=0,s = '$r^2$ = ' + str(r**2), zorder = 4)  
    plt.scatter(viv[j],varC, zorder = 1)
    plt.savefig(nomVar[j] ,dpi=200)
    
VCfin = np.zeros(11)
k = np.zeros(11)


for j in range(len(dist)):
    VCfin[int(dist[j])-1] = VCfin[int(dist[j])-1] + varC[j]
    k[int(dist[j])-1] = k[int(dist[j])-1] + 1

VCfin = VCfin/k       

plt.figure(11)
plt.xlabel('Distancia')
plt.ylabel('Variation of Confidence')
plt.title('Distancia')
plt.scatter([1,2,3,4,5,6,7,8,9,10,11], VCfin,zorder = 2)
m,b,r,p,stderr = stats.stats.linregress(dist,varC)
x = np.linspace(1,12,100)
plt.plot(x, m*x+b, zorder =3)
plt.text(x=0,y=0,s = '$r^2$ = ' + str(r**2), zorder = 4)  
plt.scatter(dist,varC,zorder = 1) 
plt.savefig('dist' ,dpi=200)

#%%
#Esto es para graficar Ci vs Cf, lo hice por un pedido puntual especial
Cfin = np.zeros(10)
k = np.zeros(10)

for i in range(len(Ci)):
    Cfin[int(Ci[i]/11)] = Cfin[int(Ci[i]/11)] + Cf[i]
    k[int(Ci[i]/11)] = k[int(Ci[i]/11)] + 1     

Cfin = Cfin/k

plt.figure()
plt.xlabel('Confianza inicial')
plt.ylabel('Confianza final')
plt.scatter(['0-10','11-20','21-30','31-40','41-50','51-60','61-70','71-80','81-90','91-100'],Cfin)
plt.savefig('Confianzas2')



    
#%%
#Cambio del agreement vs cambio en la confianza


varA = np.array([])
varC = np.array([])

A = np.where(N[:,7]==1)[0].astype(int) #Tomo los indices de las repreguntas
for i in A:
     
    I = np.where(N[:,4]==N[i,4])[0].astype(int) #indices de todas las preguntas con el mismo número
    j = I[np.where(I==i)[0].astype(int)-1] #busco el indice de la pregunta anterior a la que estoy ubicado ahora en i, esto busca la pregunta inicial a partir de la repregunta
    
    if N[i,8] != -1:
        varA = np.append(varA, abs(N[i,6]-N[i,8]))
    else:
        varA = np.append(varA,0)

    varC = np.append(varC,abs(N[i,11]-N[j,11]))
    
m, b, r, p, stdE = stats.linregress(varC,varA)
plt.plot(varC,varA,'o')
x = np.arange(0, 2.1 ,0.1)
plt.plot(x, m*x+b)

#%%
#variación de agreement vs treatment
varA = []
M = []

    
A = np.where(N[:,7] == 1)[0].astype(int) #Tomo los indices de las repreguntas

for i in A:
    
    if N[i,8] != -1:
        varA.append(abs(N[i,6]-N[i,8]))
    else:
        varA.append(0)

    if N[i,6] != N[i,9]:
        M.append(2) #Manipulada es 2, no manipulada es 1
    else:
        M.append(1)
#    else:
#        
#        if N[i,6] == N[i,9]:
#            varA.append(0)
#            M.append(1)


m, b, r, p, stdE = stats.linregress(M,varA)
plt.plot(M,varA,'o')
x = np.arange(0,2.1,0.1)
plt.plot(x, m*x+b)

varA = np.array(varA)

P = [np.mean(varA[[int(i) for i, e in enumerate(M) if e == 1]]),np.mean(varA[[int(i) for i, e in enumerate(M) if e == 2]])]


#%%
np.savetxt('Genero.txt',[[np.sum(Gm)/4],[(len(Gm)-np.sum(Gm))/4]], fmt = '%.10s', newline=', ')
np.savetxt('Edad.txt',plt.hist(Edad[np.where(Edad<100)[0].astype(int)],bins = np.arange(10,100,5))[0]/4, fmt = '%.10s', newline=', ')
np.savetxt('CL.txt',[[(len(CL)-np.sum(CL))/4],[np.sum(CL)/4]], fmt = '%.10s', newline=', ')
np.savetxt('NTotal.txt',[len(varA)/4], fmt = '%.10s')
np.savetxt('DR.txt',[np.sum(D)/np.sum(M),'+-',np.sqrt((np.sum(D)/np.sum(M)**2)*(1-np.sum(D)/np.sum(M)))], fmt = '%.18s')

#%%
#Grafico de interacciones
x = np.arange(0,101,0.1)

MECi = 0.06 * x
plt.figure(1)
plt.xlabel('Initial confidence')
plt.ylabel('Marginal effects of manipulation on initial confidence')
plt.plot(x, MECi, color = 'k',linestyle = '-')
plt.plot(x, MECi + np.sqrt(1.32 + x**2 * 1.69e-4 - 2 * x * 0.014), color = 'k', linestyle = '--')
plt.plot(x, MECi - np.sqrt(1.32 + x**2 * 1.69e-4 - 2 * x * 0.014), color = 'k', linestyle = '--')
plt.savefig('Ci')

MEvarA = -1.7 - 0.09 * x
plt.figure(2)
plt.xlabel('Change of issue preference')
plt.ylabel('Marginal effects of manipulation on change of issue preference')
plt.plot(x, MEvarA, color = 'k',linestyle = '-')
plt.plot(x,MEvarA + np.sqrt(0.16 + x**2 * 4e-4 + 2*x * 2.4e-3), color = 'k', linestyle = '--')
plt.plot(x,MEvarA - np.sqrt(0.16 + x**2 * 4e-4 + 2*x * 2.4e-3), color = 'k', linestyle = '--')
plt.savefig('varA')

#barra = np.zeros(10)
#cont = np.zeros(10)
#
#for i in range(len(varC)):
#
#    barra[int(varA[i]/10.1)] = barra[int(varA[i]/10.1)] + varC[i]
#    cont[int(varA[i]/10.1)] = cont[int(varA[i]/10.1)] + 1
#
#e = np.zeros(10)
#
#for j in range(10):
#    e[j] = np.mean((varC[np.where(varA <= 10*i)[0].astype(int)]-barra[j])**2)
#        
#barraF = barra/cont
#
# 
#
#plt.figure(3)
#plt.plot(np.arange(0,100,10), barraF/max(barraF),'o')

#%%
#estadistica descriptiva
cols = ['varA','M','usrID','varC','ALi','F','O1','O3','O2','Coinc','Gm','Pol','Rel','Ed','CL','CLsm','S','SocEc','OfOp','CamLad','Edad','Paisa','Paisb','Intera','Interb','Interc','Interd','Conv','Freca','Frecb','Frecc','Frecd','Prob','Vote','Sort','Ci','dist','qstID16','qstID17','qstID18','qstID19','qstID20','qstID21','qstID22','qstID23','qstID39','qstID40','qstID41']
desc = stats.describe(df)
np.savetxt('EstDesc.csv',[[y for y in cols],[y for y in desc.mean],[y for y in np.std(df)],[y for y in desc.minmax[0]],[y for y in desc.minmax[1]]], fmt = '%.10s', delimiter=', ')