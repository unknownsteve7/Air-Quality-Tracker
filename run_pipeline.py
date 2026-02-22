

from transform_data import combine_data
from database_manager import save_to_sqlite, save_to_parquet

def run_pipeline():
    print("Starting data pipeline...")

    print("Combining weather and pollution data...")
    df = combine_data()
    print("Data combined successfully")

    print("Saving data to SQLite database...")
    save_to_sqlite(df)
    print("Data saved to SQLite")

    print("Saving data to Parquet file...")
    save_to_parquet(df)
    print("Data saved as Parquet")

    print("Pipeline completed!")

if __name__ == "__main__":
    run_pipeline()