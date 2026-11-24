# Загрузка данных в Unity Catalog

**Источник:** https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/

## Цель модуля

Научиться выбирать и реализовывать способ загрузки данных в Unity Catalog в Azure Databricks: управляемые коннекторы Lakeflow Connect, notebooks (DataFrame и Structured Streaming), SQL-методы (CTAS, CREATE OR REPLACE TABLE, COPY INTO), CDC-потоки с AUTO CDC API, потоковая загрузка из Kafka и Event Hubs, Auto Loader и оркестрация через Lakeflow pipelines.

## Ключевые понятия

- **Lakeflow Connect** - управляемые коннекторы для источников: SaaS (Salesforce, HubSpot, Jira, Workday), база данных с CDC (MySQL, PostgreSQL, SQL Server; через ingestion gateway), query-based (запросы по cursor-колонке без CDC).
- **Ingestion gateway (шлюз загрузки)** - компонент Lakeflow Connect, который читает изменения из журнала источника.
- **SCD type 1 / SCD type 2** - перезапись текущего состояния или хранение истории (колонки `__START_AT` и `__END_AT`).
- **Full refresh (полная перезагрузка)** - очистка и повторная загрузка таблицы.
- **CTAS (CREATE TABLE AS SELECT)** - создание таблицы из запроса; падает, если таблица уже существует.
- **CREATE OR REPLACE TABLE** - полная замена содержимого с сохранением прав и истории.
- **COPY INTO** - идемпотентная загрузка файлов: уже загруженные файлы пропускаются.
- **read_files** - табличная функция для чтения файлов в SQL.
- **AUTO CDC API** - API Lakeflow для применения вставок, обновлений и удалений; обрабатывает запоздавшие события по sequence-колонке.
- **Structured Streaming** - потоковая обработка через `spark.readStream` и `writeStream`; checkpoint обеспечивает отказоустойчивость.
- **Trigger (триггер)** - режим запуска микропакетов: по умолчанию, processingTime, availableNow.
- **Auto Loader (cloudFiles)** - источник, который инкрементально обнаруживает новые файлы в облачном хранилище; режимы directory listing и file notification.
- **cloudFiles.schemaEvolutionMode** - режим эволюции схемы: addNewColumns, addNewColumnsWithTypeWidening, rescue, failOnNewColumns, none.
- **_rescued_data** - колонка для данных, которые не соответствуют схеме.
- **Lakeflow pipelines (Spark Declarative Pipelines)** - декларативный фреймворк с streaming tables и flows.
- **Streaming table (потоковая таблица)** - Delta-таблица для потоковой загрузки с обработкой каждой строки ровно один раз.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/1-introduction

Загрузка данных из пакетных файлов, потоков Kafka и транзакционных БД в единую платформу с управлением. Способы: managed connectors (Lakeflow Connect), notebooks, SQL-команды (COPY INTO, CTAS), Structured Streaming и Auto Loader, оркестрация через Lakeflow pipelines.

### 2. Ingest data with Lakeflow Connect
https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/2-ingest-data-lakeflow-connect

Три типа коннекторов: SaaS, Database connectors (CDC через gateway) и query-based (по cursor-колонке; без gateway и staging). Пайплайн состоит из подключения (connection), определения загрузки (ingestion definition) и расписания. Для SQL Server создается шлюз. Описаны SCD type 1 и 2, include_columns и exclude_columns, full refresh и несколько назначений.

### 3. Ingest data with notebooks
https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/3-ingest-data-notebooks

Пакетная загрузка через `spark.read` (CSV, JSON, Parquet, XML с rowTag). JDBC-подключение к БД с секретами из `dbutils.secrets` и выталкиванием запроса (pushdown) в подзапрос. Запись в Unity Catalog: `saveAsTable`, режимы overwrite, append, ignore, error. Потоковая загрузка через `spark.readStream` (Kafka, файлы со явной схемой) и `writeStream` с checkpoint. Для полуструктурированных данных - тип VARIANT, `parse_json` и `variant_get`.

### 4. Ingest data with SQL methods
https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/4-ingest-data-sql-methods

CTAS - создание таблицы из запроса (падает, если таблица существует). CREATE OR REPLACE TABLE - полная замена с сохранением прав и истории. COPY INTO - инкрементальная загрузка файлов, пропускает уже загруженные; требует существующей таблицы. Опции PATTERN, FILES, mergeSchema, VALIDATE ALL. COPY INTO подходит для тысяч файлов, для миллионов рекомендуется Auto Loader или streaming tables.

### 5. Ingest data with CDC feed
https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/5-ingest-data-change-data-capture-feed

CDC-запись содержит данные, тип операции и sequence-колонку. AUTO CDC API (`create_auto_cdc_flow` в Python и `AUTO CDC INTO` в SQL) применяет изменения по ключам; `stored_as_scd_type` задает SCD 1 или 2; `apply_as_deletes` определяет удаления; `ignore_null_updates` (IGNORE NULL UPDATES) не перезаписывает значения null при частичных обновлениях. Запоздавшие события игнорируются по сравнению sequence-значений.

