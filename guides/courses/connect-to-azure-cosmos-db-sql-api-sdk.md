# Подключение к Azure Cosmos DB для NoSQL с помощью SDK

**Источник** https://learn.microsoft.com/en-us/training/paths/connect-to-azure-cosmos-db-sql-api-sdk

## О курсе

Библиотеки Azure Cosmos DB и их настройка для подключения из .NET-приложения.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB
- **Предварительные требования:** Опыт создания облачных приложений на Microsoft C# или аналогичном языке программирования.

## Чему научитесь

- Знакомство с библиотеками Azure Cosmos DB и их загрузка в .NET-проект.
- Настройка SDK Azure Cosmos DB for NoSQL различными способами.

## Модули

1. **Использование SDK Azure Cosmos DB SQL API**. Научиться подключать SDK Azure Cosmos DB for NoSQL (.NET, Python, JavaScript) через пакетный менеджер, создавать клиент и работать с базами и контейнерами, использовать один экземпляр клиента, а также настраивать режим подключения, уровень согласованности и предпочтительные регионы. [guide](../modules/use-azure-cosmos-db-sql-api-sdk.md)
2. **Настройка SDK Azure Cosmos DB for NoSQL (SQL API)**. Научиться настраивать SDK Azure Cosmos DB for NoSQL для типичных задач: работа без облака через эмулятор, диагностика ошибок подключения, параллелизм и производительность клиента, а также логирование HTTP-запросов SDK. [guide](../modules/configure-azure-cosmos-db-sql-api-sdk.md)

## Ключевые технологии и понятия

- SDK для Cosmos DB for NoSQL
- CosmosClient
- Database / DatabaseProxy
- Container / ContainerProxy
- Connection mode (режим подключения)
- Consistency level на клиенте
- ApplicationRegion / ApplicationPreferredRegions (.NET), preferred_locations (Python), preferredLocations (JavaScript)
- Singleton client (одиночный клиент)
- Azure Cosmos DB emulator (эмулятор)
- Transient error (временная ошибка)
- Built-in retry (встроенные повторы)
- Коды 429, 449, 500, 503
- Resource-related time-outs (таймауты из-за ресурсов клиента)
- MaxItemCount, MaxConcurrency, MaxBufferedItemCount

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/connect-to-azure-cosmos-db-sql-api-sdk
- Модуль «Использование SDK Azure Cosmos DB SQL API»: https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/
- Модуль «Настройка SDK Azure Cosmos DB for NoSQL (SQL API)»: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api-sdk/
