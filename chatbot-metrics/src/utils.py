import requests
from src.settings import settings, METRICS_MAPPING, SAMPLING_MAPPING
import pandas as pd
import json
from typing import Any, List



def get_sessions(start_date, end_date) -> List[str]:
    """
    Get a list of session IDs within a specified date range.

    Args:
        start_date (datetime): The start date for the date range.
        end_date (datetime): The end date for the date range.

    Returns:
        List[str]: A list of session IDs within the specified date range.
    """
    url = f"{settings.api.API_URI}/sessions/?skip=0&limit=0"
    try:
        response = requests.get(url,headers={"Authorization":f"Bearer {settings.api.API_TOKEN}", "Content-Type": "application/json"})
        # check if response is ok
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df.sort_values(by=['created_at'], inplace=True, ascending=False)
        mask = (df["created_at"] >= start_date) & (df["created_at"] <= end_date)
        df = df[mask]
        session_list = df["session_id"].tolist()
        return session_list
    except requests.HTTPError as e:
        print(e)
        return None    



def get_data(metric:str) -> Any:
    """
    Get metric data from the API.

    Args:
        metric (str): The name of the metric to retrieve.

    Returns:
        Any: The data for the specified metric.
    """
    url = f"{settings.api.API_URI}/metrics/{metric}"
    try:
        response = requests.get(url,headers={"Authorization":f"Bearer {settings.api.API_TOKEN}", "Content-Type": "application/json"})
        # check if response is ok
        response.raise_for_status()
        data = json.loads(response.json())
        return data
    except requests.HTTPError as e:
        print(e)
        return None
    


def get_all_data() -> dict[str,pd.DataFrame | dict]:
    """
    Get all available data for configured metrics.

    Returns:
        dict[str, Union[pd.DataFrame, dict]]: Processed data for each metric.
    """
    processed_data = {}
    for metric in METRICS_MAPPING.values():
        data = get_data(metric)
        if metric == "keywords" or metric == "topics":
            if data:
                processed_data[metric] = data
            else:
                processed_data[metric] = {}
        else:
            if data:
                processed_data[metric] = pd.DataFrame(data)
                processed_data[metric]["date"] = pd.to_datetime(processed_data[metric]["date"], unit="ms")
                processed_data[metric].columns = ["date",f"{metric}_count"]
            else:
                processed_data[metric] = pd.DataFrame(columns=["date",f"{metric}_count"])
    return processed_data


def get_data_by_date(data: dict, start_date, end_date):
    """
    Filter data within a specified date range for all available metrics.

    Args:
        data (dict): Processed data for all metrics.
        start_date (datetime): The start date for the date range.
        end_date (datetime): The end date for the date range.

    Returns:
        dict: Filtered data for each metric.
    """
    for metric, df in data.items():
        if metric == "keywords" or metric == "topics":
            continue
        else:
            if len(df) == 0:
                continue
            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            df = df[mask]
            data[metric] = df
    return data

def get_data_by_sampling(data: dict, sampling:str):
    """
    Resample data to a specified sampling rate for all available metrics.

    Args:
        data (dict): Processed data for all metrics.
        sampling (str): The desired sampling rate.

    Returns:
        Union[None, dict]: Resampled data for each metric, or None if the sampling rate is invalid.
    """
    if sampling not in SAMPLING_MAPPING.keys():
        return None
    sampling_rate = SAMPLING_MAPPING[sampling]
    
    for metric, df in data.items():
        if metric == "keywords" or metric == "topics":
            continue
        else:
            if len(df) == 0:
                continue
            df = df.resample(
                sampling_rate,
                on="date",
                closed="left",
                axis=0,
                kind="timestamp",
                ).agg({f"{metric}_count":"sum"})
            data[metric] = df
    return data




def get_feedbacks(start_date, end_date) -> pd.DataFrame:
    """
    Get feedback data within a specified date range.

    Args:
        start_date (datetime): The start date for the date range.
        end_date (datetime): The end date for the date range.

    Returns:
        Union[pd.DataFrame, None]: DataFrame containing feedback data or None if an error occurs.
    """
    url = f"{settings.api.API_URI}/feedback/?skip=0&limit=0"
    try:
        response = requests.get(url,headers={"Authorization":f"Bearer {settings.api.API_TOKEN}", "Content-Type": "application/json"})
        # check if response is ok
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df.sort_values(by=['created_at'], inplace=True, ascending=False)
        mask = (df["created_at"] >= start_date) & (df["created_at"] <= end_date)
        df = df[mask]
        return df
    except requests.HTTPError as e:
        print(e)
        return None


def save_csv_data(metric:str):
    """
    Save data for a metric to a CSV file.

    Args:
        metric (str): The name of the metric.

    Returns:
        bool: True if data was successfully saved, False otherwise.
    """
    data = get_data(metric)
    if data:
        df = pd.DataFrame.from_records(data,columns=["date",f"{metric}_count"])
        df.to_csv(f"{settings.api.RESOURCES_PATH}/{metric}.csv",index=False)
        return True
    return False