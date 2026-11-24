# Операции с данными в Azure Cosmos DB для NoSQL через SDK

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/

## Цель модуля

Выполнять с помощью Azure Cosmos DB SDK point read и все операции записи (create, replace, upsert, delete), частичное обновление (patch), настраивать TTL элементов, защищать параллельные изменения через ETag, а также выбирать между транзакционным батчем и bulk-выполнением.

## Ключевые понятия

- **Point read** - чтение одного элемента по `id` и значению ключа партиции; самая дешевая операция чтения (около 1 RU для элемента 1 КБ при session-консистентности).
- **Create / Replace / Upsert / Delete** - четыре операции записи; различаются поведением при уже существующем или отсутствующем элементе (409, 404 или вставка).
- **Partial document update (patch)** - отправка списка операций JSON Patch, которые сервер применяет к элементу; до 10 операций за запрос; все операции атомарны.
- **Time to live (TTL)** - обратный отсчет в секундах от последнего изменения; `DefaultTimeToLive` контейнера включает механизм, `ttl` элемента переопределяет его, `-1` исключает элемент.
- **Оптимистичная конкурентность (optimistic concurrency)** - использование `_etag` как условия записи; при несовпадении возвращается 412 Precondition Failed.
- **Транзакционный батч (transactional batch)** - до 100 операций, атомарно выполняемых в одной логической партиции; при ошибке остальные операции получают 424.
- **Bulk execution** - высокопроизводительная запись множества независимых операций без атомарности по всей партиции.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/1-introduction

Модуль проходит набор операций, которые нужны слою данных: point read, четыре операции записи, patch, TTL, ETag и два варианта работы с несколькими элементами (транзакционный батч и bulk). Пример в тексте - сервис обработки заказов компании Contoso.

### 2. Выполнение point read
URL: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/2-perform-point-reads

Point read использует id и ключ партиции, SDK направляет запрос напрямую в нужную физическую партицию, без участия движка запросов. Для элемента 1 КБ point read стоит около 1 RU, запрос, возвращающий один элемент, около 3 RU. При strong или bounded staleness стоимость чтения удваивается. Отсутствующий элемент SDK сигнализирует ошибкой (NotFound), а не null: ее нужно ловить явно. `ReadManyItemsAsync` (.NET) и `read_items` (Python) читают несколько элементов по разным ключам; в Python ненайденные элементы просто не попадают в результат. Если ключ партиции неизвестен, нужен запрос.

### 3. Создание, замена, upsert и удаление элементов
URL: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/3-create-replace-insert-update-delete

Таблица поведения: Create при существующем элементе - 409 Conflict; Replace при отсутствующем - 404; Upsert вставляет или заменяет; Delete при отсутствующем - 404. Ориентиры стоимости для элемента 1 КБ: create или delete около 5 RU, replace примерно вдвое дороже create, upsert около 5 RU при вставке и около 10 при замене. `id` уникален только внутри логической партиции. Upsert может перезаписать элемент, созданный другим процессом; для дубликатов как ошибки используйте create. Ответ можно не возвращать (`EnableContentResponseOnWrite = false` в .NET, `no_response=True` в Python), что экономит трафик, но не RU.

### 4. Обновление элементов частичным патчем
URL: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/4-update-with-patch

Patch отправляет операции, а не весь документ, и сервер применяет их без предварительного чтения. Операции: Add, Set, Replace, Remove, Increment, Move (copy и test не поддерживаются). Все операции одного запроса применяются атомарно. Increment выполняет арифметику на сервере, поэтому два одновременных уменьшения складываются корректно. Условный patch через filter predicate возвращает 412, если условие ложно. Ограничения: до 10 операций на запрос; системные свойства (`id`, `_etag`, `_ts`, `_rid`) и свойство ключа партиции патчить нельзя; Replace и Remove требуют существующего пути; Add создает только один уровень. Стоимость RU у patch примерно равна стоимости replace того же документа; выигрыш - в трафике и отсутствии лишнего чтения, особенно для больших документов.

### 5. Настройка времени жизни элементов (TTL)
URL: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/5-configure-item-time-to-live

