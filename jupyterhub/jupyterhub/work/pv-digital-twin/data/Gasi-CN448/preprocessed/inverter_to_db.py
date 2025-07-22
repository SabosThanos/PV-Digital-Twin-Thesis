import os
import glob
import pandas as pd
from sqlalchemy import create_engine

# Define the directory containing the Excel files
directory = "./CN448-2025-01/Inverter"

columns_to_keep=[
    "Site Name",
    "ManageObject",
    "Start Time",
    "Inverter status",
    "Active power(kW)",
    "Daily energy(kWh)",
    "Output reactive power(kvar)",
    "Power factor",
    "Total input power(kW)",
    "Inverter efficiency(%)",
    "Grid voltage/Grid AB line voltage(V)",
    "BC line voltage(V)",
    "CA line voltage(V)",
    "Phase A voltage(V)",
    "Phase B voltage(V)",
    "Phase C voltage(V)",
    "Grid current/Grid phase A current(A)",
    "Phase B current(A)",
    "Phase C current(A)",
    "Grid frequency(Hz)",
    "Internal temperature(℃)"
]

rename_dict = {
    "Site Name": "plant_code",
    "ManageObject": "dev_id",
    "Start Time": "collect_time",
    "Inverter status": "inverter_state",
    "Active power(kW)": "active_power",
    "Daily energy(kWh)": "day_cap",
    "Output reactive power(kvar)": "reactive_power",
    "Power factor": "power_factor",
    "Total input power(kW)": "input_power",
    "Inverter efficiency(%)": "efficiency",
    "Grid voltage/Grid AB line voltage(V)": "u_ab",
    "BC line voltage(V)": "u_bc",
    "CA line voltage(V)": "u_ca",
    "Phase A voltage(V)": "u_a",
    "Phase B voltage(V)": "u_b",
    "Phase C voltage(V)": "u_c",
    "Grid current/Grid phase A current(A)": "i_a",
    "Phase B current(A)": "i_b",
    "Phase C current(A)": "i_c",
    "Grid frequency(Hz)": "frequency",
    "Internal temperature(℃)": "temperature"
}

# PostgreSQL Connection
engine = create_engine("postgresql://postgres:bhSfWIhKfNGHoE0AZF6grXOqa1UcMAiJnQdQWnW6XqtmFnrsXOGBeCWcxM2kBwA4@127.0.0.1:5432/postgres")

# Get all Excel files in the directory
excel_files = glob.glob(os.path.join(directory, "*.xlsx"))
for file in excel_files:
    df=pd.read_excel(file, skiprows=3)
    df=df[columns_to_keep]
    df['Start Time'] = df['Start Time'].str.replace('DST', '').str.strip()  # Remove 'DST'
    df['Start Time'] = pd.to_datetime(df['Start Time'])  # Convert to datetime format
    df = df.rename(columns=rename_dict)

    # Insert entire DataFrame into PostgreSQL
    df.to_sql('inverter_data', engine, if_exists='append', index=False)

print(directory)