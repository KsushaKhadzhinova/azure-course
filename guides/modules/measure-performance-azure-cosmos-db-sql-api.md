# Измерение производительности Azure Cosmos DB (SQL API) с Azure Monitor

**Источник:** https://learn.microsoft.com/en-us/training/modules/measure-performance-azure-cosmos-db-sql-api/

## Цель модуля

Научиться использовать Azure Monitor для наблюдения за Azure Cosmos DB: измерять пропускную способность (Total Request Units), обнаруживать события ограничения скорости (429), анализировать логи через диагностические настройки и запросы KQL.

## Ключевые понятия

- **Azure Monitor** - комплексный сервис мониторинга Azure; собирает метрики и телеметрию Azure Cosmos DB.
- **Metrics (метрики)** - серверные счетчики (пропускная способность, доступность хранилища, задержка, согласованность, системные показатели); собираются каждую минуту, хранятся 30 дней по умолчанию.
- **Diagnostic logs (диагностические логи)** - события и трассировки, которые сохраняются только после создания диагностической настройки (diagnostic setting).
- **Diagnostic setting (диагностическая настройка)** - правило отправки ресурсных логов в Log Analytics, Event Hubs или Storage Account.
- **Total Request Units** - метрика потребления RU по операциям; можно разбивать по CollectionName, DatabaseName, OperationType, Region, Status, StatusCode.
- **429 (Request rate too large)** - ответ при превышении provisioned RU/s; причины: большая частота запросов, высокая частота метаданных, временная ошибка сервиса.
- **Hot partition (горячая партиция)** - перекос нагрузки на одну физическую партицию; диагностируется по графику Normalized RU Consumption.
- **Log Analytics / KQL (Kusto Query Language)** - хранилище логов и язык запросов к ним.
- **AzureDiagnostics vs resource-specific tables** - общая устаревшая таблица и предпочтительные таблицы с префиксом CDB.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/measure-performance-azure-cosmos-db-sql-api/1-introduction

Azure Cosmos DB создает данные мониторинга через Azure Monitor, который собирает метрики и телеметрию. Цели модуля: понимать, как Cosmos DB использует Azure Monitor для серверных метрик; измерять пропускную способность; наблюдать события ограничения скорости; запрашивать логи телеметрии; измерять пропускную способность распределения хранения между партициями (эта тема в исходных уроках не раскрыта).

### 2. Azure Monitor
Источник: https://learn.microsoft.com/en-us/training/modules/measure-performance-azure-cosmos-db-sql-api/2-understand-azure-monitor

- **Метрики**: собираются по умолчанию каждую минуту, хранятся 30 дней; включают пропускную способность, доступность хранилища, задержку, согласованность и системные показатели. Имена измерений (например, имя контейнера) не чувствительны к регистру.
- **Диагностические логи**: события и трассировки, например изменение пропускной способности контейнера; по ним можно строить запросы.
- **Портал Azure Cosmos DB**: метрики на вкладке Metrics аккаунта; хранятся 7 дней.
- **NoSQL SDK и REST API**: программный мониторинг через заголовки и SDK (.NET, Java, Python, Node.js).
- Возможности Azure Monitor: сбор и маршрутизация, анализ метрик, анализ логов, алерты, программный мониторинг.
- Страница Overview базы данных в портале показывает краткую сводку запросов и почасовой биллинг; Azure Monitor собирает больше метрик, включая request units.
- Ресурсные логи не собираются без диагностической настройки, а метрики собираются автоматически и могут направляться в другие места той же настройкой.
- Анализ метрик: Metrics explorer, фильтр Cosmos DB standard metrics в Metric Namespace.
- Логи хранятся в таблицах AzureDiagnostics и AzureActivity; для записей Cosmos DB фильтр `resourceprovider` равен `MICROSOFT.DOCUMENTDB`.
- Алерты: например, когда контейнер или база превысили provisioned throughput.
- NoSQL API не содержит метрик уровня аккаунта (объем хранения, общее число запросов), но дает метрики уровня коллекции через REST API и .NET SDK.

### 3. Измерение пропускной способности
Источник: https://learn.microsoft.com/en-us/training/modules/measure-performance-azure-cosmos-db-sql-api/3-measure-throughput

- Метрика **Total Request Units** показывает RU по операциям; помогает выявить операции, которые потребляют больше RU или накапливают больше RU за интервал.
- Для дорогих вставок и upsert проверьте индексную политику (over- или under-indexing); для запросов - добавьте фильтр, используйте partition key, уменьшите результат.
- Путь в портале: Azure Monitor - Metrics - ресурс Azure Cosmos DB accounts - аккаунт - Total Request Units - агрегация, временной диапазон и гранулярность.
- Разбивка (Apply splitting) по CollectionName, DatabaseName, OperationType, Region, Status, StatusCode позволяет сравнить разные типы операций.

### 4. События ограничения скорости (429)
Источник: https://learn.microsoft.com/en-us/training/modules/measure-performance-azure-cosmos-db-sql-api/4-observe-rate-limiting-events

