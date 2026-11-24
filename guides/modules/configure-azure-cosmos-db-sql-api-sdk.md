# Настройка SDK Azure Cosmos DB for NoSQL (SQL API)

**Источник:** https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api-sdk/

## Цель модуля

Научиться настраивать SDK Azure Cosmos DB for NoSQL для типичных задач: работа без облака через эмулятор, диагностика ошибок подключения, параллелизм и производительность клиента, а также логирование HTTP-запросов SDK.

## Ключевые понятия

- **Azure Cosmos DB emulator (эмулятор)** - локальная среда для разработки и тестирования без подписки Azure; доступна для Windows, Linux и как Docker-образ.
- **Transient error (временная ошибка)** - ошибка, причина которой скоро устраняется сама; приложение должно быть готово ее повторить.
- **Built-in retry (встроенные повторы)** - SDK сам повторяет часть чтений и запросов при временных сбоях, но не повторяет записи.
- **Коды 429, 449, 500, 503** - коды, при которых повтор запроса имеет смысл; **400, 401, 403, 404** указывают на ошибку на стороне клиента и повторять их не нужно.
- **Resource-related time-outs (таймауты из-за ресурсов клиента)** - таймауты, вызванные высокой загрузкой CPU или портов на клиентской машине, а не сервисом.
- **MaxItemCount, MaxConcurrency, MaxBufferedItemCount** - параметры запроса, управляющие размером страницы, параллелизмом и буферизацией результатов.
- **Client builder (CosmosClientBuilder)** - класс .NET для fluent-настройки клиента, в том числе подключения собственных обработчиков запросов.
- **RequestHandler** - базовый класс .NET, от которого наследуется обработчик для логирования HTTP-запросов и ответов.
- **Diagnostics levels (уровни диагностики, JavaScript)** - `info`, `debug`, `debug-unsafe`; последний включает чувствительные данные запросов и ответов.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api-sdk/1-introduction

Модуль учит настраивать SDK для распространенных сценариев: работа с эмулятором, устранение ошибок подключения, параллелизм и логирование.

### 2. Включение офлайн-разработки
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api-sdk/2-enable-offline-development

Эмулятор использует тот же API, что и облачный сервис, поэтому подключение к нему отличается от подключения к облаку только адресом и ключом. Эндпоинт по умолчанию - `https://localhost:8081/` (в JavaScript для IPv4 рекомендуется `https://127.0.0.1:8081/`). Ключ эмулятора - статический известный ключ по умолчанию; при запуске эмулятора с опцией `/Key` можно сгенерировать новый. Эмулятор в Docker-образе публикуется в Microsoft Container Registry (`mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator`). При ошибке SSL в контейнере может понадобиться импорт SSL-сертификата контейнера или отключение проверки TLS (`NODE_TLS_REJECT_UNAUTHORIZED = 0`), что допустимо только для локальной разработки.

### 3. Обработка ошибок подключения
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api-sdk/3-handle-connection-errors

SDK для .NET, Python и JavaScript имеет встроенную логику повторов для временных сбоев чтения и запросов; для записей SDK не повторяет запросы автоматически, и повтор записи должен реализовать код приложения (считается лучшей практикой). Рекомендуется использовать последнюю версию SDK. Повторять стоит на 429, 449, 500 и 503; при 50x-ошибках доступности можно открыть обращение в поддержку Azure. Ошибки 400, 401, 403 и 404 исправляются в коде приложения, а не повтором.

### 4. Потоки и параллелизм
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api-sdk/4-implement-threading-parallelism

- Таймауты часто вызваны перегрузкой клиентской машины (CPU или порты); следите за ресурсами и масштабируйтесь заранее.
- В .NET используйте async/await и не блокируйте выполнение через `Task.Wait` или `Task.Result`.
- Не используйте LINQ `ToList()` для больших выборок, так как он синхронно вычитывает весь запрос; используйте `ToFeedIterator<T>()`.
- Настройки запроса в .NET: `MaxItemCount` (по умолчанию 100; `-1` - динамический размер), `MaxConcurrency` (`1` отключает параллелизм, `-1` - выбор SDK, идеально - число физических партиций), `MaxBufferedItemCount` (`-1` - выбор SDK).
- В Python используйте асинхронные запросы через `azure.cosmos.aio` (нужна библиотека `aiohttp`), не смешивайте sync и async вызовы, применяйте итераторы вместо `list(...)`. Параметр `max_item_count` задает размер страницы (по умолчанию 100).
- В JavaScript используйте async/await и итераторы (`iterator.hasMoreResults()`, `fetchNext()`) вместо `fetchAll()` для больших выборок; параметр `maxItemCount` задает размер страницы.
- Во всех SDK включайте partition key в фильтр запроса, чтобы ограничить его одной партицией.
- Пакетные операции (TransactionalBatch в Python, `container.items.bulk` в JavaScript) выполняются только в пределах одного partition key: до 100 операций, размер - до 4 MB (Python) или 2 MB (JavaScript).

### 5. Настройка логирования
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api-sdk/5-configure-logging

