# Пакетная обработка данных в Azure Cosmos DB (SQL API)

**Источник:** https://learn.microsoft.com/en-us/training/modules/process-bulk-data-azure-cosmos-db-sql-api/

## Цель модуля

Научиться выполнять большие объемы операций с Azure Cosmos DB for NoSQL параллельно через режим bulk в .NET SDK: включать AllowBulkExecution, формировать список задач и запускать их через `Task.WhenAll`, учитывать расход RU/s, задержку и размер документов.

## Ключевые понятия

- **Bulk execution (пакетное выполнение)** — режим SDK, при котором операции группируются по физической партиции и отправляются параллельно.
- **AllowBulkExecution** — свойство `CosmosClientOptions`, которое включает пакетный режим.
- **Task / Task.WhenAll** — модель асинхронного программирования C#; SDK формирует пакеты из запущенных задач.
- **Stream API** — варианты операций с потоками, которые позволяют избежать лишней сериализации и десериализации.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/process-bulk-data-azure-cosmos-db-sql-api/1-introduction

Введение: отправка миллионов записей (например, ночных логов) с максимальной пропускной способностью. Модуль показывает пакетную обработку в .NET SDK через привычные классы C#.

### 2. Create bulk operations with the SDK
https://learn.microsoft.com/en-us/training/modules/process-bulk-data-azure-cosmos-db-sql-api/2-create-bulk-operations-sdk

Включение bulk через `CosmosClientOptions` с `AllowBulkExecution = true`; такой options передается в конструктор `CosmosClient` как с ключом и endpoint, так и с managed identity. Операции создаются как задачи (например, `CreateItemAsync`) и добавляются в список без немедленного запуска. Затем `Task.WhenAll` запускает их: SDK группирует операции по физической партиции, отправляет пакеты параллельно и сам собирает результаты. Пример с циклом `foreach` по коллекции из 250 000 товаров.

### 3. Review bulk operation caveats
https://learn.microsoft.com/en-us/training/modules/process-bulk-data-azure-cosmos-db-sql-api/3-review-bulk-operation-caveats

Ограничения: расход RU/s выше, чем у отдельных операций, поэтому пропускную способность нужно учитывать вместе с другими параллельными операциями. Если пакет не заполнен, SDK ждет 100 миллисекунд, что влияет на задержку. Пакет ограничен 2 МБ или 100 операциями; крупные документы снижают эффективность.

### 4. Implement bulk best practices
https://learn.microsoft.com/en-us/training/modules/process-bulk-data-azure-cosmos-db-sql-api/4-implement-bulk-best-practices

Передавайте партиционный ключ явно, если он известен, чтобы не тратить ресурсы на его определение. В API-сценариях используйте варианты Stream, чтобы избежать лишней сериализации. Если элементы уже разделены по логическим партициям, создайте рабочую задачу на каждый партиционный ключ, которая порождает дочерние задачи для операций внутри этого ключа.

### 5. Exercise: Move multiple documents in bulk with the Azure Cosmos DB for NoSQL SDK
https://learn.microsoft.com/en-us/training/modules/process-bulk-data-azure-cosmos-db-sql-api/5-exercise-move-multiple-documents-bulk-sdk

Практика (около 15 минут): перенести несколько документов пакетно с помощью .NET SDK. Нужна подписка Azure с правами администратора.

### 6. Knowledge check
https://learn.microsoft.com/en-us/training/modules/process-bulk-data-azure-cosmos-db-sql-api/6-knowledge-check

Проверочный тест (около 5 минут). Вопросы и ответы в источнике не приведены.

### 7. Summary
https://learn.microsoft.com/en-us/training/modules/process-bulk-data-azure-cosmos-db-sql-api/7-summary

Итоги: параллельное выполнение массовых операций через bulk-функции SDK и классы Task в C#. Ссылка на документацию: Bulk import data to Azure Cosmos DB for NoSQL account by using the .NET SDK.

## Важные команды / код / настройки

**Включение bulk-режима:**

```
CosmosClientOptions options = new () 
{ 
    AllowBulkExecution = true 
};

CosmosClient client = new (endpoint, credential, options);
```

**Клиент с managed identity (из урока 2):**

```
using Azure.Identity;
using Microsoft.Azure.Cosmos;

// Configure the account endpoint
string accountEndpoint = "https://<cosmos-account-name>.documents.azure.com:443/";

// Use DefaultAzureCredential to authenticate with Managed Identity
DefaultAzureCredential credential = new DefaultAzureCredential();

// Create CosmosClient with the account endpoint and Managed Identity
CosmosClient client = new CosmosClient(accountEndpoint, credential);
```

Для режима managed identity параметр options тоже можно передать в конструктор (см. предыдущий пример).

**Пакетное создание элементов:**

```
List<Product> productsToInsert = GetOurProductsFromSomeWhere();

List<Task> concurrentTasks = new List<Task>();

foreach(Product product in productsToInsert)
{
    concurrentTasks.Add(
        container.CreateItemAsync<Product>(
            product, 
            new PartitionKey(product.partitionKeyValue))
    );
}

Task.WhenAll(concurrentTasks);
```

**Ограничения пакета (из урока 3):** максимум 2 МБ или 100 операций в одном пакете; ожидание заполнения пакета 100 миллисекунд.

## Что запомнить

- Для массовой загрузки включайте `AllowBulkExecution = true` в `CosmosClientOptions`.
- Операции добавляйте в список задач без запуска; запуск через `Task.WhenAll` позволяет SDK группировать их по физическим партициям.
- Пакетный режим повышает пропускную способность, но увеличивает расход RU/s и может добавить до 100 мс задержки на неполных пакетах.
- Передавайте партиционный ключ явно и используйте Stream API в сценариях без лишней сериализации.
- Крупные документы снижают эффективность пакетов (лимит 2 МБ или 100 операций).

## Связанные материалы

- Bulk import data to Azure Cosmos DB for NoSQL account by using the .NET SDK (упоминается в уроке 7).
