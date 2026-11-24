# Проектирование и реализация конвейеров данных в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/

## Цель модуля

Спроектировать конвейер данных по архитектуре medallion (bronze, silver, gold), выбрать между notebook и Lakeflow pipelines, настроить логику задач в Lakeflow Jobs (зависимости, условия, For each, параметры) и заложить обработку ошибок (expectations, повторы, таймауты, уведомления, исключения в коде).

## Ключевые понятия

- **Medallion architecture (bronze, silver, gold)** - слои данных: сырые данные, очищенные и проверенные, курируемые для потребления.
- **Notebook** - пошаговое процедурное выполнение кода; полный контроль, подходит для прототипов и сложной логики.
- **Lakeflow pipelines (Lakeflow Declarative Pipeline)** - декларативный подход: описываются потоковые таблицы и материализованные представления, движок сам управляет порядком, параллелизмом и восстановлением.
- **Streaming table** - Delta-таблица для append-only обработки; каждая запись обрабатывается ровно один раз.
- **Materialized view** - кешированный результат запроса, который обновляется по изменениям источников.
- **Lakeflow Jobs / DAG** - задачи и зависимости в виде направленного ациклического графа.
- **Dependency condition** - условие запуска задачи: All succeeded, At least one succeeded, None failed, All done, At least one failed, All failed.
- **If/else condition task** - ветвление по значениям задач или параметров.
- **Run if dependencies** - запуск по результатам предыдущих задач, без сравнения значений.
- **For each task** - выполнение вложенной задачи для каждого элемента массива с настраиваемым параллелизмом.
- **Expectations (ожидания качества данных)** - правила валидации: Warn/EXPECT, Drop (ON VIOLATION DROP ROW), Fail (ON VIOLATION FAIL UPDATE).
- **Retry policy, timeouts, notifications** - механизмы устойчивости на уровне задачи.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/1-introduction

Надёжный конвейер требует проектирования рабочих процессов, которые переживают сбои, масштабируются и поддерживаются. В Azure Databricks есть два подхода: notebook и Lakeflow pipelines. Важны порядок операций, зависимости задач и обработка ошибок.

### 2. Проектирование порядка операций конвейера
Источник: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/2-design-order-operations-pipeline

Этапы по порядку:
- **Ingest** - приём из источника без изменений (bronze); учитывайте тип источника (потоковый или пакетный), сохраняйте сырые данные, обрабатывайте только новые или изменённые данные.
- **Clean and validate** - приведение схемы, обработка null, дедупликация, проверки качества (silver).
- **Transform for consumption** - соединения, агрегаты, денормализация, бизнес-логика; логика должна быть понятной и тестируемой.
- **Load** - выбор способа записи: full refresh, incremental append или merge; партиционирование; эволюция схемы (gold).
- **Serve** - представления для потребителей, производительность, контроль доступа.
- **Monitor and optimize** - метрики выполнения, тренды качества данных, стоимость и производительность.

### 3. Выбор между notebook и Lakeflow pipelines
Источник: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/3-choose-notebook-lakeflow-pipelines

- **Notebook** подходит для сложной логики (ветвления, циклы по внешним API, свой retry), прототипирования, внешних библиотек и тонкой настройки производительности.
- **Lakeflow pipelines** подходят для стандартных ETL-паттернов, встроенного контроля качества (expectations), автоматического управления зависимостями, наблюдаемости (lineage, граф выполнения) и внешних потоковых приёмников (Apache Kafka, Azure Event Hubs, Delta-таблицы, пользовательские источники Python).
- В сравнении: notebook - полный контроль и ручная обработка ошибок; декларативный конвейер - системное управление выполнением, встроенные retry, декларативные expectations, автоматический lineage.
- Часто используют оба подхода: notebook для предобработки и обучения моделей, Lakeflow pipelines для основного ETL.

### 4. Проектирование логики задач Lakeflow Job
Источник: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/4-design-task-logic-lakeflow-job

