# Анализ и настройка производительности запросов в Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/analyze-tune-query-performance-azure-cosmos-db-nosql/

## Цель модуля

Научиться диагностировать дорогие запросы Azure Cosmos DB for NoSQL по их метрикам (request charge, server-side query metrics, index metrics, распределение по физическим партициям) и применять исправление, которое указывают эти метрики.

## Ключевые понятия

- **Request Unit (RU)** - единица стоимости операции в Azure Cosmos DB. Точечное чтение элемента 1 KB стоит около 1 RU; запрос, сканирующий контейнер, может стоить тысячи RU.
- **Request charge** - стоимость операции в RU, которую SDK получает из заголовка ответа. Для запроса возвращается по одному значению на каждую страницу.
- **Baseline (базовая линия)** - набор измерений репрезентативных операций (точечное чтение, фильтрованный запрос, запись), снятых до изменений для последующего сравнения.
- **Total Request Units (метрика Azure Monitor)** - потребление RU по аккаунту с возможностью разбивки по Operation Type и CollectionName.
- **Server-side query metrics** - метрики выполнения запроса на стороне сервера: RetrievedDocumentCount, OutputDocumentCount, IndexHitRatio, IndexLookupTime, DocumentLoadTime, TotalTime.
- **RetrievedDocumentCount / OutputDocumentCount** - число загруженных движком документов и число документов в результате. Большой разрыв указывает на сканирование.
- **Index metrics (метрики индекса)** - показывают использованные (utilized) и потенциальные (potential) индексы для запроса. Включаются явно (opt-in).
- **Index impact score** - оценка влияния индекса, которая отражает форму запроса, а не данные.
- **429 (Too Many Requests)** - ответ сервиса при превышении provisioned throughput. Имеет четыре причины: высокая частота запросов, высокая частота метаданных, временная ошибка сервиса, TXN_WAIT_FOR_TRANSACTION_END.
- **Normalized RU Consumption (%) By PartitionKeyRangeID** - график, показывающий загрузку каждой физической партиции; выявляет "горячие" партиции.
- **Fan-out (разветвление запроса)** - ситуация, когда запрос обращается ко всем физическим партициям контейнера.
- **Cross-partition query** - запрос, который не ограничен одним значением partition key и затрагивает несколько партиций.
- **MaxConcurrency / MaxBufferedItemCount / MaxItemCount** - опции SDK (.NET), управляющие параллелизмом, предвыборкой и размером страницы для cross-partition запросов.
- **Global secondary index** - копия контейнера с другим partition key, которая позволяет адресовать запрос к одной партиции при равенстве по новому ключу.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/analyze-tune-query-performance-azure-cosmos-db-nosql/1-introduction

Введение описывает типичную ситуацию: сервис получает периодические ошибки в пиковую нагрузку, и команда сначала повышает throughput, не зная, какая операция дорогая. Модуль предлагает метод на основе измерений: стоимость операции, метрики запроса, метрики индекса и распределение по партициям. Цель модуля - диагностировать дорогой запрос по метрикам и применить подходящее исправление.

### 2. Оценка потребления RU и дорогих запросов
Источник: https://learn.microsoft.com/en-us/training/modules/analyze-tune-query-performance-azure-cosmos-db-nosql/2-evaluate-request-unit-high-cost-queries

- Стоимость операции читается из заголовка ответа; для запроса суммируйте request charge всех страниц.
- Важны одновременно стоимость и частота: запрос 200 RU, выполняемый два раза в день, может обходиться дешевле, чем запрос 4 RU, выполняемый 50 раз в секунду.
- Для базовой линии фиксируйте индексную политику, уровень согласованности, размер страницы (MaxItemCount) и число физических партиций. Чтение 1 KB элемента стоит 1 RU при session, consistent prefix или eventual; strong и bounded staleness стоят вдвое больше.
- Метрика Total Request Units в Azure Monitor позволяет найти операции (Create/Upsert, Read, Query), которые доминируют в потреблении. Подробные данные по каждому запросу требуют диагностических логов в Log Analytics; полный текст запросов требует включения функции полнотекстовых запросов, поэтому включайте ее только на время расследования.

### 3. Анализ метрик запросов
Источник: https://learn.microsoft.com/en-us/training/modules/analyze-tune-query-performance-azure-cosmos-db-nosql/3-analyze-query-metrics

