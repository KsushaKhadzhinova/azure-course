# Определение индексов в Azure Cosmos DB для SQL API (NoSQL)

**Источник:** https://learn.microsoft.com/en-us/training/modules/define-indexes-azure-cosmos-db-sql-api/

## Цель модуля

Понять, как Azure Cosmos DB для NoSQL индексирует JSON-элементы по умолчанию, что такое индекс и политика индексирования, и какие типы путей и операторов используются при описании политики.

## Ключевые понятия

- **Индекс** - инвертированный индекс, который объединяет деревья путей всех элементов контейнера; позволяет быстро находить совпадения без перебора элементов.
- **Indexing policy (политика индексирования)** - набор правил include/exclude путей, которые определяют, какие свойства индексируются; задаётся в JSON.
- **Indexing mode** - `consistent` (индекс обновляется синхронно при операциях) или `none` (индексирование отключено).
- **Automatic** - автоматическое индексирование элементов при записи.
- **Included / excluded paths** - включаемые и исключаемые пути индексирования.
- **Операторы путей** - `?` (скалярное значение, конец пути), `[]` (массив без индекса), `*` (wildcard, любой элемент дальше по пути).
- **Range indexes** - индексы по диапазонам для строк и чисел (используются по умолчанию).

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/define-indexes-azure-cosmos-db-sql-api/1-introduction

По умолчанию Cosmos DB индексирует все пути элементов, что удобно при разработке нового приложения. Цели: описать индекс и политику индексирования и определить типы данных политики.

### 2. Понимание индексов
Источник: https://learn.microsoft.com/en-us/training/modules/define-indexes-azure-cosmos-db-sql-api/2-understand-indexes

- Политика по умолчанию: операции create, update и delete обновляют индекс, и индексируются все свойства каждого элемента.
- Индекс можно представить как объединение деревьев всех элементов; каждый узел хранит метаданные о том, какие элементы ему соответствуют.
- Пример: запрос `SELECT * FROM products p WHERE p.sku = 'BK-M38S-38'` обходит инвертированный индекс от корня к свойству `sku` и находит один элемент, вместо перебора всех элементов.

### 3. Понимание политик индексирования
Источник: https://learn.microsoft.com/en-us/training/modules/define-indexes-azure-cosmos-db-sql-api/3-understand-indexing-policies

- Политика по умолчанию: `indexingMode` = consistent; `automatic` = true; `includedPaths` = `/*`; `excludedPaths` = путь `_etag`.
- **Consistent** - индекс обновляется синхронно; стандартный выбор.
- **None** - индексирование отключено; применяется при массовых операциях (отключить на время, затем вернуть consistent) или когда контейнер используется только как key-value хранилище с point read.
- Операторы путей: `?` (скаляр), `[]` (массив), `*` (всё, что ниже). Примеры: `/*` - все свойства; `/name/?` - скалярное значение name; `/category/*` - все свойства category; `/metadata/sku/?`; `/tags/[]/name/?`.

### 4. Стратегии политики индексирования
Источник: https://learn.microsoft.com/en-us/training/modules/define-indexes-azure-cosmos-db-sql-api/4-review-indexing-policy-strategies

- Конфликты include и exclude разрешаются в пользу более точного пути. Пример: exclude `/category/*` и include `/category/name/?` - индексируется только `category.name`.
- Корневой путь `/*` должен быть включён или исключён.
- Стратегия 1 (рекомендуется): включить всё (`/*`) и исключить лишнее. Такая политика продолжает работать при изменении схемы.
- Стратегия 2: исключить всё (`/*`) и выборочно включить нужные пути (например, `/name/?` и `/tags/[]/name/?`).

### 5. Упражнение: просмотр политики индексирования по умолчанию в портале
Источник: https://learn.microsoft.com/en-us/training/modules/define-indexes-azure-cosmos-db-sql-api/5-exercise-review-default-index-policy-for-container-portal

Упражнение (около 15 минут) в лабораторной среде: создать группу ресурсов, подготовить окружение, включить провайдеры ресурсов. Подробных шагов в исходниках нет.

### 6. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/define-indexes-azure-cosmos-db-sql-api/6-knowledge-check

В исходных материалах вопросы не приведены.

### 7. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/define-indexes-azure-cosmos-db-sql-api/7-summary

Модуль разобрал механизм индексов и политик, политику по умолчанию и её влияние на запросы. Ключевые навыки: связь индекса и политики, типы политик индексирования.

## Важные команды / код / настройки

Политика индексирования по умолчанию (JSON):

```
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    {
      "path": "/*"
    }
  ],
  "excludedPaths": [
    {
      "path": "/\"_etag\"/?"
    }
  ]
}
```

Стратегия «исключить всё, включить выборочно» (из урока 4):

```
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    {
      "path": "/name/?"
    },
    {
      "path": "/tags/[]/name/?"
    }
  ],
  "excludedPaths": [
    {
      "path": "/*"
    }
  ]
}
```

Настройки: `indexingMode` - `consistent` или `none`; `automatic` - `true`/`false`; путь `_etag` исключён по умолчанию.

## Что запомнить

- Индекс по умолчанию покрывает все свойства всех элементов, поэтому запросы работают сразу без настройки.
- Политика индексирования - это набор include/exclude путей в JSON; при конфликте побеждает более точный путь.
- Предпочтительна стратегия «включить всё, исключить лишнее»: она устойчива к изменениям схемы.
- Режим `none` подходит для массовых загрузок (временно) и для key-value сценариев только с point read.
- Пути описываются операторами `?` (скаляр), `[]` (массив), `*` (всё ниже).

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/define-indexes-azure-cosmos-db-sql-api/
- Indexing policies in Azure Cosmos DB (ссылка из урока 7)
