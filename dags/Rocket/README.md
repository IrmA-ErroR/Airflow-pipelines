# Ракеты

[Launch Library 2](https://thespacedevs.com/llapi) - онлайн-хранилище данных о  предыдущих 
и будущих запусках ракет из различных источников

Данные о предстоящих запусках ракет ```https://ll.thespacedevs.com/2.0.0/launch/upcoming/```

Данные представлены в формате JSON, содержат информацию о запуске ракеты, а для каждого запуска есть информация о конкретной ракете, такая как идентификатор, имя и URL-адрес изображения.


```bash
docker run -it -p 8080:8080 \
-v "$(pwd)/dags:/opt/airflow/dags" \
--entrypoint=/bin/bash \
--name airflow \
apache/airflow:2.0.0-python3.8 \
-c '(
airflow db init && \
airflow users create --username admin --password admin --firstname Anonymous --lastname Admin --role Admin --email admin@example.org \
); \
airflow webserver & \
airflow scheduler'

```

Загруженные фотографии ракет можно посмотреть: 
```
docker exec -it airflow ls /tmp/images
```
Путь к файлам в контейнере: ```airflow@d5958612f3a5:/tmp/images/```