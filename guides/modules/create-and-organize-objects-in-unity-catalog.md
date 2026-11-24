# Создание и организация объектов в Unity Catalog

**Источник:** https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/

## Цель модуля

Спроектировать и создать структуру Unity Catalog из трёх уровней пространства имён (catalog → schema → таблицы, представления, тома, функции), применить единые соглашения об именах, настроить managed storage, создать таблицы (managed, external, с ключами и ограничениями), представления (стандартные, динамические, материализованные, streaming tables), тома, функции и процедуры, подключить внешние базы через foreign catalog и настроить AI/BI Genie.

## Ключевые понятия

- **Трёхуровневое пространство имён** - `catalog.schema.object`; catalog задаёт границы окружения или домена, schema - логическую группу, объекты хранят данные.
- **Catalog (каталог)** - верхний уровень изоляции; может иметь собственный managed storage location и привязки к рабочим областям.
- **Schema (схема)** - второй уровень; в Databricks `CREATE DATABASE` - синоним `CREATE SCHEMA`.
- **Managed table (управляемая таблица)** - Databricks управляет и метаданными, и файлами; при удалении таблицы файлы удаляются.
- **External table (внешняя таблица)** - регистрирует метаданные для данных во внешнем хранилище; при удалении файлы остаются.
- **Информационные ограничения (PRIMARY KEY, FOREIGN KEY)** - не enforced, используются для оптимизатора и моделирования.
- **Standard view / Dynamic view** - виртуальное представление; динамическое применяет фильтры строк и маски столбцов через `is_account_group_member()`.
- **Materialized view** - кешированный результат в Delta-таблице, обновляется инкрементально или полностью.
- **Streaming table** - Delta-таблица для append-only данных, которую обслуживает выделенный serverless pipeline.
- **Volume (том)** - governed-хранилище файлов; managed или external; путь `/Volumes/<catalog>/<schema>/<volume>/...`.
- **Foreign catalog (внешний каталог)** - зеркало внешней базы данных через connection; запросы выполняются на стороне внешней системы.
- **AI/BI Genie** - пространство с таблицами, описаниями, связями, SQL-выражениями и примерами для вопросов на естественном языке.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/1-introduction

Модуль строит структуру данных для разных окружений (dev, test, prod) и доменов с централизованным управлением. Создаются каталоги, схемы, таблицы, представления и тома; подключаются внешние базы; настраивается Genie.

### 2. Соглашения об именах
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/2-apply-naming-conventions

- Имена объектов до 255 символов, хранятся в нижнем регистре (`SalesData`, `salesdata`, `SALESDATA` - один объект); сопоставление регистронезависимое.
- Запрещены точки, пробелы, косая черта и управляющие ASCII-символы. Дефисы и специальные символы допустимы в обратных кавычках: `` `sales-data` ``.
- Имена столбцов сохраняют регистр, но запросы регистронезависимы.
- Рекомендуется lowercase с подчёркиваниями; не использовать camelCase и PascalCase.
- Слои в схемах: `bronze` (сырые), `silver` (очищенные), `gold` (агрегированные). Префикс `vw_` для представлений, `tmp_` для временных таблиц.
- Каталоги по домену (`sales_data`) или по окружению (`dev`, `test`, `prod`); комбинация `{domain}_{environment}`.
- Соглашения для ресурсов: кластеры `{environment}_{domain}_cluster`; job `job_{layer}_{purpose}`; Lakeflow pipelines `pipe_...`; потоковые `stream_{source}_to_{target}`; ноутбуки `notebook_{layer}_{purpose}`; дашборды `dashboard_{domain}_{purpose}`; запросы `query_{purpose}`.
- Внедрение: документировать, ограничивать права CREATE TABLE и CREATE SCHEMA, проверять имена в CI/CD, аудировать через information schema.

### 3. Создание каталога
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/3-create-catalog

- Каталог - основа изоляции; нужна роль metastore admin или привилегия CREATE CATALOG.
- При создании автоматически появляются схемы `default` и `information_schema`.
- Рабочие области: по умолчанию каталог доступен всем привязанным рабочим областям; для production ограничьте доступ production-рабочими областями.
- Managed storage: рекомендуется задавать; требуется внешний location и привилегия CREATE MANAGED STORAGE. Если у metastore нет default storage, его нужно указать явно.
- Удаление управляемой таблицы: файлы удаляются через восемь дней (по тексту урока).

