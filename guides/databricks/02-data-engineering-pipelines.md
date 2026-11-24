# Data Engineering на Azure Databricks: ingestion, pipelines, streaming, jobs

Конспект для изучения инженерии данных на Azure Databricks. Материал собран из markdown-копий документации и учебных модулей Microsoft Learn (список источников - в конце). Все примеры кода и SQL взяты из источников дословно или с минимальными заменами плейсхолдеров; там, где источники не дают ответа, это отмечено в разделе «Пробелы в источниках». Утверждения, которые являются моими выводами, а не фактами из источников, помечены как **Вывод конспекта**.

Английские термины (Auto Loader, streaming table, materialized view, expectation, checkpoint и т. д.) оставлены как есть.

---

## 0. Терминология и эволюция названий

В источниках встречаются несколько названий одного и того же семейства продуктов:

- **Lakeflow pipelines** - декларативные конвейеры на Azure Databricks. Построены на **Apache Spark Declarative Pipelines (SDP)** и совместимы с ним. В старых материалах и в API-справке встречается прежнее название **Delta Live Tables (DLT)**. Соответствие API: `@dlt.table` -> `@dp.table`, `@dlt.view` -> `@dp.temporary_view`, `@dlt.apply_changes(...)` -> `dp.create_auto_cdc_flow(...)`, `@dlt.expect(...)` -> `dp.expect(...)`.
- **Lakeflow Jobs** - оркестрация задач (бывшие Databricks Workflows / Jobs).
- **Lakeflow Connect** - коннекторы для загрузки данных (managed, file, database, SaaS, streaming).
- Lakeflow pipelines требуют план **Premium** (источник: страница `ldp`).

Ключевая мысль, которую повторяют все источники: Databricks рекомендует начинать с наиболее управляемого уровня (Lakeflow Connect / Lakeflow pipelines) и спускаться ниже (Structured Streaming API, Spark-ноутбуки) только если нужного не хватает.

---

## 1. Ingestion: загрузка данных

### 1.1. Уровни ингестии

Источник `ingestion/overview` описывает слои инструментов ингестии:

| Слой | Что это | Когда |
|---|---|---|
| Fully-managed connectors (Lakeflow Connect) | Коннекторы к SaaS, базам данных с CDC, автоматические retries и schema evolution | Популярные источники (Salesforce, SQL Server и др.) |
| Lakeflow pipelines | Декларативный фреймворк: вы описываете трансформации, движок управляет оркестрацией, мониторингом и качеством | Файлы из облачного хранилища, message buses, трансформации |
| SQL и Spark APIs | Auto Loader, COPY INTO, `spark.readStream`, Kafka и др. | Кастомизация там, где managed-слой не покрывает источник |
| Create or modify a table using file upload (Add data UI) | Загрузка локальных файлов в managed Delta-таблицу | Небольшие файлы вручную |
| DIY | Собственные коннекторы на Python/Java, Airbyte, Debezium и т. п. | Нет готового варианта |

Также Databricks рекомендует по возможности не копировать данные, а использовать **Lakehouse Federation** (запросы к внешним источникам без перемещения) или **OpenSharing** (безопасный обмен данными между платформами).

### 1.2. Auto Loader

**Auto Loader** инкрементально и эффективно обрабатывает новые файлы по мере их появления в облачном хранилище. Реализован как Structured Streaming source с именем **`cloudFiles`**.

Ключевые факты из источника `ingestion/cloud-object-storage/auto-loader`:

- Поддерживаемые источники: S3, **ADLS (`abfss://`)**, GCS, Unity Catalog volumes (`/Volumes/`), Azure Blob Storage (`wasbs://`; драйвер WASB помечен как deprecated, рекомендуется ABFS).
- Форматы файлов: JSON, CSV, XML, PARQUET, AVRO, ORC, TEXT, BINARYFILE; поддерживаются также предсжатые файлы.
- **Отслеживание прогресса**: метаданные обнаруженных файлов хранятся в RocksDB в checkpoint location. Это обеспечивает обработку **exactly once**, а при сбое Auto Loader продолжает с места остановки. Состояние вручную поддерживать не нужно.
- В Lakeflow pipelines указывать schema и checkpoint location не нужно - pipeline управляет ими сам.
- **Режимы обнаружения файлов**: directory listing (по умолчанию) и file notification. Databricks рекомендует file notification mode для большинства нагрузок.
- Порядок обнаружения и обработки файлов **не гарантируется** ни в одном режиме. Для Lakeflow pipelines с AUTO CDC нужно настраивать `pipelines.cdc.tombstoneGCThresholdInSeconds` (по умолчанию два дня).
- Преимущества над `spark.readStream.format(...)` на файлах: масштабируемость (миллиарды файлов, backfill асинхронно), стоимость обнаружения (масштабируется с числом файлов, а не директорий), schema inference и evolution с rescue данных, снижение облачных затрат в file notification mode.

Пример из источника `query/streaming` (SQL, чтение директории JSON из volume):

```sql
SELECT * FROM STREAM read_files('/Volumes/catalog/schema/volumes/path/to/files', format => 'json')
```

Пример потокового чтения (Python) из того же источника:

```python
display(spark.readStream.format("cloudFiles").option("cloudFiles.format", "json").load("/Volumes/catalog/schema/volumes/path/to/files"))
```

Пример создания streaming table из файлов, в том числе с расписанием (`sql/mv-st/streaming`):

```sql
CREATE OR REFRESH STREAMING TABLE sales
  SCHEDULE EVERY 1 hour
  AS SELECT * FROM STREAM read_files(
    "/Volumes/my_catalog/my_schema/my_volume/path/to/data",
    format => "json"
  );
```

Пример из учебного модуля (Python, Lakeflow pipelines, `@dp.table`):

```python
from pyspark import pipelines as dp

@dp.table
def customers_bronze():
  return (
    spark.readStream.format("cloudFiles")
     .option("cloudFiles.format", "json")
     .option("cloudFiles.inferColumnTypes", "true")
     .load("/Volumes/raw_data/customers")
  )
```

В источниках встречаются опции `cloudFiles.schemaLocation`, `cloudFiles.inferColumnTypes`, `cloudFiles.format`, `cloudFiles.useNotifications`, `cloudFiles.useManagedFileEvents`, `cloudFiles.cleanSource`, `cloudFiles.maxFilesPerTrigger`, `cloudFiles.maxBytesPerTrigger`, `cloudFiles.schemaHints`, `cloudFiles.schemaEvolutionMode`, `cloudFiles.includeExistingFiles`. Полное описание назначения каждой опции в собранных источниках не раскрыто (см. раздел «Пробелы»).

Опция `includeExistingFiles` в SQL `read_files` (по умолчанию файлы, уже лежащие в папке при создании таблицы, читаются):

```sql
CREATE OR REFRESH STREAMING TABLE sales
  SCHEDULE EVERY 1 hour
  AS SELECT *
  FROM STREAM read_files(
    '/path/to/files',
    includeExistingFiles => false
  );
```

### 1.3. COPY INTO

Источники дают `COPY INTO` меньше, чем Auto Loader. Из `d0-azure-databricks-delta` (раздел Delta Lake): COPY INTO позволяет **загружать данные инкрементально и идемпотентно из облачного хранилища с помощью SQL**. Пример из раздела ADLS (`azure-datalake-gen2`):

