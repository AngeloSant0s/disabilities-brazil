import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
sns.set(style="white",font_scale=5)
sns.despine(left=False, bottom=True)
sns.set_context("paper")
#######################################
def share(data, start, end, column):
    """
    Creates a dataframe with columns year and proportion of some variable

    Args:
        data (frame): data
        start (_type_): year where starts
        end (_type_): final year
        column (_type_): columns with information (must be a dummy)

    Returns:
        _type_: data frame like this:
                    | year  | share |
                    -----------------
                    | start |  45.7 |
                            ... 
                    |  end  |  68.7 |
    """
    dis_share = []
    for y in range(start,end+1):
        dic = {}
        share = data.loc[data['ano'] == y]
        print(share.loc[share[column] == 1].shape[0])
        print(share.shape[0])
        d = 100*(share.loc[share[column] == 1].shape[0]/share.shape[0])
        dic['year'] = y
        dic['share'] = d
        dis_share.append(dic)
    dis_share = pd.DataFrame(dis_share)
    return dis_share

########################################
regions = ['MATRICULA_CO',
'MATRICULA_NORTE',
'MATRICULA_NORDESTE',
'MATRICULA_SUDESTE',
'MATRICULA_SUL']

st1 = []
for y in range(2007,2015):  
    st1 = []  
    print(y)
    for r in regions:    
        print(r)
        os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
        ne = pd.read_csv(r+'.CSV', delimiter= '|')
        #ne = ne.loc[ne['FK_COD_ESTADO_ESCOLA'] !=  23]
        #ne = ne.loc[ne['ID_POSSUI_NEC_ESPECIAL'] == 1]
        ne = ne.rename( columns = {'PK_COD_ENTIDADE' : 'id_escola',
                                'FK_COD_ALUNO' : 'cd_aluno_inep', 
                                'PK_COD_TURMA' : 'id_turma',
                                'ANO_CENSO' : 'ano',
                                'NUM_IDADE' : 'idade',
                                'FK_COD_ETAPA_ENSINO' : 'grade',
                                'ID_POSSUI_NEC_ESPECIAL' : 'disabled'})
        ne = ne[['ano','cd_aluno_inep', 'id_escola', 'id_turma','grade','idade','disabled']]
        st1.append(ne)
    s1 = pd.concat(st1, axis = 0)
    s1.to_pickle('d_individual_'+str(y)+'.pkl')


for y in range(2015,2018):  
    st2 = []  
    print(y)
    for r in regions:
        print(r)
        os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
        ne = pd.read_csv(r+'.CSV', delimiter= '|')
        #ne = ne.loc[ne['CO_UF'] !=  23]
        #ne = ne.loc[ne['IN_NECESSIDADE_ESPECIAL'] == 1]
        ne = ne.rename( columns = {'CO_ENTIDADE' : 'id_escola',
                                'CO_PESSOA_FISICA' : 'cd_aluno_inep', 
                                'ID_TURMA' : 'id_turma',
                                'NU_ANO_CENSO' : 'ano',
                                'NU_IDADE' : 'idade',
                                'TP_ETAPA_ENSINO' : 'grade',
                                'IN_NECESSIDADE_ESPECIAL': 'disabled'})
        ne = ne[['ano','cd_aluno_inep', 'id_escola', 'id_turma','grade','idade','disabled']]
        st2.append(ne)
    s2 = pd.concat(st2, axis = 0)
    s2.to_pickle('d_individual_'+str(y)+'.pkl')

for y in range(2007,2018):
    print(y)
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    base = pd.read_pickle('d_individual_'+str(y)+'.pkl')
    print(base.shape[0])
    base = base.groupby(['ano','cd_aluno_inep']).first().reset_index()
    base.to_pickle('d_individual_gby'+str(y)+'.pkl')
    print(base.shape[0])
