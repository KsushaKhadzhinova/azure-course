# Оптимизация производительности запросов в Azure Cosmos DB

**Источник:** https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/

## Цель модуля

Научиться снижать задержку и стоимость запросов (RU) в Azure Cosmos DB for NoSQL для AI-приложений: настраивать range, composite и tuple индексы под шаблоны поиска, выбирать тип векторного индекса (flat, quantizedFlat, diskANN), строить политику индексации, которая балансирует чтение и запись, и выбирать уровень согласованности (consistency level).

## Ключевые понятия

- **Indexing policy (политика индексации)** — правила, какие пути индексируются и какими индексами; задается для контейнера.
- **Range index** — поддерживает равенство, диапазоны, ORDER BY по одному свойству и строковые функции.
- **Composite index** — индекс по нескольким свойствам с заданным порядком сортировки; нужен для ORDER BY по нескольким полям.
- **Spatial index** — геопространственные запросы (ST_DISTANCE, ST_WITHIN, ST_INTERSECTS).
- **Tuple index** — индекс комбинаций свойств внутри элементов массива.
- **Vector index** — ускоряет поиск по сходству через VectorDistance; типы flat, quantizedFlat, diskANN.
- **Indexing mode** — consistent (синхронное обновление, по умолчанию) или none (индексация отключена); lazy устарел.
- **Consistency level** — уровень согласованности чтений: Strong, Bounded staleness, Session, Consistent prefix, Eventual.
- **Index transformation** — асинхронное обновление индексов после изменения политики.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/1-introduction

Введение: AI-приложение поиска документов с эмбеддингами, которое требует ответа менее 100 мс. Политика по умолчанию индексирует все свойства, включая большие массивы эмбеддингов, поэтому растут стоимость и хранение. Модуль учит анализировать запросы, настраивать индексы, выбирать тип векторного индекса и уровень согласованности.

### 2. Understand indexes in Azure Cosmos DB
https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/2-understand-indexes-cosmos-db

По умолчанию все свойства индексируются range-индексами. Описаны типы индексов и режимы индексации. Размер индекса зависит от числа путей, кардинальности значений и размера массивов; эмбеддинги в range-индексе только увеличивают стоимость. Партиционный ключ (кроме `/id`) не индексируется автоматически и его нужно добавить явно. Правила путей: `/*`, `/property/?`, `/array/[]`, `/nested/*`; более конкретный путь имеет приоритет.

### 3. Configure range and composite indexes
https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/3-configure-range-composite-indexes

Range-индексы для фильтров по типу, статусу, дате и числам. Composite-индексы для ORDER BY по нескольким свойствам: порядок и направление должны совпадать с запросом. Для фильтра по одному свойству и сортировки по другому полезно включать фильтруемое свойство в ORDER BY. Для нескольких фильтров равенства сначала идут equality-свойства, затем один range-фильтр. Для нескольких range-фильтров нужны несколько composite-индексов. Tuple-индекс ускоряет фильтры по элементам массива (например, chunks). Изменения индекса применяются асинхронно: добавление не дает эффекта до окончания transformation, удаление действует сразу.

### 4. Tune vector indexes for embedding workloads
https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/4-tune-vector-indexes-embeddings

Vector index задается в политике индексации (`vectorIndexes`). Эмбеддинги исключаются из range-индекса. Flat: точный перебор, до 505 измерений, для малых наборов или сильной фильтрации. QuantizedFlat: сжатие векторов, 1 000–50 000 векторов на физическую партицию, до 4 096 измерений. DiskANN: приближенный поиск для больших наборов (более 50 000 векторов на партицию), до 4 096 измерений, рекомендован для продакшена. Quantized и diskANN работают эффективно только после 1 000 векторов. Параметры `quantizationByteSize` и `indexingSearchListSize` настраиваются. Векторная политика не меняется после создания контейнера.

### 5. Reduce RU costs with strategic indexing
https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/5-reduce-ru-costs-strategic-indexing

Начинайте с анализа запросов: фильтры, сортировки, комбинации свойств, частота. Метрики запроса (index utilization, retrieved и output document count) помогают найти отсутствующие индексы. Индексируйте только используемые свойства, включайте партиционный ключ, создавайте 5–10 самых важных composite-индексов. Для записи-тяжелых нагрузок индексов должно быть меньше, для чтения-тяжелых — больше. Большинство AI-приложений читают чаще, чем пишут. Тестируйте стоимость на реалистичных данных.

### 6. Choose consistency levels for optimal performance
https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/6-choose-consistency-levels-performance

Пять уровней от строгого к слабому: Strong (линеаризуемость; не поддерживается при нескольких регионах записи), Bounded staleness (отставание не более K версий или T секунд), Session (read-your-writes в рамках сессии; рекомендуется для большинства приложений), Consistent prefix (порядок записей сохраняется), Eventual (наименьшая задержка и наибольшая пропускная способность). Для Strong и Bounded staleness чтение идет с двух реплик (2× RU), для остальных — с одной (1×). Для поиска документов, загруженных пользователем, подходит Session. PBS-метрики в портале показывают, как часто Eventual возвращает актуальные данные.

### 7. Exercise - Optimize query performance with vector indexes on Azure Cosmos DB for NoSQL
https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/7-exercise-optimize-query-performance

