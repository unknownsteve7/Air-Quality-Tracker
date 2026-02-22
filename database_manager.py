import sqlite3
import pandas as pd
import json
from transform_data import combine_data

def clean_for_sqlite(df):
    """
    Convert any list/dict columns into JSON strings so SQLite can store them.
    """
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x
        )
    return df

def save_to_sqlite(df, db_name="weather_history.db", table_name="city_metrics"):
    df = clean_for_sqlite(df)
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
    print(f"Data saved to {db_name} in table {table_name}")

def save_to_parquet(df, file_name="city_metrics.parquet"):
    df.to_parquet(file_name, engine="pyarrow", index=False)
    print(f"Data saved as Parquet file: {file_name}")

if __name__ == "__main__":
    df = combine_data()
    save_to_sqlite(df)
    save_to_parquet(df)