# Выполнение запросов и создание приложения генеративного ИИ с Azure Cosmos DB

**Источник** https://learn.microsoft.com/en-us/training/paths/execute-queries-azure-cosmos-db-sql-api

## О курсе

SQL-запросы для Azure Cosmos DB for NoSQL через Data Explorer и SDK и создание генеративного AI-приложения.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB, Azure OpenAI in Foundry Models
- **Предварительные требования:** Опыт создания облачных приложений на C#, Python, JavaScript или аналогичном языке программирования.

## Чему научитесь

- Написание SQL-запросов к Azure Cosmos DB for NoSQL.
- Запросы с подзапросами и перекрестными произведениями (cross-products).
- Создание генеративного AI-приложения на Python с Azure Cosmos DB for NoSQL.

## Модули

1. **Запросы к Azure Cosmos DB для NoSQL с помощью SQL**. Научиться создавать и выполнять SQL-запросы к JSON-документам в Azure Cosmos DB для NoSQL, формировать (проецировать) результаты в нужную структуру, проверять типы свойств и использовать встроенные функции, а также выполнять запросы через SDK. [guide](../modules/query-azure-cosmos-db-sql-api.md)
2. **Составление сложных запросов в Azure Cosmos DB SQL API**. Научиться писать сложные запросы к JSON-документам с вложенными массивами: кросс-произведения (cross-product) через JOIN, коррелированные подзапросы, параметризованные запросы и постраничный вывод результатов в SDK. [guide](../modules/author-complex-queries-azure-cosmos-db-sql-api.md)
3. **Создание генеративных AI-приложений с Azure Cosmos DB for NoSQL и Python**. Научиться строить генеративное AI-приложение на Python, которое работает с приватными данными: сохранять и извлекать векторы в Azure Cosmos DB for NoSQL, выполнять similarity search, реализовать retrieval augmented generation (RAG) и оркестрировать модели через LangChain. [guide](../modules/build-generative-ai-applications-with-azure-cosmos-db-nosql.md)

## Ключевые технологии и понятия

- SQL-запрос Cosmos DB для NoSQL
- Проекция
- DISTINCT
- VALUE
- Проверки типов
- Встроенные функции
- QueryIterator / query_items
- JOIN (внутри элемента)
- Cross-product (кросс-произведение)
- Correlated subquery (коррелированный подзапрос)
- Parameterized query (параметризованный запрос)
- Feed iterator (итератор страниц)
- QueryDefinition / QueryRequestOptions (.NET)
- Azure Cosmos DB for NoSQL

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/execute-queries-azure-cosmos-db-sql-api
- Модуль «Запросы к Azure Cosmos DB для NoSQL с помощью SQL»: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/
- Модуль «Составление сложных запросов в Azure Cosmos DB SQL API»: https://learn.microsoft.com/en-us/training/modules/author-complex-queries-azure-cosmos-db-sql-api/
- Модуль «Создание генеративных AI-приложений с Azure Cosmos DB for NoSQL и Python»: https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/
