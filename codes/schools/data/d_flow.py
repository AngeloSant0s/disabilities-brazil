'''

Author: Angelo Santos

This code will create a dataframe will flow of disabled students, we have four possibilities:
    1. Special school -> Regular school without AEE
    2. Special school -> Regular school with AEE
    3. Regular school without AEE -> Regular school with AEE 
    4. At home -> Regular school
    
'''
import os
import math
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
sns.set_style('white')
sns.despine(left=False, bottom=True)
sns.set_context("paper")

########################################## FUNCTIONS - START

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


def line_frame(data, column, start, end):
    line_frame = []
    for h in data[column].unique():
        row = data.loc[dics[column] == h]
        for y in range(start, end+1):
            line_dic = {}
            line_dic['year'] = y
            line_dic['share'] = row[str(y)].item()
            line_dic['hue'] = h
            line_frame.append(line_dic)
    line_frame = pd.DataFrame(line_frame)
    return line_frame

########################################## FUNCTIONS - END

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
                               'FK_COD_ETAPA_ENSINO' : 'grade',
                               'ID_POSSUI_NEC_ESPECIAL' : 'disabled'})
    ne = ne[['ano','cd_aluno_inep', 'id_escola', 'id_turma','grade','idade','disabled']]
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
                               'TP_ETAPA_ENSINO' : 'grade',
                               'IN_NECESSIDADE_ESPECIAL': 'disabled'})
    ne = ne[['ano','cd_aluno_inep', 'id_escola', 'id_turma','grade','idade','disabled']]
    st2.append(ne)
s2 = pd.concat(st2, axis = 0)

ceara = pd.concat([s1,s2], axis = 0).reset_index().drop('index', axis =1)
ceara = ceara.groupby(['ano','cd_aluno_inep']).first().reset_index()
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/individual')
ceara.to_pickle('d_individual_flow_v1.pkl')
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/individual')
ceara = pd.read_pickle('d_individual_flow_v1.pkl')

'''

Share of Disabled enrollments

'''
dis_share = share(ceara, 2007, 2017, 'disabled')
sns.lineplot(data = dis_share, x='year', y='share').set(ylabel='Share of disabled students', title = 'Disabled students share in enrollments')

'''

Uploading classroom and school information about special enviroments

'''
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/classroomns')
classroomns = pd.read_pickle('d_special_classroomns.pkl')
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/schools')
schools = pd.read_pickle('d_special_schools_pub_priv.pkl')
'''

Share of Schools with the special classroom

'''
sch_share = share(schools, 2007, 2017, 'aee')
sns.lineplot(data = sch_share, x='year', y='share').set(ylabel='Share of schools', title = 'Proportion of schools with targeting classroomn')
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
ceara = ceara.loc[(ceara['grade'] < 25) | (ceara['grade'] == 41) | (ceara['grade'] == 56)]
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
non = ceara.loc[ceara['disabled'] == 0]
disabled = ceara.loc[ceara['disabled'] == 1]
enrollment = []
ceara = disabled
for y in range(2007,2018):
    ceara_y = ceara.loc[disabled['ano'] == y]
    dic = {}
    dic['year'] = y
    dic['special'] = ceara_y.special_edu.value_counts()[1]
    dic['regular'] = ceara_y.special_edu.value_counts()[0]
    dic['nan'] = ceara_y.special_edu.isna().sum()
    enrollment.append(dic)

enrollment = pd.DataFrame(enrollment)
enrollment['%regular'] = 100*(enrollment['regular']/(enrollment['regular'] + enrollment['special']))
enrollment['%special'] = 100 - enrollment['%regular']
sns.lineplot(data = enrollment, x='year', y='%regular').set(ylabel='Share of disabled students', title = 'Disabled students regular enrollments')
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
non = ceara.loc[ceara['disabled'] == 0]
disabled = ceara.loc[ceara['disabled'] == 1]

flow = []
drop_outs = []
ceara = disabled
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

Plotting new entrants by grades

