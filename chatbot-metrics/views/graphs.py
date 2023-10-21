from src.plots import plot_timeseries, plot_wordcloud
import streamlit as st

# Graphs
def GraphsView(data):
    '''
    GraphsView is a Streamlit application for displaying various time series and word cloud graphs.

    Args:
        data (dict): A dictionary containing data for plotting.

    This function creates a Streamlit application to display multiple time series graphs (e.g., Messages, Tickets, Sessions, Tickets per session, Average messages per session) and word cloud graphs (e.g., Keywords, AI Topics) based on the provided data.

    Parameters:
        - data (dict): A dictionary containing data for plotting, including keys "messages," "tickets," "sessions," "ticketsp," "avg_messages," "keywords," and "topics."

    Returns:
        None
    '''

    fig_messages = plot_timeseries(data["messages"], "Messages", "messages")
    fig_tickets = plot_timeseries(data["tickets"], "Tickets", "tickets")
    fig_sessions = plot_timeseries(data["sessions"], "Sessions", "sessions")
    # fig_ticketsp = plot_timeseries(data["ticketsp"], "Tickets per session", "ticketsp")
    # fig_avg_messages = plot_timeseries(data["avg_messages"], "Average messages per session", "avg_messages")
    fig_keywords = plot_wordcloud(data["keywords"], "Keywords")
    fig_topics = plot_wordcloud(data["topics"], "AI Topics")
    
    
    left,center,right=st.columns(3)
    left.plotly_chart(fig_messages,use_container_width=True)
    right.plotly_chart(fig_tickets,use_container_width=True)
    center.plotly_chart(fig_sessions,use_container_width=True)
    
    top1,top2 = st.columns(2)
    top1.pyplot(fig_keywords,use_container_width=True)
    top2.pyplot(fig_topics,use_container_width=True)
    bottom1,bottom2=st.columns(2)
    # bottom1.plotly_chart(fig_ticketsp,use_container_width=True)
    # bottom2.plotly_chart(fig_avg_messages,use_container_width=True)