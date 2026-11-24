# Запросы к Azure Cosmos DB для NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/

## Цель модуля

Писать параметризованные запросы Azure Cosmos DB для NoSQL с нужной структурой результата, обращаться к вложенным массивам через подзапросы и JOIN и постранично получать большие результаты с помощью continuation token.

## Ключевые понятия

- **FROM-алиас** - имя, которым запрос обращается к элементам контейнера; запрос всегда выполняется над одним контейнером.
- **Отсутствующие свойства** - свойство, которого нет в элементе, дает undefined, и элемент тихо выпадает из результата; типы не приводятся друг к другу.
- **Регистр** - имена свойств и строковые значения чувствительны к регистру; ключевые слова - нет.
- **Параметризованный запрос (parameterized query)** - текст запроса отделен от значений (`@name`), что закрывает путь SQL-инъекций. Параметры заменяют значения, но не имена свойств и алиасы.
- **Коррелированный подзапрос (correlated subquery)** - подзапрос, который ссылается на элемент внешнего запроса; выполняется для каждого элемента.
- **EXISTS, ARRAY, ARRAY_CONTAINS** - инструменты для фильтрации и проекции массивов внутри элемента.
- **JOIN (self-join)** - расширяет массив внутри одного элемента в декартово произведение; не объединяет контейнеры и элементы.
- **Continuation token** - непрозрачная закладка для продолжения запроса с того места, где остановилась предыдущая страница.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/1-introduction

Каталог товаров в основном читается запросами (фильтры по категории и цене, выборка по тегам, постраничная выдача). Сценарий: API каталога Contoso с несколькими сотнями тысяч товаров, где массив тегов вложен в каждый товар, а значения фильтров приходят из строки запроса. Модуль описывает модель стоимости запросов, параметризацию, проекцию, подзапросы, JOIN и постраничность.

### 2. Понимание языка запросов SQL
URL: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/2-understand-sql-query-language

Запросы работают с JSON-элементами. Структура: FROM (источник с алиасом), WHERE (фильтр), SELECT (проекция). `SELECT *` возвращает элементы целиком; перечисление свойств уменьшает объем ответа. Отсутствующее свойство дает undefined, и элемент пропадает из результата без ошибки. Функции IS_DEFINED, IS_NULL, IS_NUMBER, IS_STRING, IS_ARRAY, IS_OBJECT помогают проверять свойства. Сравнения не приводят типы: строка "63.50" не равна числу для фильтра `>= 50`. Имена свойств и строки чувствительны к регистру. По умолчанию индексируются все свойства. Стоимость определяется объемом чтения и числом партиций: равенство по ключу партиции направляет запрос в одну физическую партицию, IN - в набор партиций, диапазон по ключу партиции - во все.

### 3. Создание и выполнение запросов
URL: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/3-create-execute-queries

Значения из внешнего источника передаются параметрами (`@category`, `@max`), а не конкатенацией. Параметры заменяют только значения. Тип значения сохраняется: число дает числовое сравнение, строка - строковое. Проекция: алиасы через AS, объектный литерал `{ "price": p.price } AS scannerData`, `SELECT VALUE` для массива скаляров, `SELECT DISTINCT VALUE`. Встроенные функции: CONCAT, LOWER, STARTSWITH, CONTAINS, LIKE, GetCurrentDateTime, ARRAY_LENGTH. Функция в SELECT не влияет на использование индекса, а в WHERE может его отключить: LOWER в условии не использует индекс, STARTSWITH и диапазоны - используют; флаг нечувствительности к регистру сохраняет использование индекса, но сканирует больше записей. Выполнение в .NET: `GetItemQueryIterator<T>` и `FeedIterator<T>` с постраничным чтением, `RequestCharge` на каждой странице. В Python: `query_items`, `get_response_headers()` возвращает заряд только последней страницы; для суммы используется `response_hook`. Задание `PartitionKey` в опциях запроса ограничивает запрос одной логической партицией.

### 4. Реализация коррелированных подзапросов
URL: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/4-implement-correlated-subqueries

Подзапрос может быть некоррелированным или коррелированным (ссылается на внешний элемент и выполняется для каждого элемента). Выражение `t IN p.tags` связывает t с элементами массива. EXISTS возвращает элемент один раз, если хотя бы один элемент массива подходит. Одно условие на один элемент и два условия на разные элементы дают разные результаты: `EXISTS (SELECT VALUE d FROM d IN o.details WHERE d.price > 30 AND STARTSWITH(d.name, 'Road'))` требует, чтобы одна строка удовлетворяла обоим условиям. ARRAY_CONTAINS проверяет членство (с третьим аргументом true - частичное совпадение объекта); ARRAY_CONTAINS_ANY и ARRAY_CONTAINS_ALL проверяют набор значений, но не используют индекс. ARRAY(...) возвращает результат подзапроса массивом (пустой массив сохраняется у элемента). Скалярный подзапрос: `(SELECT VALUE COUNT(1) FROM t IN p.tags) AS tagCount`. Чтобы снизить стоимость, добавляйте индексируемые предикаты во внешний WHERE и сохраняйте ключ партиции.

### 5. Создание кросс-продуктовых запросов
URL: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/5-create-cross-product-queries

JOIN в Azure Cosmos DB для NoSQL работает внутри одного элемента (self-join) и не объединяет элементы или контейнеры. Для товара с двумя тегами `JOIN t IN p.tags` вернет две строки. Элементы с пустым массивом или без него не попадают в результат вовсе, что легко пропустить. Фильтры: индексируемые условия на родителе сокращают элементы до расширения; подзапрос в JOIN отбирает только нужные элементы массива. Несколько JOIN перемножаются: 5 тегов и 4 размера дают 20 строк; в одном запросе по умолчанию допускается до 10 JOIN (увеличивается обращением в поддержку). Пример из SDK: JOIN с подзапросом по тегу и параметрами, результат - плоская проекция `name` и `tag`.

