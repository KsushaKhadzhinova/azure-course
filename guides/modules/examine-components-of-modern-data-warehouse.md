# Компоненты современного хранилища данных

**Источник:** https://learn.microsoft.com/en-us/training/modules/examine-components-of-modern-data-warehouse/

## Цель модуля

Получить общее представление о компонентах крупномасштабного аналитического решения: архитектуре хранилища данных, процессах приема данных, аналитических хранилищах и сервисах Azure для их реализации. Модуль знакомит с Microsoft Fabric и Azure Databricks и включает практику в Microsoft Fabric.

## Ключевые понятия

- **Microsoft Fabric** — единая SaaS-платформа аналитики с общим хранилищем OneLake; включает Lakehouse, Warehouse, Data Factory, Power BI и другие компоненты.
- **Azure Databricks** — управляемый сервис аналитики на Apache Spark с форматом Delta Lake, Unity Catalog и Databricks SQL.
- **ETL и ELT** — извлечение, преобразование и загрузка (преобразование до загрузки) и извлечение, загрузка и преобразование (преобразование после загрузки).
- **Data lakehouse** — архитектура, сочетающая гибкость data lake и SQL-аналитику data warehouse; реализуется через Delta Lake.
- **Star schema и snowflake schema** — схемы хранилища с таблицами фактов и измерений.
- **Semantic model** — табличная модель с отношениями, иерархиями и мерами на DAX, которая лежит в основе Power BI и Fabric.
- **Direct Lake** — режим Fabric, в котором семантическая модель читает Delta-таблицы из OneLake без импорта копии данных.
- **OneLake shortcut** — ссылка на внешнее хранилище, которая позволяет работать с данными без копирования.
- **Mirroring** — непрерывная репликация внешней базы данных в OneLake.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/examine-components-of-modern-data-warehouse/1-introduction

Введение в две аналитические платформы Azure: Microsoft Fabric (SaaS с OneLake) и Azure Databricks (Spark, Delta Lake). Крупномасштабная аналитика сочетает традиционное хранилище для BI с обработкой больших данных из data lake.

### 2. Describe data warehousing architecture
https://learn.microsoft.com/en-us/training/modules/examine-components-of-modern-data-warehouse/2-describe-warehousing

Элементы архитектуры: прием и обработка данных (ETL или ELT, пакетная и потоковая обработка), аналитическое хранилище (data warehouse, data lake, lakehouse), аналитическая модель (semantic model вместо устаревших кубов SSAS Multidimensional), визуализация и AI-ассистированная аналитика (Copilot в Fabric и Power BI, Genie в Azure Databricks). Описаны компоненты Fabric (Lakehouse, Warehouse, Data Factory, Power BI) и Azure Databricks (Lakehouse, Databricks SQL, Notebooks, Unity Catalog, Genie).

### 3. Explore data ingestion pipelines
https://learn.microsoft.com/en-us/training/modules/examine-components-of-modern-data-warehouse/3-data-ingestion-pipelines

Способы приема данных в Fabric: Data Factory (pipelines и Dataflows Gen2), OneLake shortcuts, Mirroring, Eventstream и Fabric Notebooks. Azure Data Factory — отдельный сервис для сценариев вне Fabric. В Azure Databricks: Lakeflow pipelines (декларативный подход) и Databricks Notebooks.

### 4. Explore analytical data stores
https://learn.microsoft.com/en-us/training/modules/examine-components-of-modern-data-warehouse/4-analytical-data-stores

Хранилище данных — реляционная БД со схемой «звезда» или «снежинка», подходит для структурированных данных и SQL. Data lake — файловое хранилище с schema-on-read, подходит для смешанных данных. Lakehouse объединяет оба подхода на основе Delta Lake. Fabric Lakehouse (Delta в OneLake, SQL analytics endpoint, Spark) и Fabric Warehouse (T-SQL, строгая схема, конкурентность). В Azure Databricks — Databricks SQL Warehouse для BI-инструментов. Возможна комбинация: копирование в data lake, обработка в Azure Databricks и загрузка результатов в Fabric Warehouse.

### 5. Exercise: Explore data analytics in Microsoft Fabric
https://learn.microsoft.com/en-us/training/modules/examine-components-of-modern-data-warehouse/5-exercise-data-analytics-fabric

Практика (около 30 минут): создать lakehouse в Microsoft Fabric, загрузить и проанализировать данные. Нужна учетная запись Microsoft Fabric (есть бесплатная пробная версия).

### 6. Knowledge check
https://learn.microsoft.com/en-us/training/modules/examine-components-of-modern-data-warehouse/6-knowledge-check

Проверочный тест (около 3 минут). Вопросы и ответы в источнике не приведены.

### 7. Summary
https://learn.microsoft.com/en-us/training/modules/examine-components-of-modern-data-warehouse/7-summary

Итоги: элементы решения, особенности приема данных, типы аналитических хранилищ и сервисы Azure, а также практика с Fabric. Рекомендуемый следующий шаг — сертификация Azure Data Fundamentals.

## Важные команды / код / настройки

В источнике нет команд и кода. Упомянутые сущности и режимы:

- **OneLake** — общий слой хранения для всех нагрузок Fabric; стандартный формат лейкхауса — Delta Lake.
- **Direct Lake** — режим семантической модели, который читает Delta-таблицы из OneLake без импорта.
- **Databricks SQL Warehouse** — SQL-эндпоинт для BI и параллельных запросов.
- **Fabric Mirroring** — автоматическая near-real-time репликация без пайплайнов (Azure SQL Database, Azure Cosmos DB, Snowflake и другие).
- **Eventstream** — маршрутизация и фильтрация потоков (Event Hubs, Kafka, IoT Hub) в Lakehouse или Eventhouse.

## Что запомнить

- Microsoft Fabric объединяет инженерию данных, хранилище, аналитику в реальном времени и Power BI поверх общего OneLake.
- Azure Databricks на Apache Spark и Delta Lake подходит для code-first рабочих процессов и мультиоблачных сценариев.
- ELT загружает данные в хранилище и затем преобразует их; ETL преобразует до загрузки.
- Lakehouse сочетает гибкость data lake и SQL-аналитику data warehouse; основа — Delta Lake.
- Для приема данных в Fabric выбирайте Data Factory (pipelines, Dataflows Gen2), shortcuts, Mirroring, Eventstream или Notebooks в зависимости от сценария.

## Связанные материалы

- Сертификация Azure Data Fundamentals (упоминается в уроке 7).
- Try Microsoft Fabric for free (упоминается в уроке 5).
