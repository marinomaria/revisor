# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 12:40:05 2018

@author: Milton
"""
#Todos
#%%
import pandas as pd
import numpy as np
import datetime as dt

#Colocar el pais acá. Opciones 'mx', 'co', 'cl'
pais = ['cl','co','mx']

for Pais in pais:

    k = 0
    
    idP = np.array([])  #Vector donde indica el idPregunta que ya respondió el usuario
    reps = np.array([]) #Vector donde indica las repreguntas que ya respondió el usuario
    
    Us = [] #vector de usuarios útiles        
        
    
    if Pais == 'mx' or Pais == 'co':
        #Cargo los excels en una nueva matriz
        for i in range(1): #Dentro de Range hay que poner el número de matrices que tengo, 17 para chile, 1 para Colombia, 1 para Mexico
            df = pd.read_excel(io=Pais + 'Datos'+ str(i) +'.xlsx')#Cargo los excels en una estructura de pandas, xlsx para Mx y Co. xls para Cl
            if i==0: #esta condición es para evitar problemas con el concatenate
                M = df.values #df.values es el array de numpy contenido en la estructura pandas. Este array tiene todo el excel menos los titulos 
            else:
                M = np.concatenate((M,df.values),axis=0)
            print(i)
    
            M = M.tolist()
            
            M = [y for y in filter(lambda x: type(x[2]) == int,M)]
            M = [y for y in filter(lambda x: type(x[0]) == int,M)]
            M = [y for y in filter(lambda x: type(x[1]) == str,M)]

    
        if Pais == 'co':
            
            M = np.array([y for y in filter(lambda x: type(x[15]) == dt.datetime,M)])
            
            M = M[M[:,2].argsort(kind='mergesort')]
            fc = np.shape(M)
            M = M.tolist()
            
            FechaI = dt.datetime(2018,6,13,0,0,0) #fecha de inicio y finalizacion del experimento (para colombia del 13/6 al 17/6)
            FechaF = dt.datetime(2018,6,17,8,0,0)
            
            cant = 41
            DonVot = [1,34] #lugares de donde está la pregunta de donde votas y el valor de la respuesta de No Voto en el País
            
            for i in range(fc[0]):
            
                if i-k != 0: #Para que no haya problemas con el primero
                    
                    if M[i-k][2] != M[i-k-1][2]: 
                        idP = np.array([])
                        reps = np.array([]) 
                
                if M[i-k][12] == 1 or M[i-k][13] == 1 or FechaF < M[i-k][15] or FechaI > M[i-k][15] or M[i-k][1] != 'Colombia': #Comentar la parte del pais para los que no tenemos ip
                    del M[i-k]
                    k = k +1
                
                else:
                    if M[i-k][4] not in idP:   #Si todavía no respondiste la pregunta
                        idP = np.append(idP,M[i-k][4]) #Lo agrego al vector
                        
                        if i-k == 0:
                            Us.append(M[i-k][2])
                        else:
                            if M[i-k][2] != M[i-k-1][2]: 
                                Us.append(M[i-k][2])
                            
                        
                    else:
                        if M[i-k][7]==1:   #Si la que respondió está catalogada como repregunta
                            
                            if M[i-k][4] not in reps and len(reps) <= 4: #Si todavía no respondió esa repregunta
                                reps = np.append(reps, M[i-k][4])
                                if i-k == 0:
                                    Us.append(M[i-k][2])   
                                else:
                                     if M[i-k][2] != M[i-k-1][2]:
                                         Us.append(M[i-k][2])
                            else:
                                del M[i-k]
                                k = k+1
                                
                        else:
                            del M[i-k]
                            k = k+1
                
    
            cons  = [17,18,20,22,23,41]
            lib = [15,16,19,21,39,40]
    
        else:
            M = np.array([y for y in filter(lambda x: type(x[15]) == pd._libs.tslib.Timestamp,M)])
            
            M = M[M[:,2].argsort(kind='mergesort')]
            fc = np.shape(M)
            M = M.tolist()
            
            FechaI = dt.datetime(2018,6,27,0,0,0) #fecha de inicio y finalizacion del experimento (para colombia del 13/6 al 17/6)
            FechaF = dt.datetime(2018,7,1,15,0,0)
            
            cant = 41
            DonVot = [1,34] #lugares de donde está la pregunta de donde votas y el valor de la respuesta de No Voto en el País
        
            for i in range(fc[0]):
            
                if i-k != 0: #Para que no haya problemas con el primero
                    
                    if M[i-k][2] != M[i-k-1][2]: 
                        idP = np.array([])
                        reps = np.array([]) 
                
                if M[i-k][12] == 1 or M[i-k][13] == 1 or FechaF < M[i-k][15] or FechaI > M[i-k][15] or M[i-k][1] != 'Mexico': #Comentar la parte del pais para los que no tenemos ip
                    del M[i-k]
                    k = k +1
                
                else:
                    if M[i-k][4] not in idP:   #Si todavía no respondiste la pregunta
                        idP = np.append(idP,M[i-k][4]) #Lo agrego al vector
                        
                        if i-k == 0:
                            Us.append(M[i-k][2])
                        else:
                            if M[i-k][2] != M[i-k-1][2]: 
                                Us.append(M[i-k][2])
                            
                        
                    else:
                        if M[i-k][7]==1:   #Si la que respondió está catalogada como repregunta
                            
                            if M[i-k][4] not in reps and len(reps) <= 4: #Si todavía no respondió esa repregunta
                                reps = np.append(reps, M[i-k][4])
                                if i-k == 0:
                                    Us.append(M[i-k][2])   
                                else:
                                     if M[i-k][2] != M[i-k-1][2]:
                                         Us.append(M[i-k][2])
                                         
                            else:
                                del M[i-k]
                                k = k+1
                                
                        else:
                            del M[i-k]
                            k = k+1
                            
            cons  = [17,18,20,22,23]
            lib = [15,19,21,39,41]
            
        M = np.array(M)
    
                
    
    else:
        if Pais == 'cl':
            for i in range(17): #Dentro de Range hay que poner el número de matrices que tengo, 17 para chile, 1 para Colombia, 1 para Mexico
                df = pd.read_excel(io=Pais + 'Datos'+ str(i) +'.xls', sheet_name='Datos '+ str(i))  #Cargo los excels en una estructura de pandas, xlsx para Mx y Co. xls para Cl
                if i==0: #esta condición es para evitar problemas con el concatenate
                    M = df.values #df.values es el array de numpy contenido en la estructura pandas. Este array tiene todo el excel menos los titulos 
                else:
                    M = np.concatenate((M,df.values),axis=0)
                print(i)
            
            M = np.insert(M,1,'Chile',axis = 1)
            fc = np.shape(M)
            
            cant = 39
            DonVot = [1,16] #lugares de donde está la pregunta de donde votas y el valor de la respuesta de No Voto en el País
            
            for i in range(fc[0]):
                
                if i-k != 0: #Para que no haya problemas con el primero
                    
                    if M[i-k,2] != M[i-k-1,2]: 
                        idP = np.array([])
                        reps = np.array([])       
                
                if M[i-k,12] == 1 or M[i-k,13] == 1:# or FechaF < M[i-k][15] or FechaI > M[i-k][15] or M[i-k][1] != 'Colombia': #Comentar la parte del pais para los que no tenemos ip
                    M = np.delete(M,i-k,0)
                    k = k +1
                
                else:
                    if M[i-k,4] not in idP:   #Si todavía no respondiste la pregunta
                        idP = np.append(idP,M[i-k,4]) #Lo agrego al vector
    
                        if i-k == 0:
                            Us.append(M[i-k,2])
                        
                        else:                    
                            if M[i-k,2] != M[i-k-1,2]: 
                                Us.append(M[i-k,2])
                
                        
                    else:
                        if M[i-k,7]==1:   #Si la que respondió está catalogada como repregunta
                            
                            if M[i-k,4] not in reps and len(reps) < 4: #Si todavía no respondió esa repregunta
                                reps = np.append(reps, M[i-k,4])
                                if i-k == 0:
                                    Us.append(M[i-k,2])
                                
                                else:                    
                                    if M[i-k,2] != M[i-k-1,2]: 
                                        Us.append(M[i-k,2])
                                        
                                        
                            else:
                                M = np.delete(M,i-k,0)
                                k = k+1
                                
                        else:
                            M = np.delete(M,i-k,0)
                            k = k+1
                            
            cons  = [15,16,17,18,39,40]
            lib = [19,20,21,22,23,41]
     
    
                
    #            print ('i = '+ str(i))
    
    
        else:
            print('Falta insertar pais')
    
    #Meto 0s donde deberían haber 0s y hay nulos
    
    D = np.where(pd.isnull(M[:,6]))[0].astype(int)
    M[D,6] = 0
    
    D = np.where(pd.isnull(M[:,8]))[0].astype(int)
    M[D,8] = 0
    
    D = np.where(pd.isnull(M[:,9]))[0].astype(int)
    M[D,9] = 0
    
    D = np.where(pd.isnull(M[:,11]))[0].astype(int)
    M[D,11] = 0
    
    D = np.where(pd.isnull(M[:,7]))[0].astype(int)
    M[D,7] = 0
    
    D = np.where(pd.isnull(M[:,5]))[0].astype(int)
    M[D,5] = 0
        
    c = 0
    #Borro los usuarios que no votan en el pais
    for n in range(len(Us)):
        A = np.where(M[:,2] == Us[n-c])[0].astype(int)
        P29 = np.where(M[A,4] == 29)[0].astype(int)
        P30 = np.where(M[A,4] == 30)[0].astype(int)
        if len(A)>0:    
            if M[A[DonVot[0]],2] == DonVot[1] or np.sum(M[A,7]) != 4 or len(M[A,7]) != cant or M[A[P29[0]],6] == 3 or M[A[P30],6] > 100:
                M = np.delete(M, A, axis = 0)
                del Us[n-c]
                c = c + 1
    
        else:
            del Us[n-c]
            c = c + 1
    #    print (n)
    
    #Borro los usuarios que hicieron menos de cuatro repreguntas
    k = 0
    rep = np.array([])
    
    for i in range(len(Us)):
        U = np.where(M[:,2] == Us[i-k])[0].astype(int)
        
    
    DD = [i for i,e in enumerate(M[:,4]) if e in cons]
    DI = [i for i,e in enumerate(M[:,4]) if e in lib]
    M[DI,5] = 2
    M[DD,5] = 1
    
    if Pais == 'co':
        #Donde debo corregir el bug de colombia?
        p = 0
        for i in range(np.shape(M)[0]):
            if M[i,3] == 7 and M[i,6] == 100 and M[i,7] == 1 and M[i,9] == 0 and p==0:
                p = 1
                ind = i
    #        print(M[i,2])
    
    #Corrige el bug en colombia
        c = 0
        for i in range(len(Us)):
            if Us[i-c] < ind:
                A = np.where(M[:,2] == Us[i-c])[0].astype(int)
                if len(A) > 26:
                    if M[A[24],3] == 7 and M[A[24],6] == 100 and M[A[24],9] == 100:
                        M[A[24],9] = 0
                    
                    if M[A[26],3] == 7 and M[A[26],6] == 100 and M[A[26],9] == 100:
                        M[A[26],9] = 0
                else:
                    if len(A) == 0:
                        del Us[i-c]
                        c = c + 1
             
        
        
    #Creo la matriz Us
    N = M
    
    mUs = np.vstack((Us,np.zeros(len(Us)),np.zeros(len(Us)),np.zeros(len(Us)),np.zeros(len(Us)))).T
    
    if Pais == 'co' or Pais == 'mx':
        c = 41 #criterio de cantidad de preguntas que significa un formulario completo, 39 en chile y USA, 41 en colombia y Mexico
    else:
        c = 39
    #qué usuarios terminaron?
    
    for i in range(len(mUs[:,0])):
        
        A = np.where(N[:,2] == mUs[i,0])[0].astype(int)
        
        if len(A) == c:
            mUs[i,1] = 1        
        
        IzDe = np.zeros(2)
        M = np.zeros(2)
        AL = 0
        
        for j in A: 
            if N[j,7] != 1 and N[j,5] != 0:
                IzDe[int(N[j,5]-1)] = IzDe[int(N[j,5]-1)] + N[j,6]
                M[int(N[j,5]-1)] = M[int(N[j,5]-1)] + 1
                AL = AL + 2*abs(N[j,6]-50)
                
        P = IzDe/M
        mUs[i,2] = (P[1]-P[0]+100)/2
        
        mUs[i,3] = AL/np.sum(M)
        
    mUs[:,0] = np.array([int(y) for y in mUs[:,0]])
    
    
    
    txt = 'Guardo la matriz N completamente limpia y la matriz Us Con las columnas ID, Completo?, Orientacion politica, polarizacion'
    np.savez('MatrizLimpiaConCeros' + Pais + '.npz', txt=txt, N=N, Us=mUs)

               
    