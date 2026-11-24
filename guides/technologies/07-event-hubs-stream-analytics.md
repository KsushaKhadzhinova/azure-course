# Azure Event Hubs и Azure Stream Analytics

## Что это и зачем

**Azure Event Hubs** - полностью управляемая (PaaS) платформа потоковой передачи данных в реальном времени. По описанию Microsoft, она может принимать миллионы событий в секунду с низкой задержкой и поддерживает протоколы Apache Kafka, AMQP 1.0 и HTTPS. Типичные сценарии: телеметрия IoT, логирование приложений, clickstream-аналитика, обработка финансовых транзакций и event sourcing. Event Hubs служит буфером и распределенным журналом событий: producer'ы пишут, consumer'ы читают независимо друг от друга ([docs/d0-azure-event-hubs-event-hubs-about.md](docs/d0-azure-event-hubs-event-hubs-about.md)).

**Azure Stream Analytics (ASA)** - полностью управляемый движок обработки потоков. Он читает данные из входов (чаще всего Event Hubs или IoT Hub), выполняет над ними SQL-подобный запрос с временными ограничениями и пишет результат в выходы (Blob Storage, Azure SQL Database, Data Lake Storage, Cosmos DB, Power BI и др.). По описанию Microsoft, ASA обрабатывает потоки с субмиллисекундными задержками и не требует провижининга инфраструктуры ([docs/d0-azure-stream-analytics-stream-analytics-introduction.md](docs/d0-azure-stream-analytics-stream-analytics-introduction.md)).

Вместе они образуют типовой конвейер: **источник -> Event Hubs -> Stream Analytics (запрос с окнами) -> хранилище или BI**. Учебный путь Microsoft по этой теме ("Implement a Data Streaming Solution with Azure Stream Analytics") описывает ASA как облачный движок для построения масштабируемых решений real-time аналитики ([pages/11-implement-data-streaming-asa.md](pages/11-implement-data-streaming-asa.md)).

## Архитектура и ключевые компоненты

### Event Hubs

| Компонент | Что делает (по источникам) |
|---|---|
| Producer applications | Отправляют события через Event Hubs SDK, Kafka-клиенты или HTTPS |
| Namespace | Контейнер для одного или нескольких event hub. На уровне namespace задаются streaming capacity, сетевая безопасность и geo-disaster recovery |
| Event hub (Kafka topic) | Append-only распределенный журнал, состоит из одной или нескольких partitions |
| Partitions | Упорядоченные последовательности событий; используются для масштабирования. Сравнение из документации: партиции - это полосы на шоссе, больше полос - выше пропускная способность |
| Consumer applications | Читают события по offset в каждой partition и сохраняют checkpoint |
| Consumer group | Независимое представление потока; каждая группа ведет собственную позицию чтения |
| Capture | Автоматическая запись потока в Blob Storage или Data Lake Storage |

Источники: [docs/d0-azure-event-hubs-event-hubs-about.md](docs/d0-azure-event-hubs-event-hubs-about.md), [docs/d1-azure-event-hubs-event-hubs-features.md](docs/d1-azure-event-hubs-event-hubs-features.md).

**Тиры (pricing tiers):** Basic, Standard, Premium, Dedicated. Масштабирование зависит от тира: в Standard используются throughput units (TU), в Premium - processing units (PU), в Dedicated - capacity units (CU) ([docs/d1-azure-event-hubs-event-hubs-quotas.md](docs/d1-azure-event-hubs-event-hubs-quotas.md)).

**Протоколы:** AMQP 1.0 (высокая пропускная способность, постоянные соединения, используется Azure SDK), Apache Kafka (существующие Kafka-приложения без изменения кода, достаточно переключить bootstrap server), HTTPS (только отправка, подходит для редкой низкообъемной публикации) ([docs/d1-azure-event-hubs-event-hubs-features.md](docs/d1-azure-event-hubs-event-hubs-features.md)).

### Stream Analytics

