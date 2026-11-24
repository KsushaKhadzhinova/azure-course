# Введение в потоковую обработку данных

**Источник:** https://learn.microsoft.com/en-us/training/modules/introduction-to-data-streaming/

## Цель модуля

Понять, что такое потоковые данные, и научиться начинать работу с Azure Stream Analytics: обрабатывать поток событий (фильтровать, агрегировать) и передавать результаты в выходные приемники или визуализации.

## Ключевые понятия

- **Data stream (поток данных)** - неограниченная, постоянно пополняемая последовательность записей, обычно связанных с событиями во времени.
- **Temporal data (временные данные)** - каждая запись содержит время, когда произошло (или было зафиксировано) событие.
- **Temporal windows (временные окна)** - агрегация потока по окнам, например число постов в минуту или средние осадки за час. В no-code редакторе упоминаются tumbling, hopping и session окна.
- **Stream Analytics job (задание)** - PaaS-сервис в подписке Azure с входами, выходами и запросом, который работает постоянно.
- **Stream Analytics cluster (кластер)** - однотенантное развертывание того же движка с настраиваемой масштабируемостью под нагрузку и бюджет.
- **Input (вход)** - источник потока: Azure Event Hubs, Azure IoT Hub, Blob storage, Azure Data Lake Storage Gen2, Apache Kafka. Reference input - статические справочные данные для обогащения потока.
- **Output (выход)** - приемник результатов: Azure Data Lake Storage Gen2, Azure SQL Database, Azure Cosmos DB, Azure Data Explorer, Power BI, Event Hubs и др.
- **Query (запрос)** - SQL-подобный запрос, который выбирает, фильтрует и агрегирует данные из входа и записывает результат в выход.
- **TIMESTAMP BY** - явно задает поле, которое используется как временная метка события. По умолчанию используется время поступления события на вход.
- **Exactly once processing / at-least-once delivery** - гарантии обработки: события не теряются, а для выбранных выходов обработка выполняется ровно один раз.
- **No-code editor** - визуальный редактор (drag-and-drop) для построения задания без написания SQL.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/introduction-to-data-streaming/1-introduction

Потоковые данные генерируют приложения, IoT-устройства и датчики. Примеры: рекомендации по clickstream в интернет-магазине, телеметрия производственного оборудования, проверка кредитных транзакций на мошенничество. Azure Stream Analytics - облачный движок для фильтрации, агрегации и обработки потоков.

### 2. Understand data streams
https://learn.microsoft.com/en-us/training/modules/introduction-to-data-streaming/2-understand-data-streams

Поток - это бесконечная серия данных о событиях. Типичные цели: непрерывный анализ для выявления проблем и трендов, понимание поведения системы, запуск действий при превышении порогов. Характеристики решений: неограниченный источник, временные метки у каждой записи, агрегация по временным окнам, использование результатов для автоматизации, визуализации или сохранения в аналитическое хранилище.

### 3. Understand event processing
https://learn.microsoft.com/en-us/training/modules/introduction-to-data-streaming/3-understand-event-processing

Схема работы: вход (input) -> запрос (query) -> выход (output). Запущенный запрос выполняется постоянно. Stream Analytics - полностью управляемый PaaS-сервис со встроенным checkpointing и восстановлением. Описаны входы, выходы, запросы с TIMESTAMP BY, поле EventProcessedUtcTime, а также кластеры и no-code редактор.

### 4. Exercise - Get started with Azure Stream Analytics
https://learn.microsoft.com/en-us/training/modules/introduction-to-data-streaming/4-process-events-azure-stream-analytics

Практическое задание (около 15 минут): пример решения, которое анализирует потоковые данные телефонных звонков для выявления мошеннических звонков. Нужны подписка Azure и учетная запись Power BI.

### 5. Module assessment
https://learn.microsoft.com/en-us/training/modules/introduction-to-data-streaming/5-knowledge-check

Итоговая проверка знаний (около 3 минут). Текст в источнике не приведен.

### 6. Summary
https://learn.microsoft.com/en-us/training/modules/introduction-to-data-streaming/6-summary

Azure Stream Analytics - PaaS-решение для непрерывной обработки потока данных для отчетности в реальном времени, автоматических действий и интеграции с аналитикой предприятия. Модуль охватывает: понятие потоков данных, обработку событий, оконные функции и начало работы с Azure Stream Analytics.

## Важные команды / код / настройки

Пример запроса из источника (фильтрация холодных температур):

```
SELECT observation_time, weather_station, temperature
INTO cold-temps
FROM weather-events TIMESTAMP BY observation_time
WHERE temperature < 0
```

Запрос выбирает события из входа `weather-events` с температурой ниже 0 и записывает результат в выход `cold-temps`.

## Что запомнить

- Потоковые данные неограничены и постоянно поступают; у каждой записи должна быть временная метка.
- Azure Stream Analytics строит задание из трех частей: входы, запрос и выходы.
- Запрос на SQL-подобном языке с `TIMESTAMP BY` определяет время события; без него используется время поступления.
- Агрегация выполняется по временным окнам (tumbling, hopping, session).
- Сервис гарантирует, что события не теряются (at-least-once), и поддерживает exactly once для выбранных выходов.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/introduction-to-data-streaming/
- В источнике упоминаются (без ссылок в тексте): документация Azure Stream Analytics, Event delivery guarantees, Overview of Azure Stream Analytics cluster, No-code stream processing in Azure Stream Analytics.
