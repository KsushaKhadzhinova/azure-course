# Очистка, преобразование и загрузка данных в Unity Catalog

**Источник:** https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/

## Цель модуля

Научиться профилировать данные, выбирать типы колонок, устранять дубликаты и пропуски, фильтровать, группировать и агрегировать, объединять таблицы (join и set-операторы), менять форму данных (denormalization, PIVOT, UNPIVOT) и загружать результаты в таблицы Unity Catalog стратегиями append, overwrite и merge.

## Ключевые понятия

- **Data profiling (профилирование данных)** - сбор сводной статистики: количества, null-проценты, распределения; `ANALYZE TABLE`, `DESCRIBE TABLE EXTENDED`, `describe()`.
- **Anomaly detection и data profiling в Unity Catalog** - обнаружение аномалий свежести и полноты (на уровне схемы, Public Preview) и детальный профиль отдельной таблицы (snapshot, time series, inference).
- **Типы данных** - целочисленные (TINYINT, SMALLINT, INT, BIGINT), DECIMAL(p,s) для точных расчетов, FLOAT и DOUBLE для приближенных, DATE, TIMESTAMP, TIMESTAMP_NTZ, STRING, BINARY, ARRAY, MAP, STRUCT.
- **QUALIFY** - фильтрация по результату оконной функции без подзапроса.
- **exceptAll()** - разность с сохранением дубликатов.
- **Join-типы** - INNER, LEFT, RIGHT, FULL, SEMI, ANTI, CROSS.
- **Set-операторы** - UNION (с DISTINCT по умолчанию), UNION ALL, INTERSECT, EXCEPT (и MINUS как синоним).
- **Denormalization (денормализация)** - объединение связанных таблиц в одну широкую для быстрых запросов.
- **PIVOT / UNPIVOT** - превращение строк в колонки и обратно; UNPIVOT по умолчанию исключает NULL (можно INCLUDE NULLS).
- **INSERT INTO (append), INSERT OVERWRITE, REPLACE WHERE, REPLACE USING, REPLACE ON** - стратегии загрузки.
- **MERGE INTO (upsert)** - обновление существующих строк и вставка новых по условию совпадения.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/1-introduction

Сырые данные требуют очистки и преобразования; без этого аналитика ненадежна. Unity Catalog дает управление результатами. Инструменты: профилирование, выбор типов, устранение дубликатов и null, фильтрация, группировка, соединения, денормализация, PIVOT/UNPIVOT и стратегии загрузки.

### 2. Profile data
https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/2-profile-data-summary-statistics

`ANALYZE TABLE ... COMPUTE STATISTICS` (для таблицы, столбцов или всех столбцов) собирает статистику; `DESCRIBE TABLE EXTENDED` показывает ее. В PySpark `df.describe()` дает count, mean, stddev, min и max. Для управляемых таблиц Unity Catalog predictive optimization выполняет ANALYZE автоматически. Профили в Unity Catalog: snapshot (вся таблица при обновлении), time series (по временным окнам) и inference (для моделей). Метрики: num_nulls, distinct_count, min, max, frequent_items, quantiles; drift считается тестами Колмогорова-Смирнова и хи-квадрат.

### 3. Choose column data types
https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/3-choose-appropriate-column-data-types

Подбирайте тип по диапазону значений (TINYINT для статусов, INT для большинства идентификаторов, BIGINT для больших). Для денег используйте DECIMAL, так как FLOAT и DOUBLE дают ошибки округления в десятичных значениях. TIMESTAMP нормализуется к UTC и зависит от часового пояса сессии; TIMESTAMP_NTZ хранит время как есть (Public Preview). Сложные типы: ARRAY, MAP, STRUCT. Приводите типы явно при загрузке.

### 4. Resolve duplicates and nulls
https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/4-resolve-duplicate-missing-null-values

Дубликаты находят через GROUP BY ... HAVING COUNT(*) > 1, QUALIFY с оконной функцией или в PySpark через `Window.partitionBy` и `exceptAll`. Удаляют через `dropDuplicates()`, `distinct()` или ROW_NUMBER() с QUALIFY (оставить последнюю запись по `updated_at`). Null находят через IS NULL, удаляют через `dropna()` (параметры how и subset), заполняют через `fillna()` или COALESCE. Выбор стратегии зависит от смысла колонки; решения нужно документировать.

### 5. Transform data with filters and aggregations
https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/5-transform-data-filter-group-aggregate

Фильтрация: `filter()` и `where()` в PySpark (условия с `&` и `|` в скобках), WHERE в SQL; для null - `isNull()` и `isNotNull()`, а не сравнение с None. Группировка: `groupBy()` и GROUP BY. Агрегаты: count, sum, avg, min, max через `agg()` или SQL; HAVING фильтрует группы. Цепочка трансформаций в PySpark выполняется лениво; фильтры лучше ставить раньше.

