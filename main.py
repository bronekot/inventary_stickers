import os
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import segno
from config import *
from converters import mm_to_pixels

from aztec_code_generator import AztecCode


a4_width: int = mm_to_pixels(A4_WIDTH_MM)
a4_height: int = mm_to_pixels(A4_HEIGHT_MM)
num_labels: int = NUM_LABELS_PER_ROW * NUM_LABELS_PER_COLUMN

# Определяем отступ между наклейками в пикселях
label_border: int = mm_to_pixels(LABEL_BORDER_MM)


def generate_barcode_text_image(value: str, width: int, qr_margin: int) -> Image:
    """Генерирует изображение с инвентарным номером для заданного значения.

    Args:
        value (str): значение, для которого нужно сгенерировать текст-картинку
        width (int): ширина изображения для текста-картинки

    Returns:
        Image: изображение с текстом-картинкой
    """
    global font_size
    font_size_temp = font_size
    # width = round(width)
    # Создаем изображение штрих-кода
    font_height = 0
    
    while True:
        font = ImageFont.truetype(font_path, font_size_temp)
        barcode_image = Image.new("1", (width - max(int(font.getsize('p')[1]/2), qr_margin), font.getsize('Pp')[1]), color=1)
        barcode_draw = ImageDraw.Draw(barcode_image)
        value_bbox = barcode_draw.textbbox((0, 0), value, font=font)
        value_size = (value_bbox[2] - value_bbox[0], value_bbox[3] - value_bbox[1])
        if value_size[0] < barcode_image.width and value_size[1] < barcode_image.height:
            font_height = font.getsize('Pp')[1]
            break
        else:
            font_size_temp -= 1
    barcode_draw.text((0, 0), value, font=font, fill=None)
    return barcode_image, font_height


import yaml

def get_client_name_by_prefix(prefix: Optional[str]) -> Optional[str]:
    """
    Возвращает название клиента по заданному префиксу.

    Args:
        prefix (str, optional): Префикс клиента.

    Returns:
        str: Название клиента, если префикс найден в словаре клиентов. Иначе - None.
    """
    with open('clients.yaml', 'r', encoding='utf-8') as f:
        clients = yaml.safe_load(f)

    return clients.get(prefix.upper()) if prefix else None

def inventory_label(num: int, prefix: Optional[str] = None) -> Tuple[str, Optional[str]]:
    """
    Генерирует ярлык для инвентаря на основе заданного номера и необязательного префикса.

    Args:
        num (int): Номер, который будет включен в ярлык.
        prefix (str, optional): Префикс для добавления к ярлыку перед номером.

    Returns:
        Tuple[str, Optional[str]]: Кортеж из сгенерированного ярлыка и названия клиента (если клиент найден по префиксу).
    """

    global global_barcode_prefix

    client_name = get_client_name_by_prefix(prefix)

    if prefix is not None:
        inv = prefix.upper() + str(num).zfill(barcode_digits - len(prefix))
    else:
        inv = str(num).zfill(barcode_digits)

    if global_barcode_prefix:
        inv =  global_barcode_prefix.lower() + inv

    return inv, client_name



# def generate_qrcode(value: str, qr_size: int) -> Tuple[Image.Image, float]:
#     """Генерирует изображение с QR-кодом для заданного значения.

#     Аргументы:
#         value: Значение, которое будет закодировано в QR-код.

#     Возвращает:
#         Кортеж, содержащий сгенерированное изображение с QR-кодом и размер модуля.
#     """
#     qr = qrcode.QRCode(
#         version=None, error_correction=qrcode.ERROR_CORRECT_H, box_size=1, border=0
#     )
#     qr.add_data(value)
#     qr.make(fit=True)
#     qr_image = qr.make_image(fill_color="black", back_color="white").convert("1")
#     module_size = qr_size / qr.modules_count

#     return qr_image.resize((qr_size, qr_size)), module_size



qr_versions = {
    1: 21,
    2: 25,
    3: 29,
    4: 33,
    5: 37,
    6: 41,
    7: 45,
    8: 49,
    9: 53,
    10: 57,
    11: 61,
    12: 65,
    13: 69,
    14: 73,
    15: 77,
    16: 81,
    17: 85,
    18: 89,
    19: 93,
    20: 97,
    21: 101,
    22: 105,
    23: 109,
    24: 113,
    25: 117,
    26: 121,
    27: 125,
    28: 129,
    29: 133,
    30: 137,
    31: 141,
    32: 145,
    33: 149,
    34: 153,
    35: 157,
    36: 161,
    37: 165,
    38: 169,
    39: 173,
    40: 177,
    'M1': 11,
    'M2': 13,
    'M3': 15,
    'M4': 17,
}

