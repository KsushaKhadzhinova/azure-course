# Транзакции с несколькими элементами в Azure Cosmos DB (SQL API)

**Источник:** https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/

## Цель модуля

Научиться писать хранимые процедуры на JavaScript, которые выполняют несколько операций как одну логическую единицу работы прямо внутри движка базы данных, и откатывать такие транзакции при ошибке.

## Ключевые понятия

- **Транзакция (transaction)** - последовательность операций, объединенных в одну единицу работы с гарантиями ACID (атомарность, согласованность, изолированность, долговечность).
- **Хранимая процедура (stored procedure)** - функция на JavaScript, зарегистрированная в контейнере и выполняемая на стороне сервера; все ее операции образуют одну транзакцию.
- **Область видимости партиции (logical partition scope)** - хранимая процедура работает в пределах одного значения ключа логической партиции; операции над несколькими значениями ключа в одной процедуре выполнить нельзя.
- **Контекст (getContext)** - объект, через который функция получает доступ к ответу HTTP (`getResponse()`) и к контейнеру (`getCollection()`).
- **Ограничение по времени** - операции внутри процедуры должны завершиться в пределах таймаута серверного запроса; для длинных списков используется логический флаг и возврат указателя для продолжения.
- **Откат (rollback)** - если из скрипта выброшено исключение, вся транзакция откатывается.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/1-introduction

Модуль посвящен написанию JavaScript-хранимых процедур для NoSQL API в Azure Cosmos DB, которые выполняют несколько операций как единое целое. После модуля нужно уметь писать хранимые процедуры и откатывать транзакции.

### 2. Понимание транзакций в контексте JavaScript SDK
URL: https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/2-understand-transactions

Транзакция должна обеспечивать ACID. В Azure Cosmos DB для NoSQL хранимая процедура выполняет одну или несколько операций как одну единицу работы в пределах одного контейнера. Процедуры привязаны к одной логической партиции. Транзакции выполняются на сервере и должны уложиться в серверный таймаут. Для длинных списков операций каждая функция, выполняющая операцию, возвращает логическое значение: если оно `true`, процедура может продолжать работу; если `false`, ее нужно завершить как можно быстрее, обычно вернув указатель, с которого следующий вызов продолжит работу.

### 3. Написание хранимых процедур
URL: https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/3-author-stored-procedures

Транзакция определяется как JavaScript-функция, которая выполняется при вызове процедуры. Внутри функции `getContext()` возвращает контекст, с помощью которого можно получить ответ (`getResponse()`) или контейнер (`getCollection()`). Модуль показывает, как доработать процедуру создания товара: сохранить логическое значение, которое возвращает `createDocument`, и передать третьим параметром callback для обработки ошибок и установки ответа. Сокращение `__` (два подчеркивания) эквивалентно `getContext().getCollection()`.

### 4. Откат транзакций
URL: https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/4-rollback-transactions

Все операции внутри JavaScript-функции автоматически оборачиваются в одну транзакцию. Если функция завершилась без исключения, изменения фиксируются; если выброшено исключение, вся транзакция откатывается. Начало функции соответствует `BEGIN TRANSACTION`, конец - `COMMIT TRANSACTION`, а ошибка - `ROLLBACK TRANSACTION`. Ошибку из callback можно повторно выбросить, чтобы прервать выполнение и откатить процедуру.

### 5. Создание хранимых процедур с помощью JavaScript SDK
URL: https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/5-create-stored-procedures-sdk

В примере используется .NET SDK: текст процедуры хранится в строке (или читается из `*.js` файла), создается объект `StoredProcedureProperties` с `Id` и `Body`, после чего вызывается `CreateStoredProcedureAsync` у свойства `Scripts` контейнера. Метод возвращает `StoredProcedureResponse` с метаданными созданной процедуры.

### 6. Упражнение: создание хранимой процедуры в портале Azure
URL: https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/6-exercise-create-stored-procedure-azure-portal

Практическое задание (около 15 минут) на создание хранимой процедуры через портал Azure. Для него нужна подписка Azure с административным доступом: создать группу ресурсов, настроить локальную среду и включить провайдеры ресурсов. Текст урока не содержит дополнительных шагов сверх запуска упражнения.

### 7. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/7-knowledge-check

Контрольные вопросы модуля (около 5 минут). Содержание вопросов в источнике не приведено.

### 8. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/8-summary

Создание хранимой процедуры через портал или .NET SDK; откат транзакции в процедуре путем выброса ошибки.

## Важные команды / код / настройки

Минимальная процедура, возвращающая строку:

```javascript
function greet() {
    var context = getContext();
    var response = context.getResponse();
    response.setBody("Hello, Learn!");
}
```

Процедура создания документа с обработкой ошибок и проверкой серверного таймаута:

```javascript
function createProduct(item) {
    var context = getContext();
    var container = context.getCollection();
    var accepted = container.createDocument(
        container.getSelfLink(),
        item,
        (error, newItem) => {
            if (error) throw error;
            context.getResponse().setBody(newItem)
        }
    );
    if (!accepted) return;
}
```

Откат транзакции через выброс ошибки:

```javascript
throw new Error('Something');
```

Создание процедуры в .NET SDK:

```csharp
string sproc = @"function greet() {
    var context = getContext();
    var response = context.getResponse();
    response.setBody('Hello, Learn!');
}";

StoredProcedureProperties properties = new()
{
    Id = "greet",
    Body = sproc
};

await container.Scripts.CreateStoredProcedureAsync(properties);
```

## Что запомнить

- Хранимая процедура выполняет несколько операций как одну транзакцию, с гарантиями ACID в пределах одного контейнера.
- Процедура работает только в пределах одного значения ключа логической партиции.
- Выброс любого исключения в JavaScript откатывает всю транзакцию.
- Для длинных операций проверяйте логическое значение, возвращаемое операциями, и при `false` завершайте процедуру, возможно вернув указатель.
- Процедуры создаются через портал Azure или .NET SDK (`Scripts.CreateStoredProcedureAsync`).

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/
- How to write stored procedures, triggers, and user-defined functions in Azure Cosmos DB (упомянуто в источнике, URL не приведен)
- How to write stored procedures and triggers in Azure Cosmos DB by using the JavaScript query API (упомянуто в источнике, URL не приведен)
