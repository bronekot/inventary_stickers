@echo off

:: Установка зависимостей
pip install -r requirements.txt --exists-action=i --quiet

:: Запуск программы
python main.py

:: Очистка временных файлов
del /Q labels\*.bmp