- **Зависимости**: задачи образуют DAG; условия запуска - All succeeded, At least one succeeded, None failed, All done, At least one failed, All failed. Пример: задача очистки запускается с All done.
- Задачи можно отключить (disable) вместо удаления - они пропускаются при запуске, но сохраняют конфигурацию и историю.
- **Параллельность**: независимые задачи выполняются одновременно; это требует вычислительных ресурсов, а число одновременных запусков в рабочей области ограничено.
- **If/else**: ветвление по выражению, например `{{tasks.quality_check.values.invalid_count}} > 100` - при истине запускается ремедиация, иначе стандартный путь.
- **Run if**: запуск по результатам задач (например, уведомление при сбое).
- **For each**: одна вложенная задача выполняется для каждого элемента массива; массив можно задать в JSON, взять из value предыдущей задачи или из параметра; параллельность задаётся числом одновременных итераций.
- **Параметры**: уровня задачи или job; ссылка `{{job.parameters.<имя>}}`; динамические значения `{{job.trigger.time.iso_date}}` (дата запуска) и `{{backfill.iso_datetime}}` (для backfill).
- **Вычислительные ресурсы**: notebook и Python-скрипты - serverless jobs compute; SQL-запросы и файлы - serverless SQL warehouse; Lakeflow pipelines - serverless pipeline compute; JAR и Spark Submit - classic jobs compute.

### 5. Проектирование обработки ошибок в конвейерах и заданиях
Источник: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/5-design-error-handling-pipelines

- **Expectations** в декларативных конвейерах: Warn (запись с метриками), Drop (исключение записи), Fail (остановка потока; другие параллельные потоки продолжают работу; для возобновления нужно ручное вмешательство).
- **Retry**: число повторов (обычно 1-3) и интервал; для непрерывных заданий применяется экспоненциальная задержка.
- **Таймауты**: expected duration (предупреждение) и maximum duration (остановка); для потоковых задач можно задать пороги метрики backlog (функция в публичном предпросмотре).
- **Уведомления**: email, Slack, Microsoft Teams, PagerDuty, пользовательские webhook; при запуске, успехе, сбое или превышении длительности. Совет: включить Mute notifications until the last retry, чтобы не получать уведомления на каждой попытке.
- **Условные потоки**: All succeeded, At least one failed, All done.
- **В notebook**: try-except с `PySparkException`, проверка `getErrorClass()` (например, `TABLE_OR_VIEW_NOT_FOUND`), повтор с экспоненциальной задержкой, передача результата через `dbutils.notebook.exit()`.
- Лучшие практики: fail fast при угрозе целостности, логировать контекст без чувствительных данных, идемпотентность и повтор только упавших задач, мониторинг трендов, тестирование сбоев.

### 6. Создание конвейера с notebook
Источник: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/6-create-pipeline-notebook-precedence

- Notebook-задачи в Lakeflow Job; зависимости задаются полем Depends on; новая задача, добавленная при выбранной задаче, автоматически зависит от неё.
- Пример DAG: Task 1 (ingest_data) → Task 2 (transform_customers) и Task 3 (transform_orders) параллельно → Task 4 (generate_report) после обоих.
- Создание: Jobs & Pipelines > Create > Job; Type = Notebook; Source = Workspace; выбрать Path и Compute; Create task.
- Параметры задачи: Parameters > Add (Key и Value); в notebook читаются через `dbutils.widgets.get()`.
- Практики: понятные имена задач (например, `bronze_ingest_orders`), папки по структуре конвейера, минимум зависимостей, workspace-notebook для production с MLflow, ограничение вывода (20 МБ всего, 8 МБ на ячейку).

### 7. Создание конвейера Lakeflow Declarative Pipeline
Источник: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/7-create-pipeline-lakeflow-declarative