Практика (около 30 минут): создать контейнеры с индексами flat, quantizedFlat и diskANN, загрузить одинаковые данные, сравнить поиск через Flask-приложение. Нужны подписка Azure, Visual Studio Code, Azure CLI и Python 3.12 или новее.

### 8. Module assessment
https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/8-knowledge-check

Проверочный тест (около 5 минут). Вопросы и ответы в источнике не приведены.

### 9. Summary
https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/9-summary

Итоги: range, composite, spatial, vector и tuple индексы; выбор векторного индекса по размеру набора; исключение эмбеддингов из range-индекса; баланс чтения и записи; Session для загруженного пользователем контента и Eventual для фоновой аналитики.

## Важные команды / код / настройки

**Политика по умолчанию (индексируются все свойства):**

```
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    { "path": "/*" }
  ],
  "excludedPaths": [
    { "path": "/\"_etag\"/?" }
  ]
}
```

**Выборочная политика (индексируются только запрашиваемые свойства):**

```
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    { "path": "/title/?" },
    { "path": "/category/?" },
    { "path": "/createdDate/?" },
    { "path": "/metadata/*" }
  ],
  "excludedPaths": [
    { "path": "/*" }
  ]
}
```

**Composite-индекс для ORDER BY по нескольким свойствам:**

```
{
  "compositeIndexes": [
    [
      { "path": "/relevanceScore", "order": "descending" },
      { "path": "/uploadDate", "order": "descending" }
    ]
  ]
}
```

Запрос `ORDER BY c.relevanceScore DESC, c.uploadDate DESC` требует этого индекса. Смешанный порядок (DESC, ASC) требует отдельного индекса.

**Composite-индекс для фильтра по нескольким свойствам:** equality-свойства первыми, затем единственный range-фильтр последним, например `/category`, `/department`, `/createdDate`.

**Tuple-индекс:** `{ "path": "/chunks/[]/{position, tokens}/?" }` в `includedPaths`.

**Политика с векторным индексом (исключение эмбеддингов из range-индекса):**

```
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    { "path": "/category/?" },
    { "path": "/createdDate/?" },
    { "path": "/documentType/?" }
  ],
  "excludedPaths": [
    { "path": "/*" },
    { "path": "/embedding/*" }
  ],
  "compositeIndexes": [
    [
      { "path": "/category", "order": "ascending" },
      { "path": "/createdDate", "order": "descending" }
    ]
  ],
  "vectorIndexes": [
    { "path": "/embedding", "type": "diskANN" }
  ]
}
```

**Параметры векторного индекса:**

```
{
  "vectorIndexes": [
    {
      "path": "/embedding",
      "type": "diskANN",
      "quantizationByteSize": 64,
      "indexingSearchListSize": 150
    }
  ]
}
```

`quantizationByteSize` — от 1 до 512 байт (по умолчанию определяется системой). `indexingSearchListSize` (только diskANN) — от 10 до 500, по умолчанию 100.

**Пороги выбора векторного индекса:** flat — до 505 измерений; quantizedFlat — 1 000–50 000 векторов на физическую партицию, до 4 096 измерений; diskANN — более 50 000 векторов на партицию, до 4 096 измерений.

**Тип данных вектора:** float32, float16, int8 или uint8; float16 уменьшает хранение вдвое по сравнению с float32 (по утверждению источника, с минимальным влиянием на точность).

**Метрики запроса в Python (фрагмент из урока 5):**

```
query_metrics_output = {}

def response_hook(headers, results):
    query_metrics_output["metrics"] = headers.get("x-ms-documentdb-query-metrics", "")
    query_metrics_output["request_charge"] = headers.get("x-ms-request-charge", "")

results = container.query_items(
    query=query,
    parameters=parameters,
    populate_query_metrics=True,
    response_hook=response_hook
)
items = list(results)
```

**Уровень согласованности в Python:**

```
from azure.cosmos import CosmosClient, ConsistencyLevel

client = CosmosClient(
    url=endpoint,
    credential=credential,
    consistency_level=ConsistencyLevel.Session
)
```

Для чтения после записи в другом запросе передавайте `session_token` из заголовка `x-ms-session-token` ответа на запись.

**Относительная стоимость чтения по уровням:** Strong и Bounded staleness — 2×; Session, Consistent prefix и Eventual — 1×.

## Что запомнить

- По умолчанию все свойства индексируются; для AI-приложений исключайте большие поля и массивы эмбеддингов, индексируя только фильтры и сортировки.
- ORDER BY по нескольким полям требует composite-индекса с тем же порядком сортировки.
- Выбор векторного индекса зависит от объема: flat для малых наборов, quantizedFlat для средних, diskANN для больших.
- Векторная политика неизменяема после создания контейнера; планируйте размерность и тип данных заранее.
- Session обеспечивает видимость только что загруженного контента и стоит в два раза дешевле Strong на чтении; Eventual подходит для фоновой аналитики.

## Связанные материалы

- Indexing policies in Azure Cosmos DB.
- Indexing overview in Azure Cosmos DB.
- Composite indexes и tuple indexes in Azure Cosmos DB.
- Vector indexes in Azure Cosmos DB; VectorDistance system function.
- Indexing metrics in Azure Cosmos DB; Optimize request cost in Azure Cosmos DB.
- Consistency levels in Azure Cosmos DB; Configure default consistency level.
- Vector search in Azure Cosmos DB for NoSQL (упоминается в уроке 4).
