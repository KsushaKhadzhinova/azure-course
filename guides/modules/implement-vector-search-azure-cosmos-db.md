# Реализация векторного поиска в Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/

## Цель модуля

Научиться хранить векторные эмбеддинги в контейнерах Azure Cosmos DB for NoSQL, настраивать векторные политики и индексы, выполнять запросы похожести с функцией VectorDistance, комбинировать векторный поиск с фильтрами и гибридным (full-text) поиском и обновлять эмбеддинги через change feed.

## Ключевые понятия

- **Embedding (эмбеддинг)** - числовое векторное представление содержимого, созданное моделью машинного обучения (например, Azure OpenAI); похожие по смыслу тексты дают близкие векторы.
- **Vector policy (векторная политика)** - задается при создании контейнера и описывает путь к эмбеддингу, тип данных, размерность и функцию расстояния; после создания не меняется.
- **dataType** - тип элементов вектора: float32 (по умолчанию), float16, int8, uint8.
- **dimensions** - число элементов вектора; должно совпадать с моделью (по умолчанию 1 536).
- **distanceFunction** - метрика похожести: cosine (по умолчанию), dotproduct, euclidean.
- **VectorDistance** - функция запроса, которая вычисляет похожесть вектора документа и вектора запроса.
- **Vector index (векторный индекс)** - тип flat (точный перебор, до 505 измерений), quantizedFlat (сжатие, до 4 096 измерений, рекомендуется до примерно 50 000 векторов на физическую партицию) и diskANN (приближенный поиск DiskANN, до 4 096 измерений, для больших наборов).
- **Pre-filtering / post-filtering** - порядок применения фильтров относительно векторного сравнения; выбирает оптимизатор.
- **Hybrid search (гибридный поиск)** - сочетание векторного и full-text поиска через функцию RRF (Reciprocal Rank Fusion).
- **FullTextScore** - функция полнотекстовой оценки; требует full-text policy и full-text index.
- **Change feed (лента изменений)** - упорядоченный журнал вставок и обновлений; используется для пересчета эмбеддингов.
- **Lease container (контейнер аренды)** - контейнер, где change feed processor хранит аренды и контрольные точки.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/1-introduction

Пример сценария: база знаний службы поддержки, где агенты ищут документацию по смыслу вопроса, а не по ключевым словам (например, "can't connect to WiFi" должен находить статьи о беспроводной сети). Цели: хранить и получать векторы с корректной векторной политикой, выполнять VectorDistance-запросы, комбинировать поиск с фильтрами и гибридным поиском, обновлять эмбеддинги через change feed. Примеры кода в модуле написаны на основе последней версии azure-cosmos Python SDK на момент написания.

### 2. Хранение и получение эмбеддингов
Источник: https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings

- Эмбеддинги хранятся как свойства документа рядом с бизнес-данными; отдельная векторная БД не нужна. Пример: text-embedding-ada-002 дает 1 536 измерений, text-embedding-3-large - 3 072.
- Для включения функции на аккаунте: портал (Settings > Features > Vector Search for NoSQL API) или `az cosmosdb update --capabilities EnableNoSQLVectorSearch`; может понадобиться до 15 минут.
- Векторная политика задается при создании контейнера. Для каждого пути: `path` (обязательно), `dataType`, `dimensions`, `distanceFunction`.
- **Функции расстояния**: cosine возвращает значения от -1 до +1 (чем выше, тем похожее); dotproduct для нормализованных векторов дает тот же результат, что и cosine, и может быть быстрее; euclidean - от 0 (идентичны) до бесконечности (чем меньше, тем похожее). Для текстовых эмбеддингов Azure OpenAI в модуле рекомендуется cosine.
- **Типы данных**: float32 - полная точность и максимальный объем; float16 - вдвое меньше хранения при незначительной потере качества; int8 и uint8 - квантование с большой экономией, но требует оценки точности.
- Несколько векторов в одном документе (например, titleEmbedding и contentEmbedding) задаются несколькими записями в векторной политике.
- **Векторные индексы**: flat - точный перебор, 100% recall, до 505 измерений; quantizedFlat - сжатые векторы, перебор с меньшей задержкой и RU, до 4 096 измерений; diskANN - приближенный поиск, лучший вариант для больших наборов (миллионы векторов), до 4 096 измерений.
- Путь эмбеддинга исключается из обычного индекса (`/embedding/*`), так как массивы чисел не выигрывают от range-индекса.
- quantizedFlat и diskANN начинают работать эффективно при наличии минимум 1 000 векторов; при меньшем числе запросы идут полным сканированием с более высокой стоимостью.
- Векторные политики нельзя изменить у существующего контейнера; векторный поиск поддерживается только в новых контейнерах.
- Выбор partition key (например, `/category`) должен совпадать с типичными запросами, чтобы они шли в одну партицию.
- Вставка: эмбеддинг генерируется API (в примере Azure OpenAI), документ сохраняется через `upsert_item`; при изменении содержимого эмбеддинг нужно пересчитать.

