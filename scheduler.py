import schedule
import time
from bot import run_post  # импорт функции

def job():
    print("Posting to Telegram...")
    run_post()

schedule.every().day.at("20:00").do(job)

# тест через 5 минут
schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
