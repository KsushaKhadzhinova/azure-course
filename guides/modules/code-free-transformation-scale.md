# Преобразование данных без кода в масштабе с Azure Data Factory

**Источник:** https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/

## Цель модуля

Научиться выполнять преобразования и очистку данных в Azure Data Factory: визуально, через Mapping Data Flow, с отладкой потоков, подготовкой данных через Wrangling Data Flow, вызовом внешних вычислительных сервисов (например, Azure Databricks) и запуском пакетов SSIS. Модуль отмечает, что Data Factory в Microsoft Fabric является следующим поколением Azure Data Factory.

## Ключевые понятия

- **Mapping Data Flow** — визуальные потоки преобразований без кода; выполняются на масштабируемых кластерах Apache Spark, которыми управляет Azure Data Factory.
- **Data Flow Debug** — режим отладки с интерактивным Spark-кластером и предпросмотром данных на каждом шаге.
- **Wrangling Data Flow (Power Query)** — интерактивная подготовка данных в редакторе Online Mashup Editor; язык M переводится в код Spark.
- **Compute transformations** — преобразования на внешних вычислительных ресурсах: HDInsight, Azure Batch, Azure Machine Learning, Azure SQL, Azure Databricks, Azure Functions.
- **Azure-SSIS Integration Runtime** — среда для переноса существующих пакетов SSIS в Azure без существенных изменений.
- **Transformation categories** — schema modifier, row modifier, multiple inputs/outputs, formatters.
- **Data Flow Expression Builder** — редактор выражений языка Data Flow с автодополнением и проверкой синтаксиса.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/1-introduction

Введение: Azure Data Factory позволяет выполнять преобразования без кода через Mapping Data Flow, использовать другие сервисы Azure и повторно использовать пакеты SSIS. Также доступна разведка данных через Wrangling Data Flows.

### 2. Explain Azure Data Factory transformation methods
https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/2-explain-transformation-methods

Три способа преобразований: Mapping Data Flows (визуально, Spark), вычислительные ресурсы (через активности pipeline) и пакеты SSIS. Таблица соответствия вычислительных сред и активностей приведена в разделе «Важные команды».

### 3. Describe Azure Data Factory transformation types
https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/3-describe-transformation-types

Четыре категории: schema modifier (например, Derived Column), row modifier (например, Sort), multiple inputs/outputs (например, Union) и formatters (например, Parse). Приведен полный список преобразований (Aggregate, Alter row, Assert, Cast, Join, Lookup, Pivot, Window и др.). Выражения создаются в Expression Builder.

### 4. Exercise - Author an Azure Data Factory mapping data flow
https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/4-author-azure-data-factory-mapping-data-flow

Практика (около 10 минут). Источник — ADLS Gen2 (набор данных о фильмах). Шаги: включить Data Flow Debug, добавить источник, Select (переименовать колонку «Rotton» в «Rotten» и удалить Rating), Filter (`toInteger(year) > 1950`), Derived Column (PrimaryGenre), Window (RatingsRank), Aggregate, Alter Row (upsert), Sink в Azure Synapse Analytics с включенным Allow upsert по ключам PrimaryGenre и year. Затем запуск pipeline.

### 5. Debug mapping data flow
https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/5-debug-mapping-data-flow

Включение Data Flow Debug поднимает Spark-кластер (обычно 5–7 минут). По умолчанию для AutoResolveIntegrationRuntime — восемь ядер и TTL 60 минут. На вкладке Data Preview виден результат на каждом шаге. Рекомендуется ограничивать число строк. Режим тарифицируется почасово, включая TTL, поэтому его нужно выключать после отладки.

### 6. Exercise - Use Azure Data Factory wrangling data
https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/6-use-wrangling-data

Power Query в Azure Data Factory позволяет готовить данные интерактивно, как в Excel, а также через формулы M. Поддерживаемые источники: Azure Blob Storage и ADLS Gen2 (CSV, Parquet, Excel), Azure SQL Database и Azure Synapse Analytics. Описаны компоненты редактора: список наборов данных, панель функций, заголовки колонок, Settings, Steps, список выходов и кнопка Publish. Не все функции M поддерживаются.

### 7. Exercise - Use compute transformations within Azure Data Factory
https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/7-use-compute-transformations

Интеграция Azure Databricks и ADF: сохранить данные в storage account, скопировать их Copy activity, затем выполнить Databricks notebook в pipeline. Шаги: создать access token в Databricks, создать notebook с параметрами (`dbutils.widgets`), создать linked service Azure Databricks, создать pipeline с Notebook activity, запустить триггер, проверить в Monitor и в журнале событий кластера.

