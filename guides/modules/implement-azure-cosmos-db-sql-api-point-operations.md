# Точечные операции с Azure Cosmos DB для NoSQL через SDK

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/

## Цель модуля

Выполнять точечные операции (CRUD) с отдельными элементами Azure Cosmos DB для NoSQL через SDK, обрабатывать коды ошибок, использовать point read и настраивать TTL (time to live) для отдельного элемента.

## Ключевые понятия

- **Point operations (точечные операции)** - операции с одним элементом по `id` и значению partition key: create, read, update, delete.
- **Модель элемента** - класс с обязательными полями `id` и свойством с именем partition key path (в примере `categoryId`).
- **Point read** - чтение по `id` и partition key; самый эффективный способ чтения (около 1 RU для 1 КБ, по данным урока); запрос обычно стоит не меньше 2.3 RU.
- **ETag** - версия элемента, используется для оптимистичной конкурентности.
- **Request charge (x-ms-request-charge)** - стоимость операции в RU.
- **TTL (time to live)** - время жизни элемента в секундах от последнего изменения, после чего он автоматически удаляется.
- **Delete by partition key** - асинхронная фоновая операция удаления всех элементов с одним partition key; ограничена 10 % RU/s контейнера в секунду и по умолчанию отключена (включается через Azure Support).

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/1-introduction

SDK используется для точечных операций, транзакций и массовой обработки. Цели модуля: выполнить CRUD через SDK и настроить TTL для элемента.

### 2. Понимание точечных операций
Источник: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/2-understand-point-operations

- В .NET класс элемента содержит как минимум `id` и свойство с именем partition key path; можно добавлять другие свойства, включая сложные типы и списки.
- Атрибут `[JsonProperty(PropertyName = "id")]` позволяет использовать в C# имя `InternalId`, сохраняя `id` в JSON.
- В Python минимальный элемент содержит `id` и атрибут partition key; для различия имён используется метод `to_dict()`, который переименовывает поля при сериализации.
- В JavaScript аналогично используется метод `toJSON()`.
- Модель в примере - класс `Product` с полями `id`, `name`, `categoryId` (partition key), `price` и `tags`.

### 3. Создание документов
Источник: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/3-create-documents

- .NET: `container.CreateItemAsync<Product>(saddle)`; результат `ItemResponse<Product>` содержит `StatusCode`, `RequestCharge`, `Resource`.
- Python: `container.create_item(body=saddle)`; метаданные через `get_response_headers()` (`x-ms-request-charge`, `etag`).
- JavaScript: `container.items.create(saddle)`; метаданные в `headers`.
- Коды ошибок из урока: 400 (Bad Request - ошибка в теле запроса), 403 (Forbidden - контейнер, вероятно, заполнен), 409 (Conflict - элемент с таким id уже есть), 413 (RequestEntityTooLarge - элемент превышает максимальный размер), 429 (TooManyRequests - превышен RU/s контейнера).
- В .NET конфликт обрабатывается через `catch (CosmosException ex) when (ex.StatusCode == HttpStatusCode.Conflict)`; в Python - через `CosmosHttpResponseError` и `ex.status_code`; в JavaScript - через `error.code`.

### 4. Чтение документа
Источник: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/4-read-document

- Point read использует пару `id` и partition key; запрос без point read для одного элемента дороже (минимум около 2.3 RU).
- .NET: `container.ReadItemAsync<Product>(id, partitionKey)` с `PartitionKey(categoryId)`.
- Python: `container.read_item(item=item_id, partition_key=partition_key_value)`.
- JavaScript: `container.item(itemId, partitionKeyValue).read()`.

### 5. Обновление документов
Источник: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/5-update-documents

- Изменения вносятся в локальный объект (например, цена с 27.12 до 35.00), затем сохраняются заменой элемента.
- .NET: `container.ReplaceItemAsync<Product>(saddle)`.
- Python: `container.replace_item(item=saddle, body=saddle)`.
- JavaScript: `container.item(saddle.id, saddle.categoryId).replace(saddle)`.
- Повторно читать элемент перед следующим обновлением не нужно.
- Cosmos DB поддерживает оптимистичную конкурентность и возвращает конфликт, если элемент изменился после последнего чтения; детали - в документации SDK.