```sql
CREATE TABLE <database-name>.<table-name>;

COPY INTO <database-name>.<table-name>
FROM 'abfss://container@storageAccount.dfs.core.windows.net/path/to/folder'
FILEFORMAT = CSV
COPY_OPTIONS ('mergeSchema' = 'true');
```

Ограничения, которые видны из справочника ошибок:

- Целевая таблица должна быть **Delta** (`COPY INTO target must be a Delta table`).
- Поддерживаемые форматы файлов: CSV, JSON, AVRO, ORC, PARQUET, TEXT, BINARYFILE. Использовать Delta-таблицу в качестве источника `COPY INTO` нельзя.
- Операции, отличные от добавления данных (append), не могут выполняться одновременно с другими транзакциями на той же таблице. Ошибка: `Concurrent COPY INTO operation detected on the table`.
- Для `COPY INTO` из s3/s3n/s3a/wasbs/abfss допускаются credentials и encryption-опции, для ADLS Gen2 - только схема `abfss://`.

**Вывод конспекта:** для регулярной загрузки файлов в современных конвейерах источники рекомендуют Auto Loader (в том числе в виде streaming table). `COPY INTO` остается полезным SQL-инструментом для идемпотентной загрузки, но подробного руководства по его опциям в собранных источниках нет.

### 1.4. Доступ к ADLS Gen2

Источник `azure-datalake-gen2` перечисляет четыре способа аутентификации:

1. **OAuth 2.0 с Microsoft Entra ID service principal** - рекомендуемый Databricks вариант. Требует роли Storage Blob Data-уровня на аккаунте хранения (в источнике сказано: назначить роли может Owner или User Access Administrator).
2. **SAS-токены** - временный доступ с гранулярными правами; можно выдавать только те права, которые есть у самого выдающего.
3. **Account keys** - полный доступ к аккаунту; Databricks рекомендует вместо них service principal или SAS.
4. **Passthrough / Unity Catalog** - для governed-данных рекомендуется Unity Catalog (см. ниже).

Credentials рекомендуется хранить в **secret scope**. Настройка через Spark-свойства кластера (формат для cluster Spark configuration):

```
spark.hadoop.fs.azure.account.auth.type.<storage-account>.dfs.core.windows.net OAuth
spark.hadoop.fs.azure.account.oauth.provider.type.<storage-account>.dfs.core.windows.net org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider
spark.hadoop.fs.azure.account.oauth2.client.id.<storage-account>.dfs.core.windows.net <application-id>
spark.hadoop.fs.azure.account.oauth2.client.secret.<storage-account>.dfs.core.windows.net {{secrets/<secret-scope>/<service-credential-key>}}
spark.hadoop.fs.azure.account.oauth2.client.endpoint.<storage-account>.dfs.core.windows.net https://login.microsoftonline.com/<directory-id>/oauth2/token
```

То же в ноутбуке:

```python
service_credential = dbutils.secrets.get(scope="<secret-scope>",key="<service-credential-key>")

spark.conf.set("fs.azure.account.auth.type.<storage-account>.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.<storage-account>.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.<storage-account>.dfs.core.windows.net", "<application-id>")
spark.conf.set("fs.azure.account.oauth2.client.secret.<storage-account>.dfs.core.windows.net", service_credential)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.<storage-account>.dfs.core.windows.net", "https://login.microsoftonline.com/<directory-id>/oauth2/token")
```

Обращение к данным по URI (Databricks рекомендует драйвер `abfss`):

```python
spark.read.load("abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<path-to-data>")

dbutils.fs.ls("abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<path-to-data>")
```

Важные оговорки из источника:

- Hive metastore client **игнорирует** Spark-сессионные конфигурации, заданные через `spark.conf.set()` в ноутбуке. Для DDL, которому нужен доступ к хранилищу (например, `ALTER TABLE ... SET LOCATION`), credentials нужно задавать в Spark-конфигурации кластера.
- Blob storage не поддерживает Microsoft Entra ID service principals.

**Unity Catalog и хранилище.** Источник `connect/unity-catalog/cloud-storage`: для governed-данных используется **storage credential** (аутентификация к облачному ресурсу, в Azure - через managed identity или service principal) и **external location** (объект Unity Catalog, описывающий путь в хранилище). Прямой доступ identity к контейнерам ADLS, данные которых управляются Unity Catalog, **обходит** Unity Catalog и раскрывает данные без аудита и политик. Рекомендуемый вариант для файлов - **volumes** (`/Volumes/...`). Для ingestion, где данные копируются в другое место (Auto Loader, COPY INTO), источники рекомендуют external volumes.

### 1.5. Загрузка файлов через UI

Источник `ingestion/create-or-modify-table` (Add data UI):

- До **10 файлов** за раз, общий размер меньше **2 GB**.
- Допустимые расширения: `.csv`, `.tsv`/`.tab`, `.json`, `.avro`, `.parquet`, `.xlsx`/`.xls`/`.xlsm`, `.txt`. Zip и tar не поддерживаются.
- Загруженные файлы попадают в внутреннее staging-хранилище, которое очищается ежедневно.
- Заголовки и формат применяются ко всем файлам сразу; файлы объединяются добавлением строк (append).
- Автоматическое определение типов можно отключить: тогда все колонки будут `STRING`.
- Имена колонок не поддерживают запятые, обратные слеши и unicode-символы (эмодзи).

Это инструмент для разовых небольших загрузок, а не для продуктивной ингестии.

---

## 2. Медальонная архитектура (bronze / silver / gold)

Источник `lakehouse/medallion`: medallion architecture - шаблон логической организации данных, при котором качество и структура данных постепенно улучшаются при переходе от bronze к silver и gold. Также называется **multi-hop architecture**. Databricks называет ее рекомендуемой практикой, но не требованием.

| Вопрос | Bronze | Silver | Gold |
|---|---|---|---|
| Что происходит | Сырая ингестия | Очистка и валидация | Dimensional modeling и агрегации |
| Кто пользователь | Data engineers, data operations, compliance/audit | Data engineers, аналитики (детальные данные), data scientists | BI-аналитики, ML-инженеры, руководство, операционные команды |

Характеристики слоев из источника:

- **Bronze**: сохраняет исходное состояние данных и исходный формат, пополняется инкрементально, служит единым источником правды и позволяет переобработку и аудит. Может быть streaming или batch, из облачного хранилища, из message bus (Kafka, Kinesis) или через Lakehouse Federation. Минимальная валидация. Рекомендуется хранить большинство полей как `STRING`, `VARIANT` или binary, чтобы защититься от неожиданных изменений схемы; можно добавлять метаданные происхождения (например, `_metadata.file_name`).
- **Silver**: строится чтением из bronze или silver. Источник не рекомендует писать в silver напрямую из ingestion, потому что изменения схемы и битые записи в источнике приведут к сбоям. Если источники append-only, чтение из bronze лучше делать потоковым (streaming); batch-чтение - для небольших справочников. Должен содержать хотя бы одно валидированное, неагрегированное представление каждой записи. Здесь делаются очистка, дедупликация, нормализация, обработка out-of-order и late-arriving данных, type casting, joins.
- **Gold**: агрегированные, отфильтрованные по периодам или регионам данные, соответствующие бизнес-логике. Часто моделируется dimensional model. Может быть несколько gold-слоев под разные бизнес-домены (HR, finance, IT). Оптимизируется под запросы и дашборды.

