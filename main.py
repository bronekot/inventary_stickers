import os
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import qrcode
from config import *
from reportlab.lib.units import mm
from converters import mm_to_pixels

a4_width: int = mm_to_pixels(A4_WIDTH_MM)
a4_height: int = mm_to_pixels(A4_HEIGHT_MM)
num_labels: int = NUM_LABELS_PER_ROW * NUM_LABELS_PER_COLUMN

# Определяем отступ между наклейками в пикселях
label_border: int = mm_to_pixels(LABEL_BORDER_MM)
# Определяем размеры каждой наклейки в пикселях
label_width: int = round(
    (a4_width - NUM_LABELS_PER_ROW * label_border*2) / NUM_LABELS_PER_ROW
)
label_height: int = round(
    (a4_height - NUM_LABELS_PER_COLUMN * label_border*2) / NUM_LABELS_PER_COLUMN
)
qr_size_max: int = int(min(label_width, label_height))

def generate_barcode_text(value: str, width: int) -> Image:
    """Генерирует изображение с инвентарным номером для заданного значения.

    Args:
        value (str): значение, для которого нужно сгенерировать текст-картинку
        width (int): ширина изображения для текста-картинки

    Returns:
        Image: изображение с текстом-картинкой
    """
    global font_size
    # width = round(width)
    # Создаем изображение штрих-кода
    barcode_image = Image.new("1", (width, font_size), color=1)
    barcode_draw = ImageDraw.Draw(barcode_image)
    font = ImageFont.truetype(font_path, font_size)
    while True:
        font = ImageFont.truetype(font_path, font_size)
        value_bbox = barcode_draw.textbbox((0, 0), value, font=font)
        value_size = (value_bbox[2] - value_bbox[0], value_bbox[3] - value_bbox[1])
        if value_size[0] < barcode_image.width and value_size[1] < barcode_image.height:
            break
        else:
            font_size -= 1
    barcode_draw.text(
        (0, 0), value, font=font, fill=None
    )
    return barcode_image


def inventory_label(num: int, prefix: Optional[str] = None) -> str:
    """
    Генерирует ярлык для инвентаря на основе заданного номера и необязательного префикса.

    Args:
        num (int): Номер, который будет включен в ярлык.
        prefix (str, optional): Префикс для добавления к ярлыку перед номером.

    Returns:
        str: Сгенерированный ярлык для инвентаря.
    """

    global global_barcode_prefix

    if prefix is not None:
        num = prefix + str(num).zfill(barcode_digits - len(prefix))
    else:
        num = str(num).zfill(barcode_digits)

    if global_barcode_prefix:
        num = global_barcode_prefix + num

    return num

def generate_qrcode(value: str) -> Tuple[Image.Image, float]:
    """Генерирует изображение с QR-кодом для заданного значения.

    Аргументы:
        value: Значение, которое будет закодировано в QR-код.

    Возвращает:
        Кортеж, содержащий сгенерированное изображение с QR-кодом и размер модуля.
    """
    qr = qrcode.QRCode(version=None, error_correction=qrcode.ERROR_CORRECT_H, box_size=1, border=0)
    qr.add_data(value)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white").convert("1")
    module_size = qr_size_max / qr.modules_count

    return qr_image.resize((qr_size_max, qr_size_max)), module_size


def generate_label(value):
    """
    Генерирует изображение с наклейкой для заданного значения.

    Args:
        value (int): Значение для генерации наклейки.

    Returns:
        Image: Изображение наклейки.
    """
    # Создаем изображение наклейки
    label_image = Image.new("1", (label_width, label_height), color=1)
    label_draw = ImageDraw.Draw(label_image)

    # Генерируем изображение с QR-кодом
    qr_image, module_size = generate_qrcode(value)
    qr_border = round(module_size * 4)
    qr_margin = max(qr_border - label_border, 0)
    if qr_margin > 0:
        qr_image = qr_image.resize((qr_size_max - qr_margin * 2, qr_size_max - qr_margin * 2))

    # Генерируем изображение с текстом штрих-кода
    barcode_text_image = generate_barcode_text(value, label_width - qr_size_max - qr_margin - qr_border)

    # Склеиваем изображения
    label_draw.text(
        (0, 0),
        str(value),
        font=ImageFont.truetype(font_path, font_size),
        fill=0,
    )
    # Размещаем изображение с QR-кодом
    label_image.paste(qr_image, (label_width - qr_size_max - qr_margin, qr_margin))
    # Размещаем изображение с текстом
    label_image.paste(
        barcode_text_image, (0, label_height - font_size)
    )

    return label_image


def main() -> None:
    """
    Основная функция программы.

    Данная функция запрашивает у пользователя стартовый инвентарный номер и префикс.
    Затем она генерирует и сохраняет изображения наклеек, используя предоставленную информацию.
    Она также определяет размеры листа A4 в пикселях.

    :return: None
    """
    start_label_number: int = int(input("Введите стартовый инвентарный номер: "))
    prefix: Optional[str] = input("Введите префикс: ")
    while prefix and not prefix.isalpha():
        print("Ошибка! Префикс должен содержать только буквы латинского алфавита.")
        prefix = input("Введите префикс: ")
    if not prefix:
        prefix = None

    label_numbers = range(start_label_number, start_label_number + num_labels + 1)
    os.makedirs("labels", exist_ok=True)
    for index, number in enumerate(label_numbers):
        value = inventory_label(number, prefix)
        label_image = generate_label(value)
        label_image.save(f"labels/{index}.bmp")

    complit(num_labels)
    os.startfile("all_labels.bmp", "print")



def complit(num_labels):
    """
    Создает изображение, содержащее num_labels наклеек.

    Аргументы:
        num_labels (int): Количество наклеек для создания.

    Возвращает:
        None. Сохраняет созданное изображение на жесткий диск.
    """

    # Создаем изображение-контейнер для всех наклеек
    all_labels_image = Image.new("1", (a4_width, a4_height), color=1)

    # Определяем начальную позицию для размещения наклеек
    x, y = 0, 0

    # Получаем список всех сгенерированных наклеек
    label_images = [Image.open(f"labels/{i}.bmp") for i in range(num_labels)]

    # Размещаем каждую наклейку на листе A4
    for i, label_image in enumerate(label_images):
        x_n = i % NUM_LABELS_PER_ROW
        y_n = i // NUM_LABELS_PER_ROW

        # Вычисляем координаты верхнего левого угла для размещения текущей наклейки
        x = round(
            x_n * (label_width + label_border*2) + label_border
        )
        y = round(
            y_n * (label_height + label_border*2) + label_border
        )

        # Размещаем текущую наклейку на листе A4
        all_labels_image.paste(label_image, (x, y))


    # Обрезаем поля (для HP 428, который добавляет свои поля при печати)
    crop_border = label_border / 8 * 5
    left = int(crop_border)
    top = int(crop_border)
    right = int(a4_width - crop_border)
    bottom = int(a4_height - crop_border)
    all_labels_image = all_labels_image.crop((left, top, right, bottom))

    # Сохраняем полученное изображение на жесткий диск
    all_labels_image.save("all_labels.bmp")

main()
