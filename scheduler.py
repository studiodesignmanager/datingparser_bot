import schedule
import time
from bot import run_post


def job():
    try:
        print("📤 Posting to Telegram...")
        run_post()
        print("✅ Post sent successfully")
    except Exception as e:
        print(f"❌ Error while posting: {e}")


def main():
    # 🔥 тестовый запуск при старте (ОДИН РАЗ)
    print("🚀 Scheduler started, running test post...")
    job()

    # ⏰ ежедневный пост в 20:00 (MSK ВНИМАНИЕ: зависит от времени сервера!)
    schedule.every().day.at("20:00").do(job)

    # 🔁 основной цикл
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
