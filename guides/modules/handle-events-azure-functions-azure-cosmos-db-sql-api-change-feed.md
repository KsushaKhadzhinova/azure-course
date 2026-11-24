# Обработка событий Azure Cosmos DB с помощью Azure Functions (change feed)

**Источник:** https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/

## Цель модуля

Научиться создавать Azure Function с триггером Azure Cosmos DB, который использует change feed и запускает функцию для пакета изменений, а также настраивать входные и выходные привязки (bindings) для Cosmos DB for NoSQL.

## Ключевые понятия

- **Azure Functions** - бессерверный сервис, который выполняет код по событию (trigger) и может использовать входные и выходные привязки.
- **Cosmos DB trigger (триггер)** - запускает функцию, когда в change feed появляется пакет изменений (создание или обновление элементов).
- **Change feed** - поток изменений контейнера, из которого триггер читает данные пакетами.
- **Lease container (контейнер аренд)** - служебный контейнер, в котором хранится состояние обработки change feed. Задается через `leaseContainerName`.
- **Input binding (входная привязка)** - чтение данных в функцию: point read (по `id` и partition key) или SQL-запрос, возвращающий несколько элементов.
- **Output binding (выходная привязка)** - запись одного или нескольких элементов в контейнер.
- **Managed identity** - аутентификация функции в Cosmos DB без строки подключения; настраивается через app settings с префиксом.
- **function.json** - файл конфигурации всех привязок функции; содержит массив `bindings`.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/1-introduction

Триггер Cosmos DB для Azure Functions использует change feed и запускает функцию, когда готов пакет изменений. Цель модуля - создать функцию с этим триггером и научиться обрабатывать пакеты изменений.

### 2. Understand Azure Function bindings for Azure Cosmos DB for NoSQL
https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/2-understand-azure-function-bindings

Функция запускается внешним событием (trigger), может читать дополнительные данные (input) и отправлять результат (output). Для Cosmos DB поддерживаются все три типа привязок, и они работают только с NoSQL API: trigger запускается по пакету документов из change feed, input читает элементы (point read или SQL-запрос), output записывает элементы в контейнер.

### 3. Configure function bindings
https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/3-configure-function-bindings

Сначала в приложении функции создается app setting с endpoint аккаунта и включается managed identity; ей выдается роль (например, Cosmos DB Built-in Data Contributor). Настройки с префиксом `CosmosDBConnection` (`__accountEndpoint` и `__credential`) группируются и используются в свойстве `connection`. Описаны конфигурации триггера, point read input, SQL query input и output-привязки в `function.json`.

### 4. Develop function
https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/4-develop-function

В C# параметр метода связывается с привязкой по имени. Для триггера это `IReadOnlyList<Product>` (пакет изменений), для point read - тип `Product`, для запроса - `IEnumerable<>`, для записи одного элемента - `out Product`, для нескольких - `IAsyncCollector<Product>` с `AddAsync`. Для неизвестной структуры можно использовать `dynamic`.

### 5. Exercise: Process Azure Cosmos DB for NoSQL data using Azure Functions
https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/5-exercise-archive-data-using-azure-functions

Практическое задание (около 15 минут) на архивирование данных через Azure Functions. Нужна подписка Azure с правами администратора; в инструкции: создать resource group, настроить локальное окружение, включить resource providers.

### 6. Knowledge check
https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/6-knowledge-check

Проверка знаний (около 5 минут). Текст в источнике не приведен.

### 7. Summary
https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/7-summary

В модуле функция обрабатывала изменения из change feed пакетами: C#-функция перебирает изменения в пакете и выполняет операцию. Итог: использовать триггер Cosmos DB в Azure Functions для обработки изменений.

## Важные команды / код / настройки

**function.json - триггер change feed:**
```
{
  "type": "cosmosDBTrigger",
  "name": "changes",
  "direction": "in",
  "connection": "CosmosDBConnection",
  "databaseName": "cosmicworks",
  "containerName": "products",
  "leaseContainerName": "productslease",
  "createLeaseContainerIfNotExists": false
}
```

**App settings для managed identity (префикс `CosmosDBConnection`):**
- `CosmosDBConnection__accountEndpoint` - `https://<your-cosmos-account>.documents.azure.com:443/`
- `CosmosDBConnection__credential` - `managedidentityID` (ID managed identity функции)

**function.json - point read input binding:**
```
{
  "type": "cosmosDB",
  "name": "item",
  "direction": "in",
  "connection": "CosmosDBConnection",
  "databaseName": "cosmicworks",
  "containerName": "products",
  "id": "91AA100C-D092-4190-92A7-7C02410F04EA",
  "partitionKey": "F3FBB167-11D8-41E4-84B4-5AAA92B1E737"
}
```

**function.json - SQL query input binding:**
```
{
  "type": "cosmosDB",
  "name": "items",
  "direction": "in",
  "connection": "CosmosDBConnection",
  "databaseName": "cosmicworks",
  "containerName": "products",
  "sqlQuery": "SELECT p.id, p.name, p.categoryId FROM products p WHERE p.price > 500"
}
```

**function.json - output binding:**
```
{
  "type": "cosmosDB",
  "name": "output",
  "direction": "out",
  "connection": "CosmosDBConnection",
  "databaseName": "cosmicworks",
  "containerName": "products"
}
```

**C# - триггер change feed:**
```
[Function("CosmosTrigger")]
public void Run([CosmosDBTrigger(
    databaseName: "cosmicworks",
    containerName:"product",
    Connection = "cosmosdbconnstr",
    LeaseContainerName = "leases",
    CreateLeaseContainerIfNotExists = true)] IReadOnlyList<Product> products,
    FunctionContext context)
{
    foreach (Product product in products ?? Enumerable.Empty<Product>())
    {
        _logger.LogInformation($"Product: {product.name}");
    }
}
```
Обратите внимание: в примере источника имя контейнера в атрибуте указано как `product` (в единственном числе), тогда как в остальных примерах используется `products`. Имя должно совпадать с фактическим контейнером.

**C# - point read и SQL-запрос (входные привязки):**
```
public static void Run(HttpRequest request, Product item)
```
```
public static async Task Run(HttpRequest request, IEnumerable<Product> items)
```

**C# - выходные привязки:**
```
public static void Run(HttpRequest request, out Product output)
```
```
public static async Task Run(HttpRequest request, IAsyncCollector<Product> output)
{
    await output.AddAsync(firstProduct);
    await output.AddAsync(secondProduct);
}
```

## Что запомнить

- Триггер Cosmos DB работает через change feed и вызывает функцию пакетом изменений (`IReadOnlyList<T>`).
- Обязательно задайте `leaseContainerName` - служебный контейнер, где хранится состояние обработки.
- Подключение лучше делать через managed identity и app settings с префиксом `CosmosDBConnection__...`, а не строкой подключения в коде.
- Input binding бывает point read (нужны `id` и `partitionKey`) или SQL-запрос (`sqlQuery`).
- Для записи одного элемента используется `out`-параметр, для нескольких - `IAsyncCollector<T>` с `AddAsync`.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/
- В источнике упоминаются (без ссылок в тексте): Azure Cosmos DB trigger and bindings for Azure Functions overview; Azure Cosmos DB trigger for Azure Functions.