Контейнерный `DefaultTimeToLive` - ворота: если он не задан, `ttl` элементов игнорируется. При `-1` механизм включен, но без истечения по умолчанию, и истекают только элементы с собственным `ttl`. Истекшие элементы сразу перестают возвращаться в запросах, физическое удаление идет в фоне (на provisioned аккаунте - за счет свободных RU, на serverless удаления тарифицируются). Включение TTL на контейнере не сбрасывает `_ts`, поэтому уже «просроченные» элементы могут истечь сразу. Установить `ttl` элемента можно patch-операцией `Set /ttl` или значением при записи. Счетчик перезапускается при каждой записи элемента (скользящее истечение). Удаление свойства `ttl` возвращает элемент к значению по умолчанию, а `-1` делает элемент бессрочным. Для TTL-удалений в change feed по умолчанию они не видны; нужен режим all versions and deletes. Удаление всех элементов одной партиции - отдельная операция `DeleteAllItemsByPartitionKey` (в превью), требующая включения возможности через Azure CLI.

### 6. Реализация оптимистичной конкурентности
URL: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/6-implement-optimistic-concurrency

Без условия последняя запись побеждает и может затереть чужое изменение (lost update). Каждый элемент имеет `_etag`, который меняется при каждой записи. Чтение сохраняет ETag, запись передает его как условие (`IfMatchEtag` в .NET; `etag` и `match_condition=MatchConditions.IfNotModified` в Python). Если элемент изменился, возвращается 412 Precondition Failed. Варианты реакции: повторить чтение и запись (ограниченное число попыток, обычно 3-4), показать конфликт пользователю, или пересмотреть операцию (например, использовать patch increment). Для create ETag не действует; upsert проверяет ETag только при существующем элементе. Для patch в .NET используется `FilterPredicate`, а не `IfMatchEtag`.

### 7. Выполнение транзакционного батча
URL: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/7-execute-transactional-batch

Батч объединяет несколько point-операций в один запрос, выполняет их по порядку и фиксирует, только если все успешны; иначе откатывает весь батч. Все операции должны относиться к одному значению ключа партиции, поэтому связанные элементы нужно проектировать с общим ключом (например, `customerId`). Ограничения: до 100 операций, до 2 МБ полезной нагрузки, до 5 секунд выполнения, одно значение ключа партиции. В результатах: неудачная операция возвращает свой код (409, 412 и т. д.), остальные - 424 Failed Dependency. Превышение лимитов и смешение ключей партиции приводят к ошибке (400 при смешении). В батче можно задать ETag для одной операции, и тогда весь батч становится условным. Батч не дешевле отдельных операций: стоимость равна сумме операций; его ценность - атомарность.

### 8. Обработка bulk-операций
URL: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/8-process-bulk-operations

Bulk предназначен для больших независимых фоновых загрузок. Атомарности нет: каждая операция успешна или нет сама по себе, неудачные можно повторить. SDK группирует операции по физическим партициям и отправляет их одним запросом. Это увеличивает задержку отдельной операции, поэтому bulk не подходит для интерактивных сценариев. В .NET включается установкой `AllowBulkExecution = true` при создании клиента (настройка на весь клиент; лучше отдельный клиент для bulk), операции запускаются без await и собираются через `Task.WhenAll`; ошибки лучше проверять через continuation. В Python нет флага bulk; рекомендуемый обходной путь - асинхронный клиент `azure.cosmos.aio` с `asyncio.gather` и семафором. При нехватке RU возвращается 429; SDK .NET по умолчанию повторяет до 9 раз (всего до 10 попыток) с общим ожиданием до 30 секунд. Рекомендуется временно повысить RU/s, исключить неиспользуемые пути индекса и распределять записи по разным значениям ключа партиции.

### 9. Упражнение: реализация операций с данными
URL: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/9-exercise-implement-data-operations