### 3. Векторные запросы похожести
Источник: https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/3-execute-vector-similarity-queries

- `VectorDistance(vector_expr_1, vector_expr_2, bool_expr, obj_expr)`: первый аргумент - путь эмбеддинга документа (например, `c.embedding`), второй - вектор запроса; `bool_expr` (по умолчанию false) при true принудительно использует перебор; `obj_expr` - опции (distanceFunction, dataType).
- Базовый запрос: SELECT TOP N c.id, c.title, VectorDistance(...) AS SimilarityScore ... ORDER BY VectorDistance(...). TOP N обязателен: без него запрос пытается вернуть все документы, что дорого по RU и медленно.
- Вектор запроса создается той же моделью, что и эмбеддинги документов: разные модели дают несовместимые векторные пространства.
- Передавайте вектор параметром (`@queryVector`), а не текстом запроса: это позволяет кэшировать план запроса и избегает длинных строк.
- Интерпретация для cosine: около +1.0 - идентичные; 0.7-0.9 - очень похожие; 0.5-0.7 - умеренно похожие; 0.1-0.5 - низкое сходство; 0.0 и ниже - непохожие. Порог 0.7 дает высокорелевантные результаты, 0.5 - включает умеренно связанные. Порог подбирается экспериментально.
- Количество результатов: RAG - 5-10; пользовательский поиск - 10-20 с пагинацией; рекомендации - 3-5.
- По умолчанию используется векторный индекс (например, DiskANN). Перебор (brute-force) потребляет заметно больше RU, имеет большую задержку и плохо масштабируется; используйте его для эталонных проверок и малых наборов.
- Оптимизация: выбирайте индекс по размеру (diskANN для больших наборов, более 50 000 векторов на партицию, quantizedFlat для меньших); используйте минимальный TOP; указывайте partition key; выбирайте только нужные поля вместо `SELECT *`; следите за RU.

### 4. Комбинация векторного поиска с фильтрами и гибридным поиском
Источник: https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/4-combine-vector-metadata-filtering

