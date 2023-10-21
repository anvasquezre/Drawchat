

from core.settings import settings
from pymongo import MongoClient
import pandas as pd
from fastapi import HTTPException
from wordcloud import WordCloud, STOPWORDS
import json

async def daily_messages_estimation(client: MongoClient):
    """
    Estimate daily message counts from USER messages.

    This asynchronous function calculates and returns the daily message counts
    from messages of type "USER" in the database.

    Args:
        - client (MongoClient): The MongoDB client obtained from the dependency
          `get_client`.

    Returns:
        - str: JSON representation of daily message counts.

    Raises:
        - HTTPException 404: If there are no messages found for estimation,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with estimating the metrics,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        await daily_messages_estimation(client)
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_MESSAGES]
        try:
            messages_cursor = collection.find(
                {"message_type" : "USER"},
                {
                    "created_at":-1,
                    "message_id":1,
                    "_id":False,
                },
                session=session).limit(0)
            
            messages = list(messages_cursor)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if not messages:
                raise HTTPException(status_code=404, detail="Error estimating metrics")
            
            df = pd.DataFrame(messages)
            result = df.resample(
                "1h",
                on="created_at",
                closed="left",
                axis=0,
                kind="timestamp",
                ).agg({"message_id":"count"})
            result.reset_index(inplace=True, drop=False)
            result.rename(columns={"created_at":"date","message_id":"daily_messages"}, inplace=True)
            result = result.to_json(orient="records")
            return result


async def daily_sessions_estimation(client: MongoClient):
    """
    Estimate daily session counts.

    This asynchronous function calculates and returns the daily session counts
    from sessions in the database.

    Args:
        - client (MongoClient): The MongoDB client obtained from the dependency
          `get_client`.

    Returns:
        - str: JSON representation of daily session counts.

    Raises:
        - HTTPException 404: If there are no sessions found for estimation,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with estimating the metrics,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        await daily_sessions_estimation(client)
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_SESSIONS]
        try:
            sessions_cursor = collection.find(
                projection={
                    "created_at":-1,
                    "session_id":1,
                    "_id":False,
                },
                session=session).limit(0)
            
            sessions = list(sessions_cursor)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if not sessions:
                raise HTTPException(status_code=404, detail="Error estimating metrics")

            df = pd.DataFrame(sessions)
            result = df.resample(
                "1h",
                on="created_at",
                closed="left",
                axis=0,
                kind="timestamp",
                ).agg({"session_id":"count"})
            result.reset_index(inplace=True, drop=False)
            result.rename(columns={"created_at":"date","session_id":"daily_sessions"}, inplace=True)
            print(result)
            result = result.to_json(orient="records")
            return result

async def daily_tickets_estimation(client : MongoClient):
    """
    Estimate daily ticket counts.

    This asynchronous function calculates and returns the daily ticket counts
    from tickets in the database.

    Args:
        - client (MongoClient): The MongoDB client obtained from the dependency
          `get_client`.

    Returns:
        - str: JSON representation of daily ticket counts.

    Raises:
        - HTTPException 404: If there are no tickets found for estimation,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with estimating the metrics,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        await daily_tickets_estimation(client)
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_TICKETS]
        try:
            ticket_cursor = collection.find(
                projection={
                    "created_at":-1,
                    "ticket_id":1,
                    "_id":False,
                },
                session=session).limit(0)
            
            tickets = list(ticket_cursor)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if not tickets:
                raise HTTPException(status_code=404, detail="Error estimating metrics")

            df = pd.DataFrame(tickets)
            result = df.resample(
                "1h",
                on="created_at",
                closed="left",
                axis=0,
                kind="timestamp",
                ).agg({"ticket_id":"count"})
            result.reset_index(inplace=True, drop=False)
            result.rename(columns={"created_at":"date","ticket_id":"daily_tickets"}, inplace=True)
            print(result)
            result = result.to_json(orient="records")
            return result


async def daily_ticketsp_estimation(client: MongoClient):
    """
    Estimate daily tickets per session.

    This asynchronous function calculates and returns the daily tickets per session
    from tickets and sessions in the database.

    Args:
        - client (MongoClient): The MongoDB client obtained from the dependency
          `get_client`.

    Returns:
        - str: JSON representation of daily tickets per session.

    Raises:
        - HTTPException 404: If there are no tickets or sessions found for estimation,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with estimating the metrics,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        await daily_ticketsp_estimation(client)
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        tickets_collection = db[settings.db.MONGO_CHATLOG_COLLECTION_TICKETS]
        sessions_collection = db[settings.db.MONGO_CHATLOG_COLLECTION_SESSIONS]
        try:
            ticket_cursor = tickets_collection.find(
                projection={
                    "created_at":-1,
                    "ticket_id":1,
                    "_id":False,
                },
                session=session).limit(0)
            
            tickets = list(ticket_cursor)

            sessions_cursor = sessions_collection.find(
                projection={
                    "created_at":-1,
                    "session_id":1,
                    "_id":False,
                },
                session=session).limit(0)
            sessions = list(sessions_cursor)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if not tickets or not sessions:
                raise HTTPException(status_code=404, detail="Error estimating metrics")

            df_tickets = pd.DataFrame(tickets).resample(
                "1h",
                on="created_at",
                closed="left",
                axis=0,
                kind="timestamp",
                ).agg({"ticket_id":"count"})
            df_tickets.reset_index(inplace=True, drop=False)
            df_tickets.rename(columns={"created_at":"date","ticket_id":"daily_tickets"}, inplace=True)
            
            df_sessions = pd.DataFrame(sessions).resample(
                "1h",
                on="created_at",
                closed="left",
                axis=0,
                kind="timestamp",
                ).agg({"session_id":"count"})
            df_sessions.reset_index(inplace=True, drop=False)
            df_sessions.rename(columns={"created_at":"date","session_id":"daily_sessions"}, inplace=True)
            
            df_merged = pd.merge(df_tickets, df_sessions, on="date", how="inner")
            df_merged["daily_ticketsp"] = df_merged.apply(lambda x: x.daily_tickets/x.daily_sessions if x.daily_sessions != 0 else 0, axis=1)
            result = df_merged[["date","daily_ticketsp"]].to_json(orient="records")
            return result

