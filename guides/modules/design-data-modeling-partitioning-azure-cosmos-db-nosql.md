# Моделирование данных и выбор ключа партиционирования в Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/

## Цель модуля

Научиться переносить реляционную схему в документную модель Azure Cosmos DB for NoSQL: выделять агрегаты, опираться на шаблоны доступа, решать, что встраивать (embed), а что ссылать (reference), применять денормализацию и предагрегацию, выбирать ключ партиционирования (включая иерархические и синтетические ключи) и находить антипаттерны и стоимость дизайна.

## Ключевые понятия

- **Aggregate root (корень агрегата)** - бизнес-объект, который управляет жизненным циклом и согласованностью связанных данных (например, заказ с позициями).
- **Access pattern (шаблон доступа)** - операция приложения: тип (чтение или запись), частота, фильтры и нужная форма результата.
- **Embed / reference (встраивание / ссылка)** - хранить связанные данные внутри элемента или в отдельном элементе, связанном идентификатором.
- **Denormalized projection (денормализованная проекция)** - копия значения из другого агрегата для быстрого чтения; авторитетный источник остается у владельца.
- **Preaggregation (предагрегация)** - хранение вычисленного ответа (например, `salesOrderCount`).
- **Item (элемент)** - JSON-документ и область атомарной операции над одним элементом.
- **Logical partition (логическая партиция)** - все элементы с одним значением ключа партиционирования; граница маршрутизации и транзакций; до 20 ГБ и 10 000 RU/s.
- **Physical partition (физическая партиция)** - до 50 ГБ и 10 000 RU/s; делится автоматически.
- **Partition key (ключ партиционирования)** - путь в контейнере и значение в элементе; задается при создании контейнера и не меняется.
- **Cardinality (кардинальность)** - число различных значений ключа; высокая кардинальность важна для распределения.
- **Hierarchical partition key (иерархический ключ, до трех уровней)** - позволяет разбивать крупный первый уровень по следующим.
- **Synthetic key (синтетический ключ)** - вычисляемое приложением значение ключа (конкатенация, суффикс, хеш-суффикс).
- **Transactional batch (транзакционный пакет)** - несколько операций атомарно внутри одной логической партиции (до 100 операций и 2 МБ полезной нагрузки).
- **Container copy job (задание копирования контейнера)** - перенос данных в новый контейнер при смене ключа (preview).
- **Change feed (лента изменений)** - источник изменений для синхронизации проекций.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/1-introduction

Сценарий Contoso: интернет-магазин переезжает с реляционной БД (девять таблиц), а одна из витрин партнеров вырастает в миллионы товаров. Нужно определить, какие данные принадлежат друг другу, и оптимизировать модель и распределение данных. Кандидаты в агрегаты: Customer, SalesOrder, Product, Category, Tag.

### 2. Identify aggregate boundaries and access patterns
https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/2-identify-access-patterns

Вопросы для определения границ: удаляется ли связанное вместе с родителем, должны ли изменения быть атомарными, может ли данные существовать отдельно, растет ли коллекция без границ, является ли данные общими. Для Contoso выделены пять агрегатов. Инвентарь шаблонов доступа фиксирует операцию, тип, частоту и фильтр. Нагрузка читающая, а фильтры повторяются по идентификаторам клиента и категории, что подсказывает границы партиций.

### 3. Map aggregates to items: embed or reference
https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/3-embed-reference

Агрегат обычно соответствует одному элементу, но это не требование. Встраивание дает атомарность и одно чтение; минус - размер и стоимость записи (Replace переписывает весь элемент). Patch API уменьшает передаваемые данные, но не обязательно RU. Лимит элемента - 2 МБ. Адреса и учетные данные клиента встраиваются; заказы ссылаются на клиента через customerId. Ссылки - не внешние ключи: приложение сама поддерживает связи.

### 4. Denormalize and preaggregate for performance
https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/4-optimize-data-reads

Страница категории требовала трех запросов; денормализация копирует название категории и теги в элемент товара. Копии поддерживаются change feed: при переименовании слушатель обновляет проекции. Подходят значения, которые часто читаются, редко меняются и малы. Предагрегация (`salesOrderCount`) позволяет ранжировать клиентов; для атомарного обновления счетчика заказ и клиент должны быть в одной логической партиции и одном транзакционном пакете. Поэтому клиент и заказы объединяются в один контейнер с полем `type`.

