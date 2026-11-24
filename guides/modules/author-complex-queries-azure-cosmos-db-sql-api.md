# Составление сложных запросов в Azure Cosmos DB SQL API

**Источник:** https://learn.microsoft.com/en-us/training/modules/author-complex-queries-azure-cosmos-db-sql-api/

## Цель модуля

Научиться писать сложные запросы к JSON-документам с вложенными массивами: кросс-произведения (cross-product) через JOIN, коррелированные подзапросы, параметризованные запросы и постраничный вывод результатов в SDK.

## Ключевые понятия

- **JOIN (внутри элемента)** - в Azure Cosmos DB for NoSQL JOIN работает только в пределах одного элемента и создает декартово произведение между исходным элементом и элементами вложенного массива.
- **Cross-product (кросс-произведение)** - все возможные комбинации значений двух наборов внутри одного элемента.
- **Correlated subquery (коррелированный подзапрос)** - подзапрос, который фильтрует элементы массива перед JOIN, чтобы сократить результат.
- **Parameterized query (параметризованный запрос)** - запрос с именованными параметрами (`@lower`, `@upper`), значения которых передаются из кода.
- **Feed iterator (итератор страниц)** - механизм постраничного чтения результатов; позволяет задать размер страницы и получать страницы по одной.
- **QueryDefinition / QueryRequestOptions (.NET)**, **query_items (Python)**, **items.query (JavaScript)** - способы передать запрос и параметры в SDK.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/author-complex-queries-azure-cosmos-db-sql-api/1-introduction

JSON-документы часто содержат вложенные документы и массивы, поэтому нужны более сложные выражения, чем в обычном реляционном SQL. Цели модуля: создать кросс-произведение запросом и реализовать коррелированный подзапрос.

### 2. Create cross-product queries
https://learn.microsoft.com/en-us/training/modules/author-complex-queries-azure-cosmos-db-sql-api/2-create-cross-product-queries

JOIN в Cosmos DB не объединяет разные элементы, а раскрывает массив внутри одного элемента. Пример: элемент с массивом `tags` из трех тегов при запросе с `JOIN t IN p.tags` дает три строки, по одной на каждый тег, с полями `id`, `name` и `tag`.

### 3. Implement correlated subqueries
https://learn.microsoft.com/en-us/training/modules/author-complex-queries-azure-cosmos-db-sql-api/3-implement-correlated-subqueries

Чтобы не раскрывать весь массив, в JOIN подставляется подзапрос с фильтром. В примере из источника оставляются только теги с `class = 'trade-in'`, и результат уменьшается на одну строку (тег `group` исключается).

### 4. Implement variables in queries
https://learn.microsoft.com/en-us/training/modules/author-complex-queries-azure-cosmos-db-sql-api/4-implement-variables-queries

Вместо жестко заданных значений (например, `500`) в WHERE используются параметры. Показано, как это делается в C# (`WithParameter`), Python (`parameters` со списком `name`/`value`) и JavaScript (`parameters` в `querySpec`). Перечислены преимущества: защита от SQL-инъекций, гибкость изменения фильтров без изменения структуры запроса, повторное использование определений запроса.

### 5. Paginate query results
https://learn.microsoft.com/en-us/training/modules/author-complex-queries-azure-cosmos-db-sql-api/5-paginate-query-results

Для постраничного чтения задается размер страницы: в .NET через `QueryRequestOptions.MaxItemCount` и `GetItemQueryIterator` с циклом по `HasMoreResults` и `ReadNextAsync`; в Python через `query_items(max_item_count=...)` и `by_page()`; в JavaScript через `items.query` с `maxItemCount` и `getAsyncIterator()`.

### 6. Exercise: Paginate cross-product query results with the Azure Cosmos DB for NoSQL SDK
https://learn.microsoft.com/en-us/training/modules/author-complex-queries-azure-cosmos-db-sql-api/6-exercise-paginate-cross-product-query-results-sdk

Практическое задание (около 15 минут) с SDK: нужна подписка Azure с правами администратора. Шаги: создать resource group, включить resource providers, настроить Azure Cosmos DB и локальное окружение.