### 4. Создание схемы
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/4-create-schema

- Нужны USE CATALOG и CREATE SCHEMA на родительском каталоге.
- Минимально для просмотра и запросов - USE SCHEMA; для создания таблиц - CREATE TABLE и другие привилегии объектов.
- Схема может иметь собственный managed location; иначе используется storage каталога.
- Схемы организуют по отделам, проектам или стадиям обработки (raw_data, cleansed_data, reporting_views).

### 5. Создание таблиц и представлений
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/5-create-tables-views-materialized

- **Managed tables** - по умолчанию; Delta Lake с ACID, time travel и enforcement схемы; при удалении удаляются и метаданные, и файлы. Поддерживаются `NOT NULL`, `CHECK`-ограничения и generated columns.
- **Primary и foreign keys** - доступны начиная с Databricks Runtime 11.3 LTS (полностью GA в 15.2+); информационные, не enforced; первичный ключ неявно NOT NULL; ограничения можно добавить через `ALTER TABLE ... ADD CONSTRAINT`.
- **External tables** - указывается `LOCATION`, которое должно защищаться external location; при удалении остаются файлы; для новых пайплайнов предпочтительны managed tables.
- **Standard views** - вычисляются при каждом обращении; обновляются вместе с таблицами; слои представлений не стоит делать слишком глубокими.
- **Dynamic views** - маскирование столбцов через CASE и `is_account_group_member('auditors')`; фильтрация строк через WHERE с проверкой группы. Требуют SQL warehouse, standard access mode compute или dedicated access mode compute на Databricks Runtime 15.4 LTS и новее.
- **Materialized views** - результат хранится как Delta-таблица; обновление вручную или по расписанию (`SCHEDULE EVERY 1 DAY`); инкрементальное обновление требует Delta-таблиц с включённым row tracking (`delta.enableRowTracking = true`, Runtime 14.1+; операция необратима и может долго выполняться на больших таблицах).
- **Streaming tables** - `CREATE OR REFRESH STREAMING TABLE`; обрабатывают только новые строки; подходят для Auto Loader, Kafka, слоёв bronze и silver. Расписание `SCHEDULE EVERY 1 HOUR` или `TRIGGER ON UPDATE`; ручное обновление `REFRESH STREAMING TABLE`.
- Рекомендация: кластеризация `CLUSTER BY` (liquid clustering) вместо ручного партиционирования.

Примеры из урока:

```
CREATE TABLE production.sales.sales_transactions (
  transaction_id BIGINT,
  customer_id INT,
  product_name STRING,
  amount DECIMAL(10,2),
  transaction_date DATE
);
```

```
CREATE VIEW sales_redacted AS
SELECT
  user_id,
  CASE WHEN
    is_account_group_member('auditors') THEN email
    ELSE 'REDACTED'
  END AS email,
  country_region,
  product,
  total
FROM sales_raw;
```

### 6. Создание томов
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/6-create-volumes

- Том - governed-контейнер для файлов любого формата (CSV, JSON, Parquet, изображения, ML-артефакты).
- **Managed volume**: хранилище управляется Unity Catalog; при удалении файлы помечаются к удалению после семидневного периода хранения (по тексту урока).
- **External volume**: указывается путь, файлы остаются в хранилище при удалении тома; путь должен входить в external location.
- Права: CREATE VOLUME на схему, USE на схему и каталог; для external - CREATE EXTERNAL VOLUME на external location.
- Привилегии тома: READ VOLUME, WRITE VOLUME, CREATE VOLUME, CREATE EXTERNAL VOLUME. Права наследуются от родительских объектов.
- Ограничение: нет ACL на уровне папок или подкаталогов; для разных уровней доступа создавайте отдельные тома.

Пути к файлам:

```
/Volumes/<catalog>/<schema>/<volume>/<path>/<filename>
```

### 7. Операции DDL
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/7-implement-data-definition-language-operations

