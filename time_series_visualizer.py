import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from decimal import Decimal
from datetime import datetime

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

sns.set_theme()


#I referenced this for setting plt axes: https://www.geeksforgeeks.org/multi-plot-grid-in-seaborn/

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'], yearfirst=True)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

df.index=df['date'].copy().rename('index')
df.rename(columns={'value':'views'})
df.drop(columns='date', inplace=True)
df.rename(columns={'value': 'views'},inplace=True)
df['views'] = df['views'].astype('int')


def draw_line_plot():
    # Draw line plot

    fig = plt.subplots(1, figsize = (10,5))
    sns.lineplot(data=df, x=df.index, y='views', sort=True, legend='auto', ax=fig[1])
    fig[1].set_xlabel('Date')
    fig[1].set_ylabel('Page Views')
    fig[1].set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig[0].savefig('line_plot.png')
    return fig[0]

# Referenced this for grouped barcharts using pyplot: https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
def draw_bar_plot():
    # Copy and modify data for monthly bar plot

    df_bar=df.copy()
    df_bar['year'] = [d.year for d in df_bar.index]
    df_bar['month_no'] = [d.month for d in df_bar.index]    
    df_bar['month'] = [d.strftime('%B') for d in df_bar.index]
    df_bar['month_short'] = [d.strftime('%b') for d in df_bar.index]
    df_bar.sort_values(by='month_no', inplace=True)
    df_bar.reset_index(inplace=True)
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=df_bar['month'].unique(), ordered=True)
    df_sums = df_bar.loc[:, 'views':].groupby(['month','year']).sum()

    years=df_bar['year'].sort_values().unique() #label locations
    x=np.arange(len(years))
    width=.03 # width of bars
    multiplier = 0
    df_views = np.reshape([int(n) for n in df_sums['views'].tolist()], (12,4))

    #Creating data dictionary for grouped bar chart
    df_dict = {}

    for i, mth in enumerate(df_bar['month'].unique()):
        df_dict[mth] = df_views[i]


    fig, ax = plt.subplots(figsize = (14,8))
            
    for mth, views in df_dict.items():
        offset = width*multiplier
        rects = ax.bar(x+offset, views, width, label='')
        multiplier += 1
        
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_xticks(x + width, years)
    ax.legend(df_bar['month'].unique(),loc='upper left', title='Months')
    
    return fig


    
def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box['year'] = [d.year for d in df_box.index]
    df_box['month_no'] = [d.month for d in df_box.index]    
    df_box.sort_values(by='month_no', inplace=True)
    df_box['month'] = [d.strftime('%B') for d in df_box.index]
    df_box['month_short'] = [d.strftime('%b') for d in df_box.index]

    # Draw box plots (using Seaborn)
    fig = plt.subplots(1, 2, figsize = (12,8), squeeze=True)
    sns.boxplot(data=df_box, x='year', y='views', ax=fig[1][0])
    sns.boxplot(data=df_box, x='month_short', y='views', ax=fig[1][1])


    fig[1][0].set_title('Year-wise Box Plot (Trend)')
    fig[1][0].set_xlabel('Year')
    fig[1][1].set_title('Month-wise Box Plot (Seasonality)')
    fig[1][1].set_xlabel('Month')

    for ax in fig[1]:
        ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig[0].savefig('box_plot.png')
    return fig[0]
