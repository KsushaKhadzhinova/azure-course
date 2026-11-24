# Визуализация данных в реальном времени: Azure Stream Analytics и Power BI

**Источник:** https://learn.microsoft.com/en-us/training/modules/visualize-real-time-data-azure-stream-analytics-power-bi/

## Цель модуля

Научиться направлять результаты запроса Azure Stream Analytics в выход Power BI и строить по ним дашборды с визуализацией в реальном времени. Важное замечание из источника: потоковая передача в Power BI выводится из эксплуатации. С 31 октября 2027 года нельзя создавать задания Stream Analytics с выходом Power BI, а существующие задания с ним перестанут работать. Microsoft рекомендует переходить на Real-Time Intelligence в Microsoft Fabric.

## Ключевые понятия

- **Power BI output** — выход Stream Analytics, который записывает результаты в таблицу потокового набора данных Power BI.
- **Streaming dataset** — набор данных Power BI, который создается автоматически и обновляется при поступлении результатов.
- **Real-time visualization tile** — плитка дашборда, которая динамически отображает данные потокового набора.
- **Authorize connection (User token и Managed Identity)** — способы авторизации выхода в Power BI.
- **Ограничения выхода** — примерно один вызов Power BI в секунду и пакеты до 15 КБ.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/visualize-real-time-data-azure-stream-analytics-power-bi/1-introduction

Введение: Power BI создает интерактивные визуализации, а Stream Analytics обрабатывает поток из Event Hubs и может выводить результаты в набор данных Power BI для дашбордов. В начале модуля указано, что потоковая передача в Power BI выводится из эксплуатации.

### 2. Use a Power BI output in Azure Stream Analytics
https://learn.microsoft.com/en-us/training/modules/visualize-real-time-data-azure-stream-analytics-power-bi/2-power-bi-output

Источники: Event Hubs, IoT Hub, Blob storage, Data Lake Storage Gen2, Apache Kafka. Свойства Power BI output: output alias (имя для запроса), group workspace (рабочая область Power BI), dataset name (не создавать заранее, набор создается автоматически и заменяет одноименный), table name. Авторизация: User token (требует интерактивного входа, продлевается примерно каждые две недели при включенной многофакторной аутентификации Microsoft Entra) или Managed Identity (только system-assigned; не требует ручного продления и подходит для автоматических развертываний; нужна обновленная рабочая область Power BI и лицензия Power BI Pro).

### 3. Create a query for real-time visualization
https://learn.microsoft.com/en-us/training/modules/visualize-real-time-data-azure-stream-analytics-power-bi/3-realtime-query

Запрос пересылает события из Event Hubs в выход Power BI; схема результата определяет схему таблицы набора данных. Можно фильтровать и агрегировать, например максимальное значение по датчику за минутные окна. Рекомендации: Power BI получает данные примерно раз в секунду, пакеты до 15 КБ; используйте оконные функции, чтобы отправлять данные не чаще раза в секунду, и включайте минимум полей.

### 4. Create real-time data visualizations in Power BI
https://learn.microsoft.com/en-us/training/modules/visualize-real-time-data-azure-stream-analytics-power-bi/4-create-real-time-data-visualizations-power-bi

После успешного запуска задания в рабочей области создается потоковый набор данных с одной таблицей. На дашборде добавляется плитка real-time visualization, которая обновляется по мере поступления данных.

### 5. Exercise - Create a real-time data visualization
https://learn.microsoft.com/en-us/training/modules/visualize-real-time-data-azure-stream-analytics-power-bi/5-exercise-create-real-time-data-visualization

Практика (около 45 минут): создать визуализацию в реальном времени с помощью Azure Stream Analytics и Power BI. Нужны подписка Azure с правами администратора и доступ к сервису Power BI.

### 6. Module assessment
https://learn.microsoft.com/en-us/training/modules/visualize-real-time-data-azure-stream-analytics-power-bi/6-knowledge-check

Проверочный тест (около 3 минут). Вопросы и ответы в источнике не приведены.

### 7. Summary
https://learn.microsoft.com/en-us/training/modules/visualize-real-time-data-azure-stream-analytics-power-bi/7-summary

Итоги: выход Power BI позволяет получать результаты запроса в набор данных и строить дашборды в реальном времени. Для новых решений источник рекомендует Real-Time Intelligence в Microsoft Fabric. Справочные материалы: Real-time streaming in Power BI.

## Важные команды / код / настройки

**Запрос с передачей событий в Power BI:**

```
SELECT
    EventEnqueuedUtcTime AS ReadingTime,
    SensorID,
    ReadingValue
INTO
    [powerbi-output]
FROM
    [eventhub-input] TIMESTAMP BY EventEnqueuedUtcTime
```

**Агрегация по минутным окнам:**

```
SELECT
    DateAdd(second, -60, System.TimeStamp) AS StartTime,
    System.TimeStamp AS EndTime,
    SensorID,
    MAX(ReadingValue) AS MaxReading
INTO
    [powerbi-output]
FROM
    [eventhub-input] TIMESTAMP BY EventEnqueuedUtcTime
WHERE SensorID <> 0
GROUP BY SensorID, TumblingWindow(second, 60)
HAVING COUNT(*) > 1
```

**Настройки выхода Power BI:**

- Output alias — имя выхода в запросе.
- Group workspace — рабочая область Power BI.
- Dataset name — не создавать заранее; набор создается заданием и заменяет существующий с тем же именем.
- Table name — имя таблицы в наборе.
- Authorize connection — User token или Managed Identity (system-assigned).

**Ограничения (из урока 3):** вызов Power BI примерно раз в секунду; пакет до 15 КБ. Используйте оконные функции и минимальный набор полей.

## Что запомнить

- Выход Power BI записывает результаты запроса в таблицу потокового набора данных, из которой строятся дашборды в реальном времени.
- Схема результата запроса определяет схему таблицы в Power BI.
- Managed Identity устраняет ручное продление авторизации User token, но требует обновленной рабочей области и лицензии Power BI Pro.
- Оконные функции ограничивают частоту отправки и размер пакетов.
- Потоковая передача в Power BI выводится из эксплуатации 31 октября 2027 года; для новых решений используйте Real-Time Intelligence в Microsoft Fabric.

## Связанные материалы

- Stream data as input into Stream Analytics (упоминается в уроке 2).
- Power BI output from Azure Stream Analytics (упоминается в уроках 2 и 3).
- Use Managed Identity to authenticate your Azure Stream Analytics job to Power BI (упоминается в уроке 2).
- Real-time streaming in Power BI (упоминается в уроке 7).
- Real-Time Intelligence in Microsoft Fabric — рекомендуемая замена (упоминается во введении).
