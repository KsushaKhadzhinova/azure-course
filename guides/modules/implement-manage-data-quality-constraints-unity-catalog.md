# Реализация и управление ограничениями качества данных в Unity Catalog

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/

## Цель модуля

Научиться обеспечивать качество данных в Azure Databricks с помощью Unity Catalog: проверять типы и приводить их (schema enforcement, cast и try_cast), задавать CHECK и NOT NULL-ограничения, проверять null, уникальность и диапазоны, управлять schema drift и настраивать pipeline expectations в Lakeflow.

## Ключевые понятия

- **Schema enforcement (контроль схемы)** - Delta Lake проверяет типы и наличие колонок при записи; несовместимая запись завершается ошибкой.
- **cast / try_cast** - `cast` при неудаче выдает ошибку, `try_cast` возвращает NULL.
- **CHECK constraint (ограничение CHECK)** - правило на уровне Delta-таблицы, проверяется при вставке и обновлении.
- **NOT NULL constraint** - запрет пустых значений; при добавлении к существующей таблице проверяет все строки.
- **Primary key constraint (первичный ключ)** - в Delta Lake информационный: документирует структуру, но не проверяется.
- **Pipeline expectations (ожидания конвейера)** - правила Lakeflow с именем, SQL-условием и действием (warn, drop, fail).
- **Schema drift (дрейф схемы)** - изменение структуры входных данных со временем (новые, удаленные или переименованные колонки).
- **Auto Loader schema evolution mode** - режим, который определяет поведение при новых колонках и изменении типов.
- **Rescued data column (колонка спасенных данных)** - колонка, куда попадают данные, не подходящие под схему (`_rescued_data`).
- **Quarantine pattern (карантин)** - отделение некорректных записей в отдельную таблицу.
- **Unity Catalog rules table** - таблица правил качества в управляемой схеме, из которой читаются expectations.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/1-introduction

Ошибки данных (несовпадение типов, пустые обязательные значения, неожиданные изменения схемы) портят аналитику. Azure Databricks предлагает схемный контроль Delta Lake, CHECK-ограничения и pipeline expectations в Lakeflow. Модуль учит проверять типы, управлять дрейфом схемы, проверять null, уникальность и диапазоны, а также использовать expectations.

### 2. Implement validation checks
https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/2-implement-validation-checks

Два механизма: pipeline expectations (warn, drop, fail) для потоковых таблиц и материализованных представлений и table constraints (отклоняют запись) для Delta-таблиц. Проверки: null (expect_or_drop, NOT NULL), уникальность (окно с count или GROUP BY ... HAVING COUNT(*) > 1; PRIMARY KEY как информационный) и диапазоны (BETWEEN, сравнения, CHECK).

### 3. Implement data type checks
https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/3-implement-data-type-checks

Schema enforcement при вставке: безопасное приведение (например, '100' в INT) проходит, а нечисловая строка вызывает ошибку. `cast` строг, `try_cast` возвращает NULL для отбраковки. CHECK-ограничения с REGEXP или try_cast проверяют формат. Для конвейера показан шаблон: валидные записи в silver, некорректные в quarantine. Также можно проверять типы через expectations.

### 4. Detect and manage schema drift
https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/4-detect-manage-schema-drift

Дрейф схемы - это изменение структуры (колонки добавлены, удалены, переименованы), а не типов. По умолчанию Delta блокирует несовпадающие записи. Auto Loader поддерживает пять режимов эволюции схемы; можно автоматически добавлять колонки (mergeSchema, MERGE WITH SCHEMA EVOLUTION), сохранять неожиданные данные в `_rescued_data` или останавливать поток. Для обработки нарушений используются drop, fail и quarantine.

### 5. Manage data quality with pipeline expectations
https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/5-manage-data-quality-pipeline-expectations

Expectation состоит из имени, SQL-условия и действия. Действия: warn (по умолчанию - записи проходят, метрики собираются), drop (некорректные строки удаляются), fail (обновление останавливается и откатывается). Можно комбинировать несколько expectations, группировать их в словарь (expect_all_or_drop) и хранить правила в таблице Unity Catalog (например, `governance.data_quality.rules`). Метрики смотрят во вкладке Data quality в интерфейсе конвейера или через журнал событий.

### 6. Exercise - Implement and Manage Data Quality Constraints with Azure Databricks
https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/6-exercise-implement-manage-data-quality-constraints-unity-catalog

Практическое задание (около 45 минут): конвейер Lakeflow Spark Declarative Pipeline для страховой компании ClearCover, который проверяет сырые данные о страховых случаях: null и диапазоны через expectations, приведение типов через `col().cast()`, дрейф схемы через колонку спасенных данных Auto Loader. Нужна подписка Azure с правами администратора.

### 7. Module assessment
https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/7-knowledge-check

Проверка знаний (около 5 минут). Текст вопросов в источнике не приведен.

### 8. Summary
https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/8-summary

Качество данных обеспечивается на нескольких уровнях: схемный контроль, явное приведение, CHECK-ограничения, expectations конвейера. Для дрейфа схемы выбирайте между остановкой, автоматической адаптацией и спасением данных. Начинайте с базовых проверок и добавляйте expectations для потоковых нагрузок; карантин изолирует проблемные записи.

## Важные команды / код / настройки

**Expectations в Python (Lakeflow):**
```
from pyspark import pipelines as dp
@dp.table
@dp.expect_or_drop("valid_email", "email IS NOT NULL")
@dp.expect_or_drop("valid_customer_id", "customer_id IS NOT NULL")
def customers():
    return spark.readStream.table("raw.customers")
```

