# Индексация данных Azure Cosmos DB (SQL API) в Azure Cognitive Search

**Источник:** https://learn.microsoft.com/en-us/training/modules/search-azure-cosmos-db-sql-api-data-azure-cognitive-search/

## Цель модуля

Научиться создавать индексатор (indexer), который переносит данные из Azure Cosmos DB for NoSQL в индекс Azure Cognitive Search, настраивать политику обнаружения изменений (change detection) и политику обнаружения удалений (deletion detection).

## Ключевые понятия

- **Azure Cognitive Search** - облачный поисковый сервис с расширенными возможностями: фильтры, фасеты, автодополнение, синонимы.
- **Search index (индекс поиска)** - набор доступных для поиска JSON-документов; обязательно имеет имя и ключ (key) - уникальный идентификатор документа.
- **Indexer (индексатор)** - компонент, который обходит источник данных по расписанию и заполняет индекс.
- **Data source (источник данных)** - ссылка на контейнер Cosmos DB с подключением, именем базы, именем контейнера и SQL-запросом.
- **Retrievable / Filterable / Sortable / Facetable / Searchable** - признаки полей индекса, которые включают возврат в результатах, фильтрацию, сортировку, фасетирование и полнотекстовый поиск.
- **High watermark (верхняя отметка)** - значение `_ts`, по которому индексатор определяет новые и измененные элементы с прошлого запуска.
- **Incremental progress (инкрементальный прогресс)** - возможность продолжить индексацию с места сбоя, если запрос сортирует по `_ts`.
- **Soft-delete (мягкое удаление)** - пометка элемента полем (например, `_isDeleted = true`), по которой индексатор удаляет его из индекса.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/search-azure-cosmos-db-sql-api-data-azure-cognitive-search/1-introduction

Azure Cognitive Search полезен, когда команда хочет получить поисковые функции (фильтры, фасеты, автодополнение, синонимы) без реализации их в самой базе данных. Цель модуля - создать индексатор, который переносит данные из Azure Cosmos DB for NoSQL в индекс Azure Cognitive Search.

### 2. Создание индексатора
Источник: https://learn.microsoft.com/en-us/training/modules/search-azure-cosmos-db-sql-api-data-azure-cognitive-search/2-create-indexer

- Компоненты поиска: индексы (JSON-документы для поиска), индексаторы (обход источников и заполнение индекса), источники данных (подключение к платформам данных).
- **Источник данных** для Cosmos DB for NoSQL задается параметрами: строка подключения к аккаунту, имя базы данных, имя контейнера и SQL-запрос, который выбирает элементы для индексации.
- **Индекс**: минимум имя и ключ. Для каждого поля настраиваются признаки: Retrievable (возвращать в результатах), Filterable (фильтры в стиле OData), Sortable (сортировка), Facetable (агрегация и группировка), Searchable (поиск по термину).
- **Индексатор**: настраивается имя и расписание; расписание определяет, как часто индексатор забирает данные из источника.

### 3. Политика обнаружения изменений
Источник: https://learn.microsoft.com/en-us/training/modules/search-azure-cosmos-db-sql-api-data-azure-cognitive-search/3-implement-change-detection-policy

- Запрос по умолчанию для источника Cosmos DB for NoSQL: `SELECT * FROM c WHERE c._ts >= @HighWaterMark ORDER BY c._ts`.
- Индексатор индексирует все элементы, возвращенные запросом, затем сохраняет временную отметку как high watermark; при следующем запуске берутся элементы с отметкой не меньше сохраненной. Так индексируются созданные и измененные с прошлого запуска элементы.
- Если запрос сортирует по `_ts`, индексатор может продолжить работу с места сбоя при временной ошибке, а не индексировать контейнер заново. Эту возможность нужно включить при настройке источника данных.
- При собственном запросе сортировка обязательно должна идти по тому же полю `_ts`.

### 4. Политика обнаружения удалений
Источник: https://learn.microsoft.com/en-us/training/modules/search-azure-cosmos-db-sql-api-data-azure-cognitive-search/4-manage-data-deletion-detection-policy

- Физическое удаление элемента из контейнера не удаляет его из индекса автоматически. Для отслеживания удалений нужна политика.
- Azure Cognitive Search поддерживает отслеживание удаления только через мягкое удаление: поле и значение-маркер. Например, документ с `"_isDeleted": true`.
- В политике мягкого удаления для источника Cosmos DB for NoSQL задаются `softDeleteColumnName` (здесь `_isDeleted`) и `softDeleteMarkerValue` (здесь `true`). Такие элементы будут удалены из индекса.

### 5. Упражнение: поиск данных
Источник: https://learn.microsoft.com/en-us/training/modules/search-azure-cosmos-db-sql-api-data-azure-cognitive-search/5-exercise-search-data-use-azure-cognitive-search

Упражнение (15 минут) по поиску данных через Azure Cognitive Search и Azure Cosmos DB for NoSQL. Требуется подписка Azure с административным доступом; нужно создать группу ресурсов, настроить локальное окружение и включить resource providers.

### 6. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/search-azure-cosmos-db-sql-api-data-azure-cognitive-search/6-knowledge-check

Итоговый тест модуля (5 минут). Содержимое вопросов в исходных материалах не приведено.

### 7. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/search-azure-cosmos-db-sql-api-data-azure-cognitive-search/7-summary

Модуль показал, как индексатор Azure Cognitive Search обходит данные Azure Cosmos DB for NoSQL и помещает их в индекс для поисковых запросов, которые было бы сложно реализовать в самой базе данных.

## Важные команды / код / настройки

- Запрос по умолчанию (источник данных): `SELECT * FROM c WHERE c._ts >= @HighWaterMark ORDER BY c._ts`.
- Параметры источника данных: Connection string, Database, Collection, Query.
- Политика мягкого удаления: `softDeleteColumnName` = `_isDeleted`, `softDeleteMarkerValue` = `true`.
- Пример документа с маркером удаления: `{ "id": "...", "categoryId": "...", "sku": "TI-R092", "name": "LL Road Tire", "_isDeleted": true }`.
- Признаки полей индекса: Retrievable, Filterable, Sortable, Facetable, Searchable.

## Что запомнить

- Индексатор заполняет индекс из контейнера Cosmos DB по расписанию через источник данных с SQL-запросом.
- Change detection опирается на `_ts` и high watermark; сортировка по `_ts` позволяет продолжать индексацию после сбоя.
- Удаления отслеживаются только через мягкое удаление (поле-маркер), а не через физическое удаление.
- Для каждого поля индекса задайте признаки поиска (фильтрация, сортировка, фасеты, полнотекстовый поиск) заранее.

## Связанные материалы

- Index data from Azure Cosmos DB using NoSQL
