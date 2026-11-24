# Прием потоковых данных с Azure Stream Analytics в Synapse

**Источник:** https://learn.microsoft.com/en-us/training/modules/ingest-streaming-data-use-azure-stream-analytics-synapse/

## Цель модуля

Научиться настраивать задание Azure Stream Analytics: определять входы (inputs) и выходы (outputs), писать запрос для выборки, фильтрации и агрегации потоковых событий по временным окнам, запускать задание и направлять результаты в хранилища (Azure Data Lake Storage Gen2, Azure SQL Database, Azure Synapse Analytics и другие).

## Ключевые понятия

- **Azure Stream Analytics** — полностью управляемый сервис потоковой обработки с языком запросов на основе SQL.
- **Input (вход)** — источник потоковых данных: Azure Event Hubs, Azure IoT Hub, Blob или Data Lake Gen2, Apache Kafka.
- **Output (выход)** — приемник результатов запроса: Data Lake, SQL-база, Synapse, Event Hubs, Power BI, Azure Cosmos DB, Azure Functions.
- **Reference data** — статические входные данные для обогащения потока.
- **TIMESTAMP BY** — выражение, которое задает временную метку события для обработки по времени.
- **Окна (windows)** — tumbling, hopping, sliding, session и snapshot; задаются в GROUP BY.
- **System.Timestamp()** — функция, возвращающая временную метку события или окна.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/ingest-streaming-data-use-azure-stream-analytics-synapse/1-introduction

Введение на примере производства: телеметрия датчиков обрабатывается потоково, выявляются аномалии, данные архивируются. Типичная схема: источник событий (Event Hubs или IoT Hub), запрос Stream Analytics, выходы (data lake, реляционная БД, другой event hub).

### 2. Stream ingestion scenarios
https://learn.microsoft.com/en-us/training/modules/ingest-streaming-data-use-azure-stream-analytics-synapse/2-stream-ingestion-scenarios

Сценарии вывода результатов: data lake (анализ Spark и serverless SQL, история и машинное обучение), реляционная БД (отчеты на стандартном SQL), живые дашборды через Power BI (поддержка этого выхода прекращается 31 октября 2027 года; для новых решений рекомендуется Real-Time Intelligence в Microsoft Fabric), пересылка событий в другой Event Hubs для многоэтапных конвейеров.

### 3. Configure inputs and outputs
https://learn.microsoft.com/en-us/training/modules/ingest-streaming-data-use-azure-stream-analytics-synapse/3-configure-inputs-outputs

Каждое задание имеет минимум один вход и один выход. Входы: Event Hubs, IoT Hub, Blob или Data Lake Gen2, Apache Kafka; в событии доступны поля данных и метаданные (например, `EventEnqueuedUtcTime`). Выход Azure SQL Database требует существующей таблицы, схема которой совпадает с результатом запроса; аутентификация через managed identity или SQL-логин. Для Synapse dedicated SQL pool рекомендуется выход Azure Synapse Analytics (выше пропускная способность и для заданий с восемью и более входными партициями). Выход Blob/ADLS Gen2 поддерживает CSV, JSON, Parquet и Delta и шаблоны папок вида YYYY/MM/DD. Также описан no-code редактор.

### 4. Define a query to select, filter, and aggregate data
https://learn.microsoft.com/en-us/training/modules/ingest-streaming-data-use-azure-stream-analytics-synapse/4-define-query

Выборка через `SELECT ... INTO ... FROM ... TIMESTAMP BY`, фильтрация через `WHERE`, агрегация по окнам через `GROUP BY` с оконной функцией. Пять типов окон: Tumbling (неперекрывающиеся фиксированные интервалы), Hopping (перекрывающиеся с шагом), Sliding (срабатывает при изменении содержимого), Session (по паузе между событиями), Snapshot (события с одинаковой временной меткой). Для SQL-выхода схема результата должна совпадать с таблицей; при необходимости используются `AS` и приведение типов.

### 5. Run a job to ingest data
https://learn.microsoft.com/en-us/training/modules/ingest-streaming-data-use-azure-stream-analytics-synapse/5-run-job-ingest

Запущенное задание работает постоянно, пока его не остановят. Результаты можно читать T-SQL из таблицы SQL или через Spark из файлов Data Lake. Мониторинг в портале: входящие события, исходящие события, ошибки выполнения, watermark delay.