- .NET: `CosmosClientBuilder` (пространство имен `Microsoft.Azure.Cosmos.Fluent`) позволяет задать регион (`WithApplicationRegion`/`WithApplicationPreferredRegions`), режим подключения (`WithConnectionModeDirect`/`WithConnectionModeGateway`) и уровень согласованности (`WithConsistencyLevel`). В продакшене рекомендуется managed identity через `DefaultAzureCredential` или `ManagedIdentityCredential`.
- .NET: чтобы логировать HTTP-запросы, создайте класс, наследующий `RequestHandler`, переопределите `SendAsync`, выведите метод и URI запроса, вызовите базовый `SendAsync` и выведите код статуса; подключите обработчик через `builder.AddCustomHandlers(...)`. Пример логов для первого запуска создания базы: `GET dbs/cosmicworks` -> 404, затем `POST dbs/` -> 201; при повторном запуске - только GET с 200.
- Python: модуль `logging`; по умолчанию базовая информация о HTTP-сессии пишется на уровне INFO, подробности (тела и незамаскированные заголовки) - на уровне DEBUG. Глобальное логирование включается через `logging_enable=True` в конструкторе клиента, для одной операции - параметром `logging_enable=True` метода. Расширенная диагностика включается через `enable_diagnostics_logging=True` и `logger=logger` (политика `CosmosHttpLoggingPolicy`).
- JavaScript: логирование через пакет `@azure/logger`; уровень задается переменной окружения `AZURE_LOG_LEVEL` (например, `info`) или `setLogLevel("info")`. Уровень диагностики задается параметром `diagnosticLevel` (`CosmosDbDiagnosticLevel.debug` и др.) или переменной `AZURE_COSMOSDB_DIAGNOSTICS_LEVEL`. Объект `diagnostics` возвращается в ответах и содержит длительность, повторы и размеры полезной нагрузки.
- Уровень `debug-unsafe` включает чувствительные запросы и ответы; не используйте его в продакшене.

### 6. Упражнение: офлайн-разработка
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api-sdk/6-exercise-for-offline-development

Упражнение (15 минут) по настройке SDK для офлайн-разработки с локальной средой. Требуется подписка Azure с административным доступом и настроенное локальное окружение.

### 7. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api-sdk/7-knowledge-check

Итоговый тест модуля (5 минут). Содержимое вопросов в исходных материалах не приведено.

### 8. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api-sdk/8-summary

Модуль показал, как настроить клиент для производительности, обработки ошибок подключения, офлайн-разработки с эмулятором и подробного логирования HTTP-запросов.

## Важные команды / код / настройки

- Эндпоинт эмулятора: `https://localhost:8081/` (Node.js при ошибке `ECONNREFUSED ::1:8081` - `https://127.0.0.1:8081/`).
- Ключ эмулятора по умолчанию - статический ключ из источника (C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==); в учебных материалах он приведен для локальной разработки.
- Запуск эмулятора с новым ключом: опция `/Key`.
- Docker: `docker pull mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator`.
- .NET: `QueryRequestOptions { MaxItemCount = 500 }`, `{ MaxConcurrency = 5 }`, `{ MaxBufferedItemCount = 5000 }`.
- Python: `container.query_items(query=..., max_item_count=500)`; `partition_key="bikes"` для запроса в одну партицию.
- JavaScript: `container.items.query("SELECT * FROM c", { maxItemCount: 500, enableCrossPartitionQuery: true })`; `{ partitionKey: "socks" }` в параметрах запроса.
- .NET: `builder.AddCustomHandlers(new LogHandler());` и `CosmosClient client = builder.Build();`.
- Python: `CosmosClient(endpoint, key, logging_enable=True)`; `CosmosClient(endpoint, key, logger=logger, enable_diagnostics_logging=True)`.
- JavaScript: `setLogLevel("info")`; `new CosmosClient({ endpoint, key, diagnosticLevel: CosmosDbDiagnosticLevel.debug })`; `export AZURE_LOG_LEVEL=info`; `export AZURE_COSMOSDB_DIAGNOSTICS_LEVEL=debug`.
- Запрещенный паттерн в .NET: `client.CreateDatabaseIfNotExistsAsync("cosmicworks").Result` (блокирует выполнение).
- Запрещенный паттерн в Python: `client.query_items(...).result()` внутри асинхронного кода.
- Отключение TLS-проверки для Node.js (только локально, при SSL-ошибке с эмулятором): `process.env.NODE_TLS_REJECT_UNAUTHORIZED = 0`.

## Что запомнить

- Эмулятор позволяет разрабатывать и тестировать без облачной подписки; подключение к нему идентично облачному, меняются только эндпоинт и ключ.
- SDK повторяет временные ошибки чтения и запросов, но не записи - повтор записи реализуйте сами.
- Повторяйте 429, 449, 500, 503; ошибки 400, 401, 403, 404 исправляйте в коде.
- Не блокируйте асинхронный код и не собирайте большие результаты целиком: используйте итераторы.
- Логирование: в продакшене - уровень info; `debug-unsafe` не используйте в продакшене.

## Связанные материалы

- Install and use the Azure Cosmos DB Emulator for local development and testing
- Best practices for Azure Cosmos DB .NET SDK
- Performance tips for Azure Cosmos DB and .NET
- Diagnose and troubleshoot issues when using Azure Cosmos DB .NET SDK
- Best practices for Azure Cosmos DB Python SDK
- Performance tips for Azure Cosmos DB and Python
- Best practices for Azure Cosmos DB Node.js SDK