Пример из источника (каталог `ops`, схемы `bronze`, `silver`, `gold`): silver содержит `customer_transactions`, `account_opportunities`, `leads_cleaned`; gold - `customer_spending`, `account_performance`, `sales_pipeline_summary`, `business_summary`.

Пример gold-агрегата (materialized view) из того же источника:

```sql
CREATE OR REPLACE MATERIALIZED VIEW main.example_output.weekly_bookings AS
SELECT date_trunc('week', check_in) AS week,
       property_id,
       status,
       count(*) AS total_bookings,
       sum(total_amount) AS total_revenue
FROM samples.wanderbricks.bookings
GROUP BY week, property_id, status
```

**Частота ингестии и стоимость.** Источник сравнивает три варианта:

| Вариант | Стоимость | Задержка | Как реализуется |
|---|---|---|---|
| Continuous incremental ingestion | Выше | Ниже | Streaming table (`spark.readStream`) с continuous pipeline; либо Structured Streaming в job с continuous trigger |
| Triggered incremental ingestion | Ниже | Выше | Streaming table, которую обновляет pipeline по расписанию или по file arrival trigger; либо `Trigger.AvailableNow` |
| Batch ingestion с ручной инкрементальностью | Ниже всего | Самая высокая (редкие запуски) | `spark.read` + перезапись партиций; требует партиционирования источника по дате |

---

## 3. Structured Streaming

Источник `structured-streaming/concepts`: два режима обработки.

- **Real-time mode (RTM)** - для операционных нагрузок с задержкой до субсекундной (источник упоминает латентность до 5 мс; примеры: fraud detection, real-time personalization).
- **Micro-batch mode** - режим по умолчанию, для аналитических пайплайнов и ETL, задержка измеряется секундами или минутами.

Оба режима используют одни и те же API; переключение - через trigger и конфигурацию compute.

### 3.1. Чтение и запись

- Чтение: Auto Loader, Delta-таблицы как источник (`spark.readStream.table`), SQL и Spark API для message bus (Kafka, Kinesis, Pub/Sub, Pulsar). Лимиты размера micro-batch (`maxFilesPerTrigger` и др.) не дают батчам расти бесконтрольно.
- Запись: **checkpoints** хранят состояние обработки для отказоустойчивости и exactly-once. Output modes: **append**, **update**, **complete** (для stateful-запросов).

Пример интерактивного чтения Kafka (Python) из `query/streaming`:

```python
display(spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "<server:ip>")
  .option("subscribe", "<topic>")
  .option("startingOffsets", "latest")
  .load()
)
```

Тот же пример в SQL:

```sql
SELECT * FROM STREAM read_kafka(
  bootstrapServers => '<server:ip>',
  subscribe => '<topic>',
  startingOffsets => 'latest'
);
```

Источник также предупреждает: примеры с `display()` и memory sink - только для интерактивной разработки. В продуктиве запрос должен писать в целевую таблицу или внешнюю систему.

Потоковое чтение Delta-таблицы (запросы подхватывают новые коммиты):

```sql
SELECT * FROM STREAM table_name
```

По умолчанию streaming-запросы ожидают, что исходная таблица содержит **только добавления**. Для обновлений и удалений Databricks рекомендует AUTO CDC в Lakeflow pipelines.

### 3.2. Triggers

Из `compute/serverless/limitations`:

- На **serverless** поддерживаются `Trigger.AvailableNow()` (рекомендуется Databricks) и `Trigger.Once()` (deprecated, но поддерживается).
- `Trigger.ProcessingTime(interval)` и `Trigger.Continuous(interval)` на serverless **не поддерживаются**. Если не задать trigger, Spark по умолчанию использует `Trigger.ProcessingTime("0 seconds")`, что на serverless приводит к ошибке `INFINITE_STREAMING_TRIGGER_NOT_SUPPORTED`. Нужно явно задать поддерживаемый trigger.
- Эти ограничения не относятся к режимам Lakeflow pipelines. Для непрерывной обработки на serverless источник предлагает serverless pipeline в continuous mode либо `Trigger.AvailableNow()` в continuous job.

Из `ingestion` и учебного модуля по triggers: continuous job на serverless поддерживает только bounded-триггеры (`Trigger.AvailableNow`), а time-based триггеры требуют classic jobs compute.

Пример быстрого запуска (Python, из `getting-started/etl-quick-start`, фрагмент с `availableNow`):

```python
(spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", checkpoint_path)
  .load(file_path)
  .select("*", col("_metadata.file_path").alias("source_file"), current_timestamp().alias("processing_time"))
  .writeStream
  .option("checkpointLocation", checkpoint_path)
  .trigger(availableNow=True)
  .toTable(table_name))
```

### 3.3. Watermarks и stateful-обработка

Stateful-запросы хранят промежуточное состояние для агрегаций, stream-stream joins и дедупликации. Watermark ограничивает, сколько система ждет опоздавших событий. Из `ldp/concepts/streaming-tables`: **unbounded stream без watermark может привести к падению пайплайна из-за нехватки памяти**. Streaming tables рассчитаны на naturally bounded streams (например, директория файлов, в которую больше ничего не попадает) или на потоки с watermark.

Из справочника ошибок (пример формулировки): `UNSUPPORTED_STREAMING_OPERATOR_WITHOUT_WATERMARK` - output mode не поддерживается для stateful-оператора на streaming DataFrame без watermark. Также `CANNOT_ASSIGN_EVENT_TIME_COLUMN_WITHOUT_WATERMARK`, и событийная колонка в `withWatermark` должна быть колонкой верхнего уровня (не вложенным полем).

Примеров кода с `withWatermark` в собранных источниках нет (см. «Пробелы»).

### 3.4. Checkpoints

- Checkpoint location обязателен: `checkpointLocation must be specified either through option("checkpointLocation", ...) or SparkSession.conf.set(...)`.
- Checkpoint хранит offsets и commit log. Ошибки вида `The commit log does not exist with checkpoint location` указывают на повреждение или неправильный путь checkpoint.
- Для Auto Loader схема (`cloudFiles.schemaLocation`) должна находиться под checkpoint location.
- Из источника Auto Loader: состояние обнаружения файлов (RocksDB) хранится в checkpoint; при удалении checkpoint обработка начнется заново.

---

## 4. Lakeflow Declarative Pipelines (DLT)

### 4.1. Основные понятия

Источник `ldp`: вы объявляете таблицы и трансформации в SQL или Python, а фреймворк сам строит граф зависимостей, выполняет инкрементальную обработку, retries и мониторинг. Из учебного модуля: retries выполняются на самом мелком уровне - сначала Spark task, затем flow, затем pipeline.

Основные объекты:

- **Flow** - запрос плюс, как правило, target. Default flow создается вместе с target: для streaming table это **append flow** с тем же именем. Можно добавлять дополнительные append flows в одну таблицу (например, backfill или несколько источников без UNION). Также есть **AUTO CDC flow** (только в streaming tables) и update flow (Python, Public Preview).
- **Streaming table** - Delta-таблица с поддержкой потоковой и инкрементальной обработки. Каждая входящая строка обрабатывается **один раз**. Принадлежит одному pipeline; другие pipelines таблицу не меняют.
- **Materialized view** - результат запроса, хранимый в кэше и обновляемый по интервалу или при triggered update. Источник: "They are always correct at the time of their update", часто инкрементальны. **Incremental refresh требует serverless compute; на classic compute materialized view полностью пересчитывается при каждом обновлении.**
- **View** (`@dp.temporary_view`) - не хранится, существует только в рамках pipeline.