- Фильтры WHERE можно добавлять к векторному запросу. Pre-filtering сужает пространство поиска до сравнения векторов и эффективен при селективных фильтрах; post-filtering применяется после ранжирования и может вернуть меньше результатов, чем запрошено. Выбор делает оптимизатор; индексируйте свойства фильтров.
- Типичные фильтры: тип документа (`c.documentType`), диапазон дат (`c.createdDate`), продукт (`c.productId IN (...)`), права доступа (`ARRAY_CONTAINS(c.accessGroups, @userGroup)`), статус (`c.status = 'published'`).
- Если WHERE содержит partition key, запрос направляется в одну партицию; параметр `partition_key="networking"` делает это явно.
- **Гибридный поиск**: нужны векторная политика, full-text policy (`defaultLanguage`, `fullTextPaths`) и индекс `fullTextIndexes`. Запрос использует `ORDER BY RANK RRF(VectorDistance(...), FullTextScore(c.content, @searchTerm1, @searchTerm2))`. Полезен для точных кодов и терминов (например, код ошибки 0x80070005) вместе с семантикой.
- **Веса RRF**: массив весов в порядке функций; `[2, 1]` делает векторный вклад вдвое весомее. Высокий вес вектора - для описаний на естественном языке; высокий вес full-text - для точных терминов; равные веса - разумная отправная точка.
- **Мульти-вектор**: `ORDER BY RANK RRF(VectorDistance(c.titleEmbedding, @queryVector), VectorDistance(c.contentEmbedding, @queryVector))` находит документы, похожие по заголовку или содержимому.
- Сложные запросы (фильтры, гибрид) дороже простых; тестируйте на реалистичных объемах; индексируйте свойства фильтров; заголовок `x-ms-request-charge` показывает RU запроса.

### 5. Обновление эмбеддингов через change feed
Источник: https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/5-change-feed-trigger-embedding-refresh

- Change feed - постоянный упорядоченный журнал вставок и обновлений; включен по умолчанию; изменения в одной партиции приходят в порядке модификации; каждое изменение появляется в ленте один раз, но потребитель сам ведет контрольные точки.
- **Push-модель** (Azure Functions trigger или change feed processor) - автоматическая доставка, балансировка между инстансами, контрольные точки; рекомендуется для эмбеддингов в продакшене.
- **Pull-модель** (`query_items_change_feed`) - полный контроль, подходит для пакетной обработки и разовых миграций; позицию (continuation token) нужно сохранять между запусками.
- Azure Functions: декоратор `@app.cosmos_db_trigger` с `container_name`, `database_name`, `connection`, `lease_container_name` и `create_lease_container_if_not_exists=True`.
- **Lease container**: хранит аренды партиций и контрольные точки; небольшой контейнер на 400 RU/s обычно достаточен; имя должно отличаться от контейнеров данных или использовать разные `leaseContainerPrefix`.
- **Выборочное обновление**: пересчитывать эмбеддинг только когда изменились поля, которые влияют на него (title, content, description, summary). Вариант - хранить хеш содержимого (`contentHash`, SHA-256) и сравнивать его.
- **Высокий объем**: пакетные вызовы API эмбеддингов (массив входов), повторы с экспоненциальной задержкой при лимитах, очередь Azure Queue Storage для буферизации, приоритизация важных документов.
- **Идемпотентность**: повторная обработка должна давать тот же результат. Документ мог быть удален до обработки - `CosmosResourceNotFoundError` обрабатывается как пропуск; при одновременных обновлениях используйте ETag; при ошибках API - повтор и dead-letter для постоянных сбоев.
- Масштабирование: Functions масштабирует инстансы по отставанию; метрика `ChangeFeedProcessorHostLag` показывает, успевает ли обработка.

### 6. Упражнение: семантический поиск
Источник: https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/6-exercise-build-semantic-search

Упражнение (30 минут): реализовать векторный поиск с Azure Cosmos DB for NoSQL. Задачи: настроить файлы проекта и скрипт развертывания, развернуть аккаунт с векторным поиском, написать функции поиска на Python, создать контейнер с векторной и индексной политиками, протестировать поиск через Flask-приложение. Требуются подписка Azure, Visual Studio Code, последняя Azure CLI и Python 3.12 или новее.

### 7. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/7-knowledge-check

Итоговый тест модуля (5 минут). Содержимое вопросов в исходных материалах не приведено.

### 8. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/8-summary

Модуль показал, как реализовать векторный поиск для AI-приложений: настроить контейнеры с векторными политиками (путь, тип данных, размерность, функция расстояния), хранить эмбеддинги вместе с метаданными, выполнять VectorDistance-запросы, комбинировать их с фильтрами и гибридным поиском, а также поддерживать эмбеддинги в актуальном состоянии через change feed.

