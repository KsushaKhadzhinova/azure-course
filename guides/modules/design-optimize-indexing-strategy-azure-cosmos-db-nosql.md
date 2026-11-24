# Проектирование и оптимизация стратегии индексации в Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/<юнит>`)

## Цель модуля

Подобрать индексную политику под соотношение чтения и записи контейнера, добавить составные и пространственные индексы, вычисляемые свойства (computed properties) и глобальные вторичные индексы (global secondary indexes), а также измерить стоимость каждого изменения в request units (RU).

## Ключевые понятия

- **Indexing policy (индексная политика)** — JSON-документ контейнера: какие пути индексируются, какой тип индекса на каждом пути и включена ли индексация.
- **Indexing mode** — `consistent` (индекс обновляется синхронно), `none` (индексация выключена; TTL при этом недоступен).
- **Range index (диапазонный индекс)** — обслуживает равенство, диапазоны, IS_DEFINED, строковые функции, ORDER BY по одному свойству и JOIN; используется по умолчанию для строк и чисел.
- **Spatial index (пространственный индекс)** — ускоряет ST_DISTANCE, ST_WITHIN, ST_INTERSECTS; по умолчанию не создается.
- **Composite index (составной индекс)** — индекс по нескольким свойствам с порядком и направлением; обязателен для ORDER BY по двум и более свойствам.
- **Included / excluded paths** — включенные и исключенные пути; `/?` — скалярное значение, `/[]` — элементы массива, `/*` — всё поддерево. Более точный путь имеет приоритет.
- **Index transformation (трансформация индекса)** — выполняется онлайн при изменении политики и тратит RU с меньшим приоритетом.
- **Computed property (вычисляемое свойство)** — значение, выведенное запросом из других свойств элемента и не хранящееся в документе; можно индексировать (префикс `cp_` в примерах).
- **Global secondary index (глобальный вторичный индекс)** — доступный только для чтения контейнер с копией данных и другим partition key; синхронизируется через change feed и является eventually consistent.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/1-introduction
По умолчанию контейнер индексирует все свойства, что ускоряет запросы, но увеличивает стоимость каждой записи. Сценарий: каталог товаров партиционирован по `/categoryId`; ночная переоценка перерасходует RU, а поиск по SKU (не ключу партиционирования) идет по всем партициям. Модуль охватывает индексную политику, составные и пространственные индексы, вычисляемые свойства и глобальные вторичные индексы.

### 2. Understand indexing policies
Источник: https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/2-understand-indexing-policies
Свойства превращаются в пути (например, `/categoryName`); индекс — инвертированный, значения хранятся по возрастанию. Типы индексов: range, spatial, composite (плюс vector и full-text для поиска). По умолчанию `id` и `_ts` всегда индексируются при `consistent`; `_etag` исключен. Путь ключа партиционирования не индексируется автоматически, кроме `/id`, его нужно добавить явно (для иерархического ключа — каждый уровень). Порядок эффективности методов фильтрации: index seek (равенство, IN), precise index scan (`>`, `<`, `STARTSWITH`), expanded index scan (STARTSWITH и STRINGEQUALS без учета регистра), full index scan (`CONTAINS`, `ENDSWITH`, `RegexMatch`, `LIKE`), full scan (`UPPER`, `LOWER`). Агрегаты с одним только CONTAINS-фильтром могут требовать полного сканирования.

### 3. Configure indexing policies for workloads
Источник: https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/3-configure-indexing-policies-workloads
Политика opt-out (`/*` включен, ненужные пути исключены) — рекомендуемая отправная точка; opt-in (`/*` исключен, нужные пути включены) дает минимальный индекс. Для чтения индексируются пути из WHERE, ORDER BY и JOIN; для записи исключаются большие строки (например, `/description/?`), поддеревья (`/tags/*`) и часто меняющиеся свойства. Изменение политики запускает трансформацию индекса: удаление пути действует сразу, добавление — только после завершения трансформации. Несколько удалений лучше группировать в одно обновление. При замене индекса сначала добавляется новый, затем удаляется старый. Через SDK replace-контейнера не работает Microsoft Entra-аутентификация на data plane; для keyless-аккаунта политику применяют через Azure CLI, портал или management API. Прогресс трансформации читается из заголовка `x-ms-documentdb-collection-index-transformation-progress`.