- **Функции**: SQL-скалярные, Python-скалярные (`LANGUAGE PYTHON`, выполняются на serverless или pro SQL warehouse), табличные (`RETURNS TABLE`), временные (`CREATE TEMPORARY FUNCTION`, только в сессии).
- **Процедуры**: `CREATE PROCEDURE` с IN, OUT, INOUT параметрами, `SQL SECURITY INVOKER` (выполняются с правами вызывающего), вызов через `CALL`; требуется Unity Catalog и Databricks Runtime 17.0 или новее.
- **ALTER CATALOG**: смена владельца (`SET OWNER TO`), теги (`SET TAGS`), `ENABLE PREDICTIVE OPTIMIZATION` (наследуется таблицами).
- **ALTER TABLE**: `ADD COLUMN` (для существующих строк - NULL), `RENAME COLUMN` (требует column mapping), `DROP COLUMN` (сначала снимите зависимые ограничения и generated columns), `ALTER COLUMN ... TYPE` (например, INT → BIGINT). Нужна привилегия MODIFY.

Примеры:

```
CREATE FUNCTION dev_catalog.finance_schema.calculate_discount(price DOUBLE, discount_rate DOUBLE)
RETURNS DOUBLE
COMMENT 'Calculate discounted price'
RETURN price * (1 - discount_rate);
```

```
CALL dev_catalog.etl_schema.refresh_customer_summary(DATE '2024-01-15', :rows);
```

### 8. Внешний каталог (foreign catalog)
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/8-implement-foreign-catalog

- **Connection** хранит параметры подключения и учётные данные (через `secret(...)`), один connection может обслуживать несколько foreign catalogs.
- **Foreign catalog** зеркалирует базу внешней системы в пространстве имён Unity Catalog.
- Требования: право CREATE CONNECTION или metastore admin; compute Runtime 13.3 LTS или новее в режиме Standard или Dedicated; сетевой доступ к порту БД.
- Метаданные синхронизируются автоматически при обращении; для высокочастотных запросов можно обновлять вручную `REFRESH FOREIGN CATALOG | SCHEMA | TABLE` по расписанию Lakeflow Jobs.
- Права: USE CATALOG, USE SCHEMA, SELECT. Запросы транслируются и выполняются на стороне внешней БД; для больших результатов возможна нехватка памяти у исполнителя Databricks.

Примеры:

```
CREATE CONNECTION postgresql_prod TYPE postgresql
OPTIONS (
  host 'prod-db.example.com',
  port '5432',
  user secret ('prod-secrets','postgres-user'),
  password secret ('prod-secrets','postgres-password')
);
```

```
CREATE FOREIGN CATALOG IF NOT EXISTS prod_customer_data
USING CONNECTION postgresql_prod
OPTIONS (database 'customers');
```

### 9. Настройка инструкций AI/BI Genie
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/9-configure-ai-bi-genie-instructions

- В пространство Genie добавляется до 25 таблиц или представлений; разумно начинать с пяти и меньше.
- Описания таблиц и столбцов пишутся бизнес-языком; для столбцов можно добавить синонимы; технические столбцы скрываются (Hide selected columns).
- **Joins**: связи берутся из внешних ключей Unity Catalog или задаются вручную (Configure > Joins, например `opportunity.accountid = accounts.id`, Many to one).
- **Prompt matching**: format assistance и entity matching; entity matching - до 1 024 уникальных значений на столбец и до 120 столбцов в пространстве.
- **SQL expressions** (measures, filters, dimensions) в Configure > Instructions > SQL Expressions; **example SQL queries** - во вкладке SQL Queries; параметры через `:parameter_name`; параметризованные примеры, совпавшие с вопросом, помечаются Trusted.
- Лимиты: instructions - 100 (примеры SQL, SQL-функции и один блок текстовых инструкций); knowledge store snippets - 200 (описания таблиц, связи, SQL-выражения).
- Итеративная настройка: тестировать вопросы, смотреть Show generated code, сохранять исправления через Add as instruction, запускать бенчмарки, читать отзывы в Monitoring. Genie также предлагает выражения и связи на основе approved-ответов; предложения требуют подтверждения.

