import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import calendar
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col=0, parse_dates=['date'])

# Clean data
df = df.loc[
    (df['value'] >= df['value'].quantile(0.025)) & 
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    plt.figure(figsize=(22, 6))
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Page Views', fontsize=12)
    plt.plot(df, color='blue', linewidth=2)
    fig = plt.gcf()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df.index.year.astype(str)
    df_bar['month'] = [date.strftime('%B') for date in df.index]
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=calendar.month_name[1:], ordered=True)

    # Draw bar plot
    df_bar = df_bar.groupby(['year', 'month'], sort=False, as_index=False).mean()
    df_bar = df_bar.pivot(index='year', columns='month', values='value')
    df_bar.plot(kind='bar', figsize=(10, 6))
    plt.xlabel('Years', fontsize=12)
    plt.ylabel('Average Page Views', fontsize=12)
    fig = plt.gcf()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

    sns.boxplot(x='year', y='value', hue='year', legend=False, data=df_box, ax=axes[0], palette='Set2')
    axes[0].set_title('Year-wise Box Plot (Trend)', fontsize=16)
    axes[0].set_xlabel('Year', fontsize=12)
    axes[0].set_ylabel('Page Views', fontsize=12)

    month_order = [calendar.month_abbr[i] for i in range(1, 13)]
    sns.boxplot(x='month', y='value', hue='month', legend=False, data=df_box, ax=axes[1], palette='Set2', order=month_order)
    axes[1].set_title('Month-wise Box Plot (Seasonality)', fontsize=16)
    axes[1].set_xlabel('Month', fontsize=12)
    axes[1].set_ylabel('Page Views', fontsize=12)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
