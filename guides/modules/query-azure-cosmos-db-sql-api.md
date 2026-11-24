# Запросы к Azure Cosmos DB для NoSQL с помощью SQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/

## Цель модуля

Научиться создавать и выполнять SQL-запросы к JSON-документам в Azure Cosmos DB для NoSQL, формировать (проецировать) результаты в нужную структуру, проверять типы свойств и использовать встроенные функции, а также выполнять запросы через SDK.

## Ключевые понятия

- **SQL-запрос Cosmos DB для NoSQL** - SQL-подобный язык для JSON-документов; источник в `FROM` выступает как переменная-псевдоним.
- **Проекция** - формирование результата в нужной JSON-структуре: переименование через `AS`, вложенные объекты `{ ... } AS поле`.
- **DISTINCT** - возвращает только уникальные значения.
- **VALUE** - возвращает скалярные значения или массив простых значений вместо объектов.
- **Проверки типов** - `IS_DEFINED`, `IS_ARRAY`, `IS_NULL`, `IS_NUMBER`, `IS_STRING`, `IS_OBJECT`, `IS_BOOLEAN`.
- **Встроенные функции** - например, `CONCAT`, `LOWER`, `GetCurrentDateTime()`.
- **QueryIterator / query_items** - механизм выполнения запроса в SDK с автоматической пагинацией.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/1-introduction

Cosmos DB для NoSQL поддерживает SQL как JSON-язык запросов. Цели: создавать и выполнять запрос, проецировать результаты, использовать встроенные функции.

### 2. Понимание языка запросов NoSQL
Источник: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/2-understand-sql-query-language

Модуль работает с условным контейнером товаров: `id`, `categoryId` (partition key), `categoryName`, `sku`, `name`, `description`, `price` (число) и `tags` (массив объектов с `id` и `name`).

### 3. Создание запросов с NoSQL
Источник: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/3-create-queries-sql

- Базовая структура: `SELECT` (звёздочка или список полей), `FROM` (контейнер), опционально `WHERE`.
- Псевдоним источника можно выбрать произвольно (например, `p`), он служит переменной для обращения к свойствам.
- Фильтр примера: цена от 50 до 100 через `p.price >= 50 AND p.price <= 100`.

### 4. Проецирование результатов запроса
Источник: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/4-project-query-results

- Переименование: `p.categoryName AS category`.
- Вложенный объект: `{ "price": p.price } AS scannerData` создаёт дочерний объект.
- `SELECT DISTINCT p.categoryName` убирает повторы.
- `SELECT VALUE p.categoryName` (можно с `DISTINCT`) возвращает массив простых значений вместо объектов, что удобно для клиентских типов.

### 5. Проверка типов в запросах
Источник: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/5-implement-type-checking-queries

- Элементы могут не содержать свойство `tags`, или содержать его не в виде массива (например, строку).
- `IS_DEFINED(p.tags)` - проверяет наличие свойства (возвращает false, если его нет).
- `IS_ARRAY(p.tags)` - проверяет, что свойство является массивом.
- `IS_NULL(p.tags)` - проверяет на null.
- `IS_NUMBER(p.price)` в `WHERE` отбирает только числовые цены; `IS_STRING(p.price)` - строковые.
- Также есть `IS_OBJECT` и `IS_BOOLEAN`.

### 6. Использование встроенных функций
Источник: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/6-use-built-functions

- `CONCAT(p.name, ' | ', p.categoryName)` - объединение строк.
- `LOWER(p.sku)` - приведение к нижнему регистру.
- `GetCurrentDateTime()` в `WHERE` - фильтр по текущей дате (пример: `p.retirementDate >= GetCurrentDateTime()`).
- Примеры не являются полным списком функций.

### 7. Выполнение запросов через SDK
Источник: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/7-execute-queries-sdk

- .NET: `QueryDefinition` с текстом запроса, `GetItemQueryIterator<T>` и цикл `while (feedIterator.HasMoreResults)` с `ReadNextAsync()`.
- Python: строка запроса передаётся в `container.query_items(query=..., enable_cross_partition_query=True)`; результаты итерируются в цикле.
- JavaScript: `container.items.query(query, { enableCrossPartitionQuery: true })`, итерация через `hasMoreResults()` и `fetchNext()`.

### 8. Упражнение: выполнение запроса через SDK
Источник: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/8-exercise-execute-sdk

Упражнение (около 15 минут) в лабораторной среде: группа ресурсов, провайдеры ресурсов, Azure Cosmos DB и локальное окружение. Подробных шагов в исходниках нет.

### 9. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/9-knowledge-check

В исходных материалах вопросы не приведены.

### 10. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/10-summary

Модуль научил создавать запросы, проецировать поля в JSON-результаты и использовать встроенные функции в фильтрах и полях.

## Важные команды / код / настройки

Базовый запрос с фильтром:

```
SELECT
    p.name,
    p.categoryName,
    p.price
FROM
    products p
WHERE
    p.price >= 50 AND
    p.price <= 100
```

Проекция с переименованием и вложенным объектом:

```
SELECT
    p.name,
    p.categoryName AS category,
    { "price": p.price } AS scannerData
FROM
    products p
WHERE
    p.price >= 50 AND
    p.price <= 100
```

Уникальные значения одним массивом:

```
SELECT DISTINCT VALUE
    p.categoryName
FROM
    products p
```

Проверка типа:

```
SELECT
    IS_DEFINED(p.tags) AS tags_exist
FROM
    products p
```

Выполнение в Python:

```
query = "SELECT * FROM products p"
for item in container.query_items(
    query=query,
    enable_cross_partition_query=True):
    print(f"{item['id']}\t{item['name']}\t{item['price']}")
```

Выполнение в JavaScript:

```
const iterator = container.items.query(
    query,
    { enableCrossPartitionQuery: true }
);

while (iterator.hasMoreResults()) {
    const { resources } = await iterator.fetchNext();
    for (const item of resources) {
        console.log(`[${item.id}]	${item.name.padEnd(35)}	${item.price.toFixed(2)}`);
    }
}
```

Настройка: `enable_cross_partition_query=True` (Python) и `enableCrossPartitionQuery: true` (JavaScript) нужны для запросов по нескольким партициям.

## Что запомнить

- Псевдоним в `FROM` - это переменная; выбирайте короткое, понятное имя.
- `AS` переименовывает поля, `{ ... } AS имя` создаёт вложенный объект, `SELECT VALUE` возвращает плоский массив.
- `DISTINCT` убирает дубликаты, `VALUE` упрощает работу клиента с простыми типами.
- Проверяйте типы через `IS_DEFINED`, `IS_ARRAY`, `IS_NULL`, `IS_NUMBER`, `IS_STRING` - в гибких данных свойства могут отсутствовать или иметь другой тип.
- Для запросов по нескольким партициям в SDK включайте cross-partition опцию.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/query-azure-cosmos-db-sql-api/
- Getting started with SQL queries; System functions (Azure Cosmos DB) (ссылки из урока 10)
