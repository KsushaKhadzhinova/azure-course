# Подготовка и обработка данных в Azure Databricks

**Источник** https://learn.microsoft.com/en-us/training/paths/azure-databricks-data-engineer-prepare-process-data

## О курсе

Построение надежных масштабируемых решений инженерии данных с Azure Databricks и Unity Catalog.

- **Уровень:** средний (Intermediate)
- **Роль:** Data Engineer
- **Продукты и сервисы:** Azure Databricks, Unity Catalog
- **Предварительные требования:** Понимание рабочих областей Azure Databricks и концепций Unity Catalog; знакомство с SQL и Python; знание основ инженерии данных и хранилищ данных.

## Чему научитесь

- Проектирование моделей данных в Unity Catalog.
- Прием данных (ingestion) из разных источников.
- Очистка, трансформация и загрузка сырых данных в пригодные для аналитики форматы.
- Контроль качества данных в архитектуре lakehouse.

## Модули

1. **Проектирование и реализация моделирования данных в Azure Databricks с Unity Catalog**. Научиться принимать ключевые решения по моделированию данных в lakehouse Azure Databricks: выбирать стратегию и инструмент загрузки, формат таблиц (Delta Lake или Apache Iceberg), схему партиционирования и кластеризации, тип slowly changing dimension (SCD), гранулярность и тип таблицы (managed или external), а также реализовывать историю изменений. [guide](../modules/design-implement-data-modeling-unity-catalog.md)
2. **Загрузка данных в Unity Catalog**. Научиться выбирать и реализовывать способ загрузки данных в Unity Catalog в Azure Databricks: управляемые коннекторы Lakeflow Connect, notebooks (DataFrame и Structured Streaming), SQL-методы (CTAS, CREATE OR REPLACE TABLE, COPY INTO), CDC-потоки с AUTO CDC API, потоковая загрузка из Kafka и Event Hubs, Auto Loader и оркестрация через Lakeflow pipelines. [guide](../modules/ingest-data-into-unity-catalog.md)
3. **Очистка, преобразование и загрузка данных в Unity Catalog**. Научиться профилировать данные, выбирать типы колонок, устранять дубликаты и пропуски, фильтровать, группировать и агрегировать, объединять таблицы (join и set-операторы), менять форму данных (denormalization, PIVOT, UNPIVOT) и загружать результаты в таблицы Unity Catalog стратегиями append, overwrite и merge. [guide](../modules/cleanse-transform-load-data-into-unity-catalog.md)
4. **Реализация и управление ограничениями качества данных в Unity Catalog**. Научиться обеспечивать качество данных в Azure Databricks с помощью Unity Catalog: проверять типы и приводить их (schema enforcement, cast и try_cast), задавать CHECK и NOT NULL-ограничения, проверять null, уникальность и диапазоны, управлять schema drift и настраивать pipeline expectations в Lakeflow. [guide](../modules/implement-manage-data-quality-constraints-unity-catalog.md)

## Ключевые технологии и понятия

- Extraction type
- Lakeflow Connect
- Auto Loader
- COPY INTO
- Delta Lake / Apache Iceberg
- Partition pruning
- Liquid clustering
- Z-ordering
- Deletion vectors
- SCD Type 0, 1, 2, 3
- Change data feed (CDF)
- Managed и external таблицы
- Гранулярность (grain)
- Ingestion gateway (шлюз загрузки)

## Для каких ролей полезно

- Data Engineer (DE, инженер данных)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/azure-databricks-data-engineer-prepare-process-data
- Модуль «Проектирование и реализация моделирования данных в Azure Databricks с Unity Catalog»: https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/
- Модуль «Загрузка данных в Unity Catalog»: https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/
- Модуль «Очистка, преобразование и загрузка данных в Unity Catalog»: https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/
- Модуль «Реализация и управление ограничениями качества данных в Unity Catalog»: https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/
