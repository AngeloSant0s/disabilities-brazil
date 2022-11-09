'''
Author: Angelo Santos

This code aims to identify all the special education institutions in the census. We have different 
columns for the same variable depending on the census year. Follows the names:
    - 2007 to 2014: ID_MOD_ENS_ESP (dummy)
    - 2015 to 2017: IN_ESPECIAL_EXCLUSIVA (dummy)

There is information if the school has infrastructure in acessibility:
    - 2007 to 2014: ID_DEPENDENCIAS_PNE (dummy)
    - 2015 to 2017: IN_DEPENDENCIAS_PNE (dummy)
    
I also created a dataset to plot evolution of educational institutions types, named d_special_schools_growth.pkl

'''
import os
import pandas as pd 
'''

I will add more years to the institution type plot. I will use information from 2000 - 2006

'''
sc_growth = []
for y in range(2000,2007):
    dic = {}
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    schools = pd.read_csv('CENSOESC_'+str(y)+'.csv', encoding = 'latin1',delimiter = '|')
    schools.loc[schools['DEP'] != 'Particular']
    dic['year'] = y
    dic['special'] = schools.ESP_EXCL.value_counts(dropna=False)['s']
    dic['regular'] = schools.ESP_EXCL.value_counts(dropna=False)['n']
    sc_growth.append(dic)
'''

Loading data from 2007 to 2014

'''
c1 = []
for y in range(2007,2015):
    dic = {}
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    # upload schools census 
    schools = pd.read_csv('ESCOLAS.csv', encoding = 'latin1',delimiter = '|')
    # restrict to non-private
    schools = schools.loc[schools['ID_DEPENDENCIA_ADM'] != 4]
    # store number of regular and special schools
    dic['year'] = y
    dic['special'] = schools.ID_MOD_ENS_ESP.value_counts(dropna=False)[1]
    dic['regular'] = schools.ID_MOD_ENS_ESP.value_counts(dropna=False)[0]
    dic['nan'] = schools.ID_MOD_ENS_ESP.value_counts(dropna=False).tolist()[1]
    sc_growth.append(dic)
    schools = schools[['ANO_CENSO','FK_COD_MUNICIPIO','PK_COD_ENTIDADE' ,'ID_MOD_ENS_ESP','ID_DEPENDENCIAS_PNE']]
    c1.append(schools)

'''

Rename and concat the datasets for schools

'''
c1 = pd.concat(c1, axis = 0)
c1 = c1.rename(columns = {'ANO_CENSO' : 'ano',
                                  'FK_COD_MUNICIPIO' : 'id_municipio',
                                  'PK_COD_ENTIDADE' : 'id_escola',
                                  'ID_MOD_ENS_ESP' : 'edu_especial',
                                  'ID_DEPENDENCIAS_PNE' : 'acessibilidade_pne'})
'''

Loading data from 2015 to 2017

'''
c2 = []
for y in range(2015,2018):
    dic = {}
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    schools = pd.read_csv('ESCOLAS.csv', encoding = 'latin1',delimiter = '|')
    schools = schools.loc[schools['TP_DEPENDENCIA'] != 4]
    dic['year'] = y
    dic['special'] = schools.IN_ESPECIAL_EXCLUSIVA.value_counts(dropna=False)[1]
    dic['regular'] = schools.IN_ESPECIAL_EXCLUSIVA.value_counts(dropna=False)[0]
    dic['nan'] = schools.IN_ESPECIAL_EXCLUSIVA.value_counts(dropna=False).tolist()[1]
    sc_growth.append(dic)
    schools = schools[['NU_ANO_CENSO','CO_MUNICIPIO','CO_ENTIDADE' ,'IN_ESPECIAL_EXCLUSIVA','IN_DEPENDENCIAS_PNE']]
    c2.append(schools)

c2 = pd.concat(c2, axis = 0)
c2 = c2.rename(columns = {'NU_ANO_CENSO' : 'ano',
                                  'CO_MUNICIPIO' : 'id_municipio',
                                  'CO_ENTIDADE' : 'id_escola',
                                  'IN_ESPECIAL_EXCLUSIVA' : 'edu_especial',
                                  'IN_DEPENDENCIAS_PNE' : 'acessibilidade_pne'})
'''

Concat both samples (07-14 and 15-17)

'''
schools = pd.concat([c1,c2], axis = 0).reset_index().drop('index',axis=1)
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/schools')
schools.to_pickle('d_special_schools.pkl')
'''

Dataset to plot institutions growth between (07-17)

'''
sc_growth = pd.DataFrame(sc_growth).reset_index()
sc_growth.to_pickle('d_special_schools_growth.pkl')