'''
frs = []
for y in range(2008,2018):
    c = ceara.loc[ceara['ano'] == y]
    ids = list(flow['new_ids'][y-2008])
    c = c.loc[c['cd_aluno_inep'].isin(ids)]
    frame = pd.DataFrame(c.grade.value_counts()).reset_index().rename(columns = {'index' : 'grades', 'grade' : 'entries'})
    frame['ano'] = y
    frame['total'] = c.shape[0]
    frs.append(frame)
frs = pd.concat(frs, axis=0)

frs['%share'] = 100*(frs['entries']/frs['total'])
frs['Kindergarden'] = ((frs['grades'] < 4 )).astype(int)
frs['Primary'] = (((frs['grades'] >= 4) & (frs['grades'] <= 8)) 
                 | (frs['grades'] == 56)
                 | ((frs['grades'] >= 14) & (frs['grades'] <= 18)) 
                 ).astype(int)


frs['First two years'] = ((frs['grades'] == 4)                  
                          | (frs['grades'] == 56)
                          | ((frs['grades'] >= 14) & (frs['grades'] <= 15)) 
                         ).astype(int)

# Grades
frs['1st grade'] = ((frs['grades'] == 56) | (frs['grades'] == 14)).astype(int)
frs['2nd grade'] = ((frs['grades'] == 4)  | (frs['grades'] == 15)).astype(int)
frs['3rd grade'] = ((frs['grades'] == 5)  | (frs['grades'] == 16)).astype(int)
frs['4th grade'] = ((frs['grades'] == 6)  | (frs['grades'] == 17)).astype(int)
frs['5th grade'] = ((frs['grades'] == 7)  | (frs['grades'] == 18)).astype(int)

# Last three years (3rd - 5th)
frs['Last three years'] = (((frs['grades'] >= 5) & (frs['grades'] <= 7)) 
                 | ((frs['grades'] >= 16) & (frs['grades'] <= 18)) 
                 ).astype(int)

# Secondary
frs['Secondary'] = ((frs['grades'] > 8) & (frs['grades'] <= 13) | (frs['grades'] > 18)).astype(int)

grades_frame = frs.groupby(['ano','Kindergarden', 'Primary','Secondary','total']).sum().reset_index()
grades_frame['%share'] = 100*(grades_frame['entries']/grades_frame['total'])

primary_frame = frs.loc[frs['Primary']== 1]
primary_frame = frs.groupby(['ano', 'First two years', 'Last three years' ,'total']).sum().reset_index()
for y in range(2008,2018):
    year = frs.loc[(frs['Primary']== 1) & (frs['ano'] == y)]['entries'].sum()
    primary_frame.loc[primary_frame['ano'] == y, 'total'] = year
primary_frame['%share'] = 100*(primary_frame['entries']/primary_frame['total'])
primary_frame = primary_frame.loc[primary_frame['Kindergarden'] == 0]

primary_grades = frs.loc[frs['Primary']== 1]
primary_grades = frs.groupby(['ano','1st grade','2nd grade','3rd grade','4th grade','5th grade', 'total']).sum().reset_index()
for y in range(2008,2018):
    year = frs.loc[((frs['First two years']== 1) | (frs['Last three years']== 1)) & (frs['ano'] == y)]['entries'].sum()
    primary_grades.loc[primary_grades['ano'] == y, 'total'] = year
primary_grades['%share'] = 100*(primary_grades['entries']/primary_grades['total'])
primary_grades = primary_grades.loc[primary_grades['Kindergarden'] == 0]

dics =[]
for c in ['1st grade','2nd grade','3rd grade','4th grade','5th grade']:
    d = {}
    d['stage'] = c
    for y in range(2008,2018):
        g = round(primary_grades.loc[(primary_grades[c] == 1) & (primary_grades['ano'] ==y)]['%share'].item(),2)
        d[str(y)] = g
        dics.append(d)

dics = pd.DataFrame(dics).groupby('stage').first().reset_index()

dics =[]
for c in ['First two years','Last three years']:
    d = {}
    d['stage'] = c
    for y in range(2008,2018):
        g = round(primary_frame.loc[(primary_frame[c] == 1) & (primary_frame['ano'] ==y)]['%share'].item(),2)
        d[str(y)] = g
        dics.append(d)

dics = pd.DataFrame(dics).groupby('stage').first().reset_index()


dics =[]
for c in ['Kindergarden','Primary','Secondary']:
    d = {}
    d['stage'] = c
    for y in range(2008,2018):
        g = round(grades_frame.loc[(grades_frame[c] == 1) & (grades_frame['ano'] ==y)]['%share'].item(),2)
        d[str(y)] = g
        dics.append(d)

dics = pd.DataFrame(dics).groupby('stage').first().reset_index()
dics = dics[['stage','2009','2011','2013','2016','2017']]
'''

