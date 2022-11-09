'''

Author: Angelo Santos

This code plots the special students enrollment evolution between 2007 and 2017. 
    - Dataset used: d_enrollment_ceara.pkl
    - Source code for data creation: d_special_enrollment.py

'''
import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
'''

Graph Settings

'''
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

PART 1: Using school info
=======

Uploading the data 

'''
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/enrollment')
data = pd.read_pickle('d_enrollment_ce.pkl')
data["%sp"] = 100*data['special']/(data['special']+data['regular']+data['nan'])
data["%sp_notnan"] = 100*data['special']/(data['special']+data['regular'])
data["%re"] = 100*data['regular']/(data['special']+data['regular']+data['nan'])
data["%na"] = 100*data['nan']/(data['special']+data['regular']+data['nan'])
'''

Plotting just percentage of disabled students enrolled in special institutions

'''
sns.lineplot(data = data, x='year', y = '%sp_notnan').set(title = 'Percentage Disabled students in special institutions', ylabel ='% of Disabled students')
'''

Plotting regular and special enrollments

'''
colors = ['g', 'b']
c = ['%sp', '%re']
title = 'Disabled enrollment'
ylabels = ['% Special schools',
           '% Regular schools']

two_scales(data,c,colors,'year',title,ylabels)

'''

Municipalities increase and regular enrollment.

First call the data

'''
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
c = ['%re','Classroom']
title = 'Disabled enrollment in regular schools and program expansion - CE'
ylabels = ['% Regular enrollment',
           '%  Municipalities']
two_scales(frame,c,colors,'year',title,ylabels)

'''

PART 2: Using classroom info
=======

Uploading the data 

'''
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/enrollment')
data = pd.read_pickle('d_enrollment_classroomns_ce.pkl')
data["%sp"] = 100*data['special']/(data['special']+data['regular']+data['nan'])
data["%sp_notnan"] = 100*data['special']/(data['special']+data['regular'])
data["%re"] = 100*data['regular']/(data['special']+data['regular']+data['nan'])
data["%na"] = 100*data['nan']/(data['special']+data['regular']+data['nan'])
'''

Plotting just percentage of disabled students enrolled in special classroomns

'''
sns.lineplot(data = data, x='year', y = '%sp_notnan').set(title = 'Percentage Disabled students in special institutions', ylabel ='% of Disabled students')
'''

Plotting regular and special enrollments

'''
colors = ['g', 'b']
c = ['%sp', '%re']
title = 'Disabled enrollment in special and regular classroomns'
ylabels = ['% Special classroomns',
           '% Regular classroomns']

two_scales(data,c,colors,'year',title,ylabels)
'''

Municipalities increase and regular enrollment.

First call the data

'''
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
c = ['%re','Classroom']
title = 'Disabled enrollment in regular schools and program expansion - CE'
ylabels = ['% Disabled students in regular classroomns',
           '%  Municipalities with the program']
two_scales(frame,c,colors,'year',title,ylabels)