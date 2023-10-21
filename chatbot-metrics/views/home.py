
import streamlit as st
import pandas as pd
from src.utils import get_data_by_date, get_data_by_sampling
from src.settings import METRICS_MAPPING


# Home Page
def HomeView(data,start_date,end_date,sammpling_freq):
    '''
    HomeView is a Streamlit application for displaying data, analytics, and providing data download options.

    Args:
        data (pandas.DataFrame): The input data to be displayed and analyzed.
        start_date (str): The start date for filtering the data.
        end_date (str): The end date for filtering the data.
        sammpling_freq (str): The sampling frequency for data.

    This function creates a Streamlit application to display data based on specified date ranges and sampling frequency. It allows users to select a metric to display, download data as a CSV file, and provides summary analytics such as total messages, total sessions, total tickets, average tickets per session, and average messages per session.

    Parameters:
        - data (pandas.DataFrame): The input data to be displayed and analyzed.
        - start_date (str): The start date for filtering the data.
        - end_date (str): The end date for filtering the data.
        - sammpling_freq (str): The sampling frequency for data.

    Returns:
        pandas.DataFrame: The filtered and sampled data.
    '''
    data = get_data_by_date(data, start_date, end_date)
    data = get_data_by_sampling(data, sammpling_freq)
    with st.expander("⏰ CSV Data WorkBook"):
        showData=st.selectbox('Metric Data: ',options=METRICS_MAPPING.keys(),index=0)
        df = data[METRICS_MAPPING[showData]]
        st.dataframe(df,use_container_width=True)
        
        @st.cache_data
        def convert_df(df):
            if isinstance(df,dict):
                df = pd.DataFrame.from_dict(df, orient='index')
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)

        
        col1,col2,col3=st.columns(3)
        
        col2.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'{METRICS_MAPPING[showData]}.csv',
            mime='text/csv',
)
        
        
    #compute top analytics
    total_messages = float(data["messages"]["messages_count"].sum())
    total_sessions = float(data["sessions"]["sessions_count"].sum())
    total_tickets = float(data["tickets"]["tickets_count"].sum())
    avg_total_ticketsp = float(total_tickets/total_sessions)*100 if total_sessions else 0
    avg_messages = float(total_messages/total_sessions) if total_sessions else 0


    total1,total2,total3,total4,total5=st.columns(5,gap='large')
    with total1:
        st.info('Total Interactions',icon="📌")
        st.metric(label="Sum of Given Period",value=f"{total_messages:,.0f}")
    with total2:
        st.info('Total Sessions',icon="📌")
        st.metric(label="Sum of Given Period",value=f"{total_sessions:,.0f}")
    with total3:
        st.info("Average Interactions per Session",icon="📌")
        st.metric(label="Average of Given Period",value=f"{avg_messages:,.0f}")
    with total4:
        st.info('Total Tickets',icon="📌")
        st.metric(label="Sum of Given Period",value=f"{total_tickets:,.0f}")
    with total5:
        st.info('Ticket Creation Rate',icon="📌")
        st.metric(label="Average of Given Period",value=f"{avg_total_ticketsp:,.0f}%")

        

    st.markdown("""---""")

    return data