'''

Merge

'''
for y in range(2007,2018):
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    ceara = pd.read_pickle('d_individual_'+str(y)+'.pkl')
    print(ceara.shape[0])
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/schools')
    schools = pd.read_pickle('d_schools.pkl')
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/classroomns')
    classroomns = pd.read_pickle('d_special_classroomns.pkl')
    '''

    Merge dataset

    '''
    ceara = ceara.merge(schools, on = ['ano','id_escola'])
    ceara = ceara.merge(classroomns, on = ['ano','id_escola','id_turma'])
    print(ceara.shape[0])
    '''

    Clean the data set:
        - grades = 41: 9 ano
        - grades window are professional and other high school stuff
        
    '''
    ceara = ceara.loc[ceara['grade'] < 43]
    ceara = ceara.loc[(ceara['grade'] < 25) | (ceara['grade'] == 41) | (ceara['grade'] == 56)]
    ceara = ceara.loc[ceara['idade'] < 20]
    '''

    Creating special_edu dummy. 1 if special school or classroom

    '''
    ceara['special_edu'] = 0
    ceara.loc[(ceara['classroom_especial'].isna()) & (ceara['edu_especial'].isna()), 'special_edu'] = np.nan
    ceara.loc[((ceara['classroom_especial'] == 2) | (ceara['edu_especial'] == 1)) & (ceara['ano'] < 2015), 'special_edu'] = 1
    ceara.loc[((ceara['classroom_especial'] == 1) | (ceara['edu_especial'] == 1)) & (ceara['ano'] >= 2015), 'special_edu'] = 1
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    ceara.to_pickle('d_individual_merged'+str(y)+'.pkl')
'''

Share of regular enrollments

'''
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/classroomns')
classroomns = pd.read_pickle('merged_ind_sch_classr.pkl')

shares = []
for y in range(2007,2018):
    dic = {}
    print(y)
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    c = pd.read_pickle('d_individual_merged'+str(y)+'.pkl')
    c = c.loc[c['special_edu']==0]
    disabled = c.loc[c['disabled'] == 1].shape[0]
    d = 100*(disabled/c.shape[0])
    dic['year'] = y
    dic['share'] = d
    shares.append(dic)

shares = pd.DataFrame(shares)

sns.lineplot(data = shares, x='year', y='share').set(ylabel='Share of disabled students', title = 'Fraction of students in regular classroomns who are disabled - Brazil')
'''

Disabled students (at least once declared disabled)

'''
ids_list = []
for y in range(2007, 2018):
    print(y)
    dic = {}
    drop = {}
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    ceara = pd.read_pickle('d_individual_merged'+str(y)+'.pkl')
    lista = list(set(ceara.loc[ceara['disabled'] == 1]['cd_aluno_inep']))    
    ids_list.extend(lista)  
            
ids_disabled = list(set(ids_list))

flow = []
drop_outs = []
for y in range(2007, 2018):
    print(y)
    dic = {}
    drop = {}
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    ceara = pd.read_pickle('d_individual_merged'+str(y)+'.pkl')
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y+1)+'/DADOS')
    ceara1 = pd.read_pickle('d_individual_merged'+str(y+1)+'.pkl')
    ceara = pd.concat([ceara,ceara1], axis = 0).reset_index().drop('index', axis = 1)
    disabled = ceara.loc[ceara['cd_aluno_inep'].isin(ids_disabled)]
    p = ceara.loc[ceara['ano'] == y]   
    p_r = ceara.loc[(ceara['ano'] == y) & (ceara['special_edu'] == 0)]   
    p_s = ceara.loc[(ceara['ano'] == y) & (ceara['special_edu'] == 1)]   
    n = ceara.loc[(ceara['ano'] == y + 1) & (ceara['special_edu'] == 0)]   
    s = ceara.loc[(ceara['ano'] == y + 1) & (ceara['special_edu'] == 1)]   
    past = set(p.cd_aluno_inep)    
    past_reg = set(p_r.cd_aluno_inep)
    past_spe = set(p_s.cd_aluno_inep)
    next = set(n.cd_aluno_inep)
    special = set(s.cd_aluno_inep)
    dic['year'] = y + 1
    dic['special'] = len(next.intersection(past_spe))
    dic['special_ids'] = next.intersection(past_spe)
    dic['regular'] = len(next.intersection(past_reg))
    dic['new'] = len(next) - dic['special'] - dic['regular']
    dic['new_ids'] = next.difference(dic['special_ids'].union(next.intersection(past_reg)))
    dic['total'] = len(next)
    flow.append(dic)
    drop['year'] = y +1
    drop['special'] = len(past_spe.difference(special))
    drop['regular'] = len(past_reg.difference(next))
    drop['total']  = len(past.difference(next))
    drop['total_special'] = len(past_spe)
    drop['ids_drop'] = past_reg.difference(next)
    drop['total_regular'] = len(past_reg)
    drop_outs.append(drop)
    
