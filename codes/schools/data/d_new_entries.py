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

#################

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

#################
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
'''

Share of regular enrollments

'''
#ceara.loc[ceara['cd_aluno_inep'].isin(ids_disabled), 'disabled'] = 1
regular = ceara.loc[ceara['special_edu']==0]
disabled_regular = share(regular, 2007, 2017, 'disabled')
sns.lineplot(data = disabled_regular, x='year', y='share').set(ylabel='Share of disabled students', title = 'Fraction of students in regular classroomns who are disabled')
'''

Disabled students (at least once declared disabled)

'''
ids_disabled = list(set(ceara.loc[ceara['disabled'] == 1]['cd_aluno_inep']))
disabled = ceara.loc[ceara['cd_aluno_inep'].isin(ids_disabled)]

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
for y in range(2008,2018):
    dic = {}
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


sns.lineplot(data = d,x = 'year', y='% increase in new entries', hue='Type').set(title = 'Percentage change in new entries by school type')


colors = ['g', 'b']
c = ['P','np']
title = 'Share of disabled in regular schools and program expansion - CE'
ylabels = ['% Disabled students in regular classroomns',
           '% Municipalities with the program']
two_scales(dados,c,colors,'year',title,ylabels)
