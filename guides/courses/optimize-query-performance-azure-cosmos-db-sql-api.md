# Оптимизация производительности запросов и операций в Azure Cosmos DB для NoSQL

**Источник** https://learn.microsoft.com/en-us/training/paths/optimize-query-performance-azure-cosmos-db-sql-api

## О курсе

Оптимизация запросов и операций Azure Cosmos DB for NoSQL: индексы, измерение производительности и integrated cache.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB
- **Предварительные требования:** Опыт создания облачных приложений на Microsoft C# или аналогичном языке программирования.

## Чему научитесь

- Настройка индексной политики под SQL-запросы.
- Измерение производительности индексной политики.
- Внедрение, настройка и мониторинг integrated cache.

## Модули

1. **Выбор индексов в Azure Cosmos DB for NoSQL (SQL API)**. Научиться настраивать индексную политику контейнера Azure Cosmos DB for NoSQL под рабочую нагрузку: read-heavy (много чтений по разным полям) и write-heavy (много записей больших документов), с учетом способов выполнения фильтров (index seek, index scan, full scan). [guide](../modules/choose-indexes-azure-cosmos-db-sql-api.md)
2. **Измерение и настройка индексов в Azure Cosmos DB для SQL API**. Научиться измерять стоимость запросов и операций в RU/s с помощью классов опций .NET SDK, включать метрики индексирования и на их основе подбирать политику индексирования (в том числе составные индексы) под конкретные запросы. [guide](../modules/measure-index-azure-cosmos-db-sql-api.md)
3. **Интегрированный кэш в Azure Cosmos DB**. Включить и настроить встроенный (integrated) кэш Azure Cosmos DB для NoSQL, чтобы снизить стоимость повторяющихся операций чтения и запросов без написания собственного клиентского кэша. [guide](../modules/implement-integrated-cache.md)

## Ключевые технологии и понятия

- Schema-agnostic (без схемы)
- Indexing policy (индексная политика)
- Inverted index (инвертированный индекс)
- Index seek
- Index scan
- Full scan (полное сканирование)
- RU/s
- Index rebuild (перестроение индекса)
- Index metrics (метрики индексирования)
- QueryRequestOptions
- Index Impact Score
- Utilized / Potential Single Indexes
- Composite index (составной индекс)
- RequestCharge (RU/s)

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/optimize-query-performance-azure-cosmos-db-sql-api
- Модуль «Выбор индексов в Azure Cosmos DB for NoSQL (SQL API)»: https://learn.microsoft.com/en-us/training/modules/choose-indexes-azure-cosmos-db-sql-api/
- Модуль «Измерение и настройка индексов в Azure Cosmos DB для SQL API»: https://learn.microsoft.com/en-us/training/modules/measure-index-azure-cosmos-db-sql-api/
- Модуль «Интегрированный кэш в Azure Cosmos DB»: https://learn.microsoft.com/en-us/training/modules/implement-integrated-cache/