- Server-side query metrics возвращаются вместе с ответом, без дополнительного обращения к сервису. В .NET SDK они доступны через GetQueryMetrics() (версия 3.36.0 и выше), в Python SDK - через заголовок x-ms-documentdb-query-metrics при populate_query_metrics=True.
- Ключевые значения: RetrievedDocumentCount, OutputDocumentCount, IndexHitRatio, IndexLookupTime, DocumentLoadTime, TotalTime.
- TotalTime отражает только серверное время. Если запрос дешевый по RU и быстрый на сервере, но медленный у клиента, проверьте сетевую задержку, обработку на клиенте и повторы (retries) из-за троттлинга.
- В .NET можно посмотреть распределение по партициям (PartitionedMetrics); в Python такой разбивки в заголовке нет, используйте график Normalized RU Consumption или сравнение запроса с фильтром по партиции и без него.
- Диагностика 429: при равномерной нагрузке и приемлемой задержке доля 429 в 1-5% может означать полное использование provisioned throughput. Низкий общий процент не исключает горячей партиции - проверяйте Normalized RU Consumption по PartitionKeyRangeID.

### 4. Анализ метрик индексов
Источник: https://learn.microsoft.com/en-us/training/modules/analyze-tune-query-performance-azure-cosmos-db-nosql/4-analyze-index-metrics

- Если RetrievedDocumentCount намного больше OutputDocumentCount, часть запроса не может использовать индекс: движок загружает документы и проверяет фильтр для каждого. В примере с UPPER(c.description) индекс не используется (Index Utilization 0%), время загрузки документов составляет почти все время выполнения.
- Index metrics включаются явно (PopulateIndexMetrics в .NET с версии 3.21.0; populate_index_metrics в Python с версии 4.6.0). Включайте их на время отладки, так как они добавляют накладные расходы.
- Метрики индексов содержат четыре секции: Utilized Single Indexes, Potential Single Indexes, Utilized Composite Indexes, Potential Composite Indexes.
- Utilized - это факт использования пути. Если ожидаемый путь отсутствует в utilized, его можно убрать из политики индексации без влияния на запрос. Potential - это гипотеза: добавьте индекс, повторите запрос и сравните RU с базовой линией.
- Index metrics возвращаются только если запрос вернул хотя бы один элемент.
- Функции, которые индекс не обслуживает: UPPER(...), GetCurrentDateTime() в фильтре, неагрегатные математические выражения. Рекомендации: нормализовать регистр при записи, передавать текущее время параметром, хранить вычисленное значение как свойство. Функции StartsWith, Contains, RegexMatch и Left индекс использует; Contains, RegexMatch, EndsWith и регистронезависимые формы StartsWith и StringEquals выполняют сканирование индекса, стоимость которого растет с кардинальностью свойства.

### 5. Оптимизация cross-partition запросов
Источник: https://learn.microsoft.com/en-us/training/modules/analyze-tune-query-performance-azure-cosmos-db-nosql/5-optimize-cross-partition-queries

- Каждая физическая партиция имеет собственный независимый индекс, поэтому запрос сначала определяет, какие партиции могут содержать совпадения.
- Равенство по partition key направляет запрос в одну партицию; IN по нескольким значениям ключа - в соответствующие партиции. Диапазонный фильтр по partition key (например, c.categoryId > "...") ведет себя как запрос без фильтра и обращается ко всем партициям.
- Fan-out добавляет фиксированную накладную нагрузку на каждую партицию и задержку на слияние результатов на клиенте. Эффект зависит от числа физических партиций: при одной партиции сужение области не убирает накладных расходов (метрика Physical Partition Count).
- Лучший способ - передать значение partition key в запрос (в тексте или через request options). На Linux и macOS в .NET SDK задавайте PartitionKey в QueryRequestOptions, так как локальная генерация плана там зависит от библиотеки, поставляемой только для Windows x64.
- Оптимистичное прямое выполнение (Optimistic Direct Execution) для однопартиционного запроса без пагинации пропускает обращение к шлюзу за планом запроса; в .NET SDK доступно с версии 3.38.0.
- Для запросов, которые нельзя сузить: увеличьте MaxConcurrency (параллелизм по партициям, -1 - выбор SDK), MaxBufferedItemCount (предвыборка), правильно подберите MaxItemCount (размер страницы). В Python SDK есть только max_item_count.
- Если запрос критичен и partition key не подходит, рассмотрите global secondary index с другим ключом (равенство по новому ключу даст одну партицию в копии; диапазон по-прежнему разветвляется).