Plot bars

'''
# Variables
w = 1.0
num_yrs = dics.shape[1] - 1
num_groups = dics.shape[0]

# Parameters
first_tick = int(math.ceil((num_groups*w/2))) 
gap = num_groups*w + 1
x = np.array([first_tick + i*gap for i in range(num_yrs)])
    
# Colors
colors = plt.cm.get_cmap('winter',num_groups)

# Plot
fig,ax = plt.subplots(1,1, figsize=(10,10))
b = []
for i in range(num_groups):
    b.append(ax.bar(x - (i - num_groups/2 + 0.5)*w, 
             dics.loc[i].values[1:], 
             width=w, 
             color=colors(i), 
             align='center', 
             edgecolor = 'black', 
             linewidth = 1.0, 
             alpha=0.5))
ax.legend([b_ for b_ in b], 
           dics['stage'].values.tolist(), 
           ncol = 3, 
           loc = 'best', 
           framealpha = 0.1,
           fontsize = 10)
           
ax.set_ylabel('Share of new primary entries', fontdict= {'fontsize': 15})
ax.set_xlabel('Years', fontdict= {'fontsize': 15})
ax.set_title('New entries by Primary education grade', fontdict= {'fontsize': 15})
ax.set_xticks(x)
ax.set_xticklabels(dics.columns.values[1:],fontdict= {'fontsize': 10})

#for i in range(num_groups):
#    ax.bar_label(b[i], 
#                 padding = 3, 
#                 label_type='center', 
#                 rotation = 'vertical')
plt.show()
'''

Idades 

'''
frs = []
for y in range(2008,2018):
    c = ceara.loc[ceara['ano'] == y]
    ids = list(flow['new_ids'][y-2008])
    c = c.loc[c['cd_aluno_inep'].isin(ids)]
    frame = pd.DataFrame(c.idade.value_counts()).reset_index().rename(columns = {'index' : 'idades', 'idade' : 'entries'})
    frame['ano'] = y
    frame['total'] = c.shape[0]
    frs.append(frame)

frs = pd.concat(frs, axis=0)
frs['%share'] = 100*(frs['entries']/frs['total'])
frs['Compulsory'] = ((frs['idades'] < 7)).astype(int)
frs['7-10']    = ((frs['idades'] >= 7) & (frs['idades'] <= 10)).astype(int)
frs['>10']  = (frs['idades'] > 10).astype(int)
idades_frame = frs.groupby(['ano','Compulsory', '7-10','>10','total']).sum().reset_index()
idades_frame['%share'] = 100*(idades_frame['entries']/idades_frame['total'])

dics =[]
for c in ['Compulsory','7-10','>10']:
    d = {}
    d['stage'] = c
    for y in range(2008,2018):
        g = round(idades_frame.loc[(idades_frame[c] == 1) & (idades_frame['ano'] == y)]['%share'].item(),2)
        d[str(y)] = g
        dics.append(d)

dics = pd.DataFrame(dics).groupby('stage').first().reset_index()
'''

Plot bars

'''
# Variables
w = 1.0
num_yrs = dics.shape[1] - 1
num_groups = dics.shape[0]

# Parameters
first_tick = int(math.ceil((num_groups*w/2))) 
gap = num_groups*w + 1
x = np.array([first_tick + i*gap for i in range(num_yrs)])
    
# Colors
colors = plt.cm.get_cmap('winter',num_groups)

# Plot
fig,ax = plt.subplots(1,1, figsize=(10,10))
b = []
for i in range(num_groups):
    b.append(ax.bar(x - (i - num_groups/2 + 0.5)*w, 
             dics.loc[i].values[1:], 
             width=w, 
             color=colors(i), 
             align='center', 
             edgecolor = 'black', 
             linewidth = 1.0, 
             alpha=0.5))
ax.legend([b_ for b_ in b], 
           dics['stage'].values.tolist(), 
           ncol = 3, 
           loc = 'best', 
           framealpha = 0.1,
           fontsize = 10)
           
ax.set_ylabel('Share of new entries', fontdict= {'fontsize': 15})
ax.set_xlabel('Years', fontdict= {'fontsize': 15})
ax.set_title('New entries by age', fontdict= {'fontsize': 15})
ax.set_xticks(x)
ax.set_xticklabels(dics.columns.values[1:],fontdict= {'fontsize': 10})

#for i in range(num_groups):
#    ax.bar_label(b[i], 
#                 padding = 3, 
#                 label_type='center', 
#                 rotation = 'vertical')
plt.show()
'''