Пример примера SQL-запроса из урока:

```
-- What's our current pipeline by region?
SELECT
  accounts.region AS Region,
  SUM(opportunity.amount) AS Pipeline
FROM opportunity
JOIN accounts ON opportunity.accountid = accounts.id
WHERE
  opportunity.forecastcategory = 'Pipeline'
  AND opportunity.stagename NOT LIKE '%closed%'
GROUP BY accounts.region;
```

### 10. Упражнение: создание и организация объектов в Unity Catalog
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/10-exercise-create-organize-objects-unity-catalog

Упражнение (около 45 минут): построить пространство имён Unity Catalog для университетской платформы данных - каталог, схемы medallion, управляемые таблицы с первичными и внешними ключами, представления, том и SQL-функцию; добавить столбцы и теги. Требуется подписка Azure с правами администратора.

### 11. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/11-knowledge-check

В исходных материалах вопросы не приведены.

### 12. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/12-summary

Структура строится от каталогов (изоляция окружений) через схемы (логическая группировка) к таблицам, представлениям и томам; внешние объекты позволяют управлять существующими данными без миграции; динамические представления дают безопасность на уровне строк и столбцов; материализованные представления ускоряют аналитику; именование и метаданные делают данные находимыми.

## Важные команды / код / настройки

Создание каталога с managed location:

```
CREATE CATALOG IF NOT EXISTS prod_catalog
MANAGED LOCATION 'abfss://prod-data@mystorageaccount.dfs.core.windows.net/catalog-root'
COMMENT 'Production catalog with dedicated ADLS Gen2 storage';
```

Создание схемы:

```
CREATE SCHEMA IF NOT EXISTS prod_catalog.customer_analytics
COMMENT 'Customer behavior and segmentation analysis';
```

Materialized view с расписанием и row tracking:

```
ALTER TABLE sales_transactions
SET TBLPROPERTIES (delta.enableRowTracking = true);

CREATE MATERIALIZED VIEW daily_sales_summary
SCHEDULE EVERY 1 DAY
AS
SELECT
  transaction_date,
  COUNT(*) AS transaction_count,
  SUM(amount) AS total_sales
FROM sales_transactions
GROUP BY transaction_date;
```

Streaming table:

```
CREATE OR REFRESH STREAMING TABLE silver_orders
  TRIGGER ON UPDATE
  AS SELECT
    order_id,
    customer_id,
    order_total
  FROM STREAM bronze_orders;
```

Тома и привилегии:

```
CREATE VOLUME IF NOT EXISTS dev_catalog.bronze_schema.landing_files
COMMENT 'Landing area for CSV files from external systems';

GRANT READ VOLUME, WRITE VOLUME ON VOLUME dev_catalog.bronze_schema.landing_files TO `data-engineers`;
```

Права для внешнего каталога:

```
GRANT USE CATALOG ON CATALOG prod_customer_data TO `data-analysts`;
GRANT USE SCHEMA ON SCHEMA prod_customer_data.public TO `data-analysts`;
GRANT SELECT ON TABLE prod_customer_data.public.transactions TO `data-analysts`;
```

Лимиты и настройки: имена до 255 символов в нижнем регистре; до 1 024 значений entity matching на столбец и 120 столбцов; Genie instructions - 100, knowledge store snippets - 200; row tracking требует Runtime 14.1+; dynamic views - Runtime 15.4 LTS+; процедуры - Runtime 17.0+.

## Что запомнить

- Трёхуровневое пространство имён: изоляцию задают каталоги, группировку - схемы, данные - таблицы, представления и тома.
- Managed tables удаляют и файлы, и метаданные; external tables и external volumes оставляют файлы в хранилище.
- Ключи PRIMARY KEY и FOREIGN KEY информационные: помогают оптимизатору, но не проверяют данные.
- Динамические представления дают безопасность на уровне строк и столбцов без копий таблиц.
- Foreign catalog позволяет запрашивать внешние БД без ETL, а права Unity Catalog остаются централизованными.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/
- Связанные темы из уроков: Unity Catalog, Lakeflow Jobs, AI/BI Genie, Delta Lake (упомянуты в уроках модуля)