def generate_qrcode(value: str, qr_size: int, is_micro: bool = True) -> Tuple[Image.Image, float]:
    """Генерирует изображение с QR-кодом для заданного значения.

    Аргументы:p
        value: Значение, которое будет закодировано в QR-код.
        qr_size: Размер изображения с QR-кодом в пикселях.
        is_micro: Флаг, указывающий, нужно ли генерировать Micro QR.

    Возвращает:
        Кортеж, содержащий сгенерированное изображение с QR-кодом и размер модуля.
    """
    qrcode = segno.make(value, micro=is_micro)
    qr_image = qrcode.to_pil(border=0)
    module_size = qr_size / qr_versions[qrcode.version]
    return qr_image.resize((qr_size, qr_size)), module_size


def generate_azteccode(value: str, code_size: int) -> Tuple[Image.Image, float]:
    aztec_code = AztecCode(value, ec_percent=80)
    aztec_image = aztec_code.to_pil()
    module_size = code_size / aztec_code.size
    return aztec_image.resize((code_size, code_size)), module_size


def generate_label(value: str, label_text: str, label_size: Tuple[int, int], qr_size: int) -> Image:
    """
    Генерирует изображение с наклейкой для заданного значения.

    Args:
        value (str): Значение для генерации наклейки.

    Returns:
        Image: Изображение наклейки.
    """
    (label_width, label_height) = label_size

    # Создаем изображение наклейки
    label_image = Image.new("1", label_size, color=1)
    label_draw = ImageDraw.Draw(label_image)
    is_micro = True
    is_aztec = True

    # Генерируем изображение с QR-кодом
    if is_aztec:
        qr_image, module_size = generate_azteccode(value, qr_size)
    else:
        qr_image, module_size = generate_qrcode(value, qr_size, is_micro)
    
    # вычисляем qr_border исходя из типа QR или Micro или Aztec
    if is_aztec:
        qr_border = 0
    else:
        qr_border = round(module_size * 2) if is_micro else round(module_size * 4)
    qr_margin = max(qr_border - label_border, 0)
    if qr_margin > 0:
        qr_image = qr_image.resize(
            (qr_image.width - qr_margin * 2, qr_image.height - qr_margin * 2)
        )

    # Генерируем изображение с текстом штрих-кода
    barcode_text_image, font_height_barcode_text_image = generate_barcode_text_image(
        value, label_width - qr_image.width - qr_margin - qr_border, qr_margin
    )
    # Генерируем изображение с текстом штрих-кода
    label_text_image = add_text_to_image(
        label_text, font_path, font_size, 0, 
        (0, 0, label_width - qr_image.width - qr_margin - qr_border, label_height - barcode_text_image.size[1]),
        (label_width - qr_image.width - qr_margin - qr_border, label_height - barcode_text_image.size[1])
    )
    # Размещаем текстлейбла
    label_image.paste(label_text_image, (0,0))
    # Размещаем изображение с QR-кодом
    label_image.paste(qr_image, (label_width - qr_image.width - qr_margin, qr_margin))
    # Размещаем изображение с номером
    label_image.paste(barcode_text_image, (0, label_height - int(font_height_barcode_text_image)))

    return label_image

from PIL import Image, ImageDraw, ImageFont
from functools import lru_cache
import textwrap

