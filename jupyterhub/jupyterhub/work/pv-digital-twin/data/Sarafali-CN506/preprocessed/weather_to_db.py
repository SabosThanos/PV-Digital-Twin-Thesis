import os
import glob
import pandas as pd
from sqlalchemy import create_engine

folder_names = [
    "CN506-2023-07/EMI",
    "CN506-2023-08/EMI",
    "CN506-2023-09/EMI",
    "CN506-2023-10/EMI",
    "CN506-2023-11/EMI",
    "CN506-2023-12/EMI",
    "CN506-2024-01/EMI",
    "CN506-2024-02/EMI",
    "CN506-2024-03/EMI",
    "CN506-2024-04/EMI",
    "CN506-2024-05/EMI",
    "CN506-2024-06/EMI",
    "CN506-2024-07/EMI",
    "CN506-2024-08/EMI",
    "CN506-2024-09/EMI",
    "CN506-2024-10/EMI",
    "CN506-2024-11/EMI",
    "CN506-2024-12/EMI",
    "CN506-2025-01/EMI",
    "CN506-2025-02/EMI"
]


columns_to_keep=[
    "Site Name",
    "ManageObject",
    "Start Time",
    "Device connection status",
    "Irradiance(W/㎡)",
    "Daily irradiation(MJ/㎡)",
    "Ambient temperature(℃)",
    "Wind speed(m/s)",
    "Wind direction(°)",
    "PV Temperature(℃)"
]

rename_dict = {
    "Site Name": "plant_code",
    "ManageObject": "dev_id",
    "Start Time": "collect_time",
    "Device connection status": "device_state",
    "Irradiance(W/㎡)": "irradiance",
    "Daily irradiation(MJ/㎡)": "daily_iradiation",
    "Ambient temperature(℃)": "temperature",
    "Wind speed(m/s)": "wind_speed",
    "Wind direction(°)": "wind_direction",
    "PV Temperature(℃)": "pv_temperature"
}

# PostgreSQL Connection
engine = create_engine("postgresql://postgres:bhSfWIhKfNGHoE0AZF6grXOqa1UcMAiJnQdQWnW6XqtmFnrsXOGBeCWcxM2kBwA4@127.0.0.1:5432/postgres")

# Get all Excel files in the directory
for folder in folder_names:
    directory = f"./{folder}"
    excel_files = glob.glob(os.path.join(directory, "*.xlsx"))
    for file in excel_files:
        df=pd.read_excel(file, skiprows=3)
        df=df[columns_to_keep]
        df['Start Time'] = df['Start Time'].str.replace('DST', '').str.strip()  # Remove 'DST'
        df['Start Time'] = pd.to_datetime(df['Start Time'])  # Convert to datetime format
        df = df.rename(columns=rename_dict)

        # Insert entire DataFrame into PostgreSQL
        df.to_sql('weather_data', engine, if_exists='append', index=False)