import streamlit as st
from src.chatlog import Chatlog
from src.plots import plot_pie

    
# Feedback
def FeedbackView(data):
    '''
    FeedbackView is a Streamlit application for displaying feedback data.

    Args:
        data (pandas.DataFrame): A DataFrame containing feedback data.

    This function creates a Streamlit application to display feedback data, including the total number of feedbacks, counts of positive, negative, and neutral feedbacks, and a table with the feedback data. It also provides a download button to export the data as a CSV file and allows filtering by session ID to view chat history associated with specific feedback.

    Parameters:
        - data (pandas.DataFrame): A DataFrame containing feedback data.

    Returns:
        None
    '''
    if  len(data) == 0:
        st.warning("No Feedback Found for the given date range")
        return
    fig_pie = plot_pie(data=data,values="count",labels="feedback",title="Feedbacks")
    st.plotly_chart(fig_pie,use_container_width=True)
    total_feedbacks = len(data)
    counts = data["feedback"].value_counts()
    if "positive" not in counts:
        counts["positive"] = 0
    if "negative" not in counts:
        counts["negative"] = 0
    if "neutral" not in counts:
        counts["neutral"] = 0
    positive_feedbacks = counts["positive"]
    negative_feedbacks = counts["negative"]
    neutral_feedbacks = counts["neutral"]
    total1,total2,total3,total4=st.columns(4,gap='large')
    with total1:
        st.info('Total Feedbacks',icon="📌")
        st.metric(label="Total Feedbacks",value=f"{total_feedbacks:,.0f}")
    with total2:
        st.info('Positive Feedbacks',icon="📌")
        st.metric(label="Positive Feedbacks",value=f"{positive_feedbacks:,.0f}")
    with total3:
        st.info('Negative Feedbacks',icon="📌")
        st.metric(label="Negative Feedbacks",value=f"{negative_feedbacks:,.0f}")
    with total4:
        st.info('Neutral Feedbacks',icon="📌")
        st.metric(label="Neutral Feedbacks",value=f"{neutral_feedbacks:,.0f}")

    df = data
    st.dataframe(df,use_container_width=True)
    
    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)
    col1,col2,col3=st.columns(3)
    col2.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'feedback.csv',
        mime='text/csv',
        )
    st.markdown("""--- See chats by session id ---""")
    data_filtered = st.text_input("Filter by Session ID")
    
    if data_filtered:
        session_id = data_filtered
        chat = Chatlog.from_session_id(session_id)
        chat_history = chat._chats
        
        st.markdown("""---""")
        if not chat_history:
            st.warning("No Chat History Found")
            return
        for chat_msg in chat_history:
            
            message = st.chat_message(chat_msg['message_type'])
            message.write(chat_msg['exchange'])