### 6. Transform data with joins and set operators
https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/6-transform-data-join-union-intersect-except

Joins соединяют таблицы по столбцам (INNER, LEFT, RIGHT, FULL, SEMI, ANTI, CROSS). SEMI возвращает строки левой таблицы с совпадениями, ANTI - без совпадений. Set-операторы соединяют строки одинаковой структуры: UNION (без дубликатов по умолчанию), UNION ALL, INTERSECT, EXCEPT (MINUS). PySpark `union()` ведет себя как UNION ALL. В сравнении INTERSECT имеет более высокий приоритет, чем UNION и EXCEPT.

### 7. Transform data with denormalization and pivots
https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/7-transform-data-flatten-pivot-unpivot

Денормализация объединяет таблицы в широкую таблицу (например, в gold-слое), платой за это становятся место и обновление копий. PIVOT превращает значения колонки в колонки и требует агрегатной функции (например, SUM). UNPIVOT превращает колонки в пары имя-значение; по умолчанию NULL исключаются, для их сохранения есть INCLUDE NULLS. UNPIVOT требует Databricks Runtime 12.2 LTS и выше.

### 8. Load data with merge, insert, and append
https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/8-load-data-merge-insert-append

INSERT INTO добавляет строки и не проверяет дубликаты. INSERT OVERWRITE заменяет таблицу или партицию. REPLACE WHERE заменяет строки по предикату (если хоть одна строка не подходит, запись не выполняется). REPLACE USING (рекомендуется для динамической перезаписи на всех типах compute) и REPLACE ON - новые варианты. MERGE INTO выполняет upsert с условиями WHEN MATCHED и WHEN NOT MATCHED; в PySpark используется `DeltaTable.merge`. Если одна строка источника совпадает с несколькими строками цели, MERGE падает: источник нужно дедуплицировать.

### 9. Exercise - Cleanse, Transform, and Load Data into Unity Catalog
https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/9-exercise-cleanse-transform-load-data-into-unity-catalog

Практическое задание (около 45 минут) по данным о недвижимости: выбор типов для цен и временных меток, удаление дубликатов и заполнение пропусков в PySpark, объединение таблиц inner и left join, PIVOT и UNPIVOT в SQL для анализа рынка. Нужна подписка Azure с правами администратора.

### 10. Module assessment
https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/10-knowledge-check

Проверка знаний (около 5 минут). Текст вопросов в источнике не приведен.

### 11. Summary
https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/11-summary

Порядок работы: профилируйте, очищайте, преобразуйте и загружайте стратегией, соответствующей сценарию. Из модуля: ANALYZE TABLE и мониторинг, DECIMAL для финансов, QUALIFY, dropDuplicates и fillna, фильтрация, группировка, join и set-операторы, денормализация, PIVOT и UNPIVOT, INSERT INTO, INSERT OVERWRITE и MERGE INTO.

## Важные команды / код / настройки

**Профилирование:**
```
ANALYZE TABLE sales.transactions COMPUTE STATISTICS;
ANALYZE TABLE sales.transactions COMPUTE STATISTICS FOR COLUMNS 
    transaction_id, amount, customer_id;
ANALYZE TABLE sales.transactions COMPUTE STATISTICS FOR ALL COLUMNS;
DESC EXTENDED sales.transactions amount;
DESCRIBE TABLE EXTENDED sales.transactions;
```
```
%pip install "databricks-sdk>=0.68.0"
```
Создание snapshot-профиля (Databricks SDK): `w.data_quality.create_monitor(monitor=Monitor(object_type="table", ..., data_profiling_config=DataProfilingConfig(output_schema_id=..., assets_dir="/Workspace/Users/user@example.com/monitoring", snapshot=SnapshotConfig())))`. Обновление: `w.data_quality.create_refresh(...)`.

**Типы данных (примеры из источника):**
```
CREATE TABLE orders (
    order_id INT,
    status_code TINYINT,
    total_items SMALLINT,
    transaction_id BIGINT
);
```
```
CREATE TABLE transactions (
    transaction_id INT,
    amount DECIMAL(10,2),
    tax_rate DECIMAL(5,4)
);
```
Для часовых поясов: `TIMESTAMP` (UTC внутри, часовой пояс сессии при чтении) и `TIMESTAMP_NTZ` (Public Preview).

**Дубликаты и null:**
```
SELECT customer_id, email, COUNT(*) AS occurrence_count
FROM sales.customers
GROUP BY customer_id, email
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC;
```
```
SELECT *
FROM sales.customers
QUALIFY COUNT(*) OVER (PARTITION BY customer_id, email) > 1;
```
```
SELECT *
FROM sales.customers
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY customer_id 
    ORDER BY updated_at DESC
) = 1;
```
```
df_duplicates = df.exceptAll(df.dropDuplicates(["customer_id", "email"]))
df_clean = df.dropDuplicates(["customer_id", "email"])
df_unique = df.distinct()
df_clean = df.dropna(subset=["customer_id", "amount"])
df_filled = df.fillna({"amount": 0, "status": "Unknown", "quantity": 1})
```
```
SELECT customer_id, COALESCE(amount, 0) AS amount, COALESCE(status, 'Unknown') AS status
FROM sales.transactions;
```