Сравнение streaming table и materialized view из источников:

- Streaming table: для append-only источников и низкой задержки; **joins не пересчитываются при изменении измерений** ("fast-but-wrong"); изменение запроса не переписывает уже обработанные строки без **full refresh**.
- Materialized view: всегда корректна, даже при поздних данных; подходит для агрегатов и join-ов, где источник меняется с update и delete.

Пример streaming table (SQL) из источника `ldp/...` и учебного модуля:

```sql
CREATE OR REFRESH STREAMING TABLE customers_bronze
AS SELECT * FROM STREAM read_files(
  "/Volumes/raw_data/customers",
  format => "json"
);
```

Пример materialized view (Python):

```python
from pyspark import pipelines as dp

@dp.materialized_view
def regional_sales():
  partners_df = spark.read.table("partners")
  sales_df = spark.read.table("sales")

  return (
    partners_df.join(sales_df, on="partner_id", how="inner")
  )
```

Тот же пример в SQL:

```sql
CREATE OR REPLACE MATERIALIZED VIEW regional_sales
  AS SELECT *
  FROM partners
    INNER JOIN sales USING (partner_id);
```

Агрегация в materialized view (Python, учебный модуль):

```python
from pyspark import pipelines as dp

@dp.materialized_view
def regional_sales():
  customers_df = spark.read.table("customers")
  transactions_df = spark.read.table("transactions")
  
  return (
    customers_df.join(transactions_df, on="customer_id", how="inner")
    .groupBy("region")
    .agg({"amount": "sum"})
  )
```

Правило выбора из учебного модуля: streaming tables - когда источник append-only и нужна низкая задержка; materialized views - когда нужны агрегации, сложные join-ы или обработка update и delete в источнике.

### 4.2. Режимы pipeline

- **Triggered** - обновление по расписанию или по событию (источник: "Triggered vs. continuous pipeline mode").
- **Continuous** - непрерывная обработка; для serverless pipeline в continuous mode.
- **Real-time mode** в Lakeflow pipelines - субсекундная сквозная задержка для операционных нагрузок.

Каждое обновление pipeline выполняет flow заново; обновление может быть инкрементальным (только новые записи) или полным (full refresh - перечитывает все данные источника).

### 4.3. Standalone streaming tables и materialized views

Можно создавать streaming tables и materialized views **вне pipeline** - из Databricks SQL warehouse или ноутбука на serverless general compute. Для каждой такой таблицы система создает серверный pipeline (тип в списке pipelines - `MV/ST`; внутри pipeline - `ETL`). Обновления запускаются на serverless. Примеры:

```sql
CREATE OR REFRESH STREAMING TABLE sales
  SCHEDULE EVERY 1 hour
  AS SELECT product, price FROM STREAM raw_data;
```

```sql
REFRESH STREAMING TABLE sales;
REFRESH STREAMING TABLE sales FULL;
```

Источник предупреждает: **full refresh** не рекомендуется для источников, которые не хранят полную историю или имеют короткий retention (например, Kafka), потому что full refresh очищает существующие данные.

Права: `GRANT SELECT ON st_name TO read_only_user;` и `GRANT REFRESH ON st_name TO refresh_user;`. Пользователи с SELECT не обязаны иметь SELECT на исходные таблицы. Refresh выполняется с правами владельца; если владелец потерял доступ к источнику, scheduled refresh падает, но читать таблицу можно.

### 4.4. Expectations (ожидания качества данных)

Expectation состоит из трех частей: **имени**, **constraint** (SQL-выражение, возвращающее true/false для каждой записи) и **action**. Constraint может использовать любой SQL-синтаксис, кроме пользовательских Python-функций, вызовов внешних сервисов и подзапросов.

| Action | SQL | Python-декоратор | Поведение |
|---|---|---|---|
| Warn (по умолчанию) | `CONSTRAINT name EXPECT (...)` | `@dp.expect` | Строка записывается в target; нарушения считаются в метриках |
| Drop | `ON VIOLATION DROP ROW` | `@dp.expect_or_drop` | Строка удаляется; остальные продолжают |
| Fail | `ON VIOLATION FAIL UPDATE` | `@dp.expect_or_fail` | Обновление/flow останавливается; нужна ручная работа перед повтором |

Групповые варианты в Python: `@dp.expect_all`, `@dp.expect_all_or_drop`, `@dp.expect_all_or_fail` принимают словарь правил.

Примеры из учебного модуля:

```python
@dp.expect("valid_transaction_date", "transaction_date >= '2020-01-01' AND transaction_date <= current_date()")
```

```python
@dp.expect_or_drop("valid_price", "price >= 0 AND price <= 10000")
def validated_orders():
    return spark.readStream.table("raw.orders")
```

```sql
CREATE OR REFRESH STREAMING TABLE validated_orders(
    CONSTRAINT valid_price EXPECT (price >= 0 AND price <= 10000) ON VIOLATION DROP ROW
) AS SELECT * FROM STREAM(raw.orders);
```

```sql
CREATE OR REFRESH STREAMING TABLE critical_transactions(
    CONSTRAINT required_customer_id EXPECT (customer_id IS NOT NULL) ON VIOLATION FAIL UPDATE
) AS SELECT * FROM STREAM(raw.transactions);
```

Правила можно хранить в таблице Unity Catalog и читать их функцией; тогда изменение правила не требует правки кода pipeline. Пример функции из источника:

```python
def get_rules(tag):
    df = spark.read.table("governance.data_quality.rules").filter(col("tag") == tag).collect()
    return {row["name"]: row["constraint"] for row in df}
```

Особенности:

- При нескольких параллельных flows падение одного не останавливает остальные.
- Метрики expectations видны на вкладке **Data quality** выбранного dataset в Jobs & Pipelines. Программно - через event log pipeline.
- Для `fail` метрики не записываются, в ошибке приводится входная запись: `[EXPECTATION_VIOLATION.VERBOSITY_ALL] Flow '...' failed to meet the expectation...`.
- Expectations не поддерживаются для datasets, использующих `AUTO CDC FROM SNAPSHOT` (ошибка справочника; обходной путь - промежуточная таблица).

---

## 5. Constraints в Delta-таблицах (Unity Catalog)

Expectations работают внутри pipeline. Для обычных Delta-таблиц есть стандартные SQL-constraints (источник `tables/constraints`).

- **Enforced**: `NOT NULL` и `CHECK`. Нарушение приводит к падению транзакции.
- **Informational** (не проверяются): PRIMARY KEY, FOREIGN KEY, UNIQUE. Используются для оптимизаций и документации.
- Все constraints требуют Delta Lake. Добавление constraint может повысить writer protocol до версии 3 или выше, что влияет на совместимость внешних клиентов Delta.

Пример из источника:

```sql
CREATE OR REPLACE TABLE main.default.people_demo (
  id INT NOT NULL,
  firstName STRING,
  middleName STRING NOT NULL,
  lastName STRING,
  gender STRING,
  birthDate TIMESTAMP,
  ssn STRING,
  salary INT
);

ALTER TABLE main.default.people_demo ALTER COLUMN middleName DROP NOT NULL;
ALTER TABLE main.default.people_demo ALTER COLUMN ssn SET NOT NULL;
```

