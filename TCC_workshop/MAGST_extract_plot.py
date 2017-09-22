import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os , math
import rasterstats
import glob
import numpy as np

rcParams[ 'xtick.direction' ] = 'out'
rcParams[ 'ytick.direction' ] = 'out'
rcParams[ 'xtick.labelsize' ] = 'X-large'
rcParams[ 'ytick.labelsize' ] = 'X-large'
rcParams[ 'figure.titlesize' ] = 'X-large'
rcParams[ 'axes.titlesize' ] = 'large'
rcParams[ 'axes.spines.top' ] = 'False'
rcParams[ 'axes.spines.right' ] = 'True'
rcParams[ 'savefig.dpi' ] = 1000
rcParams[ 'figure.figsize'] = 12 , 8

path = '/workspace/Shared/Users/jschroder/Yukon-Flats_workshop/Permafrost/Source'
scenarios = ['2013_AK_Can_2km_5model_a1b','2013_AK_Can_2km_5model_a2']
shp = '/workspace/Shared/Users/jschroder/Yukon-Flats_workshop/shp/Yukon_flats.shp'
metrics = ['MAGST','MAGT']

def fahrenheit2celsius(temp):
    """
    Returns temperature in Celsius.
    """
    return (temp * 1.8) + 32


def convert_ax_c_to_celsius(ax_f):
    """
    Update second axis according with first axis.
    """
    y1, y2 = ax_f.get_ylim()
    ax_c.set_ylim(fahrenheit2celsius(y1), fahrenheit2celsius(y2))
    ax_c.figure.canvas.draw()
    
for scen in scenarios :
    for metric in metrics :
        
        out = '/workspace/Shared/Users/jschroder/Yukon-Flats_workshop/Permafrost/Plots'
        
        if not os.path.exists(os.path.join(out)):
            os.makedirs(os.path.join(out))

        _ls = glob.glob(os.path.join(path ,scen , '*{}*'.format(metric)))
        _ls.sort
        #for local testing
        # value = [-3.0035198272033425,
        #  -2.98708008808435,
        #  -2.8410754967595486,
        #  -2.3157551012435436,
        #  -2.1108880502187715,
        #  -1.4119575430963582,
        #  -0.6610001603776688,
        #  0.2984456538165773,
        #  0.9133571209741093]
         
        value = [rasterstats.zonal_stats(shp,f,stats='mean')[0]['mean'] for f in _ls[1:]]
                
        #double axes trick from :
        #https://stackoverflow.com/questions/43149703/adding-a-second-y-axis-related-to-the-first-y-axis
        #and https://matplotlib.org/examples/lines_bars_and_markers/barh_demo.html

        fig, ax_f = plt.subplots()
        ax_c = ax_f.twinx()
        decade = ['2010s','2020s','2030s','2040s','2050s','2060s','2070s','2080s','2090s']
        y_pos = np.arange(len(decade))\
        
        # automatically update ylim of ax2 when ylim of ax1 changes.
        ax_f.callbacks.connect("ylim_changed", convert_ax_c_to_celsius)
        ax_f.bar(y_pos,value)

        #labels
        ax_f.set_ylabel( 'Ground Surface Temperature ($^\circ$C)',fontsize=15 )
        ax_c.set_ylabel( 'Ground Surface Temperature ($^\circ$F)',fontsize=15 )

        #set tick lavel for x
        ax_f.set_xticks(y_pos)
        ax_f.set_xticklabels(decade)

        #freezing line
        ax_f.axhline(y=0)

        #Get the upper value for the range to make the reading easier
        ymin, ymax = ax_f.get_ylim()
        ax_f.set_ylim(ymin,math.ceil(ymax))

        plt.show()
        filename = os.path.join(out , '_'.join([metric,scen,'plot']) + '.pdf')
        plt.savefig( filename )
        plt.close()


 
