import numpy as np

def buscar_statement(df, repregunta):
    return np.where((df['qst_id'] == df.loc[repregunta]['qst_id']) & (df['user_id'] == df.loc[repregunta]['user_id']) & (df['es_repr'] == 0))

def crear_variacion_de_confianza(df, index_repregunta, index_statement):
    return abs(df.loc[index_repregunta]['confianza'] - df.loc[index_statement]['confianza'])
    
def crear_variacion_de_agreement(df, index_repregunta):
    if df.loc[index_repregunta]['answer_repr'] != -1:
        return df.loc[index_repregunta]['answer'] - df.loc[index_repregunta]['answer_repr']
    else: return 0
    
def crear_variable_manipulada(df, index_repregunta):
    if df.loc[index_repregunta]['answer'] != df.loc[index_repregunta]['valor_presentado']:
        return True
    else: return False
    
def crear_distancia(repregunta, statement):
    return repregunta - statement

def crear_deteccion(df, index_repregunta):
    if df.loc[index_repregunta]['answer_repr'] != -1:
        return True
    else: return False
    
def crear_genero(df):
    return np.array(df.loc[np.where(df['qst_id'] == 29)]['answer'])

def crear_edad(df):
    return np.array(df.loc[np.where(df['qst_id'] == 30)]['answer'])

def crear_religiosidad(df):
    return np.array(df.loc[np.where(df['qst_id'] == 51)]['answer'])

def crear_confianza_inicial(df, index_statement):
    return df.loc[index_statement]['confianza']

def crear_agreement_inicial(df, index_repregunta):
    return df.loc[index_repregunta]['answer'] 

#colapsar educacion toma el df_N y un array vacía y devuelve una lista con 0s y 1s donde 1 es high y 0 es low
def colapsar_educacion(df, storage_variable): 
    ed_answers_index = np.where(df['qst_id'] == 31)[0]
    for i in ed_answers_index:
      if df.loc[i]['pais'] == 'Mexico':
          if df.loc[i]['answer'] <= 4:
            storage_variable = np.append(storage_variable, 0)
          else: 
              if df.loc[i]['answer'] == 5:
                  storage_variable = np.append(storage_variable, 1)
              else: 
                  storage_variable = np.append(storage_variable, 2)
      else:
          if df.loc[i]['answer'] == 1:
             storage_variable = np.append(storage_variable, 2)
          else: 
              if df.loc[i]['answer'] == 2:
                  storage_variable = np.append(storage_variable, 1)
              else:
                  storage_variable = np.append(storage_variable, 0)
    
    return storage_variable
          
          
def crear_timer(df, index_repregunta):
    if df.loc[index_repregunta]['timer'] != 0:
        return df.loc[index_repregunta]['timer']
    else: return 0   