@lru_cache(maxsize=None)
def add_text_to_image(text, font_path, font_size, text_color, text_position, image_size):
    image = Image.new('RGBA', image_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    font_size_temp = font_size

    current_line = ''
    while True:
        font = ImageFont.truetype(font_path, font_size_temp)
        word_width = font.getsize('a')[0]
        lines = []
        max_width = 0
        # Разбиваем текст на строки по символу перевода строки
        text_lines = text.split('\n')
        for line in text_lines:
            # Расчет максимальной длины строки
            max_length_text = int(text_position[2] / word_width) - 1
            # Используем textwrap.wrap() для разбиения строки на части
            for wrapped_line in textwrap.wrap(line, max_length_text, break_long_words=False):
                # Удаляем пробелы с начала и конца строки
                wrapped_line = wrapped_line.strip()
                line_width = draw.textsize(wrapped_line, font=font)[0]
                if line_width <= text_position[2]:
                    lines.append(wrapped_line)
                else:
                    # Если строка не влезает в заданный размер, разбиваем ее на части
                    # и добавляем части в список строк
                    lines.extend(textwrap.wrap(wrapped_line, max_length_text, break_long_words=False))
                max_width = max(max_width, line_width)

        lines.append(current_line.strip())

        # Если все строки вписываются в заданный размер, то выходим из цикла
        if sum(draw.textsize(line, font=font)[1] for line in lines) <= text_position[3] and \
           max(draw.textsize(line, font=font)[0] for line in lines) <= text_position[2] - word_width:
            break

        # Иначе уменьшаем размер шрифта и повторяем процедуру
        font_size_temp -= 1

    # Рисуем текст на изображении
    y = text_position[1]
    for line in lines:
        print(line)
        draw.text((text_position[0], y), line, font=font, fill=text_color)
        y += draw.textsize(line, font=font)[1]

    return image





def main() -> None:
    """
    Основная функция программы.

    Данная функция запрашивает у пользователя стартовый инвентарный номер и префикс.
    Затем она генерирует и сохраняет изображения наклеек, используя предоставленную информацию.
    Она также определяет размеры листа A4 в пикселях.

    :return: None
    """
    start_label_number: int = int(input("Введите стартовый инвентарный номер: "))
    prefix: Optional[str] = input("Введите префикс [по умолчанию префикса нет]: ")
    while prefix and not prefix.isalpha():
        print("Ошибка! Префикс должен содержать только буквы латинского алфавита.")
        prefix = input("Введите префикс [по умолчанию префикса нет]: ")
    if not prefix:
        prefix = None
    
    try:
        num_labels_per_row = int(
            input(
                f"Введите количество наклеек в ряд [по умолчанию {NUM_LABELS_PER_ROW}]: "
            )
        )
    except ValueError:
        num_labels_per_row = NUM_LABELS_PER_ROW
    try:
        num_labels_per_column = int(
            input(
                f"Введите количество наклеек в столбик [по умолчанию {NUM_LABELS_PER_COLUMN}]: "
            )
        )
    except ValueError:
        num_labels_per_column = NUM_LABELS_PER_COLUMN

    # Определяем размеры каждой наклейки в пикселях
    label_width: int = round(
        (a4_width - num_labels_per_row * label_border * 2) / num_labels_per_row
    )
    label_height: int = round(
        (a4_height - num_labels_per_column * label_border * 2) / num_labels_per_column
    )
    label_size = (label_width, label_height)
    # Вычисляем максимальный размер QR-кода. В дальнейшем размер может уменьшиться, чтобы соответствовать спецификации отступа в 4 модуля.
    qr_size_max: int = int(min(label_width, label_height))

    

    label_numbers = range(start_label_number, start_label_number + num_labels + 1)
    os.makedirs("labels", exist_ok=True)
    for index, number in enumerate(label_numbers):
        value, label = inventory_label(number, prefix)
        label_image = generate_label(value, label, label_size, qr_size_max)
        label_image.save(f"labels/{index}.bmp")

    all_labels_image = complit(num_labels, label_size)
    # all_labels_image = crop_labels(all_labels_image)
    # Сохраняем полученное изображение на жесткий диск
    all_labels_image.save("all_labels.bmp")
    os.startfile("all_labels.bmp", "print")

# Обрезаем поля (для HP 428, который добавляет свои поля при печати)
def crop_labels(all_labels_image: Image) -> Image:
    crop_border = label_border / 8 * 5
    left = int(crop_border)
    top = int(crop_border)
    right = int(a4_width - crop_border)
    bottom = int(a4_height - crop_border)
    return all_labels_image.crop((left, top, right, bottom))

def complit(num_labels, label_size: Tuple[int, int]) -> Image:
    """
    Создает изображение, содержащее num_labels наклеек.

    Аргументы:
        num_labels (int): Количество наклеек для создания.

    Возвращает:
        None. Сохраняет созданное изображение на жесткий диск.
    """
    (label_width, label_height) = label_size
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
        x = round(x_n * (label_width + label_border * 2) + label_border)
        y = round(y_n * (label_height + label_border * 2) + label_border)

        # Размещаем текущую наклейку на листе A4
        all_labels_image.paste(label_image, (x, y))

    
    return all_labels_image


main()
