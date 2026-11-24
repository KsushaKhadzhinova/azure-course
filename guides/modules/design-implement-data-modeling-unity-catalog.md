# Проектирование и реализация моделирования данных в Azure Databricks с Unity Catalog

**Источник:** https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/

## Цель модуля

Научиться принимать ключевые решения по моделированию данных в lakehouse Azure Databricks: выбирать стратегию и инструмент загрузки, формат таблиц (Delta Lake или Apache Iceberg), схему партиционирования и кластеризации, тип slowly changing dimension (SCD), гранулярность и тип таблицы (managed или external), а также реализовывать историю изменений.

## Ключевые понятия

- **Extraction type** — способ извлечения данных из источника: полный (full), инкрементальный (incremental), потоковый (streaming) или CDC.
- **Lakeflow Connect** — управляемые коннекторы для SaaS-приложений, баз данных и потоков.
- **Auto Loader** — инкрементальная обработка файлов в облачном хранилище с отслеживанием состояния в checkpoint.
- **COPY INTO** — пакетная загрузка из облачного хранилища в Delta-таблицы, идемпотентная.
- **Delta Lake / Apache Iceberg** — табличные форматы поверх Parquet с транзакционным журналом.
- **Partition pruning** — пропуск партиций, не соответствующих фильтру запроса.
- **Liquid clustering** — современная кластеризация для Delta-таблиц; ключи можно менять без перезаписи данных.
- **Z-ordering** — устаревший способ колокации данных через `OPTIMIZE ... ZORDER BY`.
- **Deletion vectors** — пометки удаленных строк в отдельном метафайле вместо немедленной перезаписи Parquet-файла.
- **SCD Type 0, 1, 2, 3** — стратегии изменения атрибутов измерений; Type 2 сохраняет полную историю с суррогатными ключами.
- **Change data feed (CDF)** — журнал построчных изменений Delta-таблицы (insert, update_preimage, update_postimage, delete).
- **Managed и external таблицы** — managed данные управляет Unity Catalog; у external файлы остаются в указанном местоположении.
- **Гранулярность (grain)** — уровень детализации строки таблицы.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/1-introduction

Введение: решения по загрузке, формату таблиц и партиционированию влияют на все последующие запросы. Модуль охватывает проектирование ingestion, выбор инструментов, форматов, SCD и управляемых таблиц.

### 2. Design ingestion logic and data source configuration
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/2-design-data-ingestion-logic

Три типа извлечения: полное (для малых объемов или без change tracking), инкрементальное (по timestamp или sequence) и потоковое (для данных за секунды или минуты). CDC сохраняет тип операции и позволяет корректно реплицировать удаления. Для файлов рекомендованы колоночные форматы (Parquet, ORC). Описаны конфигурации для облачных хранилищ, баз данных, потоков и SaaS. Приведен пошаговый фреймворк: требования, выбор типа извлечения, формата и проверка проекта. Пример: PostgreSQL, почасовая отчетность, инкрементальное извлечение по `order_updated_at`, Parquet в ADLS.

### 3. Choose a data ingestion tool
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/3-choose-data-ingestion-tool

Инструменты от наиболее управляемых к наиболее гибким: Lakeflow Connect (SaaS, database с CDC, query-based и community connectors), Auto Loader (файлы), COPY INTO (пакетная SQL-загрузка), Spark Structured Streaming (полный контроль), JDBC/ODBC в notebook. Azure Data Factory используется для оркестрации и первичной загрузки данных, а трансформации лучше выполнять в Azure Databricks.

### 4. Choose a data table format
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/4-choose-data-table-format

Parquet хранит данные по колонкам и использует статистики row group для пропуска данных. Delta Lake — формат по умолчанию: ACID, time travel, эволюция схемы, единый батч и стриминг. Apache Iceberg выбирают для совместимости с другими платформами (Snowflake, Athena, Trino, Spark, Flink). CSV и JSON подходят для landing zone и отладки, но для хранения лучше конвертировать в Delta.

### 5. Design and implement a data partitioning scheme
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/5-design-data-partitioning-scheme

Партиционирование рекомендуется для таблиц более 1 ТБ; каждая партиция должна содержать не менее 1 ГБ данных. Ключи должны иметь низкую кардинальность и соответствовать фильтрам запросов. Партиции меняются только перезаписью таблицы. Описаны `PARTITIONED BY`, `partitionBy` и generated columns. Для таблиц меньшего размера и при неопределенных запросах предлагается liquid clustering.

### 6. Choose a slowly changing dimension (SCD) type
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/6-choose-slowly-changing-dimension-type