Практика: point read, запросы, операции записи, условные обновления, транзакции и bulk с измерением RU (C# или Python). Нужна подписка Azure.

### 10. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/10-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 11. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/11-summary

Point read - лучший выбор, когда известны id и ключ партиции. Create отклоняет дубликаты (409), replace требует существования, upsert делает то и другое. Patch - до 10 операций. TTL истекает автоматически. ETag предотвращает потерю обновлений (412). Транзакционный батч - до 100 операций в одной партиции атомарно; bulk жертвует атомарностью ради пропускной способности.

## Важные команды / код / настройки

Point read (.NET):

```csharp
string id = "order-88431";
PartitionKey partitionKey = new PartitionKey("cust-2043");
Order order = await container.ReadItemAsync<Order>(id, partitionKey);
```

Point read (Python):

```python
order = container.read_item(item="order-88431", partition_key="cust-2043")
```

Create с обработкой конфликта (.NET):

```csharp
try
{
    await container.CreateItemAsync<Order>(order, new PartitionKey(order.customerId));
}
catch (CosmosException ex) when (ex.StatusCode == HttpStatusCode.Conflict)
{
    // An order with this id already exists in this partition.
}
```

Patch (.NET):

```csharp
List<PatchOperation> operations = new()
{
    PatchOperation.Set("/status", "shipped"),
    PatchOperation.Set("/shippedAt", DateTime.UtcNow),
    PatchOperation.Add("/trackingNumbers/-", "1Z999AA10123456784")
};
ItemResponse<Order> response = await container.PatchItemAsync<Order>(
    id: "order-88431",
    partitionKey: new PartitionKey("cust-2043"),
    patchOperations: operations);
```

Условный patch через filter predicate (.NET):

```csharp
PatchItemRequestOptions options = new()
{
    FilterPredicate = "FROM orders o WHERE o.status = 'pending'"
};
```

Patch Increment (.NET):

```csharp
await container.PatchItemAsync<Product>(
    id: "prod-4410",
    partitionKey: new PartitionKey("bikes"),
    patchOperations: new[] { PatchOperation.Increment("/inventory/quantity", -1) });
```

Patch (Python):

```python
updated = container.patch_item(
    item="order-88431",
    partition_key="cust-2043",
    patch_operations=[
        {"op": "set", "path": "/status", "value": "shipped"},
        {"op": "add", "path": "/trackingNumbers/-", "value": "1Z999AA10123456784"},
    ],
)
```

Настройка контейнера TTL (.NET):

```csharp
ContainerProperties properties = await container.ReadContainerAsync();
properties.DefaultTimeToLive = -1;
await container.ReplaceContainerAsync(properties);
```

Установка `ttl` элемента патчем:

```csharp
await container.PatchItemAsync<CheckoutSession>(
    id: "session-9f21",
    partitionKey: new PartitionKey("cust-2043"),
    patchOperations: new[] { PatchOperation.Set("/ttl", 3600) });
```

Оптимистичная конкурентность (.NET):

```csharp
ItemRequestOptions options = new ItemRequestOptions { IfMatchEtag = etag };
await container.ReplaceItemAsync<Order>(order, order.id, partitionKey, options);
```

Оптимистичная конкурентность (Python):

```python
from azure.core import MatchConditions

container.replace_item(
    item=order["id"],
    body=order,
    etag=etag,
    match_condition=MatchConditions.IfNotModified,
)
```

Транзакционный батч (.NET):

```csharp
TransactionalBatch batch = container.CreateTransactionalBatch(partitionKey)
    .CreateItem<Order>(order)
    .CreateItem<Payment>(payment)
    .PatchItem("summary-cust-2043", new[]
    {
        PatchOperation.Increment("/orderCount", 1)
    });
using TransactionalBatchResponse response = await batch.ExecuteAsync();
```

Транзакционный батч (Python):

```python
response = container.execute_item_batch(
    batch_operations=batch_operations,
    partition_key="cust-2043",
)
```

Bulk в .NET:

```csharp
CosmosClientOptions options = new CosmosClientOptions
{
    AllowBulkExecution = true
};
CosmosClient bulkClient = new CosmosClient(endpoint, new DefaultAzureCredential(), options);
```

Установка Python-зависимостей для асинхронной записи:

```
pip install azure-cosmos aiohttp
```

Ключевые лимиты:

| Параметр | Значение |
|---|---|
| Операций в транзакционном батче | 100 |
| Размер полезной нагрузки батча | 2 МБ |
| Максимальное время выполнения батча | 5 секунд |
| Значений ключа партиции в батче | 1 |
| Операций в одном patch-запросе | 10 |

## Что запомнить

- Для точного чтения, когда известны id и ключ партиции, используйте point read; это дешевле запроса.
- Create отклоняет дубликаты (409), replace требует существующий элемент (404), upsert вставляет или заменяет.
- TTL требует включенного `DefaultTimeToLive` контейнера; `ttl` элемента переопределяет его, `-1` делает элемент бессрочным.
- ETag защищает от потери обновлений: при несовпадении возвращается 412, и код должен перечитать и повторить или сообщить конфликт.
- Транзакционный батч атомарен только внутри одной логической партиции, до 100 операций.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-nosql-operations/
- Partial document update in Azure Cosmos DB; Get started with partial document update; Time to live in Azure Cosmos DB; Configure time to live in Azure Cosmos DB for NoSQL; Transactions and optimistic concurrency control; Transactional batch operations in Azure Cosmos DB; Bulk import data to Azure Cosmos DB for NoSQL with the .NET SDK; Best practices for the Azure Cosmos DB Python SDK (названия из источника, URL не приведены)
