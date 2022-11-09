'''

Author: Angelo Santos

This code plots the education institutions evolution between 2007 and 2017. 
    - Dataset used: d_special_schools_growth.pkl
    - Source code for data creation: cre_special_schools.py

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
'''

Uploading the data 

'''
os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/schools')
data = pd.read_pickle('d_special_schools_growth_pub_priv.pkl')
data["%sp"] = 100*data['special']/(data['special']+data['regular']+data['nan'])
data["%sp_notnan"] = 100*data['special']/(data['special']+data['regular'])
data["%re"] = 100*data['regular']/(data['special']+data['regular']+data['nan'])
data["%na"] = 100*data['nan']/(data['special']+data['regular']+data['nan'])
'''

Plotting just percentage of schools which are special

'''
sns.lineplot(data = data, x='year', y = '%sp_notnan').set(title = 'Percentage of special schools', ylabel ='% of schools')

'''

Plotting all the categories

'''
colors = ['g', 'b']
c = ['%sp', '%re']
title = 'Educational institutions type evolution'
ylabels = ['% Special schools',
           '% Regular schools']

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

two_scales(data,c,colors,'year',title,ylabels)