# Настройка индексов в Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/customize-indexes-azure-cosmos-db-sql-api/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/customize-indexes-azure-cosmos-db-sql-api/<юнит>`)

## Цель модуля

Научиться создавать пользовательскую политику индексирования (indexing policy) в Azure Cosmos DB for NoSQL и оценивать, подходит ли составной индекс (composite index) для решения.

## Ключевые понятия

- **Indexing policy (политика индексирования)** — набор правил, определяющих, какие пути (paths) документа индексируются; задается на уровне контейнера.
- **Indexing mode `consistent` / `automatic`** — режим индексирования и флаг автоматического индексирования, которые задаются в политике.
- **includedPaths / excludedPaths** — пути, которые включаются в индекс или исключаются из него. Например, `/*` исключает все пути.
- **Composite index (составной индекс)** — индекс по нескольким свойствам в заданном порядке; нужен для запросов с несколькими фильтрами или сортировкой по нескольким полям.
- **Ориентир порядка** — в запросе с фильтрами равенства и диапазона лучше, чтобы диапазонный фильтр стоял последним; для `ORDER BY` порядок свойств в индексе должен точно совпадать с порядком в запросе.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/customize-indexes-azure-cosmos-db-sql-api/1-introduction
По мере роста приложения индексную политику можно подстроить под потребности решения. Цели модуля: настроить пользовательскую политику индексирования и оценить, нужен ли составной индекс.

### 2. Customize the indexing policy
Источник: https://learn.microsoft.com/en-us/training/modules/customize-indexes-azure-cosmos-db-sql-api/2-customize-indexing-policy
При большой пропускной способности имеет смысл индексировать только нужные пути, чтобы уменьшить задержку и RU-стоимость операций создания и изменения элементов. В примере индексируются только `/name/?` и `/categoryName/?`. Показаны JSON-политика и эквивалент в .NET SDK (класс `IndexingPolicy`, `ContainerProperties`, метод `CreateContainerIfNotExistsAsync`). В примере всё исключается для наглядности; в общем случае лучше включать все пути по умолчанию и исключать отдельные.

### 3. Evaluate composite indexes
Источник: https://learn.microsoft.com/en-us/training/modules/customize-indexes-azure-cosmos-db-sql-api/3-evaluate-composite-indexes
Составной индекс объединяет два пути в заданном порядке. Для запроса с фильтром равенства по `name` и диапазоном по `price` подходит индекс, где диапазонное свойство стоит последним. Для `ORDER BY p.price ASC, p.name ASC` индекс должен точно повторять порядок свойств. Составные индексы описываются массивом `compositeIndexes`; можно определить несколько.

### 4. Exercise: Configure an Azure Cosmos DB for NoSQL container's index policy with the portal
Источник: https://learn.microsoft.com/en-us/training/modules/customize-indexes-azure-cosmos-db-sql-api/4-exercise-configure-containers-index-policy-portal
Практика (около 15 минут) в портале: настройка индексной политики контейнера. Нужна подписка Azure с правами администратора; создаются группа ресурсов, локальное окружение и включаются resource providers.

### 5. Knowledge check
Источник: https://learn.microsoft.com/en-us/training/modules/customize-indexes-azure-cosmos-db-sql-api/5-knowledge-check
Проверка знаний (в исходнике текст отсутствует).

### 6. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/customize-indexes-azure-cosmos-db-sql-api/6-summary
Модуль показал, как изменять содержимое индексной политики и управлять ею.

## Важные команды / код / настройки

Политика индексирования, индексирующая только `/name/?` и `/categoryName/?`:

```json
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    {
      "path": "/name/?"
    },
    {
      "path": "/categoryName/?"
    }
  ],
  "excludedPaths": [
    {
      "path": "/*"
    }
  ]
}
```

Создание контейнера с пользовательской политикой в .NET SDK:

```csharp
IndexingPolicy policy = new ()
{
    IndexingMode = IndexingMode.Consistent,
    Automatic = true
};

policy.ExcludedPaths.Add(
    new ExcludedPath{ Path = "/*" }
);

policy.IncludedPaths.Add(
    new IncludedPath{ Path = "/name/?" }
);
policy.IncludedPaths.Add(
    new IncludedPath{ Path = "/categoryName/?" }
);

ContainerProperties options = new ()
{
    Id = "products",
    PartitionKeyPath = "/categoryId",
    IndexingPolicy = policy
};
Container container = await database.CreateContainerIfNotExistsAsync(options, throughput: 400);
```

Запрос, для которого нужен составной индекс (фильтр по равенству и диапазону):

```sql
SELECT * FROM products p WHERE p.name = "Road Saddle" AND p.price > 50
```

Запрос с сортировкой по нескольким свойствам:

```sql
SELECT * FROM products p ORDER BY p.price ASC, p.name ASC
```

Составной индекс `(name ASC, price DESC)` в JSON:

```json
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
      "path": "/_etag/?"
    }
  ],
  "compositeIndexes": [
    [
      {
        "path": "/name",
        "order": "ascending"
      },
      {
        "path": "/price",
        "order": "descending"
      }
    ]
  ]
}
```

## Что запомнить

- Индексная политика задается на уровне контейнера; по умолчанию разумнее включать все пути и исключать лишние.
- Исключение `/*` всех путей — только для демонстрации; в продукции так обычно не делают.
- В SDK класс `IndexingPolicy` соответствует JSON-политике, `ContainerProperties` передается в `CreateContainerIfNotExistsAsync`.
- Составной индекс нужен для запросов с несколькими фильтрами и для `ORDER BY` по нескольким полям.
- Для фильтров равенства и диапазона диапазонное свойство в составном индексе ставится последним; порядок `ORDER BY` должен точно совпадать с индексом.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/customize-indexes-azure-cosmos-db-sql-api/
- Документация: Indexing policies in Azure Cosmos DB (упоминается в уроке 6).
- Документация: Manage indexing policies in Azure Cosmos DB (упоминается в уроке 6).
- Связанный модуль: Design and optimize an indexing strategy (`design-optimize-indexing-strategy-azure-cosmos-db-nosql`).
