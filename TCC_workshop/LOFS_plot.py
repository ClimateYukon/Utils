#DRAFT
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams[ 'xtick.direction' ] = 'out'
rcParams[ 'ytick.direction' ] = 'out'
rcParams[ 'xtick.labelsize' ] = 'medium'
rcParams[ 'ytick.labelsize' ] = 'medium'
rcParams[ 'figure.titlesize' ] = 'large'
rcParams[ 'axes.titlesize' ] = 'large'
rcParams[ 'axes.spines.top' ] = 'False'
rcParams[ 'axes.spines.right' ] = 'False'
rcParams[ 'savefig.dpi' ] = 300
rcParams[ 'figure.figsize'] = 14 , 8
# value = [rasterstats.zonal_stats(shp,f,stats='mean')[0]['mean'] for f in files]

value = [212.07856038424845,
208.03556272000526,
206.4579399282824,
202.2881863341777,
196.8376484521499,
193.11402441030364,
189.8872915090305,
184.48195545613055,
181.71750501694245]

df = pd.DataFrame(value,index = ['2010s','2020s','2030s','2040s','2050s','2060s','2070s','2080s','2090s'])

df.columns = ["LOFS"]
ax = df.plot(kind='bar', legend=False)
                                                       
totals = []

# find the values and append to list
for i in ax.patches:
 totals.append(i.get_height())

# set individual bar lables using above list
total = sum(totals)

# set individual bar lables using above list
for i in ax.patches:
 # get_x pulls left or right; get_height pushes up or down
 ax.text(i.get_x()+.08, i.get_height()-8, \
         str(round(i.get_height(), 0)),
             color='black')
plt.ylabel('Length of Freezing Season (Days)')
plt.xlabel('Decades')
plt.title('Length of Freezing Season in the Yukon Flats Area')

plt.savefig( output_filename )
plt.close()