Plot drop outs

'''
drop_non = drop_outs
drop_non['hue'] = 'Non-disabled' 
con_non = drop_non[['year','%regular','hue']]
drop_outs['hue'] = 'Disabled' 
con_dis = drop_outs[['year','%regular','hue']]

drops = pd.concat([con_dis,con_non], axis=0).reset_index()
drops = drops.rename(columns={'hue' : 'Students'})
sns.lineplot(data = drops, x='year', y='%regular', hue='Students').set(ylabel='Share of students', title = 'Dropouts in regular classroomns')

drop_outs = drop_outs.rename(columns={'ano':'year'})
c = ['%special','%regular']
title = 'Disabled dropout by type of classroomn- CE'
ylabels = ['% Special dropouts',
           '% Regular dropouts']
two_scales(drop_outs,c,colors,'year',title,ylabels)
'''

dropouts by grade

'''
dps = []
for y in range(2008,2018):
    c = ceara.loc[ceara['ano'] == y-1]
    ids = list(drop_outs['ids_drop'][y-2008])
    c = c.loc[c['cd_aluno_inep'].isin(ids)]
    frame = pd.DataFrame(c.grade.value_counts()).reset_index().rename(columns = {'index' : 'grades', 'grade' : 'drops'})
    frame['ano'] = y
    frame['total'] = c.shape[0]
    dps.append(frame)
dps = pd.concat(dps, axis=0)
dps['%share'] = 100*(dps['drops']/dps['total'])
dps['Kindergarden'] = ((dps['grades'] < 4 )).astype(int)
dps['Primary'] = (((dps['grades'] >= 4) & (dps['grades'] <= 8)) 
                 | (dps['grades'] == 56)
                 | ((dps['grades'] >= 14) & (dps['grades'] <= 18)) 
                 ).astype(int)
# Secondary
dps['Secondary'] = ((dps['grades'] > 8) & (dps['grades'] <= 13) 
                   |(dps['grades'] > 18) 
                    ).astype(int)

dps['6th grade'] = ((dps['grades'] == 7) | (dps['grades'] == 19)).astype(int)
dps['7th grade'] = ((dps['grades'] == 8)  | (dps['grades'] == 20)).astype(int)
dps['8th grade'] = ((dps['grades'] == 9)  | (dps['grades'] == 21)).astype(int)
dps['9th grade'] = ((dps['grades'] == 10)  | (dps['grades'] == 41)).astype(int)

grades_frame = dps.groupby(['ano','Kindergarden', 'Primary','Secondary','total']).sum().reset_index()
grades_frame['%share'] = 100*(grades_frame['drops']/grades_frame['total'])

dics =[]
for c in ['Kindergarden','Primary','Secondary']:
    d = {}
    d['stage'] = c
    for y in range(2008,2018):
        g = round(grades_frame.loc[(grades_frame[c] == 1) & (grades_frame['ano'] ==y)]['%share'].item(),2)
        d[str(y)] = g
        dics.append(d)

dics = pd.DataFrame(dics).groupby('stage').first().reset_index()

primary_grades = dps.loc[dps['Secondary']== 1]
primary_grades = dps.groupby(['ano','6th grade','7th grade','8th grade','9th grade','total']).sum().reset_index()
for y in range(2008,2018):
    year = dps.loc[((dps['Secondary']== 1) & ((dps['6th grade']== 1) | (dps['7th grade']== 1) | (dps['8th grade']== 1) | (dps['9th grade']== 1)) & (dps['ano'] == y))]['drops'].sum()
    primary_grades.loc[primary_grades['ano'] == y, 'total'] = year
primary_grades['%share'] = 100*(primary_grades['drops']/primary_grades['total'])
primary_grades = primary_grades.loc[primary_grades['Kindergarden'] == 0]

dics =[]
for c in ['6th grade','7th grade','8th grade','9th grade']:
    d = {}
    d['stage'] = c
    for y in range(2008,2018):
        g = round(primary_grades.loc[(primary_grades[c] == 1) & (primary_grades['ano'] ==y)]['%share'].item(),2)
        d[str(y)] = g
        dics.append(d)

dics = pd.DataFrame(dics).groupby('stage').first().reset_index()
'''

