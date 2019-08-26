import numpy as np
import pandas as pd

ww1 = pd.read_csv("export (ww1).csv", index_col=0)
ww2 = pd.read_csv("export (ww2).csv", index_col=0)

#cambiamos los nombres de los fork por 1 y 2 para ww1 y 3 y 4 para ww2
ww1['fork'].replace({9:1, 10:2}, inplace = True)
ww2['fork'].replace({9:3, 10:4}, inplace = True)

#le sumamos 100000 a los userId de ww1 y 200000 a los de ww2
ww1.user_id = ww1.user_id + 100000
ww2.user_id = ww2.user_id + 200000

#unimos ww1 y ww2
frames = [ww1, ww2]
sw = pd.concat(frames)

#espejamos las preguntas A1 y A3 para que correspondan a 0 derecha, 100 izquierda
sw.ValorRespondido[(sw.questionId == 19) | (sw.questionId == 23)] = - sw.ValorRespondido[(sw.questionId == 19) | (sw.questionId == 23)] + 100

#filramos la matriz usando las columnas Pais, OmitirDatos y EsUsuarioDePrueba, luego tiramos las columnas que no nos sirven
sw = sw[sw.Pais == 'Sweden']
sw = sw[sw['OmitirDatos?'] == 0]
sw = sw[sw.EsUsuarioDePrueba == 0]
sw.drop(['TipoDePregunta', 'OmitirDatos?', 'EsUsuarioDePrueba', 'comentarios', 'Pais', 'timer', 'creado_el'], axis=1, inplace = True)
