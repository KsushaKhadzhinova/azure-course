# Измерение и настройка индексов в Azure Cosmos DB для SQL API

**Источник:** https://learn.microsoft.com/en-us/training/modules/measure-index-azure-cosmos-db-sql-api/

## Цель модуля

Научиться измерять стоимость запросов и операций в RU/s с помощью классов опций .NET SDK, включать метрики индексирования и на их основе подбирать политику индексирования (в том числе составные индексы) под конкретные запросы.

## Ключевые понятия

- **Index metrics (метрики индексирования)** - opt-in метрики, которые показывают, как текущий индекс влияет на фильтры запроса и рекомендуют одиночные или составные индексы.
- **QueryRequestOptions** - класс опций запроса в .NET SDK; используется для `PopulateIndexMetrics` и `MaxItemCount`.
- **Index Impact Score** - оценка влияния индекса на запрос (например, High).
- **Utilized / Potential Single Indexes** - использованные и рекомендуемые одиночные индексы.
- **Composite index (составной индекс)** - индекс по нескольким путям с порядком сортировки (ascending/descending).
- **RequestCharge (RU/s)** - стоимость страницы запроса или отдельной операции.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/measure-index-azure-cosmos-db-sql-api/1-introduction

Модуль использует классы опций .NET SDK для отслеживания метаданных запросов и операций. Цели: настроить политику индексирования под запросы и измерить стоимость запроса или операции.

### 2. Включение метрик индексирования
Источник: https://learn.microsoft.com/en-us/training/modules/measure-index-azure-cosmos-db-sql-api/2-enable-indexing-metrics

- Метрики индексирования по умолчанию отключены; включайте их при диагностике производительности или если не знаете, как менять политику.
- Чтобы включить, создаётся `QueryRequestOptions` с `PopulateIndexMetrics = true`, которая передаётся в `GetItemQueryIterator<>`.
- Метрики доступны в свойстве `IndexMetrics` объекта `FeedResponse<>` каждой страницы.

### 3. Анализ результатов метрик индексирования
Источник: https://learn.microsoft.com/en-us/training/modules/measure-index-azure-cosmos-db-sql-api/3-analyze-indexing-metrics-results

Разбор трёх запросов при политике по умолчанию (consistent, все пути, без составных индексов):
- `WHERE p.price > 500` - влияние `/price/?` высокое; дополнительные индексы не рекомендуются, так как путь уже покрыт.
- `WHERE p.price > 500 AND startsWith(p.name, 'Touring')` - высокое влияние `/price/?` и `/name/?`; оба покрыты по умолчанию.
- `WHERE p.price > 500 AND p.categoryName = 'Bikes, Touring Bikes'` - метрики рекомендуют составной индекс `/categoryName ASC, /price ASC`. После добавления составного индекса в политику метрики показывают его использование.

Пример политики с составным индексом (из урока):

```
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    {
      "path": "/*"
    }
  ],
  "excludedPaths": [],
  "compositeIndexes": [
    [
      {
        "path": "/categoryName",
        "order": "ascending"
      },
      {
        "path": "/price",
        "order": "ascending"
      }
    ]
  ]
}
```

### 4. Измерение стоимости запроса
Источник: https://learn.microsoft.com/en-us/training/modules/measure-index-azure-cosmos-db-sql-api/4-measure-query-cost

- `MaxItemCount` задаёт размер страницы (в примере 25).
- В цикле по страницам выводится `response.RequestCharge`, стоимость суммируется в `totalRUs`.
- В примере с `SELECT * FROM products` (демо-база из инструмента cosmicworks) страницы стоили около 2.82, 2.82, 2.83, 2.84 и 2.25 RU; итог - 13.56 RU.

### 5. Измерение стоимости операции записи
Источник: https://learn.microsoft.com/en-us/training/modules/measure-index-azure-cosmos-db-sql-api/5-measure-point-operation-cost

- Стоимость отдельной операции доступна в свойстве `RequestCharge` объекта `ItemResponse<>`; дополнительные опции не нужны.
- Свойство `Resource` возвращает созданный элемент, десериализованный в заданный тип.
- В примере создание элемента стоило около 7.05 RU.

### 6. Упражнение: оптимизация политики индексирования под конкретный запрос
Источник: https://learn.microsoft.com/en-us/training/modules/measure-index-azure-cosmos-db-sql-api/6-exercise-optimize-containers-index-policy-for-specific-query

Упражнение (около 15 минут) в лабораторной среде. Подробных шагов в исходниках нет.

### 7. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/measure-index-azure-cosmos-db-sql-api/7-knowledge-check

В исходных материалах вопросы не приведены.

### 8. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/measure-index-azure-cosmos-db-sql-api/8-summary

Модуль показал, как через .NET SDK читать метрики индексирования и RU-стоимость запросов и операций, и как корректировать политику индексирования по самым частым запросам.

## Важные команды / код / настройки

Включение метрик индексирования (C#):

```
QueryRequestOptions options = new()
{
    PopulateIndexMetrics = true
};

FeedIterator<Product> iterator = container.GetItemQueryIterator<Product>(query, requestOptions: options);
```

Вывод метрик по страницам:

```
Console.WriteLine(response.IndexMetrics);
```

Ограничение размера страницы и подсчёт RU (C#):

```
QueryRequestOptions options = new()
{
    MaxItemCount = 25
};

double totalRUs = 0;
// внутри цикла по страницам:
Console.WriteLine($"RUs:\t\t{response.RequestCharge:0.00}");
totalRUs += response.RequestCharge;
// после цикла:
Console.WriteLine($"Total RUs:\t{totalRUs:0.00}");
```

Стоимость операции создания (C#):

```
ItemResponse<Product> response = await container.CreateItemAsync<Product>(item);
Console.WriteLine($"RUs:\t{response.RequestCharge:0.00}");
```

Настройки: `PopulateIndexMetrics` по умолчанию `false`; составной индекс `/categoryName ASC, /price ASC` в `compositeIndexes`.

## Что запомнить

- `PopulateIndexMetrics = true` включает метрики индексирования; используйте их при диагностике, так как по умолчанию они выключены.
- Метрики показывают Index Impact Score и рекомендуют одиночные или составные индексы под фильтры запроса.
- Составной индекс добавляют в `compositeIndexes` политики; после обновления индекса метрики показывают его использование.
- `RequestCharge` в `FeedResponse<>` (по страницам) и в `ItemResponse<>` (для операций) показывает стоимость в RU.
- Сравнивайте RU до и после изменения политики, чтобы оценить эффект.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/measure-index-azure-cosmos-db-sql-api/
- Indexing in Azure Cosmos DB - Overview; Indexing policies in Azure Cosmos DB (ссылки из урока 8)
