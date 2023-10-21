
from src.settings import settings
import requests
from typing import List
import pandas as pd

class Chatlog():
    """
    Chatlog Class for Managing Chat Session Data.

    This class represents a chatlog containing chat messages and session data for a specific session.

    Args:
        - session_id (str): The unique identifier for the chat session.
        - chats (list[dict]): A list of chat messages, each represented as a dictionary.
        - session_data (dict): A dictionary containing session-related data.

    Example Usage:
        chatlog = Chatlog(session_id="12345", chats=[...], session_data={...})

    Attributes:
        - _session_id (str): The private attribute storing the session ID.
        - _chats (list[dict]): The private attribute storing chat messages.
        - _session_data (dict): The private attribute storing session-related data.

    Methods:
        - get_chatlogs(session_id: str) -> List[dict]: Retrieves chat messages for the specified session.
        - get_session_info(session_id: str) -> dict: Retrieves session information for the specified session.
        - from_session_id(cls, session_id: str) -> Chatlog: Creates a Chatlog instance from a session ID.

    Example Usage:
        chatlog = Chatlog(session_id="12345")
        chatlog.get_chatlogs("12345")
        chatlog.get_session_info("12345")
        chatlog = Chatlog.from_session_id("12345")
    """
    def __init__(self, session_id:str, chats:list[dict], session_data:dict):
        self._session_id = session_id
        self._chats = chats
        self._session_data = session_data
        
    def get_chatlogs(self,session_id:str) -> List[dict]:
        """
        Retrieve chat messages for the specified session.

        Args:
            session_id (str): The unique identifier for the chat session.

        Returns:
            List[dict]: A list of chat messages, each represented as a dictionary.
        """
        url = f"{settings.api.API_URI}/sessions/{session_id}/messages/"
        try:
            response = requests.get(url,headers={"Authorization":f"Bearer {settings.api.API_TOKEN}", "Content-Type": "application/json"})
            # check if response is ok
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
            df['created_at'] = pd.to_datetime(df['created_at'])
            df.sort_values(by=['created_at'], inplace=True, ascending=True)
            data = df.to_dict('records')
            self._chats = data
            return data
        except requests.HTTPError as e:
            print(e)
            return None

    def get_session_info(self,session_id:str):
        """
        Retrieve session information for the specified session.

        Args:
            session_id (str): The unique identifier for the chat session.

        Returns:
            dict: A dictionary containing session-related data.
        """
        url = f"{settings.api.API_URI}/sessions/{session_id}"
        try:
            response = requests.get(url,headers={"Authorization":f"Bearer {settings.api.API_TOKEN}", "Content-Type": "application/json"})
            # check if response is ok
            response.raise_for_status()
            data = response.json()
            self._session_data= data
            return data
        except requests.HTTPError as e:
            print(e)
            return None

    @classmethod
    def from_session_id(cls,session_id:str) -> "Chatlog":
        """
        Create a Chatlog instance from a session ID.

        Args:
            session_id (str): The unique identifier for the chat session.

        Returns:
            Chatlog: An instance of the Chatlog class.
        """
        chats = cls.get_chatlogs(cls,session_id=session_id)
        session_data = cls.get_session_info(cls,session_id=session_id)
        return cls(session_id=session_id,chats=chats,session_data=session_data)