- **Job** - единица развертывания: содержит входы (inputs), запрос (query) и выходы (outputs).
- **Inputs** - Event Hubs, IoT Hub, Blob Storage / ADLS Gen2 (исторические данные), а также reference data из Blob Storage или SQL Database для lookup-соединений ([docs/d0-azure-stream-analytics-stream-analytics-introduction.md](docs/d0-azure-stream-analytics-stream-analytics-introduction.md)).
- **Outputs** - Blob Storage, Azure SQL Database, Data Lake Storage, Cosmos DB, Event Hubs, Power BI и другие. Полный список и параметры см. в документации по выходам.
- **Query** - SQL-подобный язык с временными расширениями (temporal constraints), агрегатами, геопространственными функциями, pattern matching и anomaly detection; поддерживаются также пользовательские функции JavaScript или C# (UDF) и user-defined aggregates ([docs/d0-azure-stream-analytics-stream-analytics-introduction.md](docs/d0-azure-stream-analytics-stream-analytics-introduction.md)).
- **Streaming units (SU)** - вычислительные ресурсы job'а (см. раздел "Безопасность и стоимость").
- **Среда выполнения** - облако или IoT Edge / Azure Stack; один и тот же язык запросов и инструменты.

## Основные понятия (glossary)

| Термин (English) | Определение |
|---|---|
| Namespace | Контейнер для event hubs, задает сетевые правила, capacity и geo-DR на уровне пространства имен ([event-hubs-about](docs/d0-azure-event-hubs-event-hubs-about.md)) |
| Event hub | Append-only журнал событий; аналог Kafka topic ([event-hubs-features](docs/d1-azure-event-hubs-event-hubs-features.md)) |
| Partition | Упорядоченная последовательность событий внутри event hub; единица параллелизма и порядка |
| Partition key | Значение, которое отправитель передает при публикации; статическая хеш-функция по нему выбирает partition. Без ключа используется round-robin ([scalability](docs/d1-azure-event-hubs-event-hubs-scalability.md)) |
| Offset | Позиция события внутри partition; курсор чтения ([features](docs/d1-azure-event-hubs-event-hubs-features.md)) |
| Consumer group | Независимое представление потока. У каждого event hub есть группа по умолчанию `$Default` ([features](docs/d1-azure-event-hubs-event-hubs-features.md)) |
| Checkpointing | Сохранение текущего offset, чтобы потребитель мог продолжить с места остановки. В AMQP это ответственность consumer'а ([features](docs/d1-azure-event-hubs-event-hubs-features.md)) |
| Epoch (exclusive) consumer | Потребитель, владеющий partition в группе; рекомендуемый режим для production AMQP ([scalability](docs/d1-azure-event-hubs-event-hubs-scalability.md)) |
| Throughput unit (TU) | Предоплаченная единица пропускной способности Standard: ingress до 1 MB/s или 1 000 событий/s, egress до 2 MB/s или 4 096 событий/s ([scalability](docs/d1-azure-event-hubs-event-hubs-scalability.md)) |
| Processing unit (PU) | Изолированный по CPU и памяти ресурс Premium ([scalability](docs/d1-azure-event-hubs-event-hubs-scalability.md)) |
| Capacity unit (CU) | Единица ресурса Dedicated-кластера ([quotas](docs/d1-azure-event-hubs-event-hubs-quotas.md)) |
| Auto-inflate | Автоматическое увеличение числа TU при росте нагрузки ([scalability](docs/d1-azure-event-hubs-event-hubs-scalability.md)) |
| Capture | Запись потока в Blob Storage или ADLS в формате Avro с окном по времени или размеру ([capture-overview](docs/d1-azure-event-hubs-event-hubs-capture-overview.md)) |
| Streaming unit (SU) | Вычислительный ресурс ASA job, объединяет CPU и память ([streaming-unit-consumption](docs/d1-azure-stream-analytics-stream-analytics-streaming-unit-consumption.md)) |
| SU V2 | Рекомендуемая модель SU: 1 SU V2 соответствует одному streaming node ([streaming-unit-consumption](docs/d1-azure-stream-analytics-stream-analytics-streaming-unit-consumption.md)) |
| SU % utilization | Метрика использования памяти job'а от 0% до 100% ([streaming-unit-consumption](docs/d1-azure-stream-analytics-stream-analytics-streaming-unit-consumption.md)) |
| Arrival time | Время поступления события на вход (например, `EventEnqueuedUtcTime` для Event Hubs) ([time-handling](docs/d2-azure-stream-analytics-stream-analytics-time-handling.md)) |
| Application time | Время создания события, задается полем в payload и выбирается через `TIMESTAMP BY` ([time-handling](docs/d2-azure-stream-analytics-stream-analytics-time-handling.md)) |
| Watermark | Порог времени, ниже которого ASA считает, что события уже пришли ([time-handling](docs/d2-azure-stream-analytics-stream-analytics-time-handling.md)) |
| Out-of-order tolerance | Допуск на перестановку событий внутри потока ([time-handling](docs/d2-azure-stream-analytics-stream-analytics-time-handling.md)) |
| Late arrival tolerance | Допуск на опоздание события относительно текущего времени; по умолчанию 5 секунд ([time-handling](docs/d2-azure-stream-analytics-stream-analytics-time-handling.md)) |
| Tumbling window | Непересекающиеся окна фиксированной длины; событие принадлежит ровно одному окну ([window-functions](pages/12-stream-analytics-window-functions.md)) |
| Hopping window | Окна фиксированной длины, которые сдвигаются на фиксированный шаг (hop) и могут перекрываться ([window-functions](pages/12-stream-analytics-window-functions.md)) |
| Sliding window | Выдает результат только когда содержимое окна меняется (событие входит или выходит); в каждом окне есть хотя бы одно событие ([window-functions](pages/12-stream-analytics-window-functions.md)) |
| Session window | Группирует события, пришедшие с небольшими интервалами; задается timeout, max duration и опционально partition key ([window-functions](pages/12-stream-analytics-window-functions.md)) |
| Snapshot window | Группирует события с одинаковой меткой времени; задается добавлением `System.Timestamp()` в `GROUP BY` ([window-functions](pages/12-stream-analytics-window-functions.md)) |
| Output error policy | Политика обработки ошибок преобразования данных на выходе: Retry (по умолчанию) или Drop ([output-error-policy](docs/d2-azure-stream-analytics-stream-analytics-output-error-policy.md)) |
| Parallel query | Запрос, в котором ключи партиционирования согласованы между входами, шагами и выходами ([parallelization](docs/d2-azure-stream-analytics-stream-analytics-parallelization.md)) |