**Фильтры и агрегаты:**
```
df_filtered = df_customer.filter(
    (col("c_nationkey") == 20) & (col("c_acctbal") > 1000)
)
df_segment_avg = df_customer.groupBy("c_mktsegment").agg(
    avg("c_acctbal").alias("avg_balance")
)
```
```
SELECT id, SUM(quantity) AS total_quantity
FROM dealer
GROUP BY id
HAVING SUM(quantity) > 20;
```

**Joins и set-операторы:**
```
SELECT e.id, e.name, e.deptno, d.deptname
FROM employee e
LEFT JOIN department d ON e.deptno = d.deptno;
```
```
df_semi = df_employee.join(df_department, on="deptno", how="semi")
df_anti = df_employee.join(df_department, on="deptno", how="anti")
```
```
SELECT customer_id, name, email FROM active_customers
UNION ALL
SELECT customer_id, name, email FROM archived_customers;
```
```
SELECT customer_id FROM active_customers
EXCEPT
SELECT customer_id FROM archived_customers;
```

**Денормализация:**
```
CREATE OR REPLACE TABLE sales.orders_denormalized AS
SELECT o.order_id, o.order_date, c.customer_name, c.region,
       p.product_name, p.category, o.quantity, o.total_price
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id;
```

**PIVOT и UNPIVOT:**
```
SELECT year, region, Q1, Q2, Q3, Q4
FROM quarterly_sales
PIVOT (
  SUM(revenue)
  FOR quarter IN (1 AS Q1, 2 AS Q2, 3 AS Q3, 4 AS Q4)
);
```
```
SELECT *
FROM regional_targets
UNPIVOT INCLUDE NULLS (
  target_amount FOR month IN (jan, feb, mar, apr)
);
```

**Загрузка:**
```
INSERT INTO sales.transactions (transaction_id, amount, transaction_date)
VALUES ('TXN001', 150.00, '2026-01-15'), ('TXN002', 275.50, '2026-01-15');
```
```
INSERT INTO sales.transactions
REPLACE WHERE transaction_date >= '2026-01-01' AND transaction_date <= '2026-01-07'
SELECT * FROM staging.corrected_transactions;
```
```
INSERT INTO sales.monthly_report
  REPLACE USING (report_month)
  SELECT region, product_category, SUM(amount) AS revenue, report_month
  FROM staging.corrected_transactions
  GROUP BY region, product_category, report_month;
```
```
MERGE INTO customers AS target
USING customer_updates AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN
    UPDATE SET target.email = source.email, target.phone = source.phone, target.last_updated = current_timestamp()
WHEN NOT MATCHED THEN
    INSERT (customer_id, name, email, phone, created_date, last_updated)
    VALUES (source.customer_id, source.name, source.email, source.phone, current_timestamp(), current_timestamp());
```
```
df_new_transactions.write.mode("append").saveAsTable("sales.transactions")
df_refreshed.write.mode("overwrite").saveAsTable("sales.daily_summary")
(df_january.write.mode("overwrite").option("replaceWhere", "report_month = '2026-01'").saveAsTable("sales.monthly_report"))
```

**Версии Runtime из источника:** REPLACE USING в SQL - Databricks Runtime 16.3+; в Python и Scala `replaceUsing` - 18.2+; REPLACE ON в SQL - 17.1+; UNPIVOT - 12.2 LTS+.

**Ограничение:** `INSERT OVERWRITE PARTITION` с `partitionOverwriteMode=dynamic` работает только на classic compute.

## Что запомнить

- Профилируйте данные до очистки: null-проценты, дубликаты и распределения подскажут, что исправлять.
- Для денег используйте DECIMAL, а не FLOAT или DOUBLE.
- QUALIFY с оконными функциями и dropDuplicates убирают дубликаты; при этом выбирайте, какую строку оставить, через ROW_NUMBER.
- Стратегия загрузки зависит от связи источника с целью: append для новых строк, overwrite или REPLACE WHERE для пересчета, MERGE для upsert.
- MERGE падает, если одна строка источника совпадает с несколькими строками цели; дедуплицируйте источник заранее.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/cleanse-transform-load-data-into-unity-catalog/
- В источнике упоминаются (без ссылок в тексте): Databricks Unity Catalog; Data quality monitoring (anomaly detection и data profiling); Databricks SDK для Python; Delta Lake Python API (DeltaTable.merge); predictive optimization.
