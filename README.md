# Генератор наклеек на инвентарь

Этот скрипт используется для генерации наклеек на инвентарь. Он генерирует QR-коды и их текст, а также размещает их на изображениях наклеек. Эти изображения сохраняются в файлы и могут быть напечатаны на принтере.

## Мотивация написания этого скрипта

Я создал этот скрипт для того, чтобы упростить и ускорить процесс учета имущества в организации. Ручное заполнение инвентарных карточек может быть долгим и утомительным, а использование программ генерации штрих-кодов и QR-кодов может быть недостаточно эффективным, если они не могут генерировать QR-код и его текстовое значение одновременно (привет Barcode Studio). Мой скрипт позволяет создавать инвентаризационные наклейки с QR-кодом и текстовым номером на одном листе A4, что делает процесс учета и инвентаризации более удобным.

## Установка

Чтобы использовать этот скрипт, вам нужно установить зависимости, используемые в этом проекте. Вы можете сделать это, выполнив следующую команду:
`pip install -r requirements.txt`

## Использование

Вы можете использовать этот скрипт, чтобы сгенерировать наклейки на инвентарь. Для этого запустите скрипт, используя следующую команду:
`python main.py`

Скрипт запросит у вас стартовый инвентарный номер и префикс. Затем он сгенерирует и сохранит изображения наклеек на инвентарь.

Вы можете напечатать изображения наклеек на принтере, используя программное обеспечение для принтера или любой другой метод, который вам нравится.

## Простой запуск скрипта в Windows

Вы можете запустить скрипт, используя `run.bat`. Для этого просто дважды щелкните по файлу `run.bat` в проводнике Windows.

Это автоматически установит зависимости, запустит скрипт и сгенерирует наклейки на инвентарь.

## Лицензия

Этот проект находится под лицензией MIT. Подробную информацию об этой лицензии вы можете найти в файле `LICENSE.md`.