- Декларативный подход: описывается итоговое состояние, движок управляет оркестрацией, инкрементальностью и повторами (уровни: Spark task, flow, pipeline).
- Streaming table: `CREATE OR REFRESH STREAMING TABLE ... AS SELECT * FROM STREAM read_files(...)` или Python `@dp.table` с `cloudFiles`. Используется для append-only данных.
- Materialized view: `CREATE OR REPLACE MATERIALIZED VIEW ...` или Python `@dp.materialized_view`; подходит для агрегатов, соединений и обработки изменений и удалений.
- Expectations: EXPECT (по умолчанию - сохраняет и считает нарушения), ON VIOLATION DROP ROW, ON VIOLATION FAIL UPDATE.
- Редактор Lakeflow Pipelines Editor: Dry run (проверка без обработки), selective execution, interactive DAG, data preview, Genie Code (создание кода на естественном языке).
- Код этих примеров - определения конвейера; он не выполняется в обычном notebook (модуль `pyspark.pipelines` и DDL доступны только в runtime конвейера).

### 8. Упражнение: проектирование и реализация конвейеров данных
Источник: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/8-exercise-design-implement-data-pipelines

Упражнение (около 45 минут): конвейер Bronze → Silver → Gold для данных бронирования отелей GlobStay с очисткой (дедупликация, фильтрация null, проверка дат), агрегатами по объектам и каналам, обработкой ошибок и параметризованными notebook. Затем задание Lakeflow Job с последовательными зависимостями, политикой повторов, уведомлениями об ошибках и задачей If/else для маршрутизации по качеству данных. Требуется подписка Azure с правами администратора.

### 9. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/9-knowledge-check

В исходных материалах вопросы не приведены.

### 10. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/10-summary

Порядок операций следует медальонной архитектуре. Notebook дают гибкость, Lakeflow pipelines снижают операционную сложность. В Lakeflow Jobs зависимости, If/else, For each и параметры управляют логикой; ошибки обрабатываются expectations, retry, уведомлениями и try-except в коде.

## Важные команды / код / настройки

Streaming table (SQL):

```
CREATE OR REFRESH STREAMING TABLE customers_bronze
AS SELECT * FROM STREAM read_files(
  "/Volumes/raw_data/customers",
  format => "json"
);
```

Streaming table (Python):

```
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

Materialized view (SQL):

```
CREATE OR REPLACE MATERIALIZED VIEW customer_transactions
AS SELECT
  c.customer_id,
  c.customer_name,
  c.region,
  t.transaction_date,
  t.amount
FROM customers c
INNER JOIN transactions t ON c.customer_id = t.customer_id;
```

Условие If/else и параметры:

```
{{tasks.quality_check.values.invalid_count}} > 100
{{job.parameters.target_catalog}}
{{job.trigger.time.iso_date}}
{{backfill.iso_datetime}}
```

Передача значений для For each:

```
regions = ["us-east", "us-west", "eu-central"]
dbutils.jobs.taskValues.set(key="regions_to_process", value=regions)
```

Ссылка в For each: `{{tasks.get_regions.values.regions_to_process}}`.

Обработка ошибок в notebook:

```
from pyspark.errors import PySparkException

try:
    df = spark.read.table("source_data")
    transformed = df.filter("amount > 0")
    transformed.write.mode("append").saveAsTable("target_data")
except PySparkException as e:
    if e.getErrorClass() == "TABLE_OR_VIEW_NOT_FOUND":
        print(f"Source table not found: {e.getMessageParameters()['relationName']}")
    else:
        raise
```

Сигнал результата задаче job:

```
dbutils.notebook.exit(f"SUCCESS: Processed {records_processed} records")
```

Настройки: expectations - EXPECT, ON VIOLATION DROP ROW, ON VIOLATION FAIL UPDATE; ограничение вывода notebook - 20 МБ всего, 8 МБ на ячейку.

## Что запомнить

- Порядок конвейера: ingest (bronze) → clean and validate (silver) → transform and load (gold) → serve и мониторинг.
- Notebook дают контроль, Lakeflow pipelines - автоматическую оркестрацию, инкрементальность и lineage; часто их комбинируют.
- Условия зависимостей (All succeeded, All done, At least one failed) определяют, как сбои распространяются по DAG.
- If/else, Run if и For each задают ветвление, реакцию на сбои и итерации по массивам.
- Ошибки обрабатываются в несколько уровней: expectations (Warn, Drop, Fail), retry и таймауты, уведомления без спама (Mute until last retry), try-except в коде.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/
- Lakeflow Jobs и Lakeflow pipelines (упомянуты в уроках модуля)
