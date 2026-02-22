import logging
import sys
from datetime import datetime
from transform_data import combine_data
from database_manager import save_to_sqlite, save_to_parquet

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("etl_pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("Starting data pipeline execution...")
    
    try:
        start_time = datetime.now()
        
        logger.info("Extracting and Transforming data (API calls)...")
        df = combine_data()
        logger.info(f"Successfully processed data for {len(df)} cities.")

        logger.info("Loading data into SQLite...")
        save_to_sqlite(df)
        
        logger.info("Loading data into Parquet format...")
        save_to_parquet(df)

        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"Pipeline completed successfully in {duration.total_seconds():.2f} seconds!")

    except Exception as e:
        logger.error(f"Pipeline failed! Error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()