### 6. Упражнение: настройка дорогого запроса
Источник: https://learn.microsoft.com/en-us/training/modules/analyze-tune-query-performance-azure-cosmos-db-nosql/6-exercise-tune-query

Практическое упражнение (45 минут): с помощью query metrics и request charge диагностировать и оптимизировать сканирование, составные фильтры и cross-partition запросы. Требуется подписка Azure; задания доступны на C# и Python.

### 7. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/analyze-tune-query-performance-azure-cosmos-db-nosql/7-knowledge-check

Итоговый тест модуля (5 минут) на проверку понимания метрик и приемов настройки. Содержимое вопросов в исходных материалах не приведено.

### 8. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/analyze-tune-query-performance-azure-cosmos-db-nosql/8-summary

Настройка запросов - это дисциплина измерений: каждая операция возвращает стоимость в RU, а метрики запроса и индекса объясняют, откуда она берется. Сравнивайте измерения при одинаковых данных и настройках; разрыв между retrieved и output указывает на сканирование; partition key в фильтре маршрутизирует запрос в одну партицию.

## Важные команды / код / настройки

- Чтение стоимости точечной операции (.NET): `response.RequestCharge` у `ItemResponse<T>`; для запроса суммируйте `page.RequestCharge` по всем страницам `FeedIterator<T>`.
- Чтение стоимости (Python): `response.get_response_headers()["x-ms-request-charge"]`; для запроса читайте заголовок после каждой страницы.
- Server-side метрики (.NET, версия 3.36.0+): `page.Diagnostics.GetQueryMetrics()`, затем `CumulativeMetrics` и `PartitionedMetrics`.
- Server-side метрики (Python): `container.query_items(..., populate_query_metrics=True)` и заголовок `x-ms-documentdb-query-metrics` (пары key=value, разделенные `;`).
- Метрики индекса (.NET, версия 3.21.0+): `QueryRequestOptions { PopulateIndexMetrics = true }`, затем `page.IndexMetrics`.
- Метрики индекса (Python, версия 4.6.0+; get_response_headers - 4.16.0+): `populate_index_metrics=True` и заголовок `x-ms-cosmos-index-utilization`.
- Область запроса по партиции (.NET): `QueryRequestOptions { PartitionKey = new PartitionKey("...") }`; в Python: параметр `partition_key="..."` в `query_items`.
- Параллелизм cross-partition запросов (.NET): `MaxConcurrency` (`-1` - выбор SDK), `MaxBufferedItemCount`, `MaxItemCount` (`-1` - выбор SDK по размеру документов).
- Python: `max_item_count` (число элементов на страницу); `enable_cross_partition_query=True` при запросе без partition key.
- Пример фильтра, который не использует индекс: `WHERE UPPER(c.description) = "..."` - нормализуйте регистр при записи и сравнивайте напрямую.
- Диагностические логи в Log Analytics: категория QueryRuntimeStatistics и функция полнотекстовых запросов; оплачиваются отдельно по объему данных, выключайте после расследования.
- Пример запроса, который обращается к одной партиции (контейнер с partition key /categoryId): `SELECT * FROM c WHERE c.categoryId = "..." AND c.price > 1000`. Запросы `SELECT * FROM c WHERE c.price > 1000` и `c.categoryId > "..."` разветвляются на все партиции.

## Что запомнить

- Сначала измеряйте: request charge и частота выполнения вместе определяют, стоит ли тюнить операцию.
- Разрыв между RetrievedDocumentCount и OutputDocumentCount указывает на сканирование; проверяйте index metrics перед изменением индекса.
- Метрики индекса (utilized и potential) - это факты и гипотезы; потенциальный индекс проверяйте по RU относительно базовой линии.
- Равенство по partition key направляет запрос в одну партицию; диапазон по partition key не сужает область.
- Четыре причины 429 требуют разных действий: увеличение RU/s помогает не во всех случаях, например при высокой частоте метаданных.

## Связанные материалы

- Tune query performance in Azure Cosmos DB
- Get query performance and execution metrics
- Indexing metrics in Azure Cosmos DB
- Troubleshoot query issues in Azure Cosmos DB for NoSQL
- Diagnose and troubleshoot 429 exceptions
- Query performance tips for SDKs
