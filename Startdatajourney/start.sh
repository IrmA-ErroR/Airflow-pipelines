#!/bin/bash

# Apache Airflow 2.2: практический курс

# Установка

# 1. Обновляем и устанавливаем необходимые пакеты
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv libpq-dev

# 2. Создаем и активируем виртуальную среду
python3 -m venv airflow_venv
source airflow_venv/bin/activate

# 3. Устанавливаем Airflow с поддержкой PostgreSQL и AWS

# Задаем пользовательскую директорию для хранения данных Airflow
export AIRFLOW_HOME=~/airflow-data
# Задаем директорию для DAG'ов
DAGS_DIR="$(pwd)/dags"

# Проверяем, существует ли директория с DAG'ами
if [ ! -d "$DAGS_DIR" ]; then
  echo -e "\nДиректория $DAGS_DIR не существует. Создаю..."
  mkdir -p "$DAGS_DIR"
  echo -e "Директория $DAGS_DIR успешно создана.\n"
else
  echo -e "\nДиректория $DAGS_DIR уже существует.\n"
fi

export AIRFLOW_VERSION=2.0.1
export PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# Отключаем загрузку примеров
export AIRFLOW__CORE__LOAD_EXAMPLES=False
# Указываем Airflow, где искать DAG-и
export AIRFLOW__CORE__DAGS_FOLDER=$DAGS_DIR


pip install "apache-airflow[postgres,aws]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Инициализация БД
airflow db init

# Созданеи администратора
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Запуск веб-сервера и планировщика
airflow webserver -p 8080 &  
airflow scheduler &  

echo -e "\n\nAirflow установлен и запущен в директории ${AIRFLOW_HOME}. Веб-интерфейс доступен по адресу: http://localhost:8080\n\n"


## Остановить
# pkill -f "airflow webserver"
# pkill -f "airflow scheduler"

### или 
#  Остановка всех процессов Airflow
# pkill -f "airflow"
