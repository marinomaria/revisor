import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% LIMPIEZA DE MATRIZ

ww1 = pd.read_excel("ww1.xlsx", index_col=0, delimiter = ',')
ww2 = pd.read_excel("ww2.xlsx", index_col=0, delimiter = ',')

#cambiamos los nombres de los fork por 1 y 2 para ww1 y 3 y 4 para ww2
ww1['fork'].replace({9:1, 10:2}, inplace = True)
ww2['fork'].replace({9:3, 10:4}, inplace = True)

#le sumamos 100000 a los userId de ww1 y 200000 a los de ww2
ww1.user_id = ww1.user_id + 100000
ww2.user_id = ww2.user_id + 200000

#unimos ww1 y ww2
frames = [ww1, ww2]
sw = pd.concat(frames)

#espejamos las preguntas A1 y A3 para que correspondan a 0 derecha, 100 izquierda (si funciona mal hacerlo en dos pasos)
sw.ValorRespondido[(sw.questionId == 19) | (sw.questionId == 23)] = - sw.ValorRespondido[(sw.questionId == 19) | (sw.questionId == 23)] + 100

#filtramos la matriz usando las columnas Pais, OmitirDatos y EsUsuarioDePrueba, luego tiramos las columnas que no nos sirven
sw = sw[sw.Pais == 'Sweden']
sw = sw[sw['OmitirDatos?'] == 0]
sw = sw[sw.EsUsuarioDePrueba == 0]
sw.drop(['TipoDePregunta', 'OmitirDatos?', 'EsUsuarioDePrueba', 'comentarios', 'Pais', 'timer', 'creado_el'], axis=1, inplace = True)

#arreglamos los usuarios con preguntas repetidas (32 en lugar de 24)
for i in sw.user_id.unique():
    #eliminamos las preguntas duplicadas dejando solo la primera, cuando se eliminan quedan como Na
    sw[(sw.user_id == i) & (sw.Es_Repregunta == 0)] = sw[(sw.user_id == i) & (sw.Es_Repregunta == 0)].drop_duplicates('questionId')
    #idem para las repreguntas
    sw[(sw.user_id == i) & (sw.Es_Repregunta == 1)] = sw[(sw.user_id == i) & (sw.Es_Repregunta == 1)].drop_duplicates('questionId')
    #eliminamos las filas que habían quedado como Na
    sw = sw[~sw.user_id.isna()]
    #eliminamos los usuarios con una cantidad de preguntas distinta de 24
    if sw[sw.user_id == i].shape != (24,8):
        sw = sw[sw.user_id != i]

#%% PIVOTEO

#cambiamos los valores respondidos para las repreguntas, si cambio la respuesta se cambia por ValorRepregunta, si no la cambio se cambia por ValorPresentadoPregunta 
sw.ValorRespondido[(sw.ValorRepregunta == -1) & (sw.Es_Repregunta == 1)] = sw.ValorPresentadoPregunta[(sw.ValorRepregunta == -1) & (sw.Es_Repregunta == 1)]
sw.ValorRespondido[(sw.ValorRepregunta != -1) & (sw.Es_Repregunta == 1)] = sw.ValorRepregunta[(sw.ValorRepregunta != -1) & (sw.Es_Repregunta == 1)]

