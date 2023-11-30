# Используйте официальный образ Python как базовый образ
FROM python:3.11

# Установите рабочий каталог в контейнере
WORKDIR /usr/src/app

# Копируйте файл requirements.txt в контейнер
COPY requirements.txt ./

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте исходный код в контейнер
COPY . .

# Укажите команду для запуска приложения
CMD [ "python", "./main.py" ]
