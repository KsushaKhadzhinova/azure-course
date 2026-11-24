# Интеграция Azure Cosmos DB для NoSQL с сервисами Azure

**Источник** https://learn.microsoft.com/en-us/training/paths/integrate-azure-cosmos-db-sql-api-azure-services

## О курсе

Интеграция Azure Cosmos DB for NoSQL с Azure Cognitive Search, Azure Functions и собственными решениями.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB, Azure AI Search, Azure Functions
- **Предварительные требования:** Опыт создания облачных приложений на Microsoft C# или аналогичном языке программирования.

## Чему научитесь

- Обработка событий change feed с помощью change feed processor.
- Использование привязок (bindings) Azure Functions для интеграции с Azure Cosmos DB.
- Индексация данных Azure Cosmos DB с помощью Azure Cognitive Search.

## Модули

1. **Использование change feed в Azure Cosmos DB (SQL API) с помощью SDK**. Реализовать change feed processor в .NET SDK для Azure Cosmos DB для NoSQL: написать делегат для обработки пакетов изменений и настроить оценку (estimator) количества непрочитанных изменений. [guide](../modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk.md)
2. **Обработка событий Azure Cosmos DB с помощью Azure Functions (change feed)**. Научиться создавать Azure Function с триггером Azure Cosmos DB, который использует change feed и запускает функцию для пакета изменений, а также настраивать входные и выходные привязки (bindings) для Cosmos DB for NoSQL. [guide](../modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed.md)
3. **Индексация данных Azure Cosmos DB (SQL API) в Azure Cognitive Search**. Научиться создавать индексатор (indexer), который переносит данные из Azure Cosmos DB for NoSQL в индекс Azure Cognitive Search, настраивать политику обнаружения изменений (change detection) и политику обнаружения удалений (deletion detection). [guide](../modules/search-azure-cosmos-db-sql-api-data-azure-cognitive-search.md)

## Ключевые технологии и понятия

- Change feed processor
- Monitored container (отслеживаемый контейнер)
- Lease container (контейнер аренды)
- Host (хост)
- Delegate (делегат)
- Change feed estimator
- Azure Functions
- Cosmos DB trigger (триггер)
- Change feed
- Lease container (контейнер аренд)
- Input binding (входная привязка)
- Output binding (выходная привязка)
- Managed identity
- function.json

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/integrate-azure-cosmos-db-sql-api-azure-services
- Модуль «Использование change feed в Azure Cosmos DB (SQL API) с помощью SDK»: https://learn.microsoft.com/en-us/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/
- Модуль «Обработка событий Azure Cosmos DB с помощью Azure Functions (change feed)»: https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/
- Модуль «Индексация данных Azure Cosmos DB (SQL API) в Azure Cognitive Search»: https://learn.microsoft.com/en-us/training/modules/search-azure-cosmos-db-sql-api-data-azure-cognitive-search/
