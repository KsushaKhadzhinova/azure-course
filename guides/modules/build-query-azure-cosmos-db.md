# Построение запросов к Azure Cosmos DB для NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/

## Цель модуля

Научиться подключаться к Azure Cosmos DB для NoSQL через SDK, выполнять CRUD-операции с элементами и писать эффективные SQL-запросы, которые минимизируют потребление Request Units (RU). Модуль рассчитан на создание AI-приложений, которые хранят и извлекают JSON-документы.

## Ключевые понятия

- **Account (аккаунт)** - верхний уровень управления; имеет DNS-endpoint вида `https://<account-name>.documents.azure.com:443/`.
- **Database (база данных)** - логическое пространство имён, группирует контейнеры; может задавать общий throughput.
- **Container (контейнер)** - основная единица масштабирования, хранит JSON-элементы; обязательно имеет partition key.
- **Item (элемент)** - JSON-документ; обязательное поле `id`, уникален в пределах partition key.
- **Partition key** - свойство, по которому данные распределяются по физическим партициям; должно иметь высокую кардинальность. Нельзя изменить без создания нового контейнера и миграции.
- **Request Units (RU/s)** - единица стоимости и пропускной способности; операции (чтение, запись, запрос) потребляют RU.
- **Manual и Autoscale throughput** - фиксированный RU/s либо масштабирование от 10 % до максимума.
- **Системные свойства** - `_rid`, `_self`, `_etag` (оптимистичная конкурентность), `_ts` (время изменения в секундах), `_attachments`.
- **Point read** - чтение одного элемента по `id` и partition key; самый дешёвый способ (около 1 RU для 1 КБ).
- **Single-partition vs cross-partition запрос** - запрос с указанием partition key дешевле и быстрее, чем запрос, который обходит все партиции.
- **Parameterized query** - запрос с параметрами `@name`, защищает от инъекций и позволяет кешировать план запроса.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/1-introduction

Модуль описывает задачу построения рекомендательного движка с JSON-каталогом товаров. Цели: объяснить модель ресурсов Cosmos DB, реализовать CRUD через SDK, выбирать между point read и запросом, писать SQL-запросы. В уроке отмечено, что примеры кода основаны на актуальной версии библиотеки `azure-cosmos` для Python.

### 2. Изучение Azure Cosmos DB для NoSQL
Источник: https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql

- Иерархия: аккаунт → базы данных → контейнеры → элементы. Аккаунт задаёт consistency level, регионы геo-репликации и сетевые политики.
- Лимит: до 500 баз данных и контейнеров суммарно на аккаунт (по умолчанию).
- Partition key должен присутствовать в каждом документе и иметь много различных значений. Примеры: `userId` для пользовательских данных, `categoryId` для каталога. Низкая кардинальность (например, булево `isActive`) и даты дают «горячие» партиции.
- Throughput: на уровне базы (общий, минимум 400 RU/s, до 25 контейнеров) или контейнера (выделенный, минимум 400 RU/s). Autoscale: минимум 10 % от максимума; минимальный максимум autoscale 1000 RU/s.
- Стоимость: point read 1 КБ ≈ 1 RU; запись 1 КБ ≈ 5-10 RU; простой отфильтрованный запрос ≈ 3-5 RU. На стоимость влияют размер элемента, индексация, уровень консистентности, сложность запроса и cross-partition запросы.
- Заголовок `x-ms-request-charge` содержит стоимость операции в RU.
- `_etag` используется для оптимистичной конкурентности: обновление с устаревшим `_etag` завершается конфликтом.

### 3. Реализация SDK Azure Cosmos DB для NoSQL
Источник: https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/3-implement-cosmos-db-sdk

- Точка входа - класс `CosmosClient`; один экземпляр клиента нужно переиспользовать на всё время жизни приложения (singleton/application-scoped service).
- Аутентификация: account keys (общий секрет с полным доступом, есть primary и secondary ключи для ротации) или Microsoft Entra ID через RBAC. Для production рекомендован Entra ID. `DefaultAzureCredential` выбирает способ автоматически (Azure CLI локально, managed identity в облаке).
- Встроенные роли: Cosmos DB Built-in Data Reader (чтение) и Cosmos DB Built-in Data Contributor (чтение и запись).
- `get_database_client()` и `get_container_client()` не делают сетевых вызовов; ошибка появляется при первой операции, если ресурса нет.
- `create_database()` / `create_container()` падают, если ресурс уже существует; `create_database_if_not_exists()` / `create_container_if_not_exists()` идемпотентны.
- `create_item()` - ошибка 409 (`CosmosResourceExistsError`) при дубликате; `upsert_item()` вставляет или заменяет; `replace_item()` требует существования и поддерживает проверку `if_match` с `_etag`.
- `read_item()` - point read; при отсутствии элемента - `CosmosResourceNotFoundError`.
- `delete_item()` - удаление по `id` и partition key.
- Метаданные: `x-ms-request-charge` (RU) и `x-ms-activity-id` (для обращения в поддержку).

Пример из урока (создание контейнера с partition key):

