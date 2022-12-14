'''

Author: Angelo Santos

This code will create a dataframe will flow of disabled students, we have four possibilities:
    1. Special school -> Regular school without AEE
    2. Special school -> Regular school with AEE
    3. Regular school without AEE -> Regular school with AEE 
    4. At home -> Regular school
    
'''
import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
sns.set_style('white')
sns.despine(left=False, bottom=True)
sns.set_context("paper")

def two_scales(data, columns, colors, x_axis, title, ylabels,fs = 10):
    fig, axs = plt.subplots()
    #define colors to use
    col1 = colors[0]
    col2 = colors[1]

    #define subplots
    #add first line to plot
    axs.plot(data[x_axis], data[columns[0]], color=col1)

    #add x-axis label
    axs.set_xlabel('Year', fontsize=10)

    #add y-axis label
    axs.set_ylabel(ylabels[0], color=col1, fontsize=fs)

    #define second y-axis that shares x-axis with current plot
    ax2 = axs.twinx()

    #add second line to plot
    ax2.plot(data[x_axis], data[columns[1]], color=col2)

    #add second y-axis label
    ax2.set_ylabel(ylabels[1], color=col2, fontsize=fs)
    axs.set_title(title, fontsize=fs)

def classroom(state = 'brasil'):
    
    global df
    br = []
    ########################################################################### 2007-2008
    for y in range(2007,2009):
        os.chdir("/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/"+str(y)+"/DADOS")
        # upload schools census (2009 - 2020)
        schools = pd.read_csv('ESCOLAS.csv', encoding = 'latin1',delimiter = '|')
        
        # restrict to non-private
        schools = schools.loc[schools['ID_DEPENDENCIA_ADM'] != 4]
        
        # condition to state
        if state != 'brasil' :
            schools = schools.loc[schools['SIGLA'] == state]
        else:
            pass
            
        # Brazilian Municipalites data creation
        m = {}
        fr = schools.loc[schools['ANO_CENSO'] == y]
        fr = fr.groupby(['ANO_CENSO','FK_COD_MUNICIPIO']).sum().reset_index()
        muns = len(fr['FK_COD_MUNICIPIO'].unique())
        print(muns)
        sala = fr.loc[fr['ID_SALA_ATENDIMENTO_ESPECIAL'] > 0].shape[0]
        m['year'] = y
        m['#Classroom'] = sala
        m['Classroom'] = sala/muns*100
        br.append(m)

    ####################################################################### 2009-2020
    
    # upload schools census (2009 - 2020)
    os.chdir(r'/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/basededados_censo')
    schools = pd.read_csv('escola.csv')
    
    # restrict to non-private schools 
    schools = schools.loc[schools['rede'] != 'privada']
    
    
    if state != 'brasil':
        schools = schools.loc[schools['sigla_uf'] == state]
    else:
        pass
    
    for y in range(2009,2021):
        m = {}
        fr = schools.loc[schools['ano'] == y]
        fr = fr.groupby(['ano','id_municipio']).sum().reset_index()
        muns = len(fr['id_municipio'].unique())
        print(muns)
        sala = fr.loc[fr['sala_atendimento_especial'] > 0].shape[0]
        m['year'] = y
        m['#Classroom'] = sala
        m['Classroom'] = sala/muns*100
        br.append(m)
    
        # Plot
    df = pd.DataFrame(br).round(1)

'''

First we need to create a panel with all the disabled students with the following information:
    - id
    - age 
    - school id
    - classroom id
    - special school dummy
    - grade
    - AEE offer 
    
Uploading census from 2007 to 2014

'''
st1 = []
for y in range(2007,2015):    
    print(y)
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    ne = pd.read_csv('MATRICULA_NORDESTE.CSV', delimiter= '|')
    ne = ne.loc[ne['FK_COD_ESTADO_ESCOLA'] ==  23]
    #ne = ne.loc[ne['ID_POSSUI_NEC_ESPECIAL'] == 1]
    ne = ne.rename( columns = {'PK_COD_ENTIDADE' : 'id_escola',
                               'FK_COD_ALUNO' : 'cd_aluno_inep', 
                               'PK_COD_TURMA' : 'id_turma',
                               'ANO_CENSO' : 'ano',
                               'NUM_IDADE' : 'idade',
                               'FK_COD_ETAPA_ENSINO' : 'grade'})
    ne = ne[['ano','cd_aluno_inep', 'id_escola', 'id_turma','grade','idade']]
    st1.append(ne)
s1 = pd.concat(st1, axis = 0)

st2 = []
for y in range(2015,2018):    
    print(y)
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    ne = pd.read_csv('MATRICULA_NORDESTE.CSV', delimiter= '|')
    ne = ne.loc[ne['CO_UF'] ==  23]
    #ne = ne.loc[ne['IN_NECESSIDADE_ESPECIAL'] == 1]
    ne = ne.rename( columns = {'CO_ENTIDADE' : 'id_escola',
                               'CO_PESSOA_FISICA' : 'cd_aluno_inep', 
                               'ID_TURMA' : 'id_turma',
                               'NU_ANO_CENSO' : 'ano',
                               'NU_IDADE' : 'idade',
                               'TP_ETAPA_ENSINO' : 'grade'})
    ne = ne[['ano','cd_aluno_inep', 'id_escola', 'id_turma','grade','idade']]
    st2.append(ne)
s2 = pd.concat(st2, axis = 0)

ceara = pd.concat([s1,s2], axis = 0).reset_index().drop('index', axis =1)
ceara = ceara.groupby(['ano','cd_aluno_inep']).first().reset_index()
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/individual')
ceara.to_pickle('d_individual_v1.pkl')