Разбор на примере перемещения клиента из Seattle в Portland. Type 0 — значение не меняется. Type 1 — перезапись без истории. Type 2 — новая строка на каждую версию с суррогатным ключом, датами действия и флагом текущей версии. Type 3 — хранится только предыдущее значение в отдельной колонке. Рекомендуется смешивать типы для разных атрибутов.

### 7. Implement a slowly changing dimension (SCD) type 2
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/7-implement-slowly-changing-dimension-type-2

Создание таблицы `sales.customer` с identity-ключом, `valid_from`, `valid_to`, `is_current` и включенным change data feed. Реализация через MERGE и последующий INSERT новых версий. Запросы: точка во времени, история клиента, time travel (`TIMESTAMP AS OF`, `VERSION AS OF`). Рекомендуется Lakeflow pipelines с AUTO CDC API.

### 8. Design and implement a temporal (history) table to record changes over time
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/8-design-temporal-history-table

Temporal-таблицы фиксируют технические изменения для отладки и аудита, в отличие от SCD2, который описывает бизнес-версии. Включение change data feed (он выключен по умолчанию и не захватывает прошлые изменения). Запросы через `table_changes`, time travel и `DESCRIBE HISTORY`. Для долгосрочного аудита история переносится в отдельную таблицу через Structured Streaming. Для соответствия требованиям настраиваются сроки хранения.

### 9. Choose granularity on a column or table based on requirements
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/9-choose-granularity

Гранулярность — уровень детализации строки. Агрегированные данные нельзя детализировать обратно, поэтому часто начинают с атомарной гранулярности. Выбор зависит от бизнес-требований, шаблонов запросов, стоимости хранения и вычислений, а также от требований комплаенса. Для таблиц фактов гранулярность определяется набором ключей измерений; для измерений — выбранным способом версионирования (Type 1, Type 2 или периодические снимки).

### 10. Choose managed vs external tables
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/10-choose-managed-vs-unmanaged-tables

Managed-таблицы: Unity Catalog управляет метаданными и файлами; доступны predictive optimization, automatic liquid clustering, кэширование метаданных и UNDROP (в течение 8 дней). Поддерживаются только Delta Lake и Apache Iceberg. External-таблицы: файлы остаются при DROP TABLE, поддерживаются CSV, JSON, Avro, Parquet, ORC и текст. Databricks рекомендует managed-таблицы для большинства случаев.

### 11. Design and implement a clustering strategy
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/11-design-clustering-strategy

Механизм data skipping на основе статистик файлов. Liquid clustering рекомендован для новых таблиц: до четырех ключей, инкрементальный `OPTIMIZE`, смена ключей через `ALTER TABLE ... CLUSTER BY`, `CLUSTER BY AUTO`. Z-ordering — устаревший подход. Deletion vectors позволяют быстрее обновлять и удалять строки; для физического удаления используются `REORG TABLE ... APPLY (PURGE)` и `VACUUM`.

### 12. Exercise - Design and Implement Data Modeling with Azure Databricks
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/12-exercise-design-implement-data-modeling-unity-catalog

Практика (около 45 минут): модель Delta Lake в Unity Catalog для банка — таблица клиентов с SCD Type 2, таблица транзакций с liquid clustering, Change Data Feed для аудита и time travel для просмотра и восстановления версий. Нужна подписка Azure с правами администратора.

### 13. Knowledge check
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/13-knowledge-check

Проверочный тест (около 5 минут). Вопросы и ответы в источнике не приведены.

### 14. Summary
https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/14-summary

Итоги: проектирование загрузки, выбор Delta Lake или Iceberg, партиционирование для таблиц более 1 ТБ, SCD для исторической точности, гранулярность, liquid clustering и managed-таблицы с predictive optimization.

## Важные команды / код / настройки

**Liquid clustering:**

```
CREATE TABLE sales.transactions (
    transaction_id STRING,
    customer_id STRING,
    product_category STRING,
    region STRING,
    transaction_date DATE,
    amount DECIMAL(12,2)
)
CLUSTER BY (region, transaction_date);

OPTIMIZE sales.transactions;
ALTER TABLE sales.transactions
CLUSTER BY (customer_id, transaction_date);
OPTIMIZE sales.transactions FULL;
CREATE TABLE sales.orders CLUSTER BY AUTO;
ALTER TABLE sales.transactions CLUSTER BY AUTO;
```

Ключей не более четырех. `CLUSTER BY AUTO` требует включенного predictive optimization.

**Z-ordering (устаревший):** `OPTIMIZE sales.legacy_transactions ZORDER BY (region, transaction_date);`