#creamos las tres columnas para etiquetar las nuevas columnas de la matriz (que se usan para el pivoteo)
sw['QID'] = 0
sw['conf']= -1
sw['Presentado']= -1
sw.index = range(len(sw.index))
for i in sw.index:
    if i%300 == 0:
        print(int(i/len(sw.index)*100),'%')
    if (sw['questionId'][i]==19) & (sw['Es_Repregunta'][i]==0):
        sw['QID'][i]='A1'
        sw['conf'][i]='A1conf'
    elif (sw['questionId'][i]==19) & (sw['Es_Repregunta'][i]==1):
        sw['QID'][i]='RA1'
        sw['conf'][i]='RA1conf'
        sw['Presentado'][i]='RA1pres'
    elif (sw['questionId'][i]==20) & (sw['Es_Repregunta'][i]==0):
        sw['QID'][i]='A2'
        sw['conf'][i]='A2conf'
    elif (sw['questionId'][i]==20) & (sw['Es_Repregunta'][i]==1):
        sw['QID'][i]='RA2'
        sw['conf'][i]='RA2conf'
        sw['Presentado'][i]='RA2pres'
    elif (sw['questionId'][i]==21) & (sw['Es_Repregunta'][i]==0):
        sw['QID'][i]='B1'
        sw['conf'][i]='B1conf'
    elif (sw['questionId'][i]==21) & (sw['Es_Repregunta'][i]==1):
        sw['QID'][i]='RB1'
        sw['conf'][i]='RB1conf'
        sw['Presentado'][i]='RB1pres'
    elif (sw['questionId'][i]==22) & (sw['Es_Repregunta'][i]==0):
        sw['QID'][i]='B2'
        sw['conf'][i]='B2conf'
    elif (sw['questionId'][i]==22) & (sw['Es_Repregunta'][i]==1):
        sw['QID'][i]='RB2'
        sw['conf'][i]='RB2conf'
        sw['Presentado'][i]='RB2pres'
    elif sw['questionId'][i]==23:
        sw['QID'][i]='A3'
        sw['conf'][i]='A3conf'
    elif sw['questionId'][i]==39:
        sw['QID'][i]='A4'
        sw['conf'][i]='A4conf'
    elif sw['questionId'][i]==40:
        sw['QID'][i]='B3'
        sw['conf'][i]='B3conf'
    elif sw['questionId'][i]==41:
        sw['QID'][i]='B4'
        sw['conf'][i]='B4conf'
    elif sw['questionId'][i]==15:
        sw['QID'][i]='C1'
        sw['conf'][i]='C1conf'
    elif sw['questionId'][i]==16:
        sw['QID'][i]='C2'
        sw['conf'][i]='C2conf'
    elif sw['questionId'][i]==17:
        sw['QID'][i]='C3'
        sw['conf'][i]='C3conf'
    elif sw['questionId'][i]==18:
        sw['QID'][i]='C4'
        sw['conf'][i]='C4conf'
    elif sw['questionId'][i]==62:
        sw['QID'][i]='Genero'
    elif sw['questionId'][i]==63:
        sw['QID'][i]='Educacion'
    elif sw['questionId'][i]==64:
        sw['QID'][i]='PP_anterior'
    elif sw['questionId'][i]==65:
        sw['QID'][i]='Elec_anterior'
    elif sw['questionId'][i]==29:
        sw['QID'][i]='Voto'
    elif sw['questionId'][i]==50:
        sw['QID'][i]='Interes'
    elif sw['questionId'][i]==31:
        sw['QID'][i]='CVoto'
    elif sw['questionId'][i]==30:
        sw['QID'][i]='Qid30'

#pivoteamos por valor respondido
swValorRespondido=sw.pivot(index='user_id', columns='QID', values='ValorRespondido')

#pivoteamos para guardar el fork
swfork=sw.pivot(index='user_id', columns='QID', values='fork')

#creamos una matriz con las filas que tienen confianza y una con las que tienen valor presentado (las repreguntas)
swConfianza=sw[sw.conf != -1]
swPresentado=swConfianza[swConfianza.Presentado != -1]

#pivoteamos por confianza y por valor presentado
swConfianza=swConfianza.pivot(index='user_id', columns='conf', values='confianza')
swPresentado=swPresentado.pivot(index='user_id', columns='Presentado', values='ValorPresentadoPregunta')

#concatenamos las tres matrices pivoteadas
Sw=pd.concat([swValorRespondido,swConfianza,swPresentado], axis=1)
#creamos una columna con el fork (usando la matriz pivoteada antes)
Sw['fork']=swfork['A1']

#reordenamos las columnas segun nuestro criterio
columnsTitles = ['fork','A1', 'A1conf','B1','B1conf','A2','A2conf','B2','B2conf','RA1','RA1conf','RA1pres','RB1','RB1conf','RB1pres','RA2','RA2conf','RA2pres','RB2','RB2conf','RB2pres','A3', 'A3conf','B3','B3conf','A4','A4conf','B4','B4conf','C1','C1conf','C2','C2conf','C3','C3conf','C4','C4conf','Genero','Educacion','Voto','CVoto','Elec_anterior','Interes','PP_anterior','Qid30']
Sw = Sw.reindex(columns=columnsTitles)

#%% GUAU GUAU GUARDO EN CSV
Sw.to_csv('SWperrrrrrrrres.csv')

       