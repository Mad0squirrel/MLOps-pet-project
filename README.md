# Проект по прогнозу цены на недвижимость

## Архитектура системы

![Архитектура системы](https://github.com/Mad0squirrel/MLOps-pet-project/blob/master/visual/architecture-1.png)

## Исследование

- Данные версионируются с помощью DVC
- Для каждого этапа обработки данных создан CLI-скрипт
- Эксперименты логируются с помощью MLflow

Даг обработки данных
```mermaid
flowchart TD                       
        node1["add_coordinates"]   
        node2["clean_data"]        
        node3["download_amenities"]
        node4["download_raw_data"] 
        node5["finalize_data"]     
        node1-->node5              
        node2-->node1              
        node2-->node5              
        node3-->node5              
        node4-->node2
```

![Бакеты в S3-хранилище](https://github.com/Mad0squirrel/MLOps-pet-project/blob/master/visual/minio-1.png)
![Эксперименты](https://github.com/Mad0squirrel/MLOps-pet-project/blob/master/visual/mlflow-1.png)
![Артефакты модели](https://github.com/Mad0squirrel/MLOps-pet-project/blob/master/visual/mlflow-2.png)

## Инфраструктура

- Minio (бакеты для DVC и MLflow)
- MLflow, PostgreSQL, PgAdmin
- Prometheus, Loki, Grafana

![Мониторинг в Grafana](https://github.com/Mad0squirrel/MLOps-pet-project/blob/master/visual/grafana-1.png)

## Бэкенд, сервинг модели

- FastAPI, Catboost
- Загружает актуальную модель из Model Registry
- Отправляет логи в Loki
- Отдает метрики для Prometheus

![Swagger документация](https://github.com/Mad0squirrel/MLOps-pet-project/blob/master/visual/swagger-1.png)

## Фронтенд

- Vite, React, Maplibre, MUI
- Предоставляет пользователю интерфейс в виде карты
- Аналитика распределения квартир
- Прогноз стоимости на основе характеристик дома и квартиры

![Аналитика конкурентов](https://github.com/Mad0squirrel/MLOps-pet-project/blob/master/visual/application-2.png)
![Прогноз по характеристикам](https://github.com/Mad0squirrel/MLOps-pet-project/blob/master/visual/application-3.png)