## Как работает / типовые сценарии

### Event Hubs: жизненный цикл события

1. **Ingest.** Producer отправляет событие в event hub. Partition выбирается по partition key или round-robin.
2. **Store.** Событие хранится с настраиваемым retention. Retention по тирам: Basic - 1 день, Standard - 7 дней, Premium и Dedicated - 90 дней ([quotas](docs/d1-azure-event-hubs-event-hubs-quotas.md)). По истечении срока событие становится недоступным ([features](docs/d1-azure-event-hubs-event-hubs-features.md)).
3. **Process.** Consumer'ы читают partitions через consumer group. Event processor clients сами распределяют partitions и управляют checkpoint'ами ([features](docs/d1-azure-event-hubs-event-hubs-features.md)).

Ключевые правила параллелизма ([scalability](docs/d1-azure-event-hubs-event-hubs-scalability.md)):

- Одна partition внутри consumer group читается одним epoch-consumer'ом. Лишние экземпляры процессора простаивают.
- Non-epoch receivers могут читать одну partition одновременно до 5 штук, но это fan-out, а не рост пропускной способности.
- Kafka consumer group использует group coordination protocol (`group.id`); при входе или выходе участника происходит rebalance.
- Число партиций задает верхнюю границу параллельных consumer'ов в группе.
- Для Standard число партиций нельзя менять после создания; для Premium и Dedicated его можно увеличить, но не уменьшить. Смена партиций меняет распределение ключей, что важно, если нужен порядок событий.

### Stream Analytics: модель времени и окон

ASA работает с двумя видами времени ([time-handling](docs/d2-azure-stream-analytics-stream-analytics-time-handling.md)):

- **Arrival time** - по умолчанию. Подходит для архивации, когда временная логика не нужна. При использовании arrival time параметры out-of-order и late arrival игнорируются.
- **Application time** - задается в payload и выбирается через `TIMESTAMP BY` в запросе. Рекомендуется, если есть временная логика и задержки источника или сети.