### 4. Configure composite and spatial indexes
Источник: https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/4-configure-composite-spatial-indexes
Составные индексы по умолчанию не существуют. В путях композитного индекса `/?` подразумевается, wildcard `/*` не поддерживается, пути чувствительны к регистру, порядок имеет значение. Для ORDER BY по нескольким свойствам порядок путей должен совпадать с ORDER BY; индекс также работает при полном обращении порядка (все направления разом). Для фильтров: хотя бы один фильтр — равенство, равенства идут первыми, диапазон (`>`, `<`, `>=`, `<=`, `!=`) — последним; один композитный индекс оптимизирует не более одного диапазона. Все свойства индекса должны присутствовать в фильтре. Пространственный индекс задается для пути с корректным GeoJSON и типами Point, Polygon, MultiPolygon, LineString; несовместим с MongoDB 2dsphere.

### 5. Configure computed properties
Источник: https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/5-configure-computed-properties
Вычисляемое свойство определяется именем и запросом на уровне контейнера. Пример: `cp_primaryCategory` извлекает первую часть `categoryName` до запятой. Правила имени: уникальность в контейнере, путь `/<имя>` на верхнем уровне, нельзя использовать системные имена (`id`, `_rid`, `_ts`), нельзя совпадать с уже индексированным путем. Правила запроса: FROM с корнем `c`, проекция через `VALUE`, без JOIN, подзапросов, WHERE, GROUP BY, ORDER BY, TOP, DISTINCT, агрегатов, пространственных, пользовательских и недетерминированных функций. Ограничения: до 20 вычисляемых свойств на контейнер; вычисляемое свойство не может ссылаться на другое. Не индексируются по умолчанию, и `/*` их не покрывает. Изменение определения индексированного свойства не запускает переиндексацию: сначала удалите путь из политики, дождитесь трансформации, затем добавьте снова. Индексация повышает стоимость записи. `SELECT *` не возвращает вычисляемые свойства, ORDER BY требует индекса.

### 6. Implement global secondary indexes
Источник: https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/6-implement-global-secondary-indexes
Глобальный вторичный индекс хранит копию данных с другим partition key, поэтому запрос по SKU становится запросом в одной партиции. Записи выполняются только в исходный контейнер. Индекс имеет собственные RU и политику индексации. Требуются включенная функция на уровне аккаунта (Features → Global Secondary Index for NoSQL API) и непрерывное резервное копирование (миграция из periodic необратима). Определение: `sourceCollectionId` и `definition` с SELECT (без WHERE, JOIN, DISTINCT, GROUP BY, ORDER BY, TOP, OFFSET LIMIT, EXISTS, алиасов AS, системных и пользовательских функций). Индексы используют autoscale-throughput. Id исходного элемента в индексе попадает в поле `_id`, а id индекса генерируется. Синхронизация идет через change feed и eventually consistent. Стоимость: чтение change feed (RU исходного контейнера), запись в индекс (RU индекса) и надбавка 50–100% на replace и delete в исходном контейнере (create не затрагивается). В аккаунте с одним регионом записи чтение change feed и запись индекса выполняются в регионе записи. Мониторинг: метрика «Global Secondary Index Propagation Latency in Seconds» (разбивка по GlobalSecondaryIndexName и GlobalSecondaryIndexStatus). Partition key индекса должен присутствовать почти во всех элементах, иначе значения null накапливаются в одной логической партиции (лимит 20 ГБ). Перед удалением исходного контейнера удалите все его индексы.

### 7. Exercise: Optimize an indexing strategy
Источник: https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/7-exercise-optimize-indexing
Практика (около 45 минут): настройка индексной политики каталога, добавление составных и глобальных вторичных индексов и сравнение стоимости запросов. Варианты на C# и Python. Нужна подписка Azure.

### 8. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/8-knowledge-check
Проверка знаний (в исходнике текст отсутствует).

### 9. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/9-summary
Индексация в Azure Cosmos DB for NoSQL — сначала решение о стоимости, потом о производительности. Модуль показывает рычаги подгонки индексации под реальную нагрузку: политику, составные и пространственные индексы, вычисляемые свойства и глобальные вторичные индексы (с надбавкой 50–100% на replace и delete в исходном контейнере).

