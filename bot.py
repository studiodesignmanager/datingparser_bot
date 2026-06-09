import requests
from telegram import Bot
from config import TOKEN, CHANNEL, HEADERS
from parser import get_online_girl
from image_utils import crop_logo

bot = Bot(token=TOKEN)


def post_to_telegram(profile):
    response = requests.get(profile['img'], headers=HEADERS)

    if response.status_code != 200:
        print("Ошибка загрузки изображения:", response.status_code)
        return

    img = crop_logo(response.content)

    caption = (
        f"👩‍💼 {profile['name']}, {profile['age']}, {profile['country']}\n"
        f"🔗 Ссылка: {profile['link']}"
    )

    bot.send_photo(
        chat_id=CHANNEL,
        photo=img,
        caption=caption
    )


# 🔥 ЭТА ФУНКЦИЯ НУЖНА scheduler.py
def run_post():
    girl = get_online_girl()

    if not girl:
        print("❌ Нет подходящих анкет онлайн.")
        return

    post_to_telegram(girl)


# локальный тест (ручной запуск)
if __name__ == "__main__":
    run_post()