```sql
ALTER TABLE main.default.people_demo ADD CONSTRAINT dateWithinRange CHECK (birthDate > '1900-01-01');
ALTER TABLE main.default.people_demo DROP CONSTRAINT dateWithinRange;
```

Правила для CHECK: выражение может использовать только детерминированные встроенные функции Spark; запрещены UDF, агрегатные функции, оконные функции и функции, возвращающие несколько строк. `ALTER TABLE ADD CONSTRAINT` проверяет существующие строки до добавления.

Informational constraints:

```sql
CREATE OR REPLACE TABLE main.default.T(pk1 INTEGER NOT NULL, pk2 INTEGER NOT NULL,
                CONSTRAINT t_pk PRIMARY KEY(pk1, pk2));
CREATE OR REPLACE TABLE main.default.S(pk INTEGER NOT NULL PRIMARY KEY,
                fk1 INTEGER, fk2 INTEGER,
                CONSTRAINT s_t_fk FOREIGN KEY(fk1, fk2) REFERENCES main.default.T);
CREATE OR REPLACE TABLE main.default.U(id INTEGER NOT NULL, email STRING NOT NULL,
                CONSTRAINT u_uq_email UNIQUE(email));
```

Внешний ключ сопоставляет колонки по позиции с PRIMARY KEY родительской таблицы; количество колонок и типы должны совпадать. UNIQUE в источнике помечен как Public Preview.

**Когда что использовать (Вывод конспекта):** NOT NULL и CHECK - на уровне таблицы, защищают любой писатель и отказывают в записи целиком. Expectations - внутри pipeline, позволяют выбрать warn/drop/fail и видеть метрики. Для строгой проверки в bronze/silver чаще подходят expectations, для гарантий целостности таблицы, которую читают внешние системы, - constraints.

---

## 6. CDC и SCD

### 6.1. Почему не MERGE INTO

Источник `sql/mv-st/streaming`: CDC-записи раньше обрабатывали через `MERGE INTO`. Но `MERGE INTO` может давать **некорректные результаты при записях не по порядку (out-of-sequence)** и требует сложной логики переупорядочивания. **AUTO CDC** автоматически обрабатывает такие записи: вы задаете ключи (KEYS), колонку порядка (SEQUENCE BY) и тип хранения - SCD type 1 (перезапись) или SCD type 2 (история).

### 6.2. AUTO CDC в SQL

SCD type 1 (текущее состояние):

```sql
CREATE OR REFRESH STREAMING TABLE target
  FLOW AUTO CDC
  FROM stream(cdc_data.users)
  KEYS (userId)
  SEQUENCE BY sequenceNum
  STORED AS SCD TYPE 1;
```

SCD type 2 (история):

```sql
CREATE OR REFRESH STREAMING TABLE target
  FLOW AUTO CDC
  FROM stream(cdc_data.users)
  KEYS (userId)
  APPLY AS DELETE WHEN operation = "DELETE"
  SEQUENCE BY sequenceNum
  COLUMNS * EXCEPT (operation, sequenceNum)
  STORED AS SCD TYPE 2;
```

Соответствие API (справочник Python): `dlt.apply_changes(...)` -> `dp.create_auto_cdc_flow(...)`; для снимков (snapshots) используется `create_auto_cdc_from_snapshot_flow`.

Дополнительно из справочника ошибок:

- Опции отслеживания истории колонок (`track_history_column_list` / `track_history_except_column_list`) допустимы только для SCD Type 2.
- AUTO CDC FROM SNAPSHOT не поддерживает TYPE BITEMPORAL-таблицы и expectations.
- Auto Full Refresh не поддерживается для SCD Type 2.
- Для удаленных записей (tombstones) хранится retention, по умолчанию два дня (`pipelines.cdc.tombstoneGCThresholdInSeconds`).

### 6.3. SCD type 2 вручную: MERGE из учебного модуля

Учебный модуль по моделированию Unity Catalog показывает таблицу с суррогатным ключом и столбцами `valid_from`, `valid_to`, `is_current`:

```sql
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

Шаг MERGE из того же источника:

```sql
MERGE INTO sales.customer AS target
USING (
    SELECT 
        source.customer_id,
        source.customer_name,
        source.email,
        source.city,
        source.region,
        current_timestamp() AS valid_from,
        CAST('9999-12-31' AS TIMESTAMP) AS valid_to,
        true AS is_current
    FROM staging.customers AS source
) AS updates
ON target.customer_id = updates.customer_id AND target.is_current = true
WHEN MATCHED AND (
    target.customer_name <> updates.customer_name OR
    target.email <> updates.email OR
    target.city <> updates.city OR
    target.region <> updates.region
) THEN UPDATE SET
    target.valid_to = current_timestamp(),
    target.is_current = false
WHEN NOT MATCHED THEN INSERT (
    customer_id, customer_name, email, city, region,
    valid_from, valid_to, is_current
) VALUES (
    updates.customer_id, updates.customer_name, updates.email, 
    updates.city, updates.region, updates.valid_from, 
    updates.valid_to, updates.is_current
);

-- Insert new versions for updated records
INSERT INTO sales.customer
SELECT 
    s.customer_id,
    s.customer_name,
    s.email,
    s.city,
    s.region,
    current_timestamp() AS valid_from,
    CAST('9999-12-31' AS TIMESTAMP) AS valid_to,
    true AS is_current
FROM staging.customers s
JOIN sales.customer h 
    ON s.customer_id = h.customer_id 
    AND h.valid_to = current_timestamp()
    AND h.is_current = false;
```

**Вывод конспекта (важно проверить на практике):** в этом примере второй `INSERT` ищет закрытые версии по условию `h.valid_to = current_timestamp()`. Выражение `current_timestamp()` вычисляется отдельно в каждом запросе, поэтому значение, записанное в первом `MERGE`, почти наверняка не совпадет со значением во втором запросе, и новые версии могут не вставиться. Также MERGE для уже существующих изменившихся ключей только закрывает текущую версию, а новую вставляет вторым запросом. Практический вывод: для продуктивного SCD2 источник советует AUTO CDC; ручной вариант требует явного хранения ключа операции (например, общий timestamp, переданный в обоих запросах, или одна транзакция с вычисленной заранее переменной).

Запросы по истории из того же источника:

```sql
SELECT customer_id, customer_name, city
FROM sales.customer
WHERE valid_from <= '2023-06-15 12:00:00'
  AND valid_to > '2023-06-15 12:00:00';
