import json
import psycopg2
from datetime import datetime
import pytz
import os

def convert_timestamp_ms_to_naive_athens_datetime(ts_ms):
    """Converts UNIX timestamp in ms to naive datetime in Athens local time (Python 3.8)"""
    utc_dt = datetime.fromtimestamp(ts_ms / 1000.0)
    athens_dt = utc_dt.astimezone(pytz.timezone("Europe/Athens"))
    return athens_dt.replace(tzinfo=None)  # remove timezone info (naive)

def insert_inverter_data_to_db(data_list, plantcode, dev_name): 
    records=[]       
    for data in data_list:
        result = {
            "plant_code": plantcode,
            "dev_id": dev_name,
            "collect_time": convert_timestamp_ms_to_naive_athens_datetime(data["collectTime"]),
            "inverter_state": "Grid Connected" if (data["dataItemMap"].get("inverter_state") == 512.0) else "Standby",
            "active_power": data["dataItemMap"].get("active_power"),
            "day_cap": data["dataItemMap"].get("day_cap"),
            "reactive_power": data["dataItemMap"].get("reactive_power"),
            "power_factor": data["dataItemMap"].get("power_factor"),
            "input_power": data["dataItemMap"].get("mppt_power"),
            "efficiency": data["dataItemMap"].get("efficiency"),
            "u_ab": data["dataItemMap"].get("ab_u"),
            "u_bc": data["dataItemMap"].get("bc_u"),
            "u_ca": data["dataItemMap"].get("ca_u"),                
            "u_a": data["dataItemMap"].get("a_u"),
            "u_b": data["dataItemMap"].get("b_u"),
            "u_c": data["dataItemMap"].get("c_u"),
            "i_a": data["dataItemMap"].get("a_i"),
            "i_b": data["dataItemMap"].get("b_i"),
            "i_c": data["dataItemMap"].get("c_i"),
            "frequency": data["dataItemMap"].get("elec_freq"),
            "temperature": data["dataItemMap"].get("temperature"),
        }
        records.append(tuple(result.values()))

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),  # Use environment variable for host
        port=os.getenv("DB_PORT", 5432),  # Use environment variable for port, default to 5432
        database=os.getenv("DB_NAME", "postgres"),  # Use environment variable for database name, default to 'postgres'
        user=os.getenv("DB_USER", "postgres"),  # Use environment variable for user, default to 'postgres'
        password=os.getenv("DB_PASSWORD")  # Use environment variable for password, default to 'postgres'
    )
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO inverter_data (
            plant_code, dev_id, collect_time, inverter_state, active_power, day_cap,
            reactive_power, power_factor, input_power, efficiency,
            u_ab, u_bc, u_ca, u_a, u_b, u_c,
            i_a, i_b, i_c, frequency, temperature
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (dev_id, collect_time) DO NOTHING
    """
    cursor.executemany(insert_query, records)
    conn.commit()
    inserted_count = cursor.rowcount
    cursor.close()
    conn.close()
    return f"Successfully inserted {inserted_count} records."


def insert_weather_data_to_db(data_list, plantcode, dev_name):        
    records = []
    for data in data_list:
        result = {
            "plant_code": plantcode,
            "dev_id": dev_name,
            "collect_time": convert_timestamp_ms_to_naive_athens_datetime(data["collectTime"]),
            "device_state": "Online",
            "irradiance": data["dataItemMap"].get("radiant_line"),
            "daily_iradiation": data["dataItemMap"].get("radiant_total"),
            "temperature": data["dataItemMap"].get("temperature"),
            "wind_speed": data["dataItemMap"].get("wind_speed"),
            "wind_direction": data["dataItemMap"].get("wind_direction"),
            "pv_temperature": data["dataItemMap"].get("pv_temperature"),
        }
        records.append(tuple(result.values()))

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),  # Use environment variable for host
        port=os.getenv("DB_PORT", 5432),  # Use environment variable for port, default to 5432
        database=os.getenv("DB_NAME", "postgres"),  # Use environment variable for database name, default to 'postgres'
        user=os.getenv("DB_USER", "postgres"),  # Use environment variable for user, default to 'postgres'
        password=os.getenv("DB_PASSWORD")  # Use environment variable for password, default to 'postgres'
    )
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO weather_data (
            plant_code, dev_id, collect_time, device_state, irradiance, daily_iradiation,
            temperature, wind_speed, wind_direction, pv_temperature
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (dev_id, collect_time) DO NOTHING;
    """
    cursor.executemany(insert_query, records)
    conn.commit()
    inserted_count = cursor.rowcount
    cursor.close()
    conn.close()

    return f"Successfully inserted {inserted_count} weather records."
