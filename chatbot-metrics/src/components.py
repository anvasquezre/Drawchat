import streamlit as st
from datetime import datetime, timedelta

# Date Input as Calendar
def calendar():
    #switcher
    today = datetime.now()
    month_ago = today - timedelta(days=1)
    start_date = st.sidebar.date_input("Start date", month_ago)
    end_date = st.sidebar.date_input("End date", today)
    start_date = datetime(start_date.year, start_date.month, start_date.day)
    end_date = datetime(end_date.year, end_date.month, end_date.day)+timedelta(days=1)
    return start_date, end_date


# Date Input as Predefined Dropdown
def predefined_time():
    today = datetime.now()
    time_input = st.sidebar.selectbox(
        "Select Time Input",
        options=["Last 24 Hours","Last 7 days", "Last 30 days", "Last 90 days", "Last 180 days", "Last 365 days"],
        index=0,
    )
    if time_input == "Last 7 days":
        start_date = today - timedelta(days=7)
        end_date = today + timedelta(days=1)
    elif time_input == "Last 30 days":
        start_date = today - timedelta(days=30)
        end_date = today+ timedelta(days=1)
    elif time_input == "Last 90 days":
        start_date = today - timedelta(days=90)
        end_date = today + + timedelta(days=1)
    elif time_input == "Last 180 days":
        start_date = today - timedelta(days=180)
        end_date = today+ timedelta(days=1)
    elif time_input == "Last 365 days":
        start_date = today - timedelta(days=365)
        end_date = today+ timedelta(days=1)
    elif time_input == "Last 24 Hours":
        start_date = today - timedelta(days=1)
        end_date = today+ timedelta(days=1)
    return start_date, end_date