**Expectations в SQL:**
```
CREATE OR REFRESH STREAMING TABLE customers(
    CONSTRAINT valid_email EXPECT (email IS NOT NULL) ON VIOLATION DROP ROW,
    CONSTRAINT valid_customer_id EXPECT (customer_id IS NOT NULL) ON VIOLATION DROP ROW
) AS SELECT * FROM STREAM(raw.customers);
```

**Действия expectations:**

| Python | SQL | Поведение |
|---|---|---|
| `@dp.expect` | `EXPECT (...)` | Warn (по умолчанию): записи попадают в таблицу, метрики логируются |
| `@dp.expect_or_drop` | `ON VIOLATION DROP ROW` | Drop: некорректные строки удаляются |
| `@dp.expect_or_fail` | `ON VIOLATION FAIL UPDATE` | Fail: обновление останавливается |

Групповые декораторы: `expect_all`, `expect_all_or_drop`, `expect_all_or_fail`.

**Ограничения Delta-таблиц:**
```
CREATE TABLE customers (
    customer_id INT NOT NULL,
    email STRING NOT NULL,
    first_name STRING,
    last_name STRING
);
```
```
ALTER TABLE customers ALTER COLUMN email SET NOT NULL;
```
```
ALTER TABLE employees ADD CONSTRAINT valid_age CHECK (age >= 18 AND age <= 120);
ALTER TABLE transactions ADD CONSTRAINT positive_amount CHECK (amount > 0);
```
```
ALTER TABLE orders
ADD CONSTRAINT valid_order_total CHECK (order_total REGEXP '^[0-9]+(\\.[0-9]+)?$')
```
```
ALTER TABLE events
ADD CONSTRAINT valid_event_date CHECK (try_cast(event_date_str AS DATE) IS NOT NULL);
```
Перед добавлением ограничения к существующей таблице проверяются все строки; операция завершится ошибкой при нарушениях.

**Приведение типов:**
```
SELECT 
    cast(raw_amount AS DECIMAL(10,2)) AS amount,
    cast(raw_date AS DATE) AS transaction_date
FROM staging_data;
```
```
SELECT 
    raw_amount,
    try_cast(raw_amount AS DECIMAL(10,2)) AS validated_amount
FROM staging_data;
```

**Auto Loader - режимы `cloudFiles.schemaEvolutionMode`:**

| Режим | Поведение |
|---|---|
| addNewColumns (по умолчанию) | Поток останавливается; новые колонки добавляются при перезапуске; типы существующих колонок не меняются |
| rescue | Схема не меняется; данные не по схеме попадают в rescued data column; поток работает |
| failOnNewColumns | Поток останавливается; нужно обновить схему или удалить проблемные данные |
| none | Схема не меняется; новые колонки игнорируются, если не задан `rescuedDataColumn` |
| addNewColumnsWithTypeWidening | Новые колонки добавляются и расширяются поддерживаемые типы (например, INT в LONG); требует Databricks Runtime 16.4+ (Public Preview) |

Пример: `.option("cloudFiles.schemaEvolutionMode", "failOnNewColumns")`; для спасения данных: `.option("rescuedDataColumn", "_rescued_data")`.

**Слияние схемы для записи и MERGE:**
```
(df.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .saveAsTable("target_table")
)
```
```
MERGE WITH SCHEMA EVOLUTION INTO target_table t
USING source_data s
ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

**Правила в Unity Catalog:**
```
CREATE OR REPLACE TABLE governance.data_quality.rules AS
SELECT col1 AS name, col2 AS constraint, col3 AS tag
FROM (
  VALUES
    ('valid_amount',    'amount > 0',                              'financial'),
    ('valid_currency',  'currency IN (''USD'', ''EUR'', ''GBP'')',  'financial'),
    ('non_null_email',  'email IS NOT NULL',                       'customer'),
    ('valid_hire_date', 'hire_date <= current_date()',             'hr')
);
```

**Путь в интерфейсе для метрик:** Jobs & Pipelines > конвейер > датасет > вкладка Data quality.

Пример сообщения о нарушении fail-expectation (из источника): `[EXPECTATION_VIOLATION.VERBOSITY_ALL] Flow 'sensor-pipeline' failed to meet the expectation. Violated expectations: 'temperature_in_valid_range'.`

## Что запомнить

- Delta Lake блокирует запись с несовместимыми типами; `try_cast` позволяет отбраковать значения без остановки запроса.
- CHECK и NOT NULL применяются при записи, а expectations конвейера действуют во время трансформации и могут удалять или останавливать поток.
- PRIMARY KEY в Delta Lake не проверяется; для гарантии уникальности используйте expectations или проверки в запросе.
- Для дрейфа схемы выбирайте режим Auto Loader: `failOnNewColumns` для контроля, `addNewColumns` для адаптации, `rescue` для сохранения неожиданных данных.
- Храните правила качества в таблице Unity Catalog, чтобы менять их в одном месте для всех конвейеров.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/implement-manage-data-quality-constraints-unity-catalog/
- В источнике упоминаются (без ссылок в тексте): Unity Catalog; Lakeflow pipelines (Spark Declarative Pipelines); Auto Loader; Delta Lake schema enforcement; Azure Databricks Data quality tab; журнал событий (event log) конвейеров Lakeflow.
