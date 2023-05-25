# Используем Python 3.11 в качестве базового образа
FROM python:3.11

# Установить зависимости
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Копировать все файлы Python в контейнер
COPY *.py /app/

# Указать рабочую директорию
WORKDIR /app

# Запустить скрипт при запуске контейнера
CMD ["python", "main.py"]

COPY /all_labels.bmp /host/path
