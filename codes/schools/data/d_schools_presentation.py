import os
import math
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

os.chdir('/Users/angelosantos/Library/CloudStorage/OneDrive-UniversityOfHouston/ideas/disabilities/data/data_created/schools')
schools = pd.read_pickle('d_schools.pkl')

for y in range(2007,2018):
    s = schools.loc[schools['ano'] == y]
    s = s.loc[s['edu_especial'] == 1]
    s_priv = s.loc[s['dependencia'] == 4].shape[0]
    p_priv = 100*(s_priv/s.shape[0])
    print(s.shape[0])
    print(p_priv)
    
dics =[]
for y in range(2007,2018):
    dic = {}
    dic['year'] = y
    s = schools.loc[schools['ano'] == y]
    all_mun = len(s.id_municipio.unique())
    print(all_mun)
    s = s.loc[s['edu_especial'] == 1]
    special_mun = len(s.id_municipio.unique())
    dic['Special schools availability'] = 100*(special_mun/all_mun)
    spe = len(s.loc[s['dependencia'] != 4]['id_municipio'].unique())
    print(100*(spe/all_mun))
    dic['Public special schools availability'] = 100*(spe/all_mun)
    dics.append(dic)

    

dics = pd.DataFrame(dics).set_index('year').T.reset_index()
dics = dics.rename(columns={'index':'Availability'})

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
           dics['Availability'].values.tolist(), 
           ncol = 3, 
           loc = 'best', 
           framealpha = 0.1,
           fontsize = 10)
           
ax.set_ylabel('Fraction of municipalities', fontdict= {'fontsize': 15})
ax.set_xlabel('Year', fontdict= {'fontsize': 15})
ax.set_title('Brazilian municipalities with special schools', fontdict= {'fontsize': 15})
ax.set_xticks(x)
ax.set_xticklabels(dics.columns.values[1:],fontdict= {'fontsize': 10})

#for i in range(num_groups):
#    ax.bar_label(b[i], 
#                 padding = 3, 
#                 label_type='center', 
#                 rotation = 'vertical')
plt.show()