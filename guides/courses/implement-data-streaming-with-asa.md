# Внедрение решения потоковой обработки данных с Azure Stream Analytics

**Источник** https://learn.microsoft.com/en-us/training/paths/implement-data-streaming-with-asa

## О курсе

Потоковая обработка данных в реальном времени с Azure Stream Analytics и визуализация результатов в Power BI.

- **Уровень:** начальный (Beginner)
- **Роль:** Data Analyst, Data Engineer
- **Продукты и сервисы:** Azure Stream Analytics, Power BI
- **Предварительные требования:** Базовое понимание облачных вычислений и аналитики данных.

## Чему научитесь

- Обработка потоков данных и интеграция результатов в приложения и аналитику.
- Прием потоковых данных с помощью Azure Stream Analytics.
- Создание дашбордов реального времени с помощью Azure Stream Analytics и Power BI.

## Модули

1. **Введение в потоковую обработку данных**. Понять, что такое потоковые данные, и научиться начинать работу с Azure Stream Analytics: обрабатывать поток событий (фильтровать, агрегировать) и передавать результаты в выходные приемники или визуализации. [guide](../modules/introduction-to-data-streaming.md)
2. **Прием потоковых данных с Azure Stream Analytics в Synapse**. Научиться настраивать задание Azure Stream Analytics: определять входы (inputs) и выходы (outputs), писать запрос для выборки, фильтрации и агрегации потоковых событий по временным окнам, запускать задание и направлять результаты в хранилища (Azure Data Lake Storage Gen2, Azure SQL Database, Azure Synapse Analytics и другие). [guide](../modules/ingest-streaming-data-use-azure-stream-analytics-synapse.md)
3. **Визуализация данных в реальном времени: Azure Stream Analytics и Power BI**. Научиться направлять результаты запроса Azure Stream Analytics в выход Power BI и строить по ним дашборды с визуализацией в реальном времени. Важное замечание из источника: потоковая передача в Power BI выводится из эксплуатации. [guide](../modules/visualize-real-time-data-azure-stream-analytics-power-bi.md)

## Ключевые технологии и понятия

- Data stream (поток данных)
- Temporal data (временные данные)
- Temporal windows (временные окна)
- Stream Analytics job (задание)
- Stream Analytics cluster (кластер)
- Input (вход)
- Output (выход)
- Query (запрос)
- TIMESTAMP BY
- Exactly once processing / at-least-once delivery
- No-code editor
- Azure Stream Analytics
- Reference data
- Окна (windows)

## Для каких ролей полезно

- Data Analyst (DA, аналитик данных)
- Data Engineer (DE, инженер данных)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/implement-data-streaming-with-asa
- Модуль «Введение в потоковую обработку данных»: https://learn.microsoft.com/en-us/training/modules/introduction-to-data-streaming/
- Модуль «Прием потоковых данных с Azure Stream Analytics в Synapse»: https://learn.microsoft.com/en-us/training/modules/ingest-streaming-data-use-azure-stream-analytics-synapse/
- Модуль «Визуализация данных в реальном времени: Azure Stream Analytics и Power BI»: https://learn.microsoft.com/en-us/training/modules/visualize-real-time-data-azure-stream-analytics-power-bi/
