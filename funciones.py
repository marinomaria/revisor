#%%
import numpy as np

def buscar_statement(df, repregunta):
    return np.where((df['qst_id'] == df.loc[repregunta]['qst_id']) & (df['user_id'] == df.loc[repregunta]['user_id']) & (df['es_repr'] == 0))

def crear_variacion_de_confianza(df, index_repregunta, index_statement):
    return abs(df.loc[index_repregunta]['confianza'] - df.loc[index_statement]['confianza'])
    
def crear_variacion_de_agreement(df, index_repregunta):
    if df.loc[index_repregunta]['answer_repr'] != -1:
        return df.loc[index_repregunta]['answer_repr'] - df.loc[index_repregunta]['answer']
    else:
        if df.loc[index_repregunta]['answer'] != df.loc[index_repregunta]['valor_presentado']:
            return df.loc[index_repregunta]['valor_presentado'] - df.loc[index_repregunta]['answer']
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
    else: return None   
    
def crear_fork(df):
    user_fork_Mx = df['fork'][0:25419:41]
    user_fork_Cl = df['fork'][25420:118200:39]
    user_fork_Co = df['fork'][118201::41]
    return np.concatenate((user_fork_Mx, user_fork_Cl, user_fork_Co))

def crear_pais(df):
    users_Mx = df['pais'][0:25419:41]
    users_Cl = df['pais'][25420:118200:39]
    users_Co = df['pais'][118201::41]
    return np.concatenate((users_Mx, users_Cl, users_Co))

def orden():
    return np.array([1, 2, 3, 4] * 4480)

def cons_lib(df, pais):
        index_preguntas = np.array(np.where((df['qst_id'] == 52) & (df['pais'] == pais))[0])
        respuestas = []
        for i in index_preguntas:
            respuestas += [df.loc[i,'answer']]
            
        LC = 100 - np.array(respuestas) # A partir de aca liberal es 0 y conservador 100:
        normalizade = []
        mean = np.mean(LC)
        for x in LC:
            if x < mean:
                normalizade += [x * (50/mean)]
            else:
                normalizade += [x * (50/(100-mean)) + 100 * (50-mean)/(100-mean)]
        
        return normalizade