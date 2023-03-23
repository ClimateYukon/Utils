import sys
import os
import warnings
from pathlib import Path
import ipywidgets as widgets
import calendar
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import cartopy.crs as ccrs
from coreapi import Client
import coreapi.auth as auth

warnings.filterwarnings("ignore")
if sys.platform == 'linux':
    path = Path("/mnt/CC/Climate_data/")
else:
    path = Path("//cargo/Store/CC/Climate_data")
os.chdir(path)

sys.path.insert(1, str(path / "Code"))

# Local code imports
import Julien_utils as Ju
import Julien_load as Jl

# Set font style
from matplotlib import rcParams

rcParams['font.family'] = 'Nunito Sans'

AHCCD = pd.read_csv('https://raw.githubusercontent.com/ClimateMess/data/main/ahccd.csv', index_col='time', parse_dates=True)


def isnumber(x):
    try:
        float(x)
        return True
    except:
        return False


token = '00'
auth = auth.TokenAuthentication(scheme='Token', token=token)
client = Client(auth=auth)
doc1 = client.get('https://weather.service.yukon.ca/api/v1/docs/')

data = client.action(doc1, ['weather', 'read'], params={
    'station_id': '99',
    'parameter_ids': '47,22',
    'timezone': 'America/Whitehorse',
    'b': '2020-01-01',
    'e': '2023-11-25'
})

data_list = [x.split(',') for x in data.split('\r\n') if len(x) > 0]
rwis = pd.DataFrame(data_list[1:], columns=data_list[0])
rwis = rwis[rwis['TA'].apply(isnumber)]
rwis['TA'] = rwis['TA'].astype('float')
rwis['date'] = pd.to_datetime(rwis['date'].astype(str) + '-' + rwis['time'], format='%Y-%m-%d-%H:%M')
rwis.index = rwis.date

month = [calendar.month_name[i] for i in range(1, 13)] + ['Yearly']
layout = widgets.Layout(width='50%', height='40px')
summary_selector = widgets.Dropdown(options=month, value=month[0], description='Select a month to summarize by or the Yearly option', style=dict(description_width='initial'), layout=layout)