```

```sql
SELECT * FROM sales.customer 
TIMESTAMP AS OF '2024-01-15';
```

Источник отмечает: time travel по умолчанию хранит историю 7 дней, поэтому для долгой истории нужны явные колонки SCD (valid_from/valid_to).

---

## 7. Lakeflow Jobs (оркестрация задач)

### 7.1. Задачи и зависимости

Lakeflow Jobs - список задач с зависимостями. Задачи выполняются последовательно или параллельно. Доступны ветвления:

- **Run if** - условие запуска задачи по статусу родительских задач: All succeeded, At least one succeeded, None failed, All done, At least one failed, All failed.
- **If/else** - условие по значению: `taskValues`, job parameters или dynamic values; операторы `==`, `!=`, `>`, `>=`, `<`, `<=`.
- **For each** - запуск вложенной задачи в цикле с разными параметрами.
- **Disabled task** - задача пропускается, но сохраняет конфигурацию и историю; downstream-задачи оцениваются по своим условиям Run if.

Из учебного модуля по error handling: типичные схемы - All succeeded (продолжать при успехе), At least one failed (запустить обработку ошибок или уведомление), All done (cleanup независимо от статуса).

### 7.2. Триггеры и расписание

Из учебного модуля `implement-lakeflow-jobs`:

| Тип | Поведение |
|---|---|
| Scheduled (расписание) | Запуск в фиксированное время |
| Table update | Запуск при обновлении отслеживаемых таблиц (Delta, Iceberg managed, external Delta, materialized views, streaming tables, views). Режимы: **Any table is updated** или **All tables are updated**. Опции: Minimum time between triggers, Wait after last change |
| File arrival | Запуск при появлении новых файлов в external location или volume; проверка примерно раз в минуту, рекурсивно по подкаталогам |
| Continuous | Новый запуск сразу после завершения или падения предыдущего |

Важные детали:

- Для table update и file arrival рекомендуется включать **file events** на external location. Без них ограничения: 50 jobs с file arrival trigger на workspace и не более 10 000 файлов в отслеживаемом месте.
- File arrival trigger реагирует только на **новые имена файлов**; перезапись файла с тем же именем не запускает job.
- Continuous job на serverless поддерживает только `Trigger.AvailableNow` для Structured Streaming (см. раздел 3.2).
- Параметры trigger доступны в задачах как `{{job.trigger.table_update.updated_tables}}`, `{{job.trigger.table_update.<catalog.schema.table>.version}}` и т. п.

Cron-синтаксис расписаний в собранных источниках не описан (см. «Пробелы»). Concurrency: при достижении maximum concurrent runs запуски могут пропускаться (`Skipped`), если очередь отключена.

### 7.3. Retries, timeouts, уведомления

- **Retry policy**: число повторов и интервал; для continuous jobs Databricks применяет exponential backoff и автоматические retries. Задача с повторами перезапускается с начала.
- **Timeouts**: expected duration (предупреждение) и maximum duration (принудительная остановка). Для streaming-задач можно задать пороги backlog (Public Preview).
- **Notifications**: email, Slack, Microsoft Teams, PagerDuty, webhooks; на start, success, failure, превышение duration. Уведомления задачи срабатывают на каждой попытке, поэтому источник советует включать mute до последнего retry.

### 7.4. Параметры

- **Job parameters** (ключ-значение на уровне job) автоматически передаются (pushdown) задачам, которые принимают key-value параметры: Notebook, Python wheel (с keyword arguments), SQL query или file, Run Job. Если ключ задачи совпадает с ключом job, UI покажет предупреждение.
- Задачи с **JSON-массивом** параметров (Python script, Python wheel с positional arguments, JAR, Spark Submit, For each) не получают job-параметры автоматически; нужно ссылаться на них явно: `{{job.parameters.<name>}}`.
- **Task values** передают результаты между задачами.

Пример из источника по Azure Data Factory (Notebook activity), где параметры передаются как `baseParameters`:

```json
{
    "activity": {
        "name": "MyActivity",
        "description": "MyActivity description",
        "type": "DatabricksNotebook",
        "linkedServiceName": {
            "referenceName": "MyDatabricksLinkedservice",
            "type": "LinkedServiceReference"
        },
        "typeProperties": {
            "notebookPath": "/Users/user@example.com/ScalaExampleNotebook",
            "baseParameters": {
                "inputpath": "input/folder1/",
                "outputpath": "output/"
            },
            "libraries": [
                {
                "jar": "dbfs:/docs/library.jar"
                }
            ]
        }
    }
}
```

Если параметр в notebook не передан, используется значение по умолчанию из notebook.

### 7.5. Repair runs

Из учебного модуля `monitor-troubleshoot-optimize-workloads`:

- Repair перезапускает **только неуспешные задачи и их зависимые** задачи, а не весь job.
- Процедура: открыть проблемный run (Start time или matrix view), нажать **Repair run**, проверить список задач, при необходимости изменить параметры (введенные значения переопределяют существующие), запустить.
- Repair доступен только для jobs с **двумя и более задачами**.
- Если задачи используют общий job cluster, repair создает новый экземпляр кластера (например, `my_job_cluster_v1`), чтобы сравнить настройки.
- **Важно**: repair перезапускает неуспешную задачу с начала. Если задача частично записала данные до падения, повтор может их продублировать. Источник рекомендует идемпотентные операции (overwrite или merge вместо append).

Остальные статусы run: Failed (падение leaf-задач), Succeeded with failures, Skipped (превышен maximum concurrent runs), Timed Out, Canceled. Статус определяется по **leaf-задачам**. Для continuous jobs доступна кнопка Restart run, которая сбрасывает backoff.

---

## 8. Orchestration с Azure Data Factory

Источники по ADF (`d1-azure-data-factory-transform-data-databricks-notebook`, `d2-azure-data-factory-transform-data`, `d2-azure-data-factory-compute-linked-services`):

- ADF умеет запускать три типа Databricks-активностей: **Databricks Notebook**, **Databricks Jar**, **Databricks Python**.
- Для запуска нужен **Azure Databricks linked service**. Аутентификация: access token или managed identity (MSI, system-assigned). Compute: существующий интерактивный кластер (`existingClusterId`), новый job cluster (`newClusterVersion`, `newClusterNodeType`, `newClusterNumOfWorker`), либо instance pool (`instancePoolId`).
- Параметры передаются через `baseParameters`. Значения можно вернуть через `dbutils.notebook.exit("returnValue")`, а в ADF прочитать выражением `@{activity('<имя активности>').output.runOutput}`. Размер возвращаемого значения ограничен **2 MB**.

Пример linked service (с new job cluster, из источника; токен - плейсхолдер):

```json
{
    "name": "AzureDatabricks_LS",
    "properties": {
        "type": "AzureDatabricks",
        "typeProperties": {
            "domain": "https://eastus.azuredatabricks.net",
            "newClusterNodeType": "Standard_D3_v2",
            "newClusterNumOfWorker": "1:10",
            "newClusterVersion": "4.0.x-scala2.11",
            "accessToken": {
                "type": "SecureString",
                "value": "YourAccessToken"
            }
        }
    }
}
```

Из учебного модуля по error handling: `dbutils.notebook.exit(...)` позволяет передать статус обратно задаче job, и downstream-задачи используют его в условиях.

Распределение ролей, которое следует из источников (**Вывод конспекта**): ADF - внешний оркестратор, который связывает разные сервисы (copy, data flow, Databricks) в единый пайплайн; Lakeflow Jobs - оркестратор внутри Databricks с нативными триггерами по таблицам и файлам, repair и управлением run. Если все шаги находятся в Databricks, Jobs обычно проще. Если пайплайн уже строится в ADF и включает нединамические сервисы, ADF вызывает Databricks-задачи как одну из активностей.

---

## 9. Сравнение: ADF vs Databricks Jobs vs Lakeflow pipelines (DLT)

| Критерий | Azure Data Factory | Lakeflow Jobs (Databricks Jobs) | Lakeflow pipelines (SDP / DLT) |
|---|---|---|---|
| Основная роль | Внешний оркестратор и перенос данных между сервисами | Оркестрация задач внутри Databricks | Декларативное построение таблиц и трансформаций |
| Что описывает разработчик | Активности и зависимости между ними | Задачи (notebook, SQL, Python, JAR, dbt и др.), зависимости, условия | Таблицы (streaming tables, materialized views), flows, expectations |
| Модель выполнения | Запускает внешние задачи (в т.ч. Databricks), отслеживает статус | Выполняет задачи на compute Databricks | Движок сам определяет порядок, инкрементальность и retries |
| Инкрементальность | Зависит от логики активности (например, watermark-колонки на уровне ADF) | Зависит от кода задачи (Structured Streaming, Auto Loader) | Встроенная: streaming tables обрабатывают строку один раз; materialized views инкрементальны на serverless |
| Качество данных | Вне Databricks или в коде задачи | Через код задачи и условия Run if | Expectations: warn / drop / fail; метрики в UI |
| Триггеры | Расписание и события ADF | Schedule, table update, file arrival, continuous | Triggered / continuous mode pipeline, расписание |
| Retries и восстановление | Retry на уровне активности | Retry, timeouts, repair runs | Retries на уровне task, flow, pipeline |
| Языки | Визуальный конструктор, JSON | Notebooks (Python, SQL, Scala), SQL, JAR, dbt и др. | SQL и Python |
| Compute | Linked service (existing cluster, job cluster, instance pool, MSI) | Job compute, all-purpose, serverless | Serverless или classic compute |
| Требования | Подписка ADF | Workspace Databricks | Lakeflow pipelines требуют план Premium |
| Когда выбирать | Координация разнородных сервисов Azure | Сложная логика, notebooks, ветвления, событийные запуски | Новые batch и incremental ETL-пайплайны с декларативными таблицами |

Источник `data-engineering/choose-etl-approach` рекомендует Lakeflow pipelines для большинства новых ETL-нагрузок, а также допускает dbt-модели, Spark-ноутбуки с Lakeflow Jobs и stored procedures на SQL warehouse.

---

## 10. Типичные ошибки (pitfalls)

1. **Запись в silver напрямую из ingestion.** Изменения схемы и битые записи в источнике сломают пайплайн. Источник рекомендует bronze в почти сыром виде (string, VARIANT, binary) и чтение из bronze в silver (`azure-databricks lakehouse/medallion`).
2. **Ожидание, что изменение запроса streaming table пересчитает старые строки.** Без full refresh старые строки не переписываются (`REFRESH STREAMING TABLE ... FULL`). Full refresh на Kafka может удалить данные, которых больше нет в источнике.
3. **Ожидание, что joins в streaming table обновятся при изменении измерения.** Они не пересчитываются; для всегда корректного результата используйте materialized view.
4. **Materialized view на classic compute считается инкрементально.** Источник: на classic compute она полностью пересчитывается при каждом обновлении; инкрементальность требует serverless.
5. **Непродуманный trigger на serverless.** Не заданный trigger по умолчанию равен `ProcessingTime("0 seconds")`, что приводит к `INFINITE_STREAMING_TRIGGER_NOT_SUPPORTED`. Используйте `Trigger.AvailableNow`.
6. **Stateful-запрос без watermark.** Растет состояние, возможен отказ по памяти и ошибки вида `UNSUPPORTED_STREAMING_OPERATOR_WITHOUT_WATERMARK`.
7. **Неверный выбор action в expectations.** `expect_or_fail` останавливает flow до ручного вмешательства; для мониторинга тренда лучше `warn`.
8. **Repair без идемпотентности.** Repair перезапускает задачу с начала; append-запись даст дубликаты. Используйте overwrite или merge.
9. **Доступ к ADLS в обход Unity Catalog.** Прямые права на контейнер обходят governance. Используйте external locations и volumes.
10. **Credentials в `spark.conf.set()` ноутбука для Hive DDL.** Hive metastore client их игнорирует; задавайте в Spark-конфигурации кластера. Секреты храните в secret scope, а не в коде.
11. **Ручной SCD2 через MERGE без проверки.** См. раздел 6.3: условие на `current_timestamp()` между запросами может не совпасть. Предпочтительнее AUTO CDC.
12. **Уведомления на каждом retry.** Включайте mute до последнего retry, иначе будет шум.
13. **Job-параметры не доходят до задачи с JSON-массивом.** Для таких задач используйте `{{job.parameters.<name>}}` явно.
14. **Удаление checkpoint.** Auto Loader и Structured Streaming начнут обработку заново или упадут с ошибкой состояния. Checkpoint не удаляют без понимания последствий.

---

## 11. Вопросы для собеседования (8)

**1. Что такое Auto Loader и чем он лучше `spark.readStream` по файлам?**
Auto Loader - Structured Streaming source `cloudFiles`, который инкрементально обрабатывает новые файлы в облачном хранилище. Отслеживает файлы в RocksDB в checkpoint, обеспечивает exactly-once, масштабируется на миллиарды файлов, поддерживает schema inference и evolution с rescue данных, а в file notification mode снижает затраты на листинг.

**2. Чем bronze, silver и gold отличаются по назначению?**
Bronze - сырые данные без валидации, неизменяемая история для аудита и переобработки. Silver - очищенные, дедуплицированные и нормализованные валидированные данные. Gold - агрегаты и dimensional-модели под бизнес-отчетность и ML.

**3. В чем разница между streaming table и materialized view?**
Streaming table обрабатывает каждую входящую строку один раз и подходит для append-only источников с низкой задержкой; joins в ней не пересчитываются. Materialized view кэширует результат запроса и всегда корректна, включая joins и агрегации; инкрементальность полноценно доступна на serverless.

**4. Какие действия есть у expectations и когда их выбирать?**
Warn (записать и посчитать нарушения), drop (удалить строку, `ON VIOLATION DROP ROW` / `expect_or_drop`), fail (остановить flow, `ON VIOLATION FAIL UPDATE` / `expect_or_fail`). Warn - для мониторинга, drop - для очистки, fail - для критичных инвариантов.

**5. Чем NOT NULL/CHECK constraints отличаются от informational PK/FK?**
NOT NULL и CHECK проверяются при записи, нарушение откатывает транзакцию. PRIMARY KEY, FOREIGN KEY и UNIQUE не проверяются, только описывают связи и могут помогать оптимизатору.

**6. Почему вместо MERGE INTO для CDC рекомендуют AUTO CDC?**
MERGE INTO может давать некорректный результат при записях не по порядку и требует сложной логики упорядочивания. AUTO CDC принимает KEYS, SEQUENCE BY и тип SCD (1 или 2), сам обрабатывает out-of-order записи и поддерживает delete через `APPLY AS DELETE WHEN`.

**7. Что делает repair run и какие у него риски?**
Перезапускает неуспешные задачи и зависимые от них, не трогая успешные. Риски: задача перезапускается с начала, поэтому частично записанные данные могут дублироваться; нужны идемпотентные операции. Repair доступен для jobs с двумя и более задачами.

**8. Когда использовать ADF, а когда Lakeflow Jobs?**
ADF - оркестратор для связи разнородных сервисов Azure; Databricks вызывается как активность (Notebook, Jar, Python) через linked service, параметры передаются через `baseParameters`. Lakeflow Jobs - оркестрация внутри Databricks с нативными триггерами по таблицам и файлам, Run if, For each, repair и уведомлениями. Для сценария, полностью живущего в Databricks, Jobs проще; ADF оправдан, если в пайплайн входят другие сервисы.

---

## 12. Пробелы в источниках

Следующего в собранных источниках нет, либо оно неполное:

- **COPY INTO**: нет отдельной справочной страницы с полным синтаксисом и всеми опциями; есть один пример из ADLS-раздела, описание ограничений через справочник ошибок и краткое упоминание в разделе Delta.
- **Auto Loader options**: нет полного справочника назначения опций (`schemaEvolutionMode`, `maxFilesPerTrigger`, `useNotifications`, `cleanSource` и др.). Перечислены только имена, встретившиеся в источниках.
- **Watermarks**: нет примеров кода с `withWatermark`, только концепция и сообщения об ошибках.
- **Expectations в Python для материализованных views**: в источниках примеры даны для streaming tables; применимость к materialized views в собранных материалах не проверена.
- **Cron-синтаксис расписаний** Lakeflow Jobs и правила Quartz: не найдены.
- **Lakeflow Jobs: конкретные UI-шаги** настройки Run if, For each, If/else даны только в обзорном виде (раздел `control-flow`).
- **AUTO CDC FROM SNAPSHOT**: описан только через сообщения об ошибках; примеров кода в собранных источниках нет.
- **Python-пример `create_auto_cdc_flow`**: есть только название функции и соответствие `dlt.apply_changes`; полного кода в собранных источниках нет.
- **Подробности Lakeflow Connect managed connectors** (например, конкретные SaaS-коннекторы и их ограничения): собраны только категории.
- **Стоимость и тарификация** (DBU, serverless, триггеры): в собранных источниках не разбирались.
- **Azure-специфика Auto Loader** (вариант file notification на Azure Event Grid/Queue, роли и права): упоминаются параметры `cloudFiles.connectionString`, `cloudFiles.queueName`, `cloudFiles.resourceGroup` и др., но пошагового руководства по настройке не найдено.
- **Курс по Structured Streaming** (`run-your-first-structured-streaming-workload`, `monitor-query-listener`): не включен в собранные markdown, поэтому подробности мониторинга streaming-запросов не раскрыты.
- Существующие сводки в `guides/courses/azure-databricks-data-engineer-*` и `guides/modules/*databricks*` в этом конспекте не использовались как первоисточник: они перечисляют темы, но не содержат фактов, которых не было бы в исходниках.

---

## 13. Источники

Локальные файлы (папка `azure-course`):

- `docs2/d2-azure-databricks-ingestion-cloud-object-storage-auto-loader.md` - https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader
- `docs2/d2-azure-databricks-ingestion-overview.md` - https://learn.microsoft.com/en-us/azure/databricks/ingestion/overview
- `docs2/d2-azure-databricks-ingestion-create-or-modify-table.md` - https://learn.microsoft.com/en-us/azure/databricks/ingestion/create-or-modify-table
- `docs2/d0-azure-databricks-delta.md` - https://learn.microsoft.com/en-us/azure/databricks/delta
- `docs/d2-azure-databricks-data-data-sources-azure-azure-datalake-gen2.md` - https://learn.microsoft.com/en-us/azure/databricks/data/data-sources/azure/azure-datalake-gen2
- `docs2/d2-azure-databricks-connect-unity-catalog-cloud-storage.md` - https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage
- `docs2/d2-azure-databricks-lakehouse-medallion.md` - https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion
- `docs2/d2-azure-databricks-structured-streaming-concepts.md` - https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/concepts
- `docs2/d2-azure-databricks-query-streaming.md` - https://learn.microsoft.com/en-us/azure/databricks/query/streaming
- `docs2/d2-azure-databricks-compute-serverless-limitations.md` - https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations
- `docs2/d2-azure-databricks-getting-started-etl-quick-start.md` - https://learn.microsoft.com/en-us/azure/databricks/getting-started/etl-quick-start
- `docs2/d2-azure-databricks-ldp.md` - https://learn.microsoft.com/en-us/azure/databricks/ldp
- `docs2/d2-azure-databricks-ldp-concepts-flows.md` - https://learn.microsoft.com/en-us/azure/databricks/ldp/concepts/flows
- `docs2/d2-azure-databricks-ldp-concepts-materialized-views.md` - https://learn.microsoft.com/en-us/azure/databricks/ldp/concepts/materialized-views
- `docs2/d2-azure-databricks-ldp-concepts-streaming-tables.md` - https://learn.microsoft.com/en-us/azure/databricks/ldp/concepts/streaming-tables
- `docs2/d2-azure-databricks-ldp-developer-python-ref.md` - https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/python-ref
- `docs2/d2-azure-databricks-sql-mv-st-streaming.md` - https://learn.microsoft.com/en-us/azure/databricks/sql/mv-st/streaming
- `docs2/d2-azure-databricks-tables-constraints.md` - https://learn.microsoft.com/en-us/azure/databricks/tables/constraints
- `docs2/d2-azure-databricks-data-engineering-choose-etl-approach.md` - https://learn.microsoft.com/en-us/azure/databricks/data-engineering/choose-etl-approach
- `docs2/d2-azure-databricks-jobs-control-flow.md` - https://learn.microsoft.com/en-us/azure/databricks/jobs/control-flow
- `docs2/d2-azure-databricks-jobs-task-parameters.md` - https://learn.microsoft.com/en-us/azure/databricks/jobs/task-parameters
- `docs2/d2-azure-databricks-error-messages-error-classes.md` - справочник ошибок Azure Databricks (фрагменты по COPY INTO, Streaming, AUTO CDC)
- `docs2/d1-azure-data-factory-transform-data-databricks-notebook.md` - https://learn.microsoft.com/en-us/azure/data-factory/transform-data-databricks-notebook
- `docs2/d2-azure-data-factory-transform-data.md` - https://learn.microsoft.com/en-us/azure/data-factory/transform-data
- `docs2/d2-azure-data-factory-compute-linked-services.md` - https://learn.microsoft.com/en-us/azure/data-factory/compute-linked-services
- `docs2/d2-azure-data-factory-concepts-pipelines-activities.md` - перечень activities ADF
- `courses2/d0-training-modules-implement-manage-data-quality-constraints-unity-catalog-5-manage-data-quality-pipeline-expectations.md` - https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/5-manage-data-quality-pipeline-expectations
- `courses2/d0-training-modules-design-implement-data-pipelines-7-create-pipeline-lakeflow-declarative.md` - https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/7-create-pipeline-lakeflow-declarative
- `courses2/d0-training-modules-design-implement-data-pipelines-5-design-error-handling-pipelines.md` - https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/5-design-error-handling-pipelines
- `courses2/d0-training-modules-design-implement-data-modeling-unity-catalog-7-implement-slowly-changing-dimension-type-2.md` - https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/7-implement-slowly-changing-dimension-type-2
- `courses2/d0-training-modules-implement-lakeflow-jobs-3-configure-job-triggers.md` - https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/3-configure-job-triggers
- `courses2/d0-training-modules-monitor-troubleshoot-optimize-workloads-azure-databricks-3-troubleshoot-repair-lakeflow-jobs.md` - https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/3-troubleshoot-repair-lakeflow-jobs

Ссылки на проверку: как в исходниках, на дату последнего обновления страниц (от 2026-08 до 2026-11).
