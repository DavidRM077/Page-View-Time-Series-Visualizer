import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")

# Clean data
df = df[
    (df["value"] >= df['value'].quantile(0.025))& 
    (df["value"] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot

    df["date"] = pd.to_datetime(df["date"])
    #df.index = pd.to_datetime(df.index)

    df.set_index('date', inplace=True)

    fig = plt.figure(figsize=(12,6))
    plt.plot(df["value"], color="red",linewidth = 1)
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.ylabel("page views")
    plt.xlabel("date")
    

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df["year"] = df.index.year
    df["month"] = df.index.month_name()

    df["month"] = pd.Categorical(
    df['month'],
    categories=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ],
    ordered=True
)
    agrupados = df.groupby(["year","month"], observed= False).mean()
    agrupados = agrupados.reset_index()  
   

    # Copy and modify data for monthly bar plot
    df_bar = agrupados.pivot(index = "year",columns="month", values="value")

    # Draw bar plot

    fig , ax = plt.subplots(figsize=(12,6))
    df_bar.plot(kind="bar", ax = ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title = 'Months')



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

    fig , axes = plt.subplots(nrows=1, ncols=2 ,figsize = (20,6))

    axes[0] = sns.boxplot(x = 'year' , y = 'value', data= df_box , ax=axes[0] , palette= 'Set2')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    axes[1] = sns.boxplot(x = 'month' , y = 'value', data= df_box , ax=axes[1], palette= 'Set2',)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    plt.tight_layout()
    

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
