from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import time

def run_loader():
    subprocess.run(["python3", "loader.py"])

app = create_app()

scheduler = BackgroundScheduler()
scheduler.add_job(run_loader, 'cron', hour=1, minute=0)
scheduler.start()

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5050)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