### 6. Ingest data with Spark Structured Streaming
https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/6-ingest-data-spark-structured-streaming

Structured Streaming обрабатывает поток как неограниченную таблицу. Kafka и Event Hubs (через Kafka-совместимый интерфейс с SASL_SSL и строкой подключения из секретов) или нативный коннектор `eventhubs` (payload в колонке body). Каждый запрос должен иметь свою checkpoint-папку. Триггеры: по умолчанию, processingTime, availableNow (обработать все доступное и остановиться; `once` устарел). Состояние запроса: isActive, status, recentProgress.

### 7. Ingest data with Auto Loader
https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/7-ingest-data-auto-loader

Auto Loader (`format("cloudFiles")`) инкрементально отслеживает новые файлы и обрабатывает каждый ровно один раз. Режимы: directory listing и file notification (рекомендуется в production с file events во внешнем location Unity Catalog). Параметры: cloudFiles.format, cloudFiles.schemaLocation, cloudFiles.inferColumnTypes (по умолчанию JSON и CSV все колонки - строки), schemaHints, maxFilesPerTrigger, maxBytesPerTrigger. Колонка _metadata содержит сведения о файле. Схема: см. режимы эволюции в таблице модуля.

### 8. Ingest data with Lakeflow pipelines
https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/8-ingest-data-lakeflow-declarative-pipelines

Lakeflow pipelines: streaming tables как цели, flows для нескольких источников (`CREATE FLOW ... INSERT INTO ... BY NAME`; в Python `@dp.append_flow`). Чекпоинты ведет сам pipeline; переименование flow сбрасывает checkpoint. Есть чтение из Kafka через `read_kafka` и Event Hubs через Kafka-интерфейс; параметры конфигурации pipeline вместо жесткого кода. Для JSON - `from_json` с `schemaLocationKey` и `schemaEvolutionMode`.

### 9. Exercise - Ingest Data into Unity Catalog
https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/9-exercise-ingest-data-into-unity-catalog

Практическое задание (около 45 минут): загрузка CSV из управляемого volume Unity Catalog в Delta-таблицы через DataFrame, `COPY INTO` и `CREATE TABLE AS SELECT`; настройка Auto Loader для новых файлов. Нужна подписка Azure с правами администратора.

### 10. Module assessment
https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/10-knowledge-check

Проверка знаний (около 5 минут). Текст вопросов в источнике не приведен.

### 11. Summary
https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/11-summary

Подведены итоги: managed connectors с CDC и SCD; notebooks для гибкой логики; CTAS, CREATE OR REPLACE и COPY INTO для файлов; CDC через AUTO CDC API; потоковая загрузка из Kafka и Event Hubs; Auto Loader для файлов с эволюцией схемы; Lakeflow pipelines для оркестрации.

## Важные команды / код / настройки

**Lakeflow Connect (фрагменты конфигурации из источника):**
```
resources:
  pipelines:
    pipeline_sqlserver:
      name: customer-orders-pipeline
      catalog: sales
      schema: bronze
      ingestion_definition:
        ingestion_gateway_id: ${resources.pipelines.gateway.id}
        objects:
          - table:
              source_schema: dbo
              source_table: orders
              destination_catalog: sales
              destination_schema: bronze
```
```
table_configuration:
  scd_type: SCD_TYPE_2
  sequence_by: last_modified
```
```
table_configuration:
  include_columns:
    - customer_id
    - order_date
    - total_amount
```
Примечание из источника: при `include_columns` новые колонки источника не попадают в назначение; при `exclude_columns` - попадают.

**Notebook (пакетная загрузка и запись):**
```
df = (spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load("/Volumes/catalog/schema/volume/data.csv"))
```
```
df_jdbc = (spark.read
    .format("jdbc")
    .option("url", "jdbc:sqlserver://server.database.windows.net:1433;database=mydb")
    .option("dbtable", "schema.tablename")
    .option("user", dbutils.secrets.get(scope="jdbc", key="username"))
    .option("password", dbutils.secrets.get(scope="jdbc", key="password"))
    .load())
```
```
df.write.mode("overwrite").saveAsTable("catalog.schema.table_name")
```

**Потоковая запись (notebook):**
```
(df_stream
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/checkpoints/my-stream")
    .toTable("catalog.schema.streaming_table"))
```
```
(parsed_df.writeStream
    .format("delta")
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)
    .toTable("catalog.schema.table_name"))
```

**Kafka и Event Hubs (Kafka-интерфейс):**
```
kafka_options = {
    "kafka.bootstrap.servers": f"{eh_namespace}.servicebus.windows.net:9093",
    "subscribe": eh_name,
    "kafka.sasl.mechanism": "PLAIN",
    "kafka.security.protocol": "SASL_SSL",
    "kafka.sasl.jaas.config": f'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{connection_string}";'
}
```
Строка подключения хранится в секрете (`dbutils.secrets.get(scope="eventhubs", key="connection-string")`).

**Нативный коннектор Event Hubs:** формат `eventhubs`, опции `eventhubs.connectionString`, `eventhubs.consumerGroup` (по умолчанию `$Default`), `eventhubs.startingPosition` (например, offset `-1` - последние события).