### 6. Настройка TTL для отдельного документа
Источник: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/6-configure-ttl-for-document

- Свойство `ttl` в JSON задаёт время жизни элемента в секундах от последнего изменения.
- В .NET используется `[JsonProperty(PropertyName = "ttl", NullValueHandling = NullValueHandling.Ignore)] public int? ttl`, чтобы не писать ttl, если он не задан.
- В Python поле `ttl` добавляется в `to_dict()` только если оно не None.
- В JavaScript поле `ttl` добавляется в `toJSON()` только если оно не null.
- Обновление элемента выполняется заменой (`ReplaceItemAsync`, `replace_item`, `replace`).
- Важно: работает только если на уровне контейнера настроен `DefaultTimeToLive`; значение `ttl = -1` отключает TTL для элемента.

### 7. Удаление документов
Источник: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/7-delete-documents

- Для удаления нужны `id` и значение partition key.
- .NET: `container.DeleteItemAsync<Product>(id, partitionKey)`; Python: `container.delete_item(item=item_id, partition_key=partition_key_value)`; JavaScript: `container.item(itemId, partitionKeyValue).delete()`.
- Удаление всех элементов одного partition key: .NET `DeleteAllItemsByPartitionKeyStreamAsync`, Python `delete_all_items_by_partition_key`.
- Эта операция асинхронная, фоновая, ограничена 10 % RU/s контейнера в секунду и по умолчанию отключена; её активирует Azure Support.

### 8. Упражнение: создание и обновление документов через SDK
Источник: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/8-exercise-create-update-documents-sdk

Упражнение (около 15 минут) в лабораторной среде: группа ресурсов, провайдеры ресурсов, Azure Cosmos DB, локальное окружение. Подробных шагов в исходниках нет.

### 9. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/9-knowledge-check

В исходных материалах вопросы не приведены.

### 10. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/10-summary

Выполнены базовые операции create, read, update, delete над элементом через SDK и обновлено значение TTL. Эти операции служат кирпичиками для массовых и транзакционных операций.

## Важные команды / код / настройки

Создание элемента (.NET):

```
ItemResponse<Product> response = await container.CreateItemAsync<Product>(saddle);

HttpStatusCode status = response.StatusCode;
double requestUnits = response.RequestCharge;
Product item = response.Resource;
```

Point read (Python):

```
item_id = "027D0B9A-F9D9-4C96-8213-C8546C4AAE71"
partition_key_value = "26C74104-40BC-4541-8EF5-9892F7F03D72"

saddle = container.read_item(item=item_id, partition_key=partition_key_value)
```

Установка TTL (Python):

```
saddle["ttl"] = 1000
container.replace_item(item=saddle, body=saddle)
```

Удаление элемента (JavaScript):

```
await container.item(itemId, partitionKeyValue).delete();
```

Атрибут TTL в модели (.NET):

```
[JsonProperty(PropertyName = "ttl", NullValueHandling = NullValueHandling.Ignore)]
public int? ttl { get; set; }
```

Настройки: `ttl` в секундах; `ttl = -1` отключает TTL для элемента; для работы TTL нужен `DefaultTimeToLive` на уровне контейнера; delete by partition key ограничен 10 % RU/s и требует активации Azure Support.

## Что запомнить

- Точечные операции работают по паре `id` и partition key; это самый дешёвый путь к отдельному элементу.
- Обрабатывайте коды 409 (конфликт id), 429 (превышение RU/s), 413 (слишком большой элемент) и 400 (ошибка тела запроса).
- Чтобы сохранить имена свойств JSON, используйте атрибуты (.NET), `to_dict()` (Python) или `toJSON()` (JavaScript).
- TTL задаётся свойством `ttl` в секундах, но работает только при настроенном `DefaultTimeToLive` контейнера.
- Удаление всех элементов по partition key - фоновая операция, отключённая по умолчанию и ограниченная 10 % RU/s.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/implement-azure-cosmos-db-sql-api-point-operations/
- Azure Cosmos DB libraries for .NET; Azure Cosmos DB Python SDK for API for NoSQL; Azure Cosmos DB Node.js SDK for API for NoSQL (ссылки из урока 10)