Watermark: при каждом событии это максимальное наблюдаемое event time минус out-of-order tolerance. Если событий нет, это текущее оценочное arrival time минус late arrival tolerance. Событие, пришедшее с event time раньше watermark, либо отбрасывается, либо его время подтягивается до значения watermark (при этом меняется `System.Timestamp`, а поле event time остается прежним). Окно с ранним событием: фиксированный допуск 5 минут; события, пришедшие раньше этого порога, отбрасываются.

Окна (все результаты выдаются в **конце** окна; `System.Timestamp()` возвращает его метку времени) ([window-functions](pages/12-stream-analytics-window-functions.md)):

- **Tumbling** - сегменты без повторов и без перекрытия.
- **Hopping** - окна длиной N, сдвигающиеся на шаг M; при M равном длине окна получается tumbling.
- **Sliding** - выдает результат при каждом входе или выходе события из окна.
- **Session** - окно открывается первым событием и продлевается, пока события приходят внутри timeout; ограничено max duration. Partition key позволяет вести отдельные сессии для каждого пользователя или устройства.
- **Snapshot** - группировка по точной метке времени.

Ограничение: максимальный размер окна для stateful-операторов (windowed aggregates, temporal joins) - 7 дней ([streaming-unit-consumption](docs/d1-azure-stream-analytics-stream-analytics-streaming-unit-consumption.md)).

### Типовые сценарии из источников

- Real-time аналитика и дашборды: Event Hubs -> ASA -> Power BI ([docs/d0-azure-stream-analytics-stream-analytics-introduction.md](docs/d0-azure-stream-analytics-stream-analytics-introduction.md)).
- Холодный путь наряду с горячим: Capture пишет тот же поток в Blob/ADLS, а ASA обрабатывает его в реальном времени ([capture-overview](docs/d1-azure-event-hubs-event-hubs-capture-overview.md)).
- Цепочка заданий: выход одного ASA job через Event Hubs становится входом другого ([event-hubs-output](docs/d2-azure-stream-analytics-event-hubs-output.md)).
- Обогащение потока статическими данными через reference data (lookup-join) ([docs/d0-azure-stream-analytics-stream-analytics-introduction.md](docs/d0-azure-stream-analytics-stream-analytics-introduction.md)).
- Anomaly detection, геопространственная аналитика, предиктивное обслуживание (перечень сценариев в документации ASA).

## Практика (steps, commands, code only from sources)

Ниже только то, что приведено в загруженных материалах. Команд Azure CLI, PowerShell и JSON-шаблонов для создания Event Hubs в проанализированных файлах нет; в таких случаях см. официальные руководства.

### 1. Настройка input Event Hubs в ASA

Из документации по входам ASA ([deep/d2-azure-stream-analytics-stream-analytics-define-inputs.md](deep/d2-azure-stream-analytics-stream-analytics-define-inputs.md)) при создании input типа Event Hubs заполняются поля:

- Event Hub namespace и Event Hub name;
- **Event Hub consumer group** (рекомендуется отдельная группа для каждого job'а; если не указана, используется группа по умолчанию);
- **Partition key** (опционально; доступно только при compatibility level 1.2 и выше);
- **Event serialization format** - JSON, CSV или Avro.

Рекомендация из того же источника: если в job есть self-join или несколько входов, несколько читателей могут одновременно читать один вход, что влияет на число читателей в группе.

### 2. Запросы с окнами (из страницы окон Stream Analytics)

Tumbling (подсчет по часовому поясу, сегменты по 10 секунд) ([pages/12-stream-analytics-window-functions.md](pages/12-stream-analytics-window-functions.md)):

```
SELECT System.Timestamp() as WindowEndTime, TimeZone, COUNT(*) AS Count
FROM TwitterStream TIMESTAMP BY CreatedAt
GROUP BY TimeZone, TumblingWindow(second,10)
```

Ожидаемый вывод из примера: окна с метками 10:15:10 (count 5), 10:15:20 (count 2), 10:15:30 (count 4).

Hopping (окно 10 секунд, шаг 5 секунд):

```
SELECT System.Timestamp() as WindowEndTime, Topic, COUNT(*) AS Count
FROM TwitterStream TIMESTAMP BY CreatedAt
GROUP BY Topic, HoppingWindow(second,10,5)
```

Sliding (выводятся только окна, где COUNT(*) >= 3):

```
SELECT System.Timestamp() as WindowEndTime, Topic, COUNT(*) AS Count
FROM TwitterStream TIMESTAMP BY CreatedAt
GROUP BY Topic, SlidingWindow(second,10)
HAVING COUNT(*) >=3
```

Session (параметры: timeout 5 секунд, max duration 10 секунд):

```
SELECT System.Timestamp() as WindowEndTime, Topic, COUNT(*) AS Count
FROM TwitterStream TIMESTAMP BY CreatedAt
GROUP BY Topic, SessionWindow(second,5,10)
```

Snapshot (группировка по метке времени через `System.Timestamp()`):

```
SELECT System.Timestamp() as WindowEndTime, Topic, COUNT(*) AS Count
FROM TwitterStream TIMESTAMP BY CreatedAt
GROUP BY Topic, System.Timestamp()
```

### 3. Партиционирование запроса (параллелизм)

Из [docs/d2-azure-stream-analytics-stream-analytics-parallelization.md](docs/d2-azure-stream-analytics-stream-analytics-parallelization.md). Фильтр (простой запрос без ключа):

```
SELECT TollBoothId
FROM Input1 PARTITION BY PartitionId
```

Агрегация с ключом (для compatibility level 1.0 и 1.1; ключ партиции в `PARTITION BY`):

```
SELECT COUNT(*) AS Count, TollBoothId
FROM Input1 Partition By PartitionId
GROUP BY TumblingWindow(minute, 3), TollBoothId, PartitionId
```

Для compatibility level 1.2 и выше, как указано в источнике, достаточно указать колонку партиционирования в свойствах входа; `PARTITION BY` в запросе не обязателен. Для параллельности ключи должны совпадать у всех входов, шагов и выходов.

Многошаговый запрос с разными PARTITION BY:

```
WITH Step1 AS (
    SELECT COUNT(*) AS Count, TollBoothId, PartitionId
    FROM Input1 Partition By PartitionId
    GROUP BY TumblingWindow(minute, 3), TollBoothId, PartitionId
)
SELECT SUM(Count) AS Count, TollBoothId
FROM Step1 Partition By TollBoothId
GROUP BY TumblingWindow(minute, 3), TollBoothId
```

### 4. Выход в Event Hubs

Параметры output Event Hubs ([docs/d2-azure-stream-analytics-event-hubs-output.md](docs/d2-azure-stream-analytics-event-hubs-output.md)): partition key column (опционально), сериализация JSON, CSV или Avro, property columns, для CSV - разделитель (запятая, точка с запятой, пробел, табуляция, вертикальная черта), для JSON - формат Line separated. Для CSV и JSON поддерживается только UTF-8. Максимальный размер сообщения - 256 KB или 1 MB в зависимости от условий, см. limits Event Hubs.

### 5. Настройка времени и политик (портал)

- Event ordering в job: параметры **Out of order events** и **Events that arrive late** (значение по умолчанию для late arrival - 5 секунд).
- Error policy в разделе Settings: Retry (по умолчанию) или Drop ([output-error-policy](docs/d2-azure-stream-analytics-stream-analytics-output-error-policy.md)).

### 6. Масштабирование job

- Portal: job -> Configure -> **Scale**. По умолчанию при создании задается 1 SU ([streaming-unit-consumption](docs/d1-azure-stream-analytics-stream-analytics-streaming-unit-consumption.md)).
- Custom autoscale: пример правил из документации - увеличивать SU, когда средняя SU % utilization за последние 2 минуты выше 75%; уменьшать, когда за последние 15 минут ниже 30% ([autoscale](docs/d1-azure-stream-analytics-stream-analytics-autoscale.md)).

## Безопасность и стоимость

**Event Hubs** ([event-hubs-about](docs/d0-azure-event-hubs-event-hubs-about.md), [features](docs/d1-azure-event-hubs-event-hubs-features.md)):

- Аутентификация: Microsoft Entra ID с RBAC, Shared Access Signatures или Managed Identities.
- Сеть: Private Link, VNet service endpoints, IP-фильтрация.
- Шифрование: данные в покое - ключами Microsoft или customer-managed keys; данные в движении - TLS 1.2.
- SLA: до 99.99% в зависимости от тира и конфигурации.
- Availability zones (Premium и Dedicated) и geo-disaster recovery с синхронизацией метаданных.

**Квоты и тарифы** ([quotas](docs/d1-azure-event-hubs-event-hubs-quotas.md)):

- Basic: 1 consumer group на hub, 1 день retention, 32 партиции на hub, 100 brokered connections на namespace, максимальная публикация 256 KB, 10 event hubs на namespace.
- Максимум единиц масштабирования: 40 TU для Standard, 16 PU для Premium, 10 CU для Dedicated (больше - через запрос в поддержку).
- Standard: 20 consumer groups на hub, 7 дней retention, 32 партиции на hub, 40 TU, максимальная публикация 1 MB.
- Premium: 100 consumer groups на hub, 90 дней retention, макс. публикация 1 MB, 100 партиций на hub и не более 200 на PU в namespace, 16 PU.
- Dedicated: 1 000 consumer groups на hub, 90 дней retention, 1 024 партиции на hub, макс. публикация 20 MB.
- Один TU Standard: ingress 1 MB/s или 1 000 событий/s; egress 2 MB/s или 4 096 событий/s.
- Capture: в Basic не поддерживается; в Premium и Dedicated включен бесплатно; в Standard тарифицируется отдельно (в таблице квот - "Pay per hour"; в обзоре Capture сказано, что плата ежемесячная, по числу TU; при расчете сверяйтесь с актуальной ценой).
- Стоимость не зависит от числа партиций: важно число TU/PU/CU ([scalability](docs/d1-azure-event-hubs-event-hubs-scalability.md)).
- При превышении TU ingress троттлится с EventHubsException, Reason ServiceBusy.

**Stream Analytics** ([stream-analytics-introduction](docs/d0-azure-stream-analytics-stream-analytics-introduction.md), [streaming-unit-consumption](docs/d1-azure-stream-analytics-stream-analytics-streaming-unit-consumption.md)):

- TLS 1.2 для входящих и исходящих соединений; built-in checkpoints зашифрованы; входящие данные не хранятся, обработка в памяти. Поддерживаются Azure Virtual Networks при запуске в Stream Analytics Cluster.
- Гарантии: exactly-once обработка и at-least-once доставка, при этом exactly-once гарантируется для выбранных выходов (см. Event Delivery Guarantees в документации).
- Оплата за потребленные SU; нет предоплаты и провижининга кластера.
- SU V2 - 1 SU соответствует одному streaming node; дробные значения 1/3 и 2/3 доступны. SU V1 - 6 SU на один node (устаревает).
- Job работает в памяти: при нехватке памяти job падает. Для production следите за SU % utilization; при значениях выше 80% или при накоплении входного backlog нужно добавить SU.
- Для автомасштабирования за пределами 1 SU V2 требуется параллельная или embarrassingly parallel топология.
- Output error policy Retry блокирует обработку (событие повторяется до успеха без таймаута), Drop отбрасывает событие без возможности восстановить его.

## Частые вопросы для собеседования

**1. Чем partition отличается от consumer group?**
Partition - упорядоченная последовательность событий внутри event hub и единица параллелизма. Consumer group - независимое представление всего потока; несколько групп могут читать один event hub параллельно, каждая со своими offset. Внутри одной группы одну partition одновременно владеет один consumer ([features](docs/d1-azure-event-hubs-event-hubs-features.md), [scalability](docs/d1-azure-event-hubs-event-hubs-scalability.md)).

**2. Сколько параллельных consumer'ов может читать группу и почему?**
Максимум равен числу партиций, потому что каждая партиция назначается ровно одному consumer'у в группе. Лишние экземпляры простаивают до освобождения партиции ([scalability](docs/d1-azure-event-hubs-event-hubs-scalability.md)).

**3. Как гарантировать порядок событий одного устройства?**
Передавать partition key (например, ID устройства) в producer. Ключ хешируется в партицию, поэтому связанные события попадают в одну партицию и сохраняют порядок прибытия ([scalability](docs/d1-azure-event-hubs-event-hubs-scalability.md)).

**4. Что такое TU, PU и CU, и что происходит при превышении лимита?**
TU - единица Standard, PU - Premium, CU - Dedicated. При превышении ingress TU событие троттлится, клиент получает EventHubsException с Reason ServiceBusy. Auto-inflate может увеличить число TU автоматически ([scalability](docs/d1-azure-event-hubs-event-hubs-scalability.md), [quotas](docs/d1-azure-event-hubs-event-hubs-quotas.md)).

**5. Чем отличаются tumbling, hopping, sliding и session windows?**
Tumbling - непересекающиеся окна фиксированной длины. Hopping - окна фиксированной длины со сдвигом на шаг, могут перекрываться. Sliding - результат выдается при входе или выходе события из окна, в каждом окне минимум одно событие. Session - окно продлевается, пока события приходят внутри timeout, и ограничено max duration ([pages/12-stream-analytics-window-functions.md](pages/12-stream-analytics-window-functions.md)).

**6. Как ASA обрабатывает поздно пришедшие события?**
Используется watermark. Событие с event time ниже watermark либо отбрасывается, либо его метка подтягивается до watermark. Поле event time при этом не меняется, меняется `System.Timestamp`. Допуск late arrival по умолчанию 5 секунд. Использование arrival time делает out-of-order и late arrival настройки неактуальными ([time-handling](docs/d2-azure-stream-analytics-stream-analytics-time-handling.md)).

**7. Что такое SU % utilization и когда нужно масштабировать job?**
Это метрика потребления памяти job'а. Высокие значения (выше 80%) или накопление backlog во входах указывают на нехватку ресурсов. Нужно добавить SU, но сначала проверить, что запрос параллелен, потому что добавление SU не помогает непараллельному запросу ([streaming-unit-consumption](docs/d1-azure-stream-analytics-stream-analytics-streaming-unit-consumption.md)).

**8. Как Capture связан с Stream Analytics?**
Capture пишет тот же поток, что читает ASA, в Blob Storage или ADLS в формате Avro с окном по времени или размеру ("first wins"). Capture копирует данные напрямую из хранилища Event Hubs, поэтому не расходует egress-квоту, которая нужна читателям, в том числе Stream Analytics ([capture-overview](docs/d1-azure-event-hubs-event-hubs-capture-overview.md)).

## Источники

Использованные файлы (относительно базовой папки `azure-course`):

- `pages/11-implement-data-streaming-asa.md` - https://learn.microsoft.com/en-us/training/paths/implement-data-streaming-with-asa/
- `pages/12-stream-analytics-window-functions.md` - https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-window-functions
- `docs/d0-azure-event-hubs-event-hubs-about.md` - https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-about
- `docs/d0-azure-stream-analytics-stream-analytics-introduction.md` - https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-introduction
- `docs/d1-azure-event-hubs-event-hubs-features.md` - https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-features
- `docs/d1-azure-event-hubs-event-hubs-quotas.md` - https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-quotas
- `docs/d1-azure-event-hubs-event-hubs-scalability.md` - https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-scalability
- `docs/d1-azure-event-hubs-event-hubs-capture-overview.md` - https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-overview
- `docs/d1-azure-stream-analytics-stream-analytics-streaming-unit-consumption.md` - https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-streaming-unit-consumption
- `docs/d1-azure-stream-analytics-stream-analytics-autoscale.md` - https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-autoscale
- `docs/d2-azure-stream-analytics-stream-analytics-time-handling.md` - https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-time-handling
- `docs/d2-azure-stream-analytics-stream-analytics-parallelization.md` - https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-parallelization
- `docs/d2-azure-stream-analytics-stream-analytics-output-error-policy.md` - https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-output-error-policy
- `docs/d2-azure-stream-analytics-event-hubs-output.md` - https://learn.microsoft.com/en-us/azure/stream-analytics/event-hubs-output
- `deep/d2-azure-stream-analytics-stream-analytics-define-inputs.md` - https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-define-inputs

Пропущено:

- `docs/d2-azure-event-hubs-event-hubs-create.md` и `docs/d1-azure-stream-analytics-stream-analytics-quick-create-portal.md` - релевантны, но в них шаги создания описывают IoT Hub и Blob Storage (для quick-create); для текста раздела Практика они не использованы.
- `deep/d0-azure-stream-analytics-stream-analytics-window-functions.md` - дублирует `pages/12-stream-analytics-window-functions.md`.
- Файлы `d2-azure-stream-analytics-media-*.png` и подобные медиа-файлы - изображения, не текст.
- Примеры Azure CLI, PowerShell и ARM для создания Event Hubs в прочитанных файлах не найдены, поэтому таких команд в документе нет.