### 5. Select a partition key
https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/5-select-partition-key

Ключ задается при создании контейнера и не меняется. Оценивают шесть критериев: высокая кардинальность, равномерное распределение хранения, равномерное распределение запросов, присутствие в частых фильтрах, неизменяемость, допустимый тип и размер (до 2048 байт, или 101 байт без больших ключей). Для Contoso: product - `/categoryId`; customer - `/customerId`; productMeta - `/type` (низкая кардинальность допустима, так как контейнер маленький). Изменить ключ можно только копированием данных в новый контейнер.

### 6. Implement hierarchical partition keys
https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/6-implement-hierarchical-partition-keys

Иерархический ключ до трех уровней позволяет одному значению первого уровня (например, арендатору) занимать несколько физических партиций и превышать 20 ГБ. Для Contoso: `/tenantId`, `/categoryId`, `/id`. Запросы маршрутизируются по префиксу иерархии, указанному в WHERE; фильтр только по второму уровню приводит к перебору всех партиций. Нужны SDK версий .NET 3.33.0+, Java 4.42.0+, Python 4.6.0+, JavaScript 4.0.0+ (в JavaScript в превью). Ключ нельзя добавить к существующему контейнеру.

### 7. Implement synthetic keys and multitenant partitioning
https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/7-synthetic-keys-multitenant

Синтетический ключ - вычисляемое свойство: конкатенация (например, `deviceId-дата`), случайный суффикс (трудно прочитать по одному идентификатору) или предвычисленный хеш-суффикс (стабильный и читаемый). Нельзя использовать встроенный хеш языка (`GetHashCode`, `hash()`), так как он не стабилен между запусками. Multitenancy в одном контейнере: общая пропускная способность, логическая изоляция; авторизация по арендатору - задача приложения. Крупного арендатора можно вынести в отдельный аккаунт.

### 8. Identify anti-patterns and estimate cost
https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/8-identify-anti-patterns-estimate-cost

Антипаттерны: низкая кардинальность ключа в большом контейнере; высокая кардинальность без выравнивания с запросами; `/id` в запросно-тяжелой нагрузке; ключ, концентрирующий текущие записи (дата); ключ под один экран; перекошенный ключ (крупный арендатор); изменяемое значение ключа; путаница "читаются вместе" и "принадлежат друг другу"; путаница проекции с источником; неограниченно растущий массив внутри элемента. Диагностика: normalized RU consumption, лог PartitionKeyStatistics, алерт на размер логической партиции. Оценка: чтение элемента 1 КБ с ключом = 1 RU (session, consistent prefix, eventual); strong и bounded staleness - вдвое дороже; умножение на пиковую частоту; учет регионов (throughput в каждом регионе).

### 9. Exercise - Design a model and partition strategy
https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/9-exercise-design-model-partitioning

Практическое задание (около 45 минут): сравнение стоимости в RU для нормализованной, встроенной и денормализованной моделей, оценка маршрутизации запросов при иерархическом ключе. Нужна подписка Azure.

### 10. Module assessment
https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/10-knowledge-check

Проверка знаний (около 5 минут). Текст вопросов в источнике не приведен.

### 11. Summary
https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/11-summary

Девять таблиц превращены в три контейнера: customer (клиенты и заказы), product (товары с встроенными тегами и названием категории), productMeta (категории и теги). Ключевые выводы: сначала границы агрегатов, затем шаблоны доступа; встраивать ограниченные данные, ссылаться на независимые и неограниченные; проекции имеют источник, механизм синхронизации и окно согласованности; логическая партиция определяет маршрутизацию и транзакции; оценивать ключ по кардинальности, распределению, неизменяемости и фильтрам; оценивать стоимость по измеренным RU.

## Важные команды / код / настройки

**Встроенный элемент клиента (фрагмент источника):** `addresses` встроен как массив, `password` - объект с `hash` и `salt`. Значения примера в источнике не воспроизведены полностью.

**Ссылка на категорию и теги в товаре:**
```
{
  "id": "C0000000-0000-0000-0000-000000000002",
  "categoryId": "C0000000-0000-0000-0000-000000000003",
  "categoryName": "Components, Saddles",
  "sku": "SE-R581",
  "name": "LL Road Seat/Saddle",
  "price": 27.12,
  "tags": [
    { "id": "C0000000-0000-0000-0000-000000000004", "name": "Tag-113" },
    { "id": "C0000000-0000-0000-0000-000000000005", "name": "Tag-5" }
  ]
}
```

