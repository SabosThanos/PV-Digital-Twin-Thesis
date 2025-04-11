import datetime
import pytz
import json
import requests
import os

def huawei_login(base_url):
    url = f'{base_url}login'
    payload = {
        "userName": os.getenv("userName"),
        "systemCode": os.getenv("systemCode"),
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers, allow_redirects=True)
    response_text = response.text

    if '"failCode":0' in response_text:
        cookies = response.cookies.get_dict()
        token = cookies.get('XSRF-TOKEN')
    else:
        token = None

    return token

def get_dev_history_kpi(token, base_url, params):
    epoch_start = int(params["timestampStart"])* 1000
    epoch_end = int(params["timestampEnd"])* 1000 - 1

    ids = params["devIds"]
    ids_str = ','.join(ids)

    url = f"{base_url}getDevHistoryKpi"
    headers = {
        'XSRF-TOKEN': token,
        'Content-Type': 'application/json',
    }
    payload = {
        "devIds": ids_str,
        "devTypeId": params["devTypeId"],
        "startTime": epoch_start,
        "endTime": epoch_end
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.text

def get_yesterday_and_today_midnight_unix_timestamps():
    # Define Greece timezone
    greece_tz = pytz.timezone('Europe/Athens')
    
    # Get current date and time in Greece
    now_greece = datetime.datetime.now(greece_tz)

    # Today at midnight
    today_midnight = greece_tz.localize(datetime.datetime(now_greece.year, now_greece.month, now_greece.day, 0, 0, 0))

    # Yesterday at midnight
    yesterday_midnight = today_midnight - datetime.timedelta(days=1)

    # Convert to Unix timestamps
    today_ts = int(today_midnight.timestamp())
    yesterday_ts = int(yesterday_midnight.timestamp())

    return yesterday_ts, today_ts