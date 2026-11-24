# Проектирование и разработка решений баз данных Azure Cosmos DB

**Источник** https://learn.microsoft.com/en-us/training/paths/design-develop-azure-cosmos-db-database-solutions

## О курсе

Проектирование и разработка приложений на Azure Cosmos DB for NoSQL: от выбора сервиса и SDK до запросов, моделирования и change feed.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB, Azure Functions, Microsoft Foundry
- **Предварительные требования:** Опыт создания облачных приложений на C# или Python; базовое знакомство с JSON и порталом Azure.

## Чему научитесь

- Оценка соответствия Azure Cosmos DB for NoSQL приложению, включая AI-нагрузки.
- Настройка request units, пропускной способности и уровней согласованности.
- Инициализация SDK для .NET и Python и подключение клиента.
- Чтение и запись данных, операции point read и создание элементов.
- Запросы с параметрами, проекциями и встроенными функциями.
- Моделирование данных и выбор ключа партиционирования по паттернам доступа.
- Чтение change feed с помощью processor и pull-моделей.
- Подключение AI-ассистента к Azure Cosmos DB через Model Context Protocol (MCP) сервер.

## Модули

1. **Знакомство с Azure Cosmos DB for NoSQL**. Научиться оценивать, подходит ли Azure Cosmos DB for NoSQL для конкретной нагрузки, понимать модель данных (аккаунт, база данных, контейнер, элемент), три механизма масштабирования (request units, партиционирование, глобальное распределение) и базовые операции в Data Explorer. [guide](../modules/explore-azure-cosmos-db-nosql.md)
2. **Настройка ресурсов Azure Cosmos DB: throughput, консистентность и TTL**. Научиться оценивать требования к throughput и консистентности и настраивать параметры аккаунта и контейнера Azure Cosmos DB для NoSQL так, чтобы сбалансировать стоимость и производительность. [guide](../modules/configure-azure-cosmos-db-resources-throughput-consistency.md)
3. **Подключение к Azure Cosmos DB for NoSQL с помощью SDK**. Научиться устанавливать и настраивать SDK Azure Cosmos DB for NoSQL для .NET и Python: создавать `CosmosClient` как синглтон, выбирать способ аутентификации и режим подключения, настраивать таймауты, повторные попытки и регионы, работать с эмулятором для офлайн-разработки и диагностировать ошибки подключения. [guide](../modules/connect-azure-cosmos-db-nosql-sdk.md)
4. **Операции с данными в Azure Cosmos DB для NoSQL через SDK**. Выполнять с помощью Azure Cosmos DB SDK point read и все операции записи (create, replace, upsert, delete), частичное обновление (patch), настраивать TTL элементов, защищать параллельные изменения через ETag, а также выбирать между транзакционным батчем и bulk-выполнением. [guide](../modules/implement-azure-cosmos-db-nosql-operations.md)
5. **Запросы к Azure Cosmos DB для NoSQL**. Писать параметризованные запросы Azure Cosmos DB для NoSQL с нужной структурой результата, обращаться к вложенным массивам через подзапросы и JOIN и постранично получать большие результаты с помощью continuation token. [guide](../modules/query-azure-cosmos-db-nosql.md)
6. **Моделирование данных и выбор ключа партиционирования в Azure Cosmos DB for NoSQL**. Научиться переносить реляционную схему в документную модель Azure Cosmos DB for NoSQL: выделять агрегаты, опираться на шаблоны доступа, решать, что встраивать (embed), а что ссылать (reference), применять денормализацию и предагрегацию, выбирать ключ партиционирования (включая иерархические и синтетические ключи) и находить антипаттерны и стоимость дизайна. [guide](../modules/design-data-modeling-partitioning-azure-cosmos-db-nosql.md)
7. **Обработка change feed и копирование данных в Azure Cosmos DB for NoSQL**. Научиться строить событийные интеграции на change feed Azure Cosmos DB (через change feed processor, pull model и триггер Azure Functions), выбирать режим change feed и перемещать данные контейнера в другой контейнер с помощью container copy jobs. [guide](../modules/process-azure-cosmos-db-nosql-change-feed.md)
8. **Инструменты разработки с AI для Azure Cosmos DB**. Научиться выбирать инструмент с AI-поддержкой для сценария Azure Cosmos DB: MCP-серверы для исследования данных и для работы агентов в продакшене, Agent Memory Toolkit для долговременной памяти агента и Agentic Retrieval для многошагового поиска. Модуль также объясняет, что инструмент берет на себя, а что остается ответственностью разработчика: модель данных, мощности, индексация, область ролей и оценка качества ответов. [guide](../modules/implement-ai-assisted-development-tools-azure-cosmos-db.md)

## Ключевые технологии и понятия

- Azure Cosmos DB for NoSQL
- Account (аккаунт)
- Database (база данных)
- Container (контейнер)
- Item (элемент)
- Request unit (RU)
- Logical partition (логическая партиция)
- Physical partition (физическая партиция)
- Partition key (ключ партиционирования)
- Global distribution (глобальное распределение)
- Autoscale
- Consistency levels (уровни согласованности)
- Hierarchical partition keys (иерархические ключи)
- Data Explorer

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/design-develop-azure-cosmos-db-database-solutions
- Модуль «Знакомство с Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/explore-azure-cosmos-db-nosql/
- Модуль «Настройка ресурсов Azure Cosmos DB: throughput, консистентность и TTL»: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/
- Модуль «Подключение к Azure Cosmos DB for NoSQL с помощью SDK»: https://learn.microsoft.com/en-us/training/modules/connect-azure-cosmos-db-nosql-sdk/
- Модуль «Операции с данными в Azure Cosmos DB для NoSQL через SDK»: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/
- Модуль «Запросы к Azure Cosmos DB для NoSQL»: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/
- Модуль «Моделирование данных и выбор ключа партиционирования в Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/
- Модуль «Обработка change feed и копирование данных в Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/
- Модуль «Инструменты разработки с AI для Azure Cosmos DB»: https://learn.microsoft.com/en-us/training/modules/implement-ai-assisted-development-tools-azure-cosmos-db/
