# Основы потоковой обработки данных в Azure

**Источник:** https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-stream-processing/

## Цель модуля

Получить концептуальное представление о пакетной (batch) и потоковой (stream) обработке данных, о типовой архитектуре потоковых решений и о сервисах Azure и Microsoft Fabric для аналитики в реальном времени. Модуль не учит реализации потоковых решений.

## Ключевые понятия

- **Batch processing (пакетная обработка)** - накопление записей и обработка группы целиком за одну операцию по расписанию или при наступлении условия.
- **Stream processing (потоковая обработка)** - обработка каждого события сразу по мере поступления; задержка в секундах или миллисекундах.
- **Lambda architecture** - комбинация пакетного и потокового слоёв для исторического и реального времени.
- **Kappa architecture** - упрощённая альтернатива без отдельного пакетного слоя; все данные обрабатываются как поток, при необходимости поток переигрывается.
- **Streaming source (источник)** - место, где фиксируются события: очередь, папка, таблица.
- **Perpetual query (постоянный запрос)** - запрос, который непрерывно обрабатывает события; может выбирать, проецировать или агрегировать данные по временным окнам (windows).
- **Sink (приёмник)** - место записи результатов: файл, таблица, дашборд или другая очередь.
- **Delta Lake** - открытый формат хранения в data lake с транзакциями, enforcement схемы и единым доступом для пакетной и потоковой обработки.
- **KQL (Kusto Query Language)** - язык запросов для телеметрии и событий в Eventhouse.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-stream-processing/1-introduction

Рост объёма данных с устройств и сети позволяет обрабатывать их в реальном времени или почти в реальном времени. Модуль даёт концептуальный обзор и описывает сервисы Azure для аналитики реального времени.

### 2. Пакетная и потоковая обработка
Источник: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-stream-processing/2-batch-stream

- **Пакетная обработка**: данные накапливаются и обрабатываются группой; запуск по расписанию, по объёму или по событию. Плюсы: эффективная обработка больших объёмов, можно выполнять в непиковое время. Минусы: задержка результатов, ошибки могут остановить весь пакет, входные данные нужно полностью подготовить.
- **Потоковая обработка**: каждая запись обрабатывается при поступлении. Подходит для непрерывно генерируемых данных и для сценариев, требующих мгновенной реакции (например, пожарная сигнализация).
- **Различия**: пакет имеет доступ ко всему набору данных, поток - к последним данным или скользящему окну; пакет подходит для больших наборов и сложной аналитики, поток - для простых агрегатов и скользящих средних; задержка пакета - часы, потока - секунды или миллисекунды.
- **Комбинация**: lambda architecture использует потоковый слой для оперативной аналитики и пакетный слой для исторической; поток может также просто записывать данные в хранилище для последующей пакетной обработки.
- В уроке упомянута kappa architecture как упрощённая альтернатива; детали архитектур вне рамок модуля.

### 3. Общие элементы архитектуры потоковой обработки
Источник: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-stream-processing/3-explore-common-elements

Типовая схема: событие генерирует данные → данные фиксируются в источнике потока → постоянный запрос обрабатывает события (выбор, проекция, агрегация по окнам) → результат пишется в приёмник.

- **Real-time analytics services**: Microsoft Fabric Real-Time Intelligence (Eventstreams, Eventhouse, Real-Time Dashboards, Activator), Spark Structured Streaming (Azure Databricks и Microsoft Fabric), Azure Stream Analytics (PaaS для потоковых заданий вне Fabric).
- **Источники**: Azure Event Hubs (высокие объёмы событий, порядок внутри партиции, гарантия at-least-once), Azure IoT Hub (IoT-устройства), Azure Data Lake Storage Gen2 (может быть источником потока), Apache Kafka (часто вместе с Apache Spark).
- **Приёмники**: Azure Event Hubs (очередь для дальнейшей обработки), Azure Data Lake Storage Gen2 / Microsoft OneLake / Azure Blob Storage (файлы), Azure SQL Database / Azure Databricks / Microsoft Fabric (таблицы), Microsoft Power BI (визуализация в реальном времени).

### 4. Microsoft Fabric Real-Time Intelligence
Источник: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-stream-processing/4-fabric-real-time-intelligence

- Набор инструментов Fabric для приёма, обработки и анализа потоков с визуализацией и действиями в одном рабочем пространстве.
- **Real-time hub** - централизованный каталог потоковых источников организации с возможностью обнаружения и совместного использования.
- Исследование данных: выбор потока, визуализация паттернов, аномалий и прогнозов; дашборды в реальном времени доступны через визуальные инструменты, естественный язык и Copilot.
- **Activator** - оповещения, которые запускают действия при выполнении условий.

### 5. Apache Spark Structured Streaming
Источник: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-stream-processing/5-spark-streaming

- Spark распределяет работу по кластеру и поддерживает Python, Scala, Java, R и SQL; доступен в Microsoft Fabric и Azure Databricks.
- Spark Structured Streaming рассматривает поток как таблицу, которая постоянно пополняется: источник → DataFrame → запрос (например, события в минуту или скользящее среднее) → приёмник.
- **Delta Lake** добавляет надёжность (отслеживание изменений, защита от частичных записей), enforcement схемы и единую работу для потоковой записи и пакетных запросов. Поддерживается в Spark-средах Microsoft Fabric и Azure Databricks.

### 6. Упражнение: изучение Real-Time Intelligence в Fabric
Источник: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-stream-processing/6-exercise-real-time-intelligence

Упражнение (около 15 минут) с примером данных в Microsoft Fabric. Нужна учётная запись Microsoft Fabric или бесплатная пробная версия. Подробных шагов в исходниках нет.

### 7. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-stream-processing/7-knowledge-check

В исходных материалах вопросы не приведены.

### 8. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-stream-processing/8-summary

Модуль охватил сравнение batch и stream, общие элементы потоковых решений, Fabric Real-Time Intelligence и Spark Structured Streaming. В качестве следующего шага упомянута сертификация Azure Data Fundamentals.

## Важные команды / код / настройки

Код и команды в уроках не приведены. Упомянутые технологии и их роли:
- Источники: Azure Event Hubs, Azure IoT Hub, Azure Data Lake Storage Gen2, Apache Kafka.
- Приёмники: Event Hubs, Data Lake Storage Gen2 / OneLake / Blob Storage, Azure SQL Database / Azure Databricks / Microsoft Fabric, Power BI.
- Языки: KQL для Eventhouse; Python, Scala, Java, R, SQL для Spark.

## Что запомнить

- Пакетная обработка даёт полноту и эффективность за счёт задержки; потоковая - мгновенность за счёт ограниченного обзора данных.
- Постоянный запрос (perpetual query) выбирает, проецирует или агрегирует события по временным окнам.
- Azure Event Hubs - основной сервис приёма высокообъёмных событий с порядком внутри партиции и гарантией at-least-once.
- Azure Stream Analytics - PaaS для потоковых заданий вне Fabric; Spark Structured Streaming - для Spark-сред (Databricks, Fabric).
- Delta Lake и Spark Structured Streaming позволяют использовать одну таблицу и для потоковой записи, и для пакетных запросов.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-stream-processing/
- Microsoft Fabric Real-Time Intelligence; Spark Structured Streaming programming guide; Lakehouse and Delta Lake tables (ссылки из уроков модуля)
- Сертификация Azure Data Fundamentals (упомянута в уроке 8)
