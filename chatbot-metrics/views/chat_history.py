from requests import session
import streamlit as st
from src.chatlog import Chatlog

# Chatlog   
def ChatlogView(data:list):
    '''
    ChatlogView is a Streamlit application for viewing chat logs.

    Args:
        data (list): A list of session IDs to choose from.

    This function creates a Streamlit application for viewing chat logs. It allows you to select a session ID from the provided list, filter by session ID, and displays chat log information, including session details and chat messages.

    Parameters:
        - data (list): A list of session IDs to populate the select box options.

    Returns:
        None
    '''
    col1,col2=st.columns((0.2,0.8))
    
    with col1:
        st.markdown("""--- or filter by session id ---""")
        data_filtered = st.text_input("Filter by Session ID")
        if not data:
            st.warning("No Session ID Found for the given date range")
        else:
            st.info("Select a Session ID")
            
            session_id = st.radio("",data)
            
            if data_filtered:
                session_id = data_filtered

    with col2:
        if session_id:
            chat = Chatlog.from_session_id(session_id)
            chat_history = chat._chats
            total1,total2,total3,total4,total5=st.columns(5,gap='large')
            with total1:
                st.info('Session ID',icon="📌")
                st.metric(label="Session ID",value=f"{chat._session_id}")
            with total2:
                st.info('Start Time',icon="📌")
                st.metric(label="Start Time",value=f"{chat._session_data['created_at']}")
            with total3:
                st.info('End Time',icon="📌")
                st.metric(label="End Time",value=f"{chat._session_data['ended_at']}")
            with total4:
                st.info('Email',icon="📌")
                st.metric(label="Email",value=f"{chat._session_data['user_email']}")
            with total5:
                st.info('Name',icon="📌")
                st.metric(label="Name",value=f"{chat._session_data['user_name']}")
            
            
            st.markdown("""---""")
            if not chat_history:
                st.warning("No Chat History Found")
                return
            for chat_msg in chat_history:
                
                message = st.chat_message(chat_msg['message_type'])
                message.write(chat_msg['exchange'])