def draw_countplot(column):
    today = datetime.today()
    year, month = (today.year, list(calendar.month_name).index(column)) if column != 'Yearly' and list(calendar.month_name).index(column) <= today.month else (today.year - 1, list(calendar.month_name).index(column))

    # Create a new figure with a specified size
    fig, ax = plt.subplots(figsize=(16, 9))

    # Extract data for the current year and selected month from the RWIS dataset
    this_year = rwis[(rwis.index.year == year) & (rwis.index.month == month)]['TA']

    # Extract data for the selected month from the AHCCD dataset
    AHCCD_month = AHCCD[AHCCD.index.month ==month]

    # Calculate and plot the historical average temperature for each variable
    df_years = AHCCD_month.loc[(AHCCD_month.index.year >= 1950) & (AHCCD_month.index.year <= 2000)]

    tasmax_norm, tasmin_norm, tas_norm = df_years[['tasmax', 'tasmin', 'tas']].mean()
    for color, line in zip(['red', 'blue', 'black'], [tasmax_norm, tasmin_norm, tas_norm]):
        ax.axhline(line, linewidth=1, linestyle=(0, (3, 10, 1, 10, 1, 10)), color=color, alpha=1)


    # # Plot daily statistics for historical temperatures and record temperatures
    # daily_stats = AHCCD_month.groupby(AHCCD_month.index.day).agg({'tasmin': 'min', 'tasmax': 'max', 'tas': 'mean'})
    # daily_stats['record_min'] = AHCCD_month.groupby(AHCCD_month.index.day)['tasmin'].min()
    # daily_stats['record_max'] = AHCCD_month.groupby(AHCCD_month.index.day)['tasmax'].max()
    # daily_stats[['tasmin', 'tasmax', 'tas']].plot(ax=ax, linewidth=0.5, linestyle='--')
    # ax.scatter(x=daily_stats.index, y=daily_stats['record_min'], color='blue', s=4)
    # ax.scatter(x=daily_stats.index, y=daily_stats['record_max'], color='red', s=4)

    #full time series max min and mean
    full_med = AHCCD_month['tas'].groupby([AHCCD_month.index.day]).mean()
    full_min = AHCCD_month['tas'].groupby([AHCCD_month.index.day]).min()
    full_max = AHCCD_month['tas'].groupby([AHCCD_month.index.day]).max()

    #records
    full_record_min = AHCCD_month['tasmin'].groupby([AHCCD_month.index.day]).min()
    full_record_max = AHCCD_month['tasmax'].groupby([AHCCD_month.index.day]).max()


    AHCCD_month['tas'].groupby([AHCCD_month.index.day,AHCCD_month.index.year]).mean().unstack().plot(ax=ax,color='black', linewidth = 0.5,alpha=0.05,title = '{} Temperatures in Whitehorse based on AHCCD (historical) and RWIS (current year)'.format(calendar.month_name[month]))


    full_med.plot(ax=ax,linewidth= 0.5, linestyle='--',color='black')
    full_min.plot(ax=ax,linewidth= 0.5, linestyle='--',color='blue')
    full_max.plot(ax=ax,linewidth= 0.5, linestyle='--',color='red')
    ax.scatter(x=full_record_min.index ,y=full_record_min.values ,color='blue',s=4)
    ax.scatter(x=full_record_max.index,y=full_record_max.values,color='red',s=4)

    this_year.groupby([this_year.index.day]).mean().plot(ax=ax,linewidth= 1, linestyle='-',color='orange')
    this_year.groupby([this_year.index.day]).min().plot(ax=ax,linewidth= 1, linestyle='dotted',color='orange')
    this_year.groupby([this_year.index.day]).max().plot(ax=ax,linewidth= 1, linestyle='dotted',color='orange')
    ax.fill_between(this_year.groupby([this_year.index.day]).min().index,this_year.groupby([this_year.index.day]).min().values,  this_year.groupby([this_year.index.day]).max().values,color='#b7b7b7',alpha=0.2)
    plt.ylim(full_record_min.min() - 5 ,full_record_max.max() +5 )
    plt.xlim(0.5,len(full_med.index)+0.5)

    handles = [    mlines.Line2D([], [], linewidth= 1, color='orange', label='T-Mean {} {} '.format(calendar.month_name[month],year)),
    mpatches.Patch(color='#b7b7b7', alpha=0.2, label='T-Max, T-Mean, T-Min, Daily range'),    mlines.Line2D([], [], linewidth=1, linestyle='--', alpha=0.5, color='black', label='Daily Historical T-Mean'),
    mlines.Line2D([], [], linewidth=1, linestyle='--', alpha=0.5, color='red', label='Highest Historical Daily T-Mean'),
    mlines.Line2D([], [], linewidth=1, linestyle='--', alpha=0.5, color='blue', label='Lowest Historical Daily T-Mean'),
    mlines.Line2D([], [], linewidth=1, linestyle=(0, (3, 10, 1, 10, 1, 10)), color='black', alpha=1, label='1950 - 2000 Daily average'),
    mlines.Line2D([], [], linewidth=1, linestyle=(0, (3, 10, 1, 10, 1, 10)), color='red', alpha=1, label='1950 - 2000 Mean Daily T-Max'),
    mlines.Line2D([], [], linewidth=1, linestyle=(0, (3, 10, 1, 10, 1, 10)), color='blue', alpha=1, label='1950 - 2000 Mean Daily T-Min'),
    mlines.Line2D([], [], color='black', linewidth=0.5, alpha=0.1, label='All years'),
    mlines.Line2D([0], [0], marker='o', color='w', label='Record High', markerfacecolor='red', markersize=4),
    mlines.Line2D([0], [0], marker='o', color='w', label='Record Low', markerfacecolor='blue', markersize=4)
    ]
    plt.legend(handles=handles, bbox_to_anchor=(1.04, 1), loc='upper left', ncol=1, fancybox=True, framealpha=0.9)

    diff = round(this_year.mean() - tas_norm,2)
    ax.text(len(full_med.index),full_record_min.min() - 4.5,'Difference to normal : {}'.format(diff), ha='right')
    ax.text(1,full_record_min.min() - 4.5,'Warning : This plot assumes that differences between AHCCD and raw weather records are insignificant.'.format(diff), ha='left')
    plt.ylabel( 'Temperatures (°C)', fontsize=12 )
    plt.xlabel( 'Days of the month', fontsize=12 )
    ax.spines[['right', 'top']].set_visible(True)
    ax.set_xticks([1,5,10,15,20,25,30])
    plt.savefig('/mnt/CC/Climate_data/tmp/{}_todate.png'.format(calendar.month_name[month]),dpi=300, bbox_inches='tight')

a = interact_manual(draw_countplot,column=summary_selector)
