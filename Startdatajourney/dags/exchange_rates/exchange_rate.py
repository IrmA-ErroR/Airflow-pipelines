from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import requests
from xml.etree import ElementTree as ET

# Функция для получения и парсинга данных с сайта ЦБ РФ
def fetch_exchange_rates(**kwargs):
    url = "https://www.cbr-xml-daily.ru/daily_utf8.xml"
    response = requests.get(url)

    if response.status_code == 200:
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()
    
        # Проверяем, что элемент ValCurs существует
        if root.tag == 'ValCurs':
            date = root.attrib.get('Date')  # Получаем дату
            # Преобразуем дату в формат YYYY-MM-DD
            date = datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')


            # Валюты, которые нужны
            currencies = {'USD': 'R01235', 'KZT': 'R01335'}
            rates = []

            for valute in root.findall('Valute'):
                char_code = valute.find('CharCode').text
                if char_code in currencies:
                    rate = valute.find('Value').text
                    nominal = valute.find('Nominal').text
                    rate_float = float(rate.replace(',', '.')) / float(nominal.replace(',', '.'))
                    
                    rates.append({
                        'currency': char_code,
                        'rate': rate_float,
                        'date': date
                    })

            print(rates)
            # Сохранение курсов валют в XCom
            kwargs['ti'].xcom_push(key='exchange_rates', value=rates)
        else:
            raise ValueError("Root element is not 'ValCurs'. Unable to parse the XML structure.")
    else:
        raise Exception(f"Failed to retrieve data. HTTP Status code: {response.status_code}")


def insert_rates_into_db(**kwargs):
        rates = kwargs['ti'].xcom_pull(key='exchange_rates')
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        
        for rate in rates:
            insert_query = """
                INSERT INTO currency_exchange_rates (base, currency, rate, date)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (base, currency, date) DO NOTHING;
            """
            pg_hook.run(insert_query, parameters=('RUB', rate['currency'], rate['rate'], rate['date']))


# Определение DAG
with DAG(
    dag_id='exchange_rate_usd_kzt_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@monthly',
    catchup=False
) as dag:

    # Создание таблицы в PostgreSQL
    create_table = PostgresOperator(
        task_id='create_table_task',
        sql='create_table.sql',
        postgres_conn_id='postgres_default',
    )

    # Получение курсов валют
    get_rate = PythonOperator(
        task_id='get_rate_task',
        python_callable=fetch_exchange_rates,
        provide_context=True,
    )

    # Вставка данных в БД для каждой валюты
    insert_rates = PythonOperator(
        task_id='insert_rates_task',
        python_callable=insert_rates_into_db,
        provide_context=True,
    )

    create_table >> get_rate >> insert_rates