```
from azure.cosmos import CosmosClient, PartitionKey

database = client.get_database_client("productcatalog")

container = database.create_container_if_not_exists(
    id="products",
    partition_key=PartitionKey(path="/categoryId"),
    offer_throughput=400
)
```

### 4. Запросы к Azure Cosmos DB для NoSQL
Источник: https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/4-query-cosmos-db-nosql

- Базовый синтаксис: `SELECT ... FROM <container alias> WHERE ...`, поддерживаются `ORDER BY` (ASC по умолчанию, DESC), `TOP`, проекции и `SELECT VALUE`.
- Операторы: `=`, `!=`, `<`, `>`, `<=`, `>=`, `AND`, `OR`, `NOT`, `IN`, `BETWEEN`. Строковые функции: `CONTAINS`, `STARTSWITH`, `ENDSWITH`, `UPPER`, `LOWER`. Сравнение строк по умолчанию чувствительно к регистру.
- Агрегаты: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
- Массивы: `ARRAY_CONTAINS(p.features, "wifi")`; для поэлементного фильтра - `JOIN f IN p.features`.
- Параметры передаются отдельным массивом; при указании partition key запрос маршрутизируется в одну партицию. Cross-partition запросы требуют `enable_cross_partition_query=True` и стоят дороже.
- Пагинация: `max_item_count` задаёт размер страницы; `by_page()` и continuation token для веб-API. Токен кодирует внутреннее состояние запроса, его нужно хранить безопасно.
- Стоимость запроса: суммируйте `x-ms-request-charge` по страницам.
- Советы по оптимизации: ранняя фильтрация, проекция только нужных полей, использование partition key, `TOP` при ограниченной выборке, настройка индексации под паттерны запросов.

Примеры запросов из урока:

```
SELECT p.id, p.name, p.price, p.categoryId
FROM products p
```

```
SELECT * FROM products p
WHERE p.categoryId = @category AND p.price < @maxPrice
```

```
SELECT VALUE COUNT(1)
FROM products p
WHERE p.categoryId = "electronics"
```

```
SELECT p.name, f AS feature
FROM products p
JOIN f IN p.features
WHERE f IN ("wifi", "bluetooth")
```

### 5. Практика: хранилище документов RAG в Azure Cosmos DB для NoSQL
Источник: https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/5-exercise-build-rag-document-store

Упражнение (около 30 минут): развернуть аккаунт Cosmos DB for NoSQL, создать базу и контейнер для чанков документов с метаданными, написать Python-функции сохранения и поиска чанков, проверить их через Flask-приложение. Требования: подписка Azure, Visual Studio Code, последняя Azure CLI, Python 3.12 или новее. Само упражнение выполняется по ссылке из урока, в исходниках подробных шагов нет.

### 6. Оценка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/6-knowledge-check

В исходных материалах вопросы не приведены (только инструкция).

### 7. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/7-summary

Итог: иерархия ресурсов, роль partition key, ручной и autoscale throughput, подключение через account keys и Entra ID с переиспользованием клиента, CRUD-операции, SQL-запросы с фильтрами, проекциями, параметрами и агрегатами, разница стоимости single- и cross-partition запросов.

## Важные команды / код / настройки

```
from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential

endpoint = "https://mycosmosaccount.documents.azure.com:443/"
client = CosmosClient(endpoint, credential=DefaultAzureCredential())
```

```
container.upsert_item(body=product)
headers = container.client_connection.last_response_headers
request_charge = headers['x-ms-request-charge']
```

```
query = """
    SELECT * FROM products p
    WHERE p.categoryId = @category AND p.price < @maxPrice
"""
parameters = [
    {"name": "@category", "value": "electronics"},
    {"name": "@maxPrice", "value": 500.00}
]
items = container.query_items(
    query=query,
    parameters=parameters,
    partition_key="electronics"
)
```

Настройки из урока:
- Partition key задаётся при создании контейнера через `PartitionKey(path="/categoryId")`; изменить его нельзя.
- Throughput: `offer_throughput=400` (ручной) или `ThroughputProperties(auto_scale_max_throughput=4000)` (autoscale, 400-4000 RU/s).
- Роли Entra ID: `Cosmos DB Built-in Data Reader`, `Cosmos DB Built-in Data Contributor`.

## Что запомнить

- Partition key выбирайте с высокой кардинальностью и с учётом частых запросов; его нельзя поменять на месте.
- Один экземпляр `CosmosClient` переиспользуйте в приложении; для production используйте `DefaultAzureCredential` и роли Entra ID.
- Point read по `id` и partition key - самый дешёвый способ получить элемент (около 1 RU на 1 КБ); используйте его, когда ключи известны.
- Запросы с partition key в условии дешевле и быстрее cross-partition запросов; всегда используйте параметры вместо конкатенации строк.
- Следите за `x-ms-request-charge` и `x-ms-activity-id`: первый показывает стоимость, второй нужен для обращения в поддержку.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/
- Azure Cosmos DB for NoSQL documentation; Azure Cosmos DB SDK for Python; Getting started with SQL queries in Azure Cosmos DB; Best practices for Azure Cosmos DB Python SDK (ссылки из уроков модуля)