Plot bars

'''
# Variables
w = 1.0
num_yrs = dics.shape[1] - 1
num_groups = dics.shape[0]

# Parameters
first_tick = int(math.ceil((num_groups*w/2))) 
gap = num_groups*w + 1
x = np.array([first_tick + i*gap for i in range(num_yrs)])
    
# Colors
colors = plt.cm.get_cmap('winter',num_groups)

# Plot
fig,ax = plt.subplots(1,1, figsize=(10,10))
b = []
for i in range(num_groups):
    b.append(ax.bar(x - (i - num_groups/2 + 0.5)*w, 
             dics.loc[i].values[1:], 
             width=w, 
             color=colors(i), 
             align='center', 
             edgecolor = 'black', 
             linewidth = 1.0, 
             alpha=0.5))
ax.legend([b_ for b_ in b], 
           dics['stage'].values.tolist(), 
           ncol = 3, 
           loc = 'best', 
           framealpha = 0.1,
           fontsize = 10)
           
ax.set_ylabel('Share of drop outs', fontdict= {'fontsize': 15})
ax.set_xlabel('Years', fontdict= {'fontsize': 15})
ax.set_title('Dropouts by secondary grades', fontdict= {'fontsize': 15})
ax.set_xticks(x)
ax.set_xticklabels(dics.columns.values[1:],fontdict= {'fontsize': 10})

#for i in range(num_groups):
#    ax.bar_label(b[i], 
#                 padding = 3, 
#                 label_type='center', 
#                 rotation = 'vertical')
plt.show()
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

######################################## LINES GRAPHS

fr = line_frame(dics,'stage', 2008, 2017)
fr = fr.rename(columns={'hue' : 'Stage',
                        'year' : 'Year',
                        'share' : 'Share of drop outs'})
sns.lineplot(data = fr, x='Year' , y = 'Share of drop outs', hue='Stage', palette='winter').set_title('Dropouts by secondary grades')

p.plot(kind='bar', stacked=True, colormap = 'winter' )

####################################### ENROLLMENT IN TREATED

os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/individual')
ceara = pd.read_pickle('d_individual_flow_v1.pkl')
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/classroomns')
classroomns = pd.read_pickle('d_special_classroomns.pkl')
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/schools')
schools = pd.read_pickle('d_special_schools_v1.pkl')

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
ceara = ceara.loc[(ceara['grade'] < 25) | (ceara['grade'] == 41) | (ceara['grade'] == 56)]
ceara = ceara.loc[ceara['idade'] < 20]
'''

Creating special_edu dummy. 1 if special school or classroom

'''
ceara['special_edu'] = 0
ceara.loc[(ceara['classroom_especial'].isna()) & (ceara['edu_especial'].isna()), 'special_edu'] = np.nan
ceara.loc[((ceara['classroom_especial'] == 2) | (ceara['edu_especial'] == 1)) & (ceara['ano'] < 2015), 'special_edu'] = 1
ceara.loc[((ceara['classroom_especial'] == 1) | (ceara['edu_especial'] == 1)) & (ceara['ano'] >= 2015), 'special_edu'] = 1

mun = ceara[['ano','id_municipio','aee']]
mun = mun.groupby(['ano','id_municipio']).sum().reset_index()
mun.loc[mun['aee'] > 0, 'aee'] = 1
mun = mun.rename(columns = { 'aee':'program'})

ceara = ceara.merge(schools, on = ['ano','id_escola'])

####################################### STUDENTS CHANGING STATUS

os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/individual')
ceara = pd.read_pickle('d_individual_flow_v1.pkl')
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/classroomns')
classroomns = pd.read_pickle('d_special_classroomns.pkl')
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/schools')
schools = pd.read_pickle('d_special_schools_pub_priv.pkl')