**Предагрегированный счетчик:** `"salesOrderCount": 28` в элементе клиента; тип `customer` и `salesOrder` объединены в контейнере `customer` по `customerId`.

**Иерархический ключ (.NET):**
```
List<string> keyPaths = new()
{
    "/tenantId",
    "/categoryId",
    "/id"
};
ContainerProperties properties = new(id: "product", partitionKeyPaths: keyPaths);
Container container = await database.CreateContainerIfNotExistsAsync(properties);
```

**Иерархический ключ (Python):**
```
container = database.create_container_if_not_exists(
    id="product",
    partition_key=PartitionKey(
        path=["/tenantId", "/categoryId", "/id"],
        kind="MultiHash",
    ),
)
```

**Чтение по полному иерархическому ключу (.NET):**
```
PartitionKey partitionKey = new PartitionKeyBuilder()
    .Add(product.tenantId)
    .Add(product.categoryId)
    .Add(product.id)
    .Build();
ItemResponse<Product> response = await container.ReadItemAsync<Product>(product.id, partitionKey);
```

**Чтение по иерархическому ключу (Python):**
```
item = container.read_item(
    item=product_id,
    partition_key=[tenant_id, category_id, product_id],
)
```

**Запрос с префиксом иерархии (.NET):**
```
QueryDefinition query = new QueryDefinition(
        "SELECT p.id, p.name, p.price FROM product p WHERE p.tenantId = @tenant AND p.categoryId = @category")
    .WithParameter("@tenant", tenantId)
    .WithParameter("@category", categoryId);
```

**Синтетический хеш-суффикс (C#):**
```
// SHA256.HashData requires .NET 5 or later.
static int Bucket(string value, int buckets)
{
    byte[] hash = SHA256.HashData(Encoding.UTF8.GetBytes(value));
    return ((hash[0] << 8) | hash[1]) % buckets;
}
string partitionKey = $"{order.orderDate:yyyy-MM-dd}-{Bucket(order.customerId, 100)}";
```

**Синтетический хеш-суффикс (Python):**
```
import hashlib
def bucket(value: str, buckets: int) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:2], "big") % buckets
partition_key = f"{order['orderDate'][:10]}-{bucket(order['customerId'], 100)}"
```

**Измерение RU (.NET и Python):** `Console.WriteLine($"Charge: {response.RequestCharge} RU");` и `response.get_response_headers()["x-ms-request-charge"]`.

**Числовые ограничения из источника:** логическая партиция - 20 ГБ и 10 000 RU/s; физическая - 50 ГБ и 10 000 RU/s; транзакционный пакет - до 100 операций и 2 МБ; элемент - до 2 МБ; значение ключа - до 2048 байт (101 байт без больших ключей); чтение 1 КБ по ключу - 1 RU с session, consistent prefix или eventual; strong и bounded staleness - вдвое больше.

## Что запомнить

- Сначала выделите агрегаты по владению и жизненному циклу, затем проверьте их шаблонами доступа.
- Встраивайте ограниченные данные, которые меняются вместе; ссылайтесь на независимые и растущие без границ данные.
- Денормализованные копии - это проекции: у них должен быть источник истины, механизм синхронизации и допустимое окно несогласованности.
- Ключ партиционирования нельзя изменить на месте: выбирайте его по кардинальности, распределению, частым фильтрам и неизменяемости.
- Иерархические ключи решают рост крупного арендатора, а синтетические - распределение записей при отсутствии подходящего свойства; для хеш-суффикса используйте стабильный алгоритм (SHA-256).

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/design-data-modeling-partitioning-azure-cosmos-db-nosql/
- В источнике упоминаются (без ссылок в тексте): Partitioning and horizontal scaling in Azure Cosmos DB; Hierarchical partition keys in Azure Cosmos DB; Create a synthetic partition key; Data modeling in Azure Cosmos DB for NoSQL; Model and partition data on Azure Cosmos DB for NoSQL; Container copy jobs in Azure Cosmos DB; Create an alert on the logical partition key storage size; Azure Cosmos DB Cost Estimator; Multitenancy and Azure Cosmos DB.
