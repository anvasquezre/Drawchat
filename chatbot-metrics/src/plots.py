from typing import Dict
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

def plot_timeseries(df:DataFrame, metric_title: str, metric_name: str):
    """
    Plot a time series graph for a metric.

    Args:
        df (DataFrame): The DataFrame containing the data.
        metric_title (str): The title for the plot.
        metric_name (str): The name of the metric.

    Returns:
        go.Figure: The Plotly figure object.
    """
    df = df.reset_index(drop=False)
    df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')
    fig = px.line(
        df,
        x="date",
        y=f"{metric_name}_count",
        title=f"{metric_title}",
        template="plotly_white",
        markers=False,
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig.update_xaxes(tickangle=90)
    return fig


def plot_wordcloud(dict:Dict, metric_title: str):
    """
    Generate and plot a word cloud from a word frequency dictionary.

    Args:
        word_freq_dict (dict): The word frequency dictionary.
        metric_title (str): The title for the plot.

    Returns:
        plt.Figure: The matplotlib figure object containing the word cloud.
    """
    wc = WordCloud(background_color="white", width=800, height=400).generate_from_frequencies(dict)
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.imshow(wc)
    plt.axis("off")
    plt.title(f"{metric_title}", fontsize=20)
    return fig
    
    
def plot_pie(data:pd.DataFrame=None,labels=None,values=None,title=None):
    data = data["feedback"].value_counts().reset_index()
    print(data)
    fig = px.pie(data, values=values, names=labels, title=title, color=labels, color_discrete_map={'positive':'green','negative':'red','neutral':'yellow'})
    return fig