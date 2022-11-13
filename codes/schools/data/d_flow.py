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
ceara.to_pickle('d_individual_disabled_flow_v1.pkl')
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/individual')
ceara = pd.read_pickle('d_individual_disabled_flow_v1.pkl')
'''

Uploading classroom and school information about special enviroments

'''
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/classroomns')
classroomns = pd.read_pickle('d_special_classroomns.pkl')
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/schools')
schools = pd.read_pickle('d_special_schools_pub_priv.pkl')
'''

Merge dataset

'''
ceara = ceara.merge(schools, on = ['ano','id_escola'])
ceara = ceara.merge(classroomns, on = ['ano','id_escola','id_turma'])
'''

Clean the data set:
    - grades = 41: 9 ano
    - grades window are professional and other high school stuff
    
'''
ceara = ceara.loc[ceara['grade'] < 43]
ceara = ceara.loc[(ceara['grade'] < 25) | (ceara['grade'] == 41)]
ceara = ceara.loc[ceara['idade'] < 20]
'''

Creating special_edu dummy. 1 if special school or classroom

'''
ceara['special_edu'] = 0
ceara.loc[(ceara['classroom_especial'].isna()) & (ceara['edu_especial'].isna()), 'special_edu'] = np.nan
ceara.loc[((ceara['classroom_especial'] == 2) | (ceara['edu_especial'] == 1)) & (ceara['ano'] < 2015), 'special_edu'] = 1
ceara.loc[((ceara['classroom_especial'] == 1) | (ceara['edu_especial'] == 1)) & (ceara['ano'] >= 2015), 'special_edu'] = 1
'''

Enrollment data

'''
enrollment = []
for y in range(2007,2018):
    ceara_y = ceara.loc[ceara['ano'] == y]
    dic = {}
    dic['year'] = y
    dic['special'] = ceara_y.special_edu.value_counts()[1]
    dic['regular'] = ceara_y.special_edu.value_counts()[0]
    dic['nan'] = ceara_y.special_edu.isna().sum()
    enrollment.append(dic)

enrollment = pd.DataFrame(enrollment)
enrollment['%regular'] = 100*(enrollment['regular']/(enrollment['regular'] + enrollment['special']))
enrollment['%special'] = 100 - enrollment['%regular']
'''

Plotting two scales

'''
colors = ['g', 'b']
c = ['%regular','%special']
title = 'Share of disabled students in regular and special classroomns'
ylabels = ['% Regular',
           '% Special']
two_scales(enrollment,c,colors,'year',title,ylabels)
'''

Plotting program and enrollment

'''
data = enrollment
data = data.rename(columns = {'ano' : 'year'})
state = 'CE'
classroom(state)
ce = df
ce = ce.loc[ce.year > 2008]
ce = ce.loc[ce.year < 2018]
data = data.loc[data.year > 2008]
data = data.loc[data.year < 2018]
'''

Join the data

'''
frame = data.join(ce.drop('year', axis =1))
'''

Plotting two scales

'''
colors = ['g', 'b']
c = ['%regular','Classroom']
title = 'Share of disabled in regular schools and program expansion - CE'
ylabels = ['% Disabled students in regular classroomns',
           '% Municipalities with the program']
two_scales(frame,c,colors,'year',title,ylabels)
'''

Creating table of flow

'''
flow = []
drop_outs = []
for y in range(2007,2017):
    dic = {}
    drop = {}
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
    dic['regular'] = len(next.intersection(past_reg))
    dic['new'] = len(next) - dic['special'] - dic['regular']
    dic['total'] = len(next)
    flow.append(dic)
    drop['year'] = y +1
    drop['special'] = len(past_spe.difference(special))
    drop['regular'] = len(past_reg.difference(next))
    drop['total']  = len(past.difference(next))
    drop['total_special'] = len(past_spe)
    drop['total_regular'] = len(past_reg)
    drop_outs.append(drop)
    
flow = pd.DataFrame(flow)
flow['%special'] = 100*(flow['special']/(flow['total'] - flow['regular']))
flow['%new'] = 100*(flow['new']/(flow['total'] - flow['regular']))  
flow['%new entries'] = 100*(pd.DataFrame(enrollment.regular.pct_change().dropna().tolist())[0])

drop_outs = pd.DataFrame(drop_outs)
drop_outs['%special'] = 100*(drop_outs['special']/(drop_outs['total_special']))
drop_outs['%regular'] = 100*(drop_outs['regular']/(drop_outs['total_regular']))   
'''

Plots Regular new enrollments

'''        
flow['new entries'] = (flow['total'] - flow['regular']) 
graph = []
for c in ['%special','%new entries']:
    flow_graph = flow[['year',c]]
    flow_graph = flow_graph.rename(columns={c : 'entries'})
    flow_graph['hue'] = c
    graph.append(flow_graph)

graph = pd.concat(graph, axis = 0 ).reset_index().drop('index', axis = 1)
sns.lineplot(data = graph, x='year', y='entries', hue='hue')
'''

Plot drop outs

'''
drop_outs = drop_outs.rename(columns={'ano':'year'})
c = ['%special','%regular']
title = 'Disabled dropout by type of classroomn- CE'
ylabels = ['% Special dropouts',
           '% Regular dropouts']
two_scales(drop_outs,c,colors,'year',title,ylabels)
'''

Regular enrollment and special share flow

'''
reg_enr = enrollment.loc[enrollment['year'] != 2007].reset_index().drop('index', axis = 1)
flow['%regular enrollment'] = reg_enr['%regular']

c = ['%regular enrollment','%special']
title = 'Disabled regular enrollment and flow from special education - CE'
ylabels = ['% Regular enrollment',
           '% Special flow']
two_scales(flow,c,colors,'year',title,ylabels)
