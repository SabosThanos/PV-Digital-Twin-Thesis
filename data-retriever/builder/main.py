import json
import time
# import psycopg2
# from psycopg2.extras import execute_batch
from helper_functions import *
from database_functions import *

yesterday_ts, today_ts = get_yesterday_and_today_midnight_unix_timestamps()
print("Yesterday timestamp: ", yesterday_ts)

with open("devices.json", "r") as f:
    device_list= json.load(f)
print("Device list: ", device_list)
for device in device_list:    
    params={
            "devIds": device["dev_id"],
            "devTypeId": [int(device["dev_type"])],
            "timestampStart": yesterday_ts,
            "timestampEnd": today_ts
        }

url = 'https://eu5.fusionsolar.huawei.com/thirdData/'
token=huawei_login(url)
if not token:
    print ("error, Failed to get token")
else:
    for device in device_list:    
        params={
                "devIds": [device["dev_id"]],
                "devTypeId": device["dev_type"],
                "timestampStart": yesterday_ts,
                "timestampEnd": today_ts
            }
        print("Params: ", params)
        data = get_dev_history_kpi(token, url, params)
        data_list = json.loads(data)["data"]
        if data_list and isinstance(data_list, list) and len(data_list)!=0:
            if device["dev_type"]=="1":
                print(insert_inverter_data_to_db(data_list, plantcode=device["plant_code"], dev_name=device["dev_name"]))
            elif device["dev_type"]=="10":
                print(insert_weather_data_to_db(data_list, plantcode=device["plant_code"], dev_name=device["dev_name"]))
        else :
            print("No data to insert.")
        time.sleep(30)