### 6. Exercise - Ingest streaming data into Azure Synapse Analytics
https://learn.microsoft.com/en-us/training/modules/ingest-streaming-data-use-azure-stream-analytics-synapse/6-exercise-ingest-streaming-data

Практика (около 45 минут): настроить задание потоковой обработки с входами, запросом и выходами для приема данных в Azure Synapse Analytics. Нужна подписка Azure с правами администратора.

### 7. Module assessment
https://learn.microsoft.com/en-us/training/modules/ingest-streaming-data-use-azure-stream-analytics-synapse/7-knowledge-check

Проверочный тест (около 3 минут). Вопросы и ответы в источнике не приведены.

### 8. Summary
https://learn.microsoft.com/en-us/training/modules/ingest-streaming-data-use-azure-stream-analytics-synapse/8-summary

Итоги: Stream Analytics обрабатывает данные в реальном времени с SQL-подобным языком и поддержкой оконных функций и направляет результаты в data lake, реляционные БД и event hubs.

## Важные команды / код / настройки

**Выборка полей (SELECT ... INTO):**

```
SELECT
    EventEnqueuedUtcTime AS ReadingTime,
    SensorID,
    ReadingValue
INTO
    [output]
FROM
    [streaming-input] TIMESTAMP BY EventEnqueuedUtcTime
```

**Фильтрация:** добавить `WHERE ReadingValue < 0`.

**Агрегация по 60-секундным tumbling-окнам:**

```
SELECT
    DateAdd(second, -60, System.Timestamp()) AS StartTime,
    System.Timestamp() AS EndTime,
    SensorID,
    MAX(ReadingValue) AS MaxReading
INTO
    [output]
FROM
    [streaming-input] TIMESTAMP BY EventEnqueuedUtcTime
GROUP BY SensorID, TumblingWindow(second, 60)
HAVING COUNT(*) >= 1
```

**Запрос к таблице SQL (T-SQL):**

```
SELECT SensorID, AVG(ReadingValue) AS AverageReading
FROM SensorReadings
GROUP BY SensorID
```

**Чтение файлов в Spark:**

```
df = spark.read.load(
    'abfss://data@datalake.dfs.core.windows.net/sensors/*',
    format='parquet'
)
display(df)
```

**Настройки выходов из источника:**

- Azure SQL Database output: сервер, база данных и существующая таблица; схема должна точно совпадать с полями запроса.
- Аутентификация managed identity: не требует повторного входа при смене пароля и истечении пользовательских токенов (каждые 90 дней) и поддерживает полностью автоматические развертывания.
- Blob/ADLS Gen2 output: форматы CSV, JSON, Parquet, Delta; шаблон папок например `YYYY/MM/DD`; минимальное число строк и максимальное время ожидания в батче; для Parquet каждый батч создает новый файл.
- Dedicated Azure Synapse Analytics output рекомендуется для большей пропускной способности и заданий с восемью и более входными партициями.

## Что запомнить

- Задание Stream Analytics состоит из входов, запроса и выходов; запрос пишется на SQL-подобном языке.
- `TIMESTAMP BY` задает время события; оконные функции (`TumblingWindow` и другие) задают агрегацию по времени.
- Tumbling-окна не перекрываются, hopping и sliding могут перекрываться, session группирует события по паузам.
- Для SQL-выхода схема результата должна совпадать с таблицей, иначе запись не выполнится.
- Managed identity упрощает аутентификацию и автоматические развертывания.
- Power BI-выход выводится из эксплуатации 31 октября 2027 года; для новых решений смотрите Real-Time Intelligence в Fabric.

## Связанные материалы

- Stream data as input into Stream Analytics (документация, упоминается в уроке 3).
- Azure SQL Database output from Azure Stream Analytics (упоминается в уроке 3).
- Blob storage and Azure Data Lake Gen2 output from Azure Stream Analytics (упоминается в уроке 3).
- Introduction to Stream Analytics windowing functions (упоминается в уроке 4).
- Common query patterns in Azure Stream Analytics (упоминается в уроке 4).
- Monitor Azure Stream Analytics jobs (упоминается в уроке 5).
- No-code stream processing in Azure Stream Analytics (упоминается в уроке 3).
- Real-Time Intelligence in Microsoft Fabric (упоминается в уроке 2).
