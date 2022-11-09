'''

Author: Angelo Santos

This code aims to identify all the special education institutions in the census. We have different 
columns for the same variable depending on the census year. Follows the names:
    - 2007 to 2014: FK_COD_MOD_ENSINO (dummy)
    - 2015 to 2017: IN_ESPECIAL_EXCLUSIVA (dummy)

I also created a dataset to plot evolution of educational institutions types, named d_special_classroomns_growth.pkl

'''
import os
import pandas as pd 
'''

Loading data from 2007 to 2014

'''
sc_growth = []
c1 = []
for y in range(2007,2015):
    dic = {}
    print(y)
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    # upload schools census 
    schools = pd.read_csv('TURMAS.csv', encoding = 'latin1',delimiter = '|')
    # restrict to non-private
    # schools = schools.loc[schools['ID_DEPENDENCIA_ADM'] != 4]
    # store number of regular and special schools
    # schools = schools
    dic['year'] = y
    dic['special'] = schools.FK_COD_MOD_ENSINO.value_counts(dropna=False)[2]
    dic['regular'] = schools.FK_COD_MOD_ENSINO.value_counts(dropna=False)[1]
    dic['nan'] = schools.FK_COD_MOD_ENSINO.isna().sum()
    sc_growth.append(dic)
    schools = schools[['ANO_CENSO','PK_COD_TURMA','FK_COD_MOD_ENSINO','PK_COD_ENTIDADE']]
    c1.append(schools)

c1 = pd.concat(c1, axis = 0)
c1 = c1.rename(columns = {'ANO_CENSO' : 'ano',
                          'PK_COD_TURMA' : 'id_turma',
                          'PK_COD_ENTIDADE' : 'id_escola',
                          'FK_COD_MOD_ENSINO' : 'classroom_especial'})

'''

Loading data from 2015 to 2017

'''
c2 = []
for y in range(2015,2018):
    dic = {}
    print(y)
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    # upload schools census 
    schools = pd.read_csv('TURMAS.csv', encoding = 'latin1',delimiter = '|')
    # restrict to non-private
    # schools = schools.loc[schools['ID_DEPENDENCIA_ADM'] != 4]
    # store number of regular and special schools
    # schools = schools
    dic['year'] = y
    dic['special'] = schools.IN_ESPECIAL_EXCLUSIVA.value_counts(dropna=False)[1]
    dic['regular'] = schools.IN_REGULAR.value_counts(dropna=False)[1]
    dic['nan'] = schools.IN_REGULAR.isna().sum()
    sc_growth.append(dic)
    schools = schools[['NU_ANO_CENSO','ID_TURMA', 'IN_ESPECIAL_EXCLUSIVA','CO_ENTIDADE']]
    c2.append(schools)

c2 = pd.concat(c2, axis = 0)
c2 = c2.rename(columns = {'NU_ANO_CENSO' : 'ano',
                          'ID_TURMA' : 'id_turma',
                          'CO_ENTIDADE' : 'id_escola',
                          'IN_ESPECIAL_EXCLUSIVA' : 'classroom_especial'})
'''

Concat the data 

'''
schools = pd.concat([c1,c2], axis = 0).reset_index().drop('index',axis=1)
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/classroomns')
schools.to_pickle('d_special_classroomns.pkl')
'''

Dataset to plot classroomns growth between (07-17)

'''
sc_growth = pd.DataFrame(sc_growth).reset_index()
sc_growth.to_pickle('d_special_classroomns_growth.pkl')

