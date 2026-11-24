# Транзакционные операции между документами в Azure Cosmos DB для SQL API

**Источник:** https://learn.microsoft.com/en-us/training/modules/perform-cross-document-transactional-operations-azure-cosmos-db-sql-api/

## Цель модуля

Научиться выполнять несколько операций над элементами одного логического partition key как одну транзакцию (transactional batch), проверять результаты батча и защищаться от потерянных обновлений с помощью оптимистичной конкурентности (ETag и if-match).

## Ключевые понятия

- **Transactional batch (транзакционный батч)** - набор операций с одним логическим partition key, которые выполняются по порядку; фиксируются, только если все операции успешны; при ошибке откатываются все.
- **Логический partition key** - все операции батча должны относиться к одному значению partition key; иначе запрос завершается ошибкой bad request.
- **Lost update (потерянное обновление)** - ситуация, когда параллельная операция перезаписывает изменения, сделанные между чтением и записью.
- **ETag (`_etag`)** - значение, которое меняется при каждом обновлении элемента.
- **Optimistic concurrency control (оптимистичная конкурентность)** - проверка через условие if-match: обновление выполняется, только если ETag не изменился; иначе возвращается ошибка 412 Precondition Failed.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/perform-cross-document-transactional-operations-azure-cosmos-db-sql-api/1-introduction

Многодокументные транзакции пишутся на языке приложения, что даёт гибкость и возможность управлять кодом по командным практикам. Цели: создать транзакционный батч и проверить результаты; реализовать оптимистичную конкурентность.

### 2. Создание транзакционного батча через SDK
Источник: https://learn.microsoft.com/en-us/training/modules/perform-cross-document-transactional-operations-azure-cosmos-db-sql-api/2-create-transactional-batch-sdk

- В .NET: `container.CreateTransactionalBatch(partitionKey)` с цепочкой `CreateItem<T>(...)`, затем `ExecuteAsync()`.
- В Python: `container.execute_item_batch(batch, partition_key=...)`, где каждая операция - кортеж `(тип_операции, аргументы, необязательный словарь kwargs)`; типы: "create", "upsert", "replace", "read", "patch", "delete".
- В JavaScript: `container.items.batch(batch, partitionKey)`, операции задаются объектами с `operationType` (например, `BulkOperationType.Create`) и `resourceBody`.
- Поддерживаются методы: CreateItem/CreateItemStream, DeleteItem, ReadItem, ReplaceItem/ReplaceItemStream, UpsertItem/UpsertItemStream.
- Если элементы имеют разные логические partition key, батч завершается ошибкой bad request.

### 3. Просмотр результатов батча через SDK
Источник: https://learn.microsoft.com/en-us/training/modules/perform-cross-document-transactional-operations-azure-cosmos-db-sql-api/3-review-batch-operation-results-sdk

- .NET: `StatusCode` (HttpStatusCode), `IsSuccessStatusCode` (bool), `GetOperationResultAtIndex<T>(index)` для получения элемента результата по индексу.
- Python: результат - список с доступом по индексу; у каждого элемента `get("statusCode")`, `get("requestCharge")`, `get("resourceBody")`. Ошибки батча обрабатываются через `CosmosBatchOperationError`, индекс упавшей операции - `e.error_index`.
- JavaScript: `response.result` - массив; у каждого элемента `statusCode`, `requestCharge`, `resourceBody`.

### 4. Упражнение: объединение нескольких операций в батч
Источник: https://learn.microsoft.com/en-us/training/modules/perform-cross-document-transactional-operations-azure-cosmos-db-sql-api/4-exercise-batch-multiple-point-operations-together-sdk

Упражнение (около 15 минут): создать группу ресурсов, включить провайдеры ресурсов, настроить Azure Cosmos DB и локальное окружение. Подробных шагов в исходниках нет.

### 5. Реализация оптимистичной конкурентности
Источник: https://learn.microsoft.com/en-us/training/modules/perform-cross-document-transactional-operations-azure-cosmos-db-sql-api/5-implement-optimistic-concurrency-control

- Проблема: между чтением элемента и его записью проходит время, за которое другой клиент может изменить документ (lost update).
- Решение: прочитать элемент, сохранить его ETag и передать условие if-match при записи. Если ETag изменился, операция завершается с 412 Precondition Failed; нужно перечитать элемент и повторить изменение.
- .NET: ETag берётся из `response.ETag`, условие задаётся через `ItemRequestOptions { IfMatchEtag = eTag }`.
- Python: ETag берётся через `item_response.get("_etag")` или `get_response_headers().get("etag")`; условие передаётся через `headers = {"If-Match": etag}` в `upsert_item`.
- JavaScript: ETag берётся из `headers.etag`; условие задаётся через `accessCondition: { type: "IfMatch", condition: eTag }`.

### 6. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/perform-cross-document-transactional-operations-azure-cosmos-db-sql-api/6-knowledge-check

В исходных материалах вопросы не приведены.

### 7. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/perform-cross-document-transactional-operations-azure-cosmos-db-sql-api/7-summary

Создан транзакционный батч, который фиксирует несколько операций как одну логическую единицу работы, и реализована оптимистичная конкурентность.

## Важные команды / код / настройки

Транзакционный батч (C#):

```
PartitionKey partitionKey = new ("accessories-used");
TransactionalBatch batch = container.CreateTransactionalBatch(partitionKey)
    .CreateItem<Product>(saddle)
    .CreateItem<Product>(handlebar);

using TransactionalBatchResponse response = await batch.ExecuteAsync();
```

Транзакционный батч (Python):

```
partition_key = "accessories-used"

batch = [
    saddle,
    handlebar
]

batch_response = container.execute_item_batch(batch, partition_key=partition_key)
```

Оптимистичная конкурентность (C#):

```
ItemResponse<Product> response = await container.ReadItemAsync<Product>("01AC0", partitionKey);
Product product = response.Resource;
string eTag = response.ETag;

product.price = 50d;

ItemRequestOptions options = new ItemRequestOptions { IfMatchEtag = eTag };
await container.UpsertItemAsync<Product>(product, partitionKey, requestOptions: options);
```

Оптимистичная конкурентность (Python):

```
item_response = container.read_item(item=item_id, partition_key=partition_key)
product = item_response
etag = item_response.get("_etag")

product["price"] = 50.0

headers = {"If-Match": etag}
container.upsert_item(body=product, headers=headers)
```

Оптимистичная конкурентность (JavaScript):

```
const { resource: product, headers } = await container.item(itemId, categoryId).read();
const eTag = headers.etag;

product.price = 50.0;

await container.items.upsert(product, {
  accessCondition: { type: "IfMatch", condition: eTag }
});
```

Настройки: все операции батча - с одним partition key; код ошибки конфликта ETag - 412 Precondition Failed.

## Что запомнить

- Транзакционный батч работает только в пределах одного логического partition key; иначе запрос завершается ошибкой.
- Батч фиксируется целиком, если все операции успешны; при ошибке откатывается весь батч.
- Результаты батча проверяйте по статусам и request charge каждой операции.
- Чтобы не потерять обновления, передавайте ETag как условие if-match при записи.
- При ошибке 412 Precondition Failed перечитайте элемент и повторите изменение.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/perform-cross-document-transactional-operations-azure-cosmos-db-sql-api/
- Transactional batch operations in Azure Cosmos DB using the SDK; Transactions and optimistic concurrency control (ссылки из урока 7)