## Важные команды / код / настройки

Opt-out политика для каталога:

```json
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    { "path": "/*" }
  ],
  "excludedPaths": [
    { "path": "/description/?" },
    { "path": "/tags/*" },
    { "path": "/\"_etag\"/?" }
  ]
}
```

Opt-in политика:

```json
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    { "path": "/categoryId/?" },
    { "path": "/price/?" },
    { "path": "/name/?" }
  ],
  "excludedPaths": [
    { "path": "/*" }
  ]
}
```

Составной индекс (сортировка по categoryId ASC и price DESC):

```json
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    { "path": "/*" }
  ],
  "excludedPaths": [
    { "path": "/\"_etag\"/?" }
  ],
  "compositeIndexes": [
    [
      { "path": "/categoryId", "order": "ascending" },
      { "path": "/price", "order": "descending" }
    ]
  ]
}
```

Пространственный индекс:

```json
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    { "path": "/*" }
  ],
  "excludedPaths": [
    { "path": "/\"_etag\"/?" }
  ],
  "spatialIndexes": [
    {
      "path": "/location/*",
      "types": [ "Point", "Polygon" ]
    }
  ]
}
```

Пространственный запрос, который может использовать индекс:

```sql
SELECT s.name
FROM s
WHERE ST_DISTANCE(s.location, { "type": "Point", "coordinates": [-122.12827, 47.63980] }) < 40000
```

Вычисляемое свойство:

```json
{
  "computedProperties": [
    {
      "name": "cp_primaryCategory",
      "query": "SELECT VALUE SUBSTRING(c.categoryName, 0, INDEX_OF(c.categoryName, ',')) FROM c"
    }
  ]
}
```

Индексация вычисляемого свойства:

```json
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    { "path": "/*" },
    { "path": "/cp_primaryCategory/?" }
  ],
  "excludedPaths": [
    { "path": "/\"_etag\"/?" }
  ]
}
```

Применение политики через Azure CLI из файла:

```bash
az cosmosdb sql container update `
    --resource-group $resourceGroup `
    --account-name $accountName `
    --database-name cosmicworks `
    --name product `
    --idx @index-policy.json
```

Тело запроса для создания глобального вторичного индекса:

```json
{
  "location": "West US 2",
  "properties": {
    "resource": {
      "id": "productBySku",
      "partitionKey": { "paths": [ "/sku" ] },
      "materializedViewDefinition": {
        "sourceCollectionId": "product",
        "definition": "SELECT c.id, c.sku, c.name, c.price, c.categoryId FROM c"
      }
    },
    "options": {
      "autoscaleSettings": { "maxThroughput": 1000 }
    }
  }
}
```

Запрос к индексу:

```sql
SELECT * FROM c WHERE c.sku = @sku
```

Таблица поддержки составных индексов из модуля: `(categoryId ASC, price ASC)` с фильтром `c.categoryId = "..." AND c.price > 2000` — поддерживается; `(price ASC, categoryId ASC)` с тем же фильтром — не поддерживается; `(categoryId ASC, price ASC)` с фильтром `c.categoryId != "..." AND c.price > 2000` — не поддерживается.

## Что запомнить

- По умолчанию индексируется всё: это ускоряет чтение, но удорожает каждую запись.
- Opt-out (`/*` включен) — безопасная отправная точка; opt-in (`/*` исключен) — минимальный индекс.
- Удаление пути из политики действует сразу, добавление — только после завершения трансформации.
- Составной индекс обязателен для ORDER BY по двум свойствам; для фильтров ставьте равенства первыми, диапазон последним.
- Глобальный вторичный индекс превращает межпартиционный запрос в запрос к одной партиции, но добавляет надбавку 50–100% на replace и delete и работает eventually consistent.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/
- Документация: Overview of indexing in Azure Cosmos DB; Indexing policies; Manage indexing policies; Computed properties; Global secondary indexes (упоминаются в уроке 9); composite indexes; indexing and querying GeoJSON data (упоминаются в уроке 4).
- Связанный модуль: Customize indexes in Azure Cosmos DB for NoSQL (`customize-indexes-azure-cosmos-db-sql-api`).
- Связанный модуль: Design data partitioning strategy (`design-data-partitioning-strategy`).