### 6. Постраничный вывод результатов с continuation token
URL: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/6-page-results-continuation-tokens

Результаты всегда приходят страницами. `MaxItemCount` (`max_item_count` в Python) задает максимум элементов на страницу, но сервис может вернуть меньше, и даже пустую страницу при продолжающихся результатах; конец определяется по `HasMoreResults` (или по исчерпанию итератора), а не по размеру страницы. Continuation token передается клиенту с каждой страницей и позволяет продолжить запрос в другом запросе или на другом экземпляре; серверная сторона не держит состояние. Токен непрозрачен и действителен только для того же запроса с теми же значениями фильтров. Пустой (null) токен означает конец результатов. Ограничения: в .NET токены не поддерживают GROUP BY и DISTINCT без ORDER BY, а агрегаты COUNT и SUM по нескольким партициям токена не дают; в Python токены работают с потоковыми межпартиционными запросами (фильтры и проекции), но не с сортировкой, подсчетом и DISTINCT. Размер токена можно ограничить через `ResponseContinuationTokenLimitInKb` (.NET) или `continuation_token_limit` (Python). OFFSET и LIMIT дешевле для перехода к произвольной странице короткого результата, но для глубокой пагинации дороже, так как пропущенные элементы все равно обрабатываются.

### 7. Упражнение: создание и постраничный вывод запросов
URL: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/7-exercise-author-page-queries

Практика на примере каталога CosmicWorks: параметры, проекции, подзапросы, кросс-продукты и постраничность с измерением RU (C# или Python). Нужна подписка Azure.

### 8. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/8-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 9. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/9-summary

Построен слой чтения API каталога: запросы возвращают данные нужной структуры, работают с вложенными данными, и используется постраничный вывод. Постраничность экономит RU, так как не читаются результаты, которые пользователь не увидит.

## Важные команды / код / настройки

Параметризованный запрос с проекцией (.NET):

```csharp
QueryDefinition query = new QueryDefinition(
        "SELECT p.name, p.price FROM product p WHERE p.categoryId = @category AND p.price <= @max")
    .WithParameter("@category", categoryId)
    .WithParameter("@max", maxPrice);
```

Параметризованный запрос (Python):

```python
query = "SELECT p.name, p.price FROM product p WHERE p.categoryId = @category AND p.price <= @max"
parameters = [
    {"name": "@category", "value": category_id},
    {"name": "@max", "value": max_price},
]
```

Проекция с алиасами и объектом:

```sql
SELECT
    p.name,
    p.categoryName AS category,
    { "price": p.price } AS scannerData
FROM product p
WHERE p.categoryId = @category
```

Список категорий без обертки:

```sql
SELECT DISTINCT VALUE p.categoryName FROM product p
```

EXISTS для фильтрации по элементам массива:

```sql
SELECT p.id, p.name
FROM product p
WHERE EXISTS (
    SELECT VALUE t
    FROM t IN p.tags
    WHERE t.name = @tag
)
```

Проекция массива через ARRAY:

```sql
SELECT
    p.id,
    p.name,
    ARRAY(
        SELECT VALUE t.name
        FROM t IN p.tags
    ) AS tagNames
FROM product p
WHERE p.categoryId = @category
```

Скалярный подзапрос:

```sql
SELECT
    p.name,
    (SELECT VALUE COUNT(1) FROM t IN p.tags) AS tagCount
FROM product p
WHERE p.categoryId = @category
```

JOIN как self-join по массиву тегов:

```sql
SELECT
    p.name,
    t.name AS tag
FROM product p
JOIN t IN p.tags
```

JOIN с предварительной фильтрацией элементов массива:

```sql
SELECT p.name, t.name AS tag
FROM product p
JOIN (SELECT VALUE t FROM t IN p.tags WHERE t.name = @tag) AS t
WHERE p.categoryId = @category
```

Постраничный вывод в .NET с MaxItemCount и продолжением по токену:

```csharp
QueryRequestOptions options = new()
{
    PartitionKey = new PartitionKey(categoryId),
    MaxItemCount = 20
};
using FeedIterator<Product> iterator =
    container.GetItemQueryIterator<Product>(query, continuationToken, options);
FeedResponse<Product> page = await iterator.ReadNextAsync();
return (page.ToList(), page.ContinuationToken);
```

Постраничный вывод в Python:

```python
pager = results.by_page(continuation_token)
page = list(next(pager))
return page, pager.continuation_token
```

## Что запомнить

- Параметризуйте все внешние значения; параметры не подходят для имен свойств и алиасов.
- Отсутствующие свойства тихо отфильтровываются, а типы не приводятся; проверяйте их функциями IS_*.
- Функции в WHERE (например, LOWER) могут отключить использование индекса; функции в SELECT этого не делают.
- EXISTS возвращает элемент один раз, JOIN даёт строку на каждый элемент массива и не возвращает элементы с пустым массивом.
- Для постраничного вывода используйте continuation token; не считайте конец результатов по размеру страницы.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-nosql/
- Query language reference for Azure Cosmos DB for NoSQL; Subqueries in Azure Cosmos DB for NoSQL; Self-joins in Azure Cosmos DB for NoSQL; Pagination in Azure Cosmos DB for NoSQL; Parameterized queries in Azure Cosmos DB for NoSQL; Query items in Azure Cosmos DB for NoSQL using .NET; Get started with Azure Cosmos DB for NoSQL using Python (названия из источника, URL не приведены)
