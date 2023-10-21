import streamlit as st
from streamlit_option_menu import option_menu
from src.utils import get_all_data, get_sessions, get_feedbacks
from src.settings import SAMPLING_MAPPING
from views import chat_history, graphs, feedback, home
from src.components import calendar, predefined_time
from src.cookies import get_manager, validate_token
from streamlit_javascript import st_javascript

from src.settings import settings
# Set page config
st.set_page_config(page_title="Chatbot Dashboard",page_icon="💻📱💻",layout="wide")

# Set title and center it
col1,col2,col3=st.columns(3)
col2.subheader("🔔 Analytics Dashboard 🔔")
st.markdown("##")

theme_plotly = "streamlit" # None or streamlit

cookie_manager = get_manager()


# Get all cookies

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

st.sidebar.image("resources/logo.png",caption="Developed and Maintaned by Tenant Evaluation")


with st.sidebar:

    selected=option_menu(
        menu_title="Main Menu",
        options=["Dashboard","Chatlogs","Feedback"],
        icons=["house","eye"],
        menu_icon="cast",
        default_index=0
    )

# Main Menu
if selected=="Dashboard":
    # Data
    data = get_all_data()
    st.subheader(f"Page: {selected}")
    date_input = st.sidebar.selectbox(
        "Select Date Input",
        options=["Calendar", "Predefined"],
        index=1,
    )
    if date_input == "Calendar":
        start_date, end_date = calendar()
    else:
        start_date, end_date = predefined_time()

    sammpling_freq=st.sidebar.selectbox(
        "Select Resampling Frequency",
        options=SAMPLING_MAPPING.keys(),
        index = 0,
    )
    data = home.HomeView(data,start_date=start_date, end_date=end_date, sammpling_freq=sammpling_freq)
    graphs.GraphsView(data)
if selected=="Chatlogs":
    
    st.subheader(f"Page: {selected}")
    date_input = st.sidebar.selectbox(
        "Select Date Input",
        options=["Calendar", "Predefined"],
        index=1,
    )
    if date_input == "Calendar":
        start_date, end_date = calendar()
    else:
        start_date, end_date = predefined_time()
    
    data = get_sessions(start_date,end_date)
    
    chat_history.ChatlogView(data)
    
if selected=="Feedback":
    st.subheader(f"Page: {selected}")
    date_input = st.sidebar.selectbox(
        "Select Date Input",
        options=["Calendar", "Predefined"],
        index=1,
    )
    if date_input == "Calendar":
        start_date, end_date = calendar()
    else:
        start_date, end_date = predefined_time()
        
    data = get_feedbacks(start_date,end_date)
    feedback.FeedbackView(data)



# #theme
# hide_st_style=""" 

# <style>
# #MainMenu {visibility:hidden;}
# footer {visibility:hidden;}
# header {visibility:hidden;}
# </style>
# """


