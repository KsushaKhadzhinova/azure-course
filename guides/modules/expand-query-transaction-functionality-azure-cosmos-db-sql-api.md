# Расширение функциональности запросов и транзакций в Azure Cosmos DB для SQL API

**Источник:** https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/

## Цель модуля

Научиться писать на JavaScript пользовательские функции (UDF), которые расширяют язык запросов, и триггеры (pre- и post-triggers), которые встраивают логику до и после операций с элементами; создавать их через SDK и подключать к операциям.

## Ключевые понятия

- **UDF (user-defined function)** - JavaScript-функция, которая принимает скалярные входы и возвращает скалярное значение; вызывается только внутри запроса через `udf.<имя>()`.
- **Ограничение UDF** - UDF не имеет доступа к объекту context и предназначена только для вычислений.
- **Триггер (trigger)** - ресурс контейнера с кодом на JavaScript, который выполняется при операции только если явно указан в опциях запроса.
- **Pre-trigger** - выполняется до операции, не принимает входных параметров; может валидировать или дополнять элемент.
- **Post-trigger** - выполняется после операции; может создавать или обновлять связанные элементы; создаваемые элементы должны иметь тот же логический partition key, что и исходный.
- **getContext()** - объект контекста, через который доступны `getRequest()`, `getResponse()` и `getCollection()`.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/1-introduction

Cosmos DB поддерживает транзакционное выполнение JavaScript. В NoSQL API можно писать триггеры и UDF. Цели: создать UDF и триггеры.

### 2. Создание пользовательских функций (UDF)
Источник: https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/2-create-user-defined-functions

- UDF расширяет грамматику запроса и добавляет небольшую бизнес-логику в запрос.
- Пример: добавить налог 15 % к цене товара и вывести поле `priceWithTax`.
- UDF вызывается в запросе синтаксисом `udf.addTax(p.price) AS priceWithTax`.

### 3. Создание UDF через SDK
Источник: https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/3-create-user-defined-functions-sdk

Код UDF хранится в строке (или читается из файла `*.js`), создаётся объект `UserDefinedFunctionProperties` с `Id` и `Body`, затем вызывается `container.Scripts.CreateUserDefinedFunctionAsync(properties)`.

### 4. Добавление триггеров к операции
Источник: https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/4-add-triggers-operation

- Pre-trigger пример: если в элементе нет свойства `label`, добавить `label = "new"`, затем `request.setBody(...)`.
- Post-trigger пример: после создания элемента создать второй элемент-представление с полями `sourceId`, `categoryId`, `displayName` (`"<name> [<categoryName>]"`) через `container.createDocument`. Ошибка в callback выбрасывается через `throw`.
- Контекст: `getRequest()` для pre-trigger, `getResponse()` для post-trigger, `getCollection()` для доступа к контейнеру.

### 5. Создание и использование триггеров через SDK
Источник: https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/5-create-use-triggers-sdk

- Создание: `container.Scripts.CreateTriggerAsync(properties)` с `TriggerProperties` (`Id`, `Body`, `TriggerOperation.Create`, `TriggerType.Pre` или `TriggerType.Post`).
- Использование: в `ItemRequestOptions` заполняются списки `PreTriggers` и `PostTriggers` по именам триггеров. Триггеры не выполняются автоматически - их нужно указывать для каждой операции.
- Результат примера: pre-trigger добавил `label: "new"` в исходный элемент; post-trigger создал второй элемент с `sourceId` и `displayName`.

### 6. Упражнение: реализация и использование UDF через SDK
Источник: https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/6-exercise-implement-use-user-defined-functions-with-the-sdk

Упражнение (около 15 минут) в лабораторной среде; подробных шагов в исходниках нет.

### 7. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/7-knowledge-check

В исходных материалах вопросы не приведены.

### 8. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/8-summary

Создана UDF, которая используется в SQL-запросе, и созданы pre- и post-триггеры, выполняемые при point-операции.

## Важные команды / код / настройки

UDF (JavaScript):

```
function addTax(preTax) {
    return preTax * 1.15;
}
```

Запрос с UDF:

```
SELECT
    p.name,
    p.price,
    udf.addTax(p.price) AS priceWithTax
FROM
    products p
```

Создание UDF (C#):

```
UserDefinedFunctionProperties properties = new()
{
    Id = "addTax",
    Body = udf
};

await container.Scripts.CreateUserDefinedFunctionAsync(properties);
```

Pre-trigger (JavaScript):

```
function addLabel() {
    var context = getContext();
    var request = context.getRequest();

    var pendingItem = request.getBody();

    if (!('label' in pendingItem))
        pendingItem['label'] = 'new';

    request.setBody(pendingItem);
}
```

Создание триггера (C#):

```
TriggerProperties properties = new()
{
    Id = "addLabel",
    Body = preTrigger,
    TriggerOperation = TriggerOperation.Create,
    TriggerType = TriggerType.Pre
};

await container.Scripts.CreateTriggerAsync(properties);
```

Подключение триггеров к операции (C#):

```
ItemRequestOptions options = new()
{
    PreTriggers = new List<string> { "addLabel" },
    PostTriggers = new List<string> { "createView" }
};

await container.CreateItemAsync(newItem, requestOptions: options);
```

Post-trigger (JavaScript; полный код в уроке 4 и 5):

```
function createView() {
    var context = getContext();
    var container = context.getCollection();
    var response = context.getResponse();

    var createdItem = response.getBody();

    var viewItem = {
        sourceId: createdItem.id,
        categoryId: createdItem.categoryId,
        displayName: `${createdItem.name} [${createdItem.categoryName}]`
    };

    var accepted = container.createDocument(
        container.getSelfLink(),
        viewItem,
        (error, newItem) => {
            if (error) throw error;
        }
    );
    if (!accepted) return;
}
```

## Что запомнить

- UDF вызывается только внутри запроса через `udf.<имя>()`, работает как вычисление без доступа к context.
- Pre-trigger не принимает параметры и подходит для валидации или дополнения элемента до записи.
- Post-trigger выполняется после операции; создаваемые им элементы должны иметь тот же логический partition key.
- Триггеры не выполняются автоматически: их нужно указывать в `PreTriggers` и `PostTriggers` для каждой операции.
- Триггеры и UDF создаются через `container.Scripts` в .NET SDK.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/
- How to write stored procedures, triggers, and user-defined functions in Azure Cosmos DB; User-defined functions (UDFs) in Azure Cosmos DB (ссылки из урока 8)
