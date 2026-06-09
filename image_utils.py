from PIL import Image
from io import BytesIO


def crop_logo(img_data):
    """
    Удаляет верхнюю часть изображения (логотип/баннер)
    и возвращает объект для отправки в Telegram.
    """

    # открываем изображение из bytes
    img = Image.open(BytesIO(img_data))

    # на всякий случай приводим к RGB (важно для PNG/WebP)
    if img.mode != "RGB":
        img = img.convert("RGB")

    width, height = img.size

    # адаптивная обрезка (вместо фиксированных пикселей)
    crop_top = int(height * 0.08)  # 8% сверху убираем логотип

    cropped = img.crop((0, crop_top, width, height))

    # готовим файл для Telegram
    output = BytesIO()
    output.name = "photo.jpg"

    cropped.save(output, format="JPEG", quality=95, optimize=True)
    output.seek(0)

    return output