## Важные команды / код / настройки

- Включение векторного поиска: `az cosmosdb update --capabilities EnableNoSQLVectorSearch`.
- Векторная политика (Python):
  ```
  vector_embedding_policy = {
      "vectorEmbeddings": [
          {"path": "/embedding", "dataType": "float32", "distanceFunction": "cosine", "dimensions": 1536}
      ]
  }
  ```
- Индексная политика с diskANN и исключением эмбеддинга:
  ```
  indexing_policy = {
      "indexingMode": "consistent",
      "automatic": True,
      "includedPaths": [{"path": "/*"}],
      "excludedPaths": [{"path": "/\"_etag\"/?"}, {"path": "/embedding/*"}],
      "vectorIndexes": [{"path": "/embedding", "type": "diskANN"}]
  }
  ```
- Создание контейнера: `database.create_container(id="knowledge-base", partition_key=PartitionKey(path="/category"), indexing_policy=indexing_policy, vector_embedding_policy=vector_embedding_policy)`.
- Вставка с эмбеддингом: `container.upsert_item(document)`; эмбеддинг через `openai_client.embeddings.create(input=..., model="text-embedding-ada-002")`.
- Векторный запрос: `SELECT TOP 10 c.id, c.title, c.category, VectorDistance(c.embedding, @queryVector) AS SimilarityScore FROM c ORDER BY VectorDistance(c.embedding, @queryVector)`.
- Порог похожести: `WHERE VectorDistance(c.embedding, @queryVector) > 0.7`.
- Перебор вместо индекса: `VectorDistance(c.embedding, @queryVector, true)`.
- Запрос с параметрами и partition key: `container.query_items(query=..., parameters=[{"name": "@queryVector", "value": query_embedding}], partition_key="networking")`.
- Полнотекстовая политика: `{"defaultLanguage": "en-US", "fullTextPaths": [{"path": "/content", "language": "en-US"}]}`; индекс: `"fullTextIndexes": [{"path": "/content"}]`.
- Гибридный запрос: `ORDER BY RANK RRF(VectorDistance(c.embedding, @queryVector), FullTextScore(c.content, @searchTerm1, @searchTerm2), [2, 1])`.
- Change feed (pull): `container.query_items_change_feed(start_time="Beginning")`, `by_page()`, `continuation_token`.
- Azure Functions trigger: `@app.cosmos_db_trigger(arg_name="documents", container_name="knowledge-base", database_name="support-db", connection="CosmosDBConnection", lease_container_name="leases", create_lease_container_if_not_exists=True)`.
- Идемпотентная обработка: `except CosmosResourceNotFoundError: pass` для удаленных документов.
- Лимиты: flat - до 505 измерений; quantizedFlat и diskANN - до 4 096.

## Что запомнить

- Векторная политика (путь, тип, размерность, distanceFunction) задается при создании контейнера и не меняется.
- Эмбеддинги хранятся в тех же документах, что и бизнес-данные; модель запроса и модель документов должны совпадать.
- VectorDistance с ORDER BY и TOP N - основа семантического поиска; без TOP запрос дорогой.
- Для больших наборов используйте diskANN; перебор - только для точной проверки.
- Гибридный поиск через RRF и FullTextScore объединяет смысл и точные термины; веса задают баланс.
- Change feed через Azure Functions поддерживает эмбеддинги актуальными; обработка должна быть идемпотентной и выборочной по изменившимся полям.

## Связанные материалы

- Vector search in Azure Cosmos DB for NoSQL
- Index and query vectors in Python
- Azure OpenAI embeddings
- VectorDistance system function
- Hybrid search in Azure Cosmos DB for NoSQL
- RRF system function
- FullTextScore system function
- Change feed in Azure Cosmos DB
- Change feed processor in Azure Cosmos DB
- Azure Functions Cosmos DB trigger