async def daily_avg_messages_estimation(client: MongoClient):
    """
    Estimate daily average messages per session.

    This asynchronous function calculates and returns the daily average messages
    per session from messages and sessions in the database.

    Args:
        - client (MongoClient): The MongoDB client obtained from the dependency
          `get_client`.

    Returns:
        - str: JSON representation of daily average messages per session.

    Raises:
        - HTTPException 404: If there are no messages or sessions found for estimation,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with estimating the metrics,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        await daily_avg_messages_estimation(client)
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        messages_collection = db[settings.db.MONGO_CHATLOG_COLLECTION_MESSAGES]
        sessions_collection = db[settings.db.MONGO_CHATLOG_COLLECTION_SESSIONS]
        try:
            message_cursor = messages_collection.find(
                {"message_type" : "USER"},
                projection={
                    "created_at":-1,
                    "message_id":1,
                    "_id":False,
                },
                session=session).limit(0)
            
            messages = list(message_cursor)

            sessions_cursor = sessions_collection.find(
                projection={
                    "created_at":-1,
                    "session_id":1,
                    "_id":False,
                },
                session=session).limit(0)
            sessions = list(sessions_cursor)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if not messages or not sessions:
                raise HTTPException(status_code=404, detail="Error estimating metrics")

            df_messages = pd.DataFrame(messages).resample(
                "1h",
                on="created_at",
                closed="left",
                axis=0,
                kind="timestamp",
                ).agg({"message_id":"count"})
            df_messages.reset_index(inplace=True, drop=False)
            df_messages.rename(columns={"created_at":"date","message_id":"daily_messages"}, inplace=True)
            
            df_sessions = pd.DataFrame(sessions).resample(
                "1h",
                on="created_at",
                closed="left",
                axis=0,
                kind="timestamp",
                ).agg({"session_id":"count"})
            df_sessions.reset_index(inplace=True, drop=False)
            df_sessions.rename(columns={"created_at":"date","session_id":"daily_sessions"}, inplace=True)
            
            df_merged = pd.merge(df_messages, df_sessions, on="date", how="inner")
            df_merged["avg_messages"] = df_merged.apply(lambda x: x.daily_messages/x.daily_sessions if x.daily_sessions != 0 else 0, axis=1)
            result = df_merged[["date","avg_messages"]].to_json(orient="records")
            return result

async def keywords_estimation(client: MongoClient):
    """
    Estimate keywords from user messages.

    This asynchronous function calculates and returns a JSON representation of keywords
    found in user messages in the database.

    Args:
        - client (MongoClient): The MongoDB client obtained from the dependency
          `get_client`.

    Returns:
        - str: JSON representation of keywords.

    Raises:
        - HTTPException 404: If there are no user messages found for keyword estimation,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with estimating the metrics,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        await keywords_estimation(client)
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_MESSAGES]
        try:
            messages_cursor = collection.find(
                {"message_type" : "USER"},
                {
                    "created_at":-1,
                    "message_id":1,
                    "exchange" : 1,
                    "_id":False,
                },
                session=session).limit(0)
            
            messages = list(messages_cursor)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if not messages:
                raise HTTPException(status_code=404, detail="Error estimating metrics")
            
            text = ' '.join([message["exchange"] for message in messages])
            stopwords = set(STOPWORDS)
            stopwords.update(["https", "http", "com", "www"])
            wc = WordCloud(stopwords=stopwords, background_color="white").generate(text)
            
    return json.dumps(wc.words_)

async def topics_estimation(client: MongoClient):
    """
    Estimate topics from AI messages.

    This asynchronous function calculates and returns a JSON representation of topics
    found in AI messages in the database.

    Args:
        - client (MongoClient): The MongoDB client obtained from the dependency
          `get_client`.

    Returns:
        - str: JSON representation of topics.

    Raises:
        - HTTPException 404: If there are no AI messages found for topic estimation,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with estimating the metrics,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        await topics_estimation(client)
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_MESSAGES]
        try:
            messages_cursor = collection.find(
                {"message_type" : "AI"},
                {
                    "created_at":-1,
                    "message_id":1,
                    "exchange" : 1,
                    "_id":False,
                },
                session=session).limit(0)
            
            messages = list(messages_cursor)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if not messages:
                raise HTTPException(status_code=404, detail="Error estimating metrics")
            
            text = ' '.join([message["exchange"] for message in messages])
            stopwords = set(STOPWORDS)
            stopwords.update(["https", "http", "com", "www"])
            wc = WordCloud(stopwords=stopwords, background_color="white").generate(text)
            
    return json.dumps(wc.words_)


FUNC_MAPPING = {
    settings.metrics.MONGO_MESSAGES_TYPE: daily_messages_estimation,
    settings.metrics.MONGO_SESSIONS_TYPE: daily_sessions_estimation,
    settings.metrics.MONGO_TICKETS_TYPE: daily_tickets_estimation,
    settings.metrics.MONGO_TICKETSP_TYPE: daily_ticketsp_estimation,
    settings.metrics.MONGO_AVG_MESSAGES_TYPE: daily_avg_messages_estimation,
    settings.metrics.MONGO_KEYWORDS_TYPE: keywords_estimation,
    settings.metrics.MONGO_TOPICS_TYPE: topics_estimation,
}