flow = pd.DataFrame(flow)
flow['%special'] = 100*(flow['special']/(flow['total'] - flow['regular']))
flow['%new'] = 100*(flow['new']/(flow['total'] - flow['regular']))  

drop_outs = pd.DataFrame(drop_outs)
drop_outs['%special'] = 100*(drop_outs['special']/(drop_outs['total_special']))
drop_outs['%regular'] = 100*(drop_outs['regular']/(drop_outs['total_regular']))   
'''

Divided bars - New entrants

'''
p =  flow[['year', '%special', '%new']]
p = p.set_index('year')
p.plot(kind='bar', stacked=True, colormap = 'winter', 
       title='Origin of new entrants',
       xlabel='Year',
       ylabel='Percent of new entries')
'''

Divided bars - All regular

'''
flow['% Not new'] = 100*(flow['regular']/flow['total'])
flow['% New'] = 100*(flow['new']/flow['total'])
flow['% Special education'] = 100*(flow['special']/flow['total'])

p =  flow[['year', '% Not new', '% New','% Special education']]
p = p.set_index('year')
p.plot(kind='bar', stacked=True, legend= 'Lower right',
       title='Composition of disabled students in regular classroomns',
       xlabel='Year',
       ylabel='Fraction of students')
'''

Enrollment in special classrooms schools

'''
enrollment = []
for y in range(2008, 2018):
    print(y)
    dic = {}
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y-1)+'/DADOS')
    ceara = pd.read_pickle('d_individual_merged'+str(y-1)+'.pkl')
    os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/raw_data/education_census/'+str(y)+'/DADOS')
    ceara1 = pd.read_pickle('d_individual_merged'+str(y)+'.pkl')
    ceara = pd.concat([ceara,ceara1], axis = 0).reset_index().drop('index', axis = 1)
    disabled = ceara.loc[ceara['cd_aluno_inep'].isin(ids_disabled)]
    d  = disabled.loc[disabled['ano'] == y-1]
    d1 = disabled.loc[disabled['ano'] == y]
    id = set(d.cd_aluno_inep.unique())
    id1 = set(d1.cd_aluno_inep.unique())
    new = list(id1.difference(id))
    new_frame = d1.loc[d1['cd_aluno_inep'].isin(new)]
    aee_e = new_frame.loc[new_frame['aee'] == 1].shape[0]
    aee_n = new_frame.loc[new_frame['aee'] == 0].shape[0]
    dic['year'] = y
    dic['program'] = aee_e
    dic['not program'] = aee_n
    enrollment.append(dic)

dados = pd.DataFrame(enrollment)
dados['With the Program'] = 100*(dados['program']/(dados['program'] + dados['not program']))
dados['Without the Program'] = 100*(dados['not program']/(dados['program'] + dados['not program']))
dados = dados.loc[dados['year'] != 2007]

p = dados[['year','With the Program','Without the Program']]
p = p.set_index('year')
p.plot(kind='bar', stacked=True, legend= 'Lower right',
       title='New entrants fraction in schools with and without the program',
       xlabel='Year',
       ylabel='Fraction of students')

d = []
da = dados[['year','P']]
da['Type'] = 'Program'
da = da.rename(columns={'P':'% increase in new entries'})
d.append(da)
da = dados[['year','np']]
da['Type'] = 'No Program'
da = da.rename(columns={'np':'% increase in new entries'})
d.append(da)
d = pd.concat(d,axis=0).reset_index().drop('index',axis=1)

schools_aee = []
for y in range(2009, 2018):
    dic = {}
    dic['Year'] = y
    sc = schools.loc[schools['ano'] == y]
    allsc = sc.shape[0]
    aee = sc.loc[sc['aee'] == 1].shape[0]
    share = 100*(aee/allsc)
    print(share)
    dic['share'] = share
    schools_aee.append(dic)
    
schools_aee = pd.DataFrame(schools_aee)
schools_aee = schools_aee.set_index('Year')
schools_aee.plot(kind='bar', stacked=True, legend=False,
       title='Share of schools with the special education classroom',
       xlabel='Year',
       ylabel='Share of schools')

'''

Regular schools with special classrooms

'''
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/schools')
schools = pd.read_pickle('d_schools.pkl')
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/classroomns')
classroomns = pd.read_pickle('d_special_classroomns.pkl')

special_classroomns = schools.merge(classroomns, on = ['ano','id_escola'])