**SQL-загрузка:**
```
CREATE TABLE catalog.schema.customers AS
SELECT customer_id, UPPER(customer_name) AS customer_name, email, created_date
FROM external_staging.raw_customers
WHERE customer_status = 'active';
```
```
CREATE OR REPLACE TABLE catalog.schema.products AS
SELECT * FROM read_files(
    '/Volumes/catalog/schema/volume/products.csv',
    format => 'csv',
    header => true
);
```
```
COPY INTO catalog.schema.events
FROM '/Volumes/catalog/schema/volume/events/'
FILEFORMAT = JSON
FORMAT_OPTIONS ('multiline' = 'true');
```
```
COPY INTO catalog.schema.orders
FROM '/Volumes/catalog/schema/volume/orders/'
FILEFORMAT = PARQUET
PATTERN = 'orders_2024*.parquet';
```
```
COPY INTO catalog.schema.sensor_data
FROM '/Volumes/catalog/schema/volume/sensors/'
FILEFORMAT = CSV
VALIDATE ALL;
```

**AUTO CDC (Python):**
```
dp.create_auto_cdc_flow(
    target="employees",
    source="employees_cdf",
    keys=["employee_id"],
    sequence_by=col("sequence_num"),
    apply_as_deletes=expr("operation = 'DELETE'"),
    except_column_list=["operation", "sequence_num"],
    stored_as_scd_type=1
)
```
**AUTO CDC (SQL):**
```
CREATE FLOW employees_cdc_flow
AS AUTO CDC INTO employees
FROM stream(bronze.employee_changes)
KEYS (employee_id)
APPLY AS DELETE WHEN operation = 'DELETE'
SEQUENCE BY sequence_num
COLUMNS * EXCEPT (operation, sequence_num)
STORED AS SCD TYPE 1;
```
```
CREATE FLOW employees_history_flow
AS AUTO CDC INTO employees_history
FROM stream(bronze.employee_changes)
KEYS (employee_id)
SEQUENCE BY sequence_num
COLUMNS * EXCEPT (operation, sequence_num)
STORED AS SCD TYPE 2
TRACK HISTORY ON * EXCEPT (last_login);
```

**Auto Loader:**
```
(spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", schema_path)
  .load("abfss://container@storage.dfs.core.windows.net/incoming/orders/")
  .writeStream
  .option("checkpointLocation", checkpoint_path)
  .trigger(availableNow=True)
  .toTable("sales.bronze.orders"))
```
```
.option("cloudFiles.schemaEvolutionMode", "rescue")
.option("rescuedDataColumn", "my_rescued_data")
.option("cloudFiles.schemaHints", "order_date DATE, amount DECIMAL(10,2)")
.option("cloudFiles.maxFilesPerTrigger", "1000")
.option("cloudFiles.maxBytesPerTrigger", "1g")
```
Для схем: `addNewColumns` - поток останавливается, новые колонки добавляются при перезапуске; `addNewColumnsWithTypeWidening` - требует Databricks Runtime 16.4+; `rescue` - схема не меняется, новые колонки в `_rescued_data`; `failOnNewColumns`; `none`.

**Мониторинг и SQL-функция:** `SELECT * FROM cloud_files_state('/path/to/checkpoint');`; метрики numFilesOutstanding и numBytesOutstanding.

**SQL read_files с Auto Loader в pipeline:**
```
CREATE OR REFRESH STREAMING TABLE bronze_orders
AS SELECT * FROM STREAM read_files(
  'abfss://container@storage.dfs.core.windows.net/incoming/orders/',
  format => 'json'
)
```

**Lakeflow pipeline (Python) с flows:**
```
dp.create_streaming_table("orders_us")
@dp.append_flow(target="orders_us")
def orders_west_flow():
    return spark.readStream.table("orders_west")
```

**Kafka в pipeline (SQL):**
```
CREATE OR REFRESH STREAMING TABLE events_raw
AS SELECT *
FROM STREAM read_kafka(
  bootstrapServers => 'kafka_server:9092',
  subscribe => 'events_topic'
)
```

## Что запомнить

- Для управляемых источников (SQL Server, Salesforce) используйте Lakeflow Connect: он дает CDC и SCD без собственного кода.
- COPY INTO подходит для тысяч файлов и пропускает уже загруженные; для миллионов файлов рекомендуется Auto Loader.
- Каждый потоковый запрос требует уникального checkpoint; общий checkpoint приводит к ошибкам обработки.
- Для CDC используйте AUTO CDC API с sequence-колонкой: он корректно обрабатывает запоздавшие события.
- Auto Loader по умолчанию читает JSON и CSV как строки; для типов задайте `cloudFiles.inferColumnTypes` или `schemaHints`.
- В Lakeflow pipelines checkpoint и эволюцию схемы ведет pipeline; переименование flow сбрасывает его checkpoint.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/ingest-data-into-unity-catalog/
- В источнике упоминаются (без ссылок в тексте): Lakeflow Connect; AUTO CDC API; Auto Loader; COPY INTO; read_files; Structured Streaming; Lakeflow pipelines; Event Hubs Kafka-compatible endpoint.
