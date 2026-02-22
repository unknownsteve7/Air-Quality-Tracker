import schedule
import time
import logging
from run_pipeline import run_pipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [SCHEDULER] %(message)s'
)

def job():
    logging.info("Triggering scheduled pipeline...")
    try:
        run_pipeline()
    except Exception as e:
        logging.error(f"Scheduled job failed: {e}")

schedule.every().hour.do(job)

if __name__ == "__main__":
    logging.info("Scheduler started. Watching for tasks...")
    
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(1)