### 8. Exercise - Integrate SQL server integration services packages within Azure Data Factory
https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/8-integrate-sql-server-integration-services-packages

Перенос существующих пакетов SSIS через Azure-SSIS Integration Runtime. Для модели развертывания проектов нужен каталог SSISDB в Azure SQL Database или Azure SQL Managed Instance; для модели пакетов нужен SSISDB не обязателен. Настройки: General (размер и число узлов, редакция, Azure Hybrid Benefit), Deployment (SSISDB, package stores), Advanced (параллельные выполнения на узел, custom setups, VNet, self-hosted IR как прокси). Выполняется за около 7 минут.

### 9. Module assessment
https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/9-knowledge-check

Проверочный тест (около 5 минут). Вопросы и ответы в источнике не приведены.

### 10. Summary
https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/10-summary

Mapping Data Flow позволяет выполнять очистку без кода перед загрузкой в хранилище данных или подготовкой к аналитике. При необходимости ADF вызывает другие сервисы Azure, а пакеты SSIS можно запускать в ADF. Не забывайте удалять ресурсы после работы, чтобы не платить за них.

## Важные команды / код / настройки

**Вычислительные среды и активности (таблица из урока 2):**

| Вычислительная среда | Активности |
|---|---|
| On-demand HDInsight cluster или собственный HDInsight | Hive, Pig, Spark, MapReduce, Hadoop Streaming |
| Azure Batch | Custom activities |
| Azure Machine Learning | Azure Machine Learning Execute Pipeline |
| Azure SQL Database, SQL Server | Stored Procedure |
| Azure Databricks | Notebook, Jar, Python |
| Azure Function | Azure Function activity |

**Выражения из упражнения с Mapping Data Flow:**

- Фильтр: `toInteger(year) > 1950`
- Получение основного жанра: функции `locate`, `iif` и `left` (индекс первого символа `|` в строке `genre1|genre2|...|genreN`; если индекс больше 1, берется `left`, иначе значение поля genres).

**Настройки отладки:**

- Data Flow Debug включается переключателем над канвасом.
- AutoResolveIntegrationRuntime: восемь ядер, TTL по умолчанию 60 минут.
- Прогрев кластера: 5–7 минут.

**Azure Synapse Analytics sink:** так как используется PolyBase, нужно указать staging-папку в Blob или ADLS (раздел PolyBase в настройках Execute Data Flow activity).

**Notebook для Databricks (из упражнения):**

```
# Creating widgets for using parameters, and printing the parameters

dbutils.widgets.text("input", "","")
y = dbutils.widgets.get("input")
print ("Param -\'input':")
print (y)
```

Путь к notebook в упражнении: `/adftutorial/mynotebook`. В Notebook activity Base Parameter `input` получает значение `@pipeline().parameters.name`.

**Прочие настройки из источника:**

- Access token Databricks в упражнении: комментарий «For ADF Integration», срок действия 10 дней. Источник отмечает, что personal access tokens подходят для обучения и тестирования; для production рекомендуются более безопасные способы, и linked service поддерживает managed identity.
- Azure-SSIS IR: Node Size, Node Number, Edition/License (Standard или Enterprise), Azure Hybrid Benefit (Save Money), Maximum Parallel Executions Per Node.
- Для Azure-SSIS IR рекомендуется размещать в той же локации, что и сервер базы данных SSISDB.
- Для Azure File Storage package store поддерживается только метод аутентификации Basic; хост задается в виде `\\<storage account name>.file.core.windows.net<file share name>`.

## Что запомнить

- Mapping Data Flow выполняет визуальные преобразования на управляемых Spark-кластерах Azure Data Factory без написания кода.
- Преобразования делятся на schema modifier, row modifier, multiple inputs/outputs и formatters; Aggregate, Window, Alter Row и Sink образуют типичный конвейер.
- Debug-режим удобен для проверки шагов, но тарифицируется почасово: выключайте его после отладки.
- Wrangling Data Flow (Power Query) подходит для интерактивной подготовки данных; поддерживается не все функции M.
- Существующие пакеты SSIS можно переносить в Azure-SSIS Integration Runtime, а сложные вычисления выполнять через Databricks, HDInsight и другие сервисы.

## Связанные материалы

- Source transformation in mapping data flows (документация Microsoft; ссылка упоминается в уроке 4).
- Power Query data wrangling functions (упоминается в уроке 6).
- Set up a self-hosted IR as proxy (упоминается в уроке 8).
- Data Factory in Microsoft Fabric — следующее поколение Azure Data Factory (упоминается во введении).