- Код 429 (Request rate too large) возникает, когда RU за секунду превышают provisioned RU/s.
- **Большая частота запросов** - самая частая причина. Проверьте Insights - Request - Total Request by Status Code. Обычно допустимо менее 5% запросов с 429; если доля выше 5%, возможна горячая партиция: проверьте Insights - Throughput - Normalized RU Consumption (%) By PartitionKeyRangeID.
- **Метаданные**: создание, чтение, изменение и удаление контейнеров или баз, список баз и контейнеров, запрос текущего throughput. Проверьте Insights - System - Metadata Requests That Exceeded Capacity (429s).
- **Временная ошибка сервиса**: одновременные 503 в Total Request by Status Code могут указывать на временные сбои сервиса.

### 5. Запросы к логам
Источник: https://learn.microsoft.com/en-us/training/modules/measure-performance-azure-cosmos-db-sql-api/5-query-logs

- Ресурсные логи собираются через диагностические настройки и отправляются в Log Analytics workspace, Event Hubs или Storage Account. Создание: портал (раздел Monitoring - Diagnostic settings), REST API, PowerShell или Azure CLI.
- Таблицы логов NoSQL API: **DataPlaneRequests** (операции создания, изменения, удаления и чтения данных); **QueryRuntimeStatistics** (запросы); **PartitionKeyStatistics** (статистика логических партиций в оценочных KB, полезно при перекосе хранения); **PartitionKeyRUConsumption** (агрегированное потребление RU/s по ключам каждую секунду, полезно при горячих партициях); **ControlPlaneRequests** (управляющие операции, например добавление или удаление регионов).
- Предпочтительный режим - resource-specific таблицы (по одной на категорию); устаревший - общая таблица AzureDiagnostics. В AzureDiagnostics фильтруйте по `ResourceProvider=="MICROSOFT.DOCUMENTDB"`.
- Resource-specific таблицы используют префикс `CDB` (например, `CDBDataPlaneRequests`).

## Важные команды / код / настройки

- Запрос количества и суммарного RU по типам операций за час (AzureDiagnostics):
  ```
  AzureDiagnostics
  | where TimeGenerated >= ago(1h)
  | where ResourceProvider=="MICROSOFT.DOCUMENTDB" and Category=="DataPlaneRequests"
  | summarize OperationCount = count(), TotalRequestCharged=sum(todouble(requestCharge_s)) by OperationName
  | order by TotalRequestCharged desc
  ```
- График успешных (200) и ограниченных (429) запросов с агрегацией по 10 минут (AzureDiagnostics):
  ```
  AzureDiagnostics
  | where TimeGenerated >= ago(1h)
  | where ResourceProvider=="MICROSOFT.DOCUMENTDB" and Category=="DataPlaneRequests"
  | summarize requestcount=count() by statusCode_s, bin(TimeGenerated, 10m)
  | render timechart
  ```
- Тот же запрос к resource-specific таблице (CDBDataPlaneRequests):
  ```
  CDBDataPlaneRequests
  | where TimeGenerated >= ago(1h)
  | summarize OperationCount = count(), TotalRequestCharged=sum(todouble(RequestCharge)) by OperationName
  | order by TotalRequestCharged desc
  ```
- График статусов для CDBDataPlaneRequests: `CDBDataPlaneRequests | where TimeGenerated >= ago(2h) | summarize requestcount=count() by StatusCode, bin(TimeGenerated, 10m) | render timechart` (в источнике указано ago(2h), хотя текст упоминает последний час).
- Метрика Total Request Units в Azure Monitor (Metrics), разбивка по OperationType.
- Пути портала: Insights - Request, Insights - Throughput, Insights - System; Monitoring - Diagnostic settings.

## Что запомнить

- Azure Monitor собирает метрики Cosmos DB автоматически (каждую минуту, 30 дней), а логи - только после диагностической настройки.
- Total Request Units с разбивкой по OperationType показывает, какие операции дороже всего.
- Для 429 сначала проверьте долю запросов: до 5% обычно нормально; выше - ищите горячую партицию или перегрузку метаданными.
- Таблица PartitionKeyRUConsumption помогает найти горячие партиции, PartitionKeyStatistics - перекос хранения.
- Предпочтительны resource-specific таблицы с префиксом CDB; устаревшая AzureDiagnostics требует фильтра ResourceProvider.

## Связанные материалы

- Azure Monitor overview
- Monitor Azure Cosmos DB
- Monitoring Azure Cosmos DB data reference
- How to monitor throughput or request unit usage of an operation in Azure Cosmos DB
- Optimize your Azure Cosmos DB application using rate limiting
- Diagnose and troubleshoot Azure Cosmos DB request rate too large (429) exceptions
- Troubleshoot issues with diagnostics queries
- Monitor Azure Cosmos DB data by using diagnostic settings in Azure
- Create diagnostic settings to send Azure Monitor platform logs and metrics to different destinations
- Tutorial: Use Kusto queries (Azure Monitor)