**Миграция с Z-ordering:** `ALTER TABLE ... CLUSTER BY (...)`, затем `OPTIMIZE ... FULL`. Liquid clustering несовместим с партиционированием. Требуется Databricks Runtime 13.3 LTS или выше.

**Deletion vectors:**

```
ALTER TABLE sales.transactions
SET TBLPROPERTIES ('delta.enableDeletionVectors' = true);

REORG TABLE sales.transactions APPLY (PURGE);
VACUUM sales.transactions;
```

По умолчанию включены для новых таблиц в Databricks Runtime 14.1 и выше.

**Партиционирование:**

```
CREATE TABLE sales.transactions (...)
PARTITIONED BY (transaction_date);
```

PySpark: `df.write.format("delta").partitionBy("transaction_date").saveAsTable("sales.transactions")`. Рекомендации: таблицы более 1 ТБ, партиции не менее 1 ГБ.

**Таблица SCD Type 2:**

```
CREATE TABLE sales.customer (
    customer_sk BIGINT GENERATED ALWAYS AS IDENTITY,
    customer_id STRING NOT NULL,
    customer_name STRING,
    email STRING,
    city STRING,
    region STRING,
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP NOT NULL,
    is_current BOOLEAN
)
USING DELTA
TBLPROPERTIES (
    delta.enableChangeDataFeed = true
);
```

Текущая версия: `valid_to = 9999-12-31`, `is_current = true`. Точечный запрос: `WHERE valid_from <= '<дата>' AND valid_to > '<дата>'`.

**Change data feed:**

```
CREATE TABLE bronze.sales_transactions (...)
USING DELTA
TBLPROPERTIES (delta.enableChangeDataFeed = true);

SELECT transaction_id, amount, _change_type, _commit_version, _commit_timestamp
FROM table_changes('bronze.sales_transactions', '2026-01-01', '2026-01-31')
WHERE _change_type IN ('insert', 'update_postimage')
ORDER BY _commit_timestamp;
```

CDF фиксирует изменения только после включения. Метаданные: `_change_type` (insert, update_preimage, update_postimage, delete), `_commit_version`, `_commit_timestamp`.

**Time travel и история:**

- `SELECT * FROM <table> TIMESTAMP AS OF '2026-01-15 14:30:00';`
- `SELECT * FROM <table> VERSION AS OF 42;`
- `DESCRIBE HISTORY bronze.sales_transactions;`

**Сроки хранения (пример из источника):**

```
ALTER TABLE bronze.sales_transactions
SET TBLPROPERTIES (
    delta.logRetentionDuration = 'interval 90 days',
    delta.deletedFileRetentionDuration = 'interval 90 days'
);
```

Значения по умолчанию: файлы данных 7 дней, журнал 30 дней (в уроке 8). Эти свойства задаются вместе.

**Архив истории через Structured Streaming:**

```
(spark.readStream
    .option("readChangeFeed", "true")
    .option("ignoreDeletes", "false")
    .table("bronze.sales_transactions")
    .writeStream
    .option("checkpointLocation", "/checkpoints/sales_history")
    .trigger(availableNow=True)
    .toTable("audit.sales_transactions_history")
)
```

**Auto Loader и COPY INTO:** Auto Loader — непрерывная инкрементальная загрузка файлов с checkpoint; COPY INTO — идемпотентная пакетная загрузка, отслеживание хранится в `_delta_log`.

**Структура landing zone:** Hive-style партиции `year=2025/month=11/day=28/`; папки `/incoming/`, `/processing/`, `/archive/`, `/failed/`.

**Безопасность:** учетные данные хранить в Databricks secrets; для облачных хранилищ использовать Unity Catalog external locations.

## Что запомнить

- Начинайте с управляемых инструментов (Lakeflow Connect, Auto Loader), переходите к более гибким только при необходимости.
- Delta Lake — формат по умолчанию; Iceberg выбирайте ради совместимости с другими платформами.
- Партиционирование имеет смысл для таблиц более 1 ТБ с партициями не менее 1 ГБ; для остальных используйте liquid clustering.
- SCD Type 2 нужен там, где важна историческая точность; Type 1 — для исправлений и контактных данных.
- Change data feed включайте до загрузки продуктивных данных: он не захватывает прошлые изменения.
- Managed-таблицы рекомендованы для большинства случаев; external-таблицы не удаляют файлы при DROP TABLE.

## Связанные материалы

- Lakeflow Connect managed connectors (документация, упоминается в уроке 3).
- Change data capture pipelines и AUTO CDC API (упоминаются в уроке 7).
- Predictive optimization и managed Iceberg tables в Unity Catalog (упоминаются в уроках 4, 10 и 11).
- Delta Lake time travel и retention settings (уроки 7 и 8).
