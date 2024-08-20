import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', header=0, parse_dates=['date'])

# Clean data
df = df[
    (df['value'] > df['value'].quantile(0.025)) &
    (df['value'] < df['value'].quantile(0.975))
]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.lineplot(x='date', y='value', data=df, ax=ax)

    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.strftime('%B')
    df['month_num'] = df['date'].dt.month
    
    df_bar = df.groupby(['year', 'month', 'month_num'])['value'].mean().reset_index()
    df_bar = df_bar.sort_values(by=['year', 'month_num'])
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.barplot(x='year', y='value', hue='month', data=df_bar, ax=ax)
    
    for container in ax.containers:
        for bar in container:
            bar.set_edgecolor('black')  # Add edge color
            bar.set_linewidth(0.5)  # Set the width of the edge lines
    
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    plt.legend(title='Months', loc='upper left')


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])

    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_ylim(0, 200000)
    
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=month_order)
    
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_ylim(0, 200000)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
