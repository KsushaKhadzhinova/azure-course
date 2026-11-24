# Доступ и управление данными в Azure Cosmos DB для NoSQL с помощью SDK

**Источник** https://learn.microsoft.com/en-us/training/paths/access-manage-data-azure-cosmos-db-sql-api-sdks

## О курсе

Использование .NET SDK для Azure Cosmos DB for NoSQL для типовых операций с базами данных, контейнерами и элементами.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB
- **Предварительные требования:** Опыт создания облачных приложений на Microsoft C# или аналогичном языке программирования.

## Чему научитесь

- Создание, чтение, обновление и удаление элементов (items) в Azure Cosmos DB for NoSQL.
- Операции над несколькими элементами в одной логической единице работы (транзакции).
- Массовые операции (bulk) из кода через SDK.

## Модули

1. **Точечные операции с Azure Cosmos DB для NoSQL через SDK**. Выполнять точечные операции (CRUD) с отдельными элементами Azure Cosmos DB для NoSQL через SDK, обрабатывать коды ошибок, использовать point read и настраивать TTL (time to live) для отдельного элемента. [guide](../modules/implement-azure-cosmos-db-sql-api-point-operations.md)
2. **Транзакционные операции между документами в Azure Cosmos DB для SQL API**. Научиться выполнять несколько операций над элементами одного логического partition key как одну транзакцию (transactional batch), проверять результаты батча и защищаться от потерянных обновлений с помощью оптимистичной конкурентности (ETag и if-match). [guide](../modules/perform-cross-document-transactional-operations-azure-cosmos-db-sql-api.md)
3. **Пакетная обработка данных в Azure Cosmos DB (SQL API)**. Научиться выполнять большие объемы операций с Azure Cosmos DB for NoSQL параллельно через режим bulk в .NET SDK: включать AllowBulkExecution, формировать список задач и запускать их через `Task. [guide](../modules/process-bulk-data-azure-cosmos-db-sql-api.md)

## Ключевые технологии и понятия

- Point operations (точечные операции)
- Модель элемента
- Point read
- ETag
- Request charge (x-ms-request-charge)
- TTL (time to live)
- Delete by partition key
- Transactional batch (транзакционный батч)
- Логический partition key
- Lost update (потерянное обновление)
- ETag (`_etag`)
- Optimistic concurrency control (оптимистичная конкурентность)
- Bulk execution (пакетное выполнение)
- AllowBulkExecution

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/access-manage-data-azure-cosmos-db-sql-api-sdks
- Модуль «Точечные операции с Azure Cosmos DB для NoSQL через SDK»: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/
- Модуль «Транзакционные операции между документами в Azure Cosmos DB для SQL API»: https://learn.microsoft.com/en-us/training/modules/perform-cross-document-transactional-operations-azure-cosmos-db-sql-api/
- Модуль «Пакетная обработка данных в Azure Cosmos DB (SQL API)»: https://learn.microsoft.com/en-us/training/modules/process-bulk-data-azure-cosmos-db-sql-api/
