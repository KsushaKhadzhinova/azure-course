# Серверное программирование в Azure Cosmos DB для NoSQL

**Источник** https://learn.microsoft.com/en-us/training/paths/create-server-side-programming-azure-cosmos-db-sql-api

## О курсе

Создание серверных конструкций на JavaScript: хранимые процедуры, пользовательские функции и триггеры.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB
- **Предварительные требования:** Опыт создания облачных приложений на Microsoft C# или аналогичном языке программирования.

## Чему научитесь

- Хранимые процедуры на JavaScript в Azure Cosmos DB for NoSQL.
- Пользовательские функции (UDF) и триггеры на JavaScript.

## Модули

1. **Транзакции с несколькими элементами в Azure Cosmos DB (SQL API)**. Научиться писать хранимые процедуры на JavaScript, которые выполняют несколько операций как одну логическую единицу работы прямо внутри движка базы данных, и откатывать такие транзакции при ошибке. [guide](../modules/build-multi-item-transactions-azure-cosmos-db-sql-api.md)
2. **Расширение функциональности запросов и транзакций в Azure Cosmos DB для SQL API**. Научиться писать на JavaScript пользовательские функции (UDF), которые расширяют язык запросов, и триггеры (pre- и post-triggers), которые встраивают логику до и после операций с элементами; создавать их через SDK и подключать к операциям. [guide](../modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api.md)

## Ключевые технологии и понятия

- Транзакция (transaction)
- Хранимая процедура (stored procedure)
- Область видимости партиции (logical partition scope)
- Контекст (getContext)
- Ограничение по времени
- Откат (rollback)
- UDF (user-defined function)
- Ограничение UDF
- Триггер (trigger)
- Pre-trigger
- Post-trigger
- getContext()

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/create-server-side-programming-azure-cosmos-db-sql-api
- Модуль «Транзакции с несколькими элементами в Azure Cosmos DB (SQL API)»: https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/
- Модуль «Расширение функциональности запросов и транзакций в Azure Cosmos DB для SQL API»: https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/
