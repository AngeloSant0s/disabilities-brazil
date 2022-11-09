'''
Author: Angelo Santos

This code aims to identify all the special education students enrollment in the census. We have different 
columns for the same variable depending on the census year. I create a dataset:

    - d_enrollment_ne.pkl: With disabled students matched with schools
    
'''
import os
import pandas as pd
'''

Uploading census from 2007 to 2014

'''
nes = []
for y in range(2007,2015):    
    print(y)
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    ne = pd.read_csv('MATRICULA_NORDESTE.CSV', delimiter= '|')
    ne = ne.loc[ne['FK_COD_ESTADO_ESCOLA'] ==  23]
    ne = ne.loc[ne['ID_POSSUI_NEC_ESPECIAL'] == 1]
    ne = ne.rename( columns = {'PK_COD_ENTIDADE' : 'id_escola',
                               'FK_COD_ALUNO' : 'cd_aluno_inep', 
                               'ANO_CENSO' : 'ano'})
    ne = ne[['ano','id_escola','cd_aluno_inep']]
    nes.append(ne)
'''

Uploading census from 2015 to 2017

'''
for y in range(2015,2018):    
    print(y)
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    ne = pd.read_csv('MATRICULA_NORDESTE.CSV', delimiter= '|')
    ne = ne.loc[ne['CO_UF'] ==  23]
    ne = ne.loc[ne['IN_NECESSIDADE_ESPECIAL'] == 1]
    ne = ne.rename( columns = {'CO_ENTIDADE' : 'id_escola',
                               'CO_PESSOA_FISICA' : 'cd_aluno_inep', 
                               'NU_ANO_CENSO' : 'ano'})
    ne = ne[['ano','id_escola','cd_aluno_inep']]
    nes.append(ne)

ceara = pd.concat(nes, axis = 0)
'''

Uploading educational intitutions type data

'''
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/schools')
schools_type = pd.read_pickle('d_special_schools_pub_priv.pkl')
'''

Merge datasets

'''
ceara = ceara.merge(schools_type, on= ['ano','id_escola'])
enrollment = []
for y in range(2007,2018):
    ceara_y = ceara.loc[ceara['ano'] == y]
    dic = {}
    dic['year'] = y
    dic['special'] = ceara_y.edu_especial.value_counts()[1]
    dic['regular'] = ceara_y.edu_especial.value_counts()[0]
    dic['nan'] = ceara_y.edu_especial.isna().sum()
    enrollment.append(dic)

enrollment = pd.DataFrame(enrollment)
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/enrollment')
enrollment.to_pickle('d_enrollment_ce.pkl')