### 7. Knowledge check
https://learn.microsoft.com/en-us/training/modules/author-complex-queries-azure-cosmos-db-sql-api/7-knowledge-check

Проверка знаний (около 5 минут). Текст в источнике не приведен.

### 8. Summary
https://learn.microsoft.com/en-us/training/modules/author-complex-queries-azure-cosmos-db-sql-api/8-summary

Вы научились писать кросс-произведения запросом с JOIN, создавать коррелированный подзапрос внутри такого запроса и реализовывать те же запросы в .NET SDK.

## Важные команды / код / настройки

**JOIN с раскрытием массива тегов:**
```
SELECT 
    p.id,
    p.name,
    t.name AS tag
FROM 
    products p
JOIN
    t IN p.tags
```

**Коррелированный подзапрос (фильтр по `class`):**
```
SELECT 
    p.id,
    p.name,
    t.name AS tag
FROM 
    products p
JOIN
    (SELECT VALUE t FROM t IN p.tags WHERE t.class = 'trade-in') AS t
```

**Параметры в C# (.NET SDK):**
```
string sql = "SELECT p.name, t.name AS tag FROM products p JOIN t IN p.tags WHERE p.price >= @lower AND p.price <= @upper"
QueryDefinition query = new (sql)
    .WithParameter("@lower", 500)
    .WithParameter("@upper", 1000);
```

**Параметры в Python SDK:**
```
query_text = (
    "SELECT p.name, t AS tag "
    "FROM products p JOIN t IN p.tags "
    "WHERE p.price >= @lower AND p.price <= @upper"
)

query = {
    "query": query_text,
    "parameters": [
        {"name": "@lower", "value": 500},
        {"name": "@upper", "value": 1000}
    ]
}
```

**Параметры в JavaScript SDK:**
```
const sql = "SELECT p.name, t.name AS tag FROM products p JOIN t IN p.tags WHERE p.price >= @lower AND p.price <= @upper";

const querySpec = {
    query: sql,
    parameters: [
        { name: "@lower", value: 500 },
        { name: "@upper", value: 1000 }
    ]
};
```

**Постраничный вывод (.NET):**
```
QueryRequestOptions options = new()
{
    MaxItemCount = 100
};

FeedIterator<Product> iterator = container.GetItemQueryIterator<Product>(query, requestOptions: options);

while(iterator.HasMoreResults)
{
    foreach(Product product in await iterator.ReadNextAsync())
    {
        // Handle individual items
    }
}
```

**Постраничный вывод (Python):**
```
iterator = container.query_items(
    query=query,
    enable_cross_partition_query=True,
    max_item_count=100  # Set maximum items per page
)

for page in iterator.by_page():
    for product in page:
        print(f"[{product['id']}]	{product['name']}	${product['price']:.2f}")
```

**Постраничный вывод (JavaScript):**
```
const options = {
    maxItemCount: 100 // Set the maximum number of items per page
};

const iterator = container.items.query(query, options);

for await (const page of iterator.getAsyncIterator()) {
    page.resources.forEach(product => {
        console.log(`[${product.id}] ${product.name} $${product.price.toFixed(2)}`);
    });
}
```

## Что запомнить

- JOIN в Cosmos DB раскрывает массив внутри одного элемента и формирует кросс-произведение.
- Подзапрос внутри JOIN (`SELECT VALUE t FROM t IN p.tags WHERE ...`) сокращает число строк до соединения.
- Параметры (`@name`) защищают от SQL-инъекций и позволяют менять фильтры без изменения текста запроса.
- Для больших результатов читайте данные страницами: задайте размер страницы (`MaxItemCount`, `max_item_count`, `maxItemCount`).
- Один и тот же запрос реализуется в .NET, Python и JavaScript SDK с похожими механизмами параметров и страниц.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/author-complex-queries-azure-cosmos-db-sql-api/
- В источнике упоминаются (без ссылок в тексте): Joins in Azure Cosmos DB; SQL subquery examples for Azure Cosmos DB.
