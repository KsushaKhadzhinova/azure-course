# Azure Synapse Analytics

## Что это и зачем

**Azure Synapse Analytics** - корпоративный сервис аналитики, который объединяет хранилища данных (data warehouse) и аналитику больших данных (big data). По официальному описанию, Synapse собирает в одном месте SQL-технологии для корпоративных хранилищ, Spark-технологии для больших данных, **Data Explorer** для аналитики логов и временных рядов, **Pipelines** для интеграции данных и ETL/ELT, а также интеграцию с Power BI, CosmosDB и AzureML.

Ключевые возможности, которые перечислены в источниках:

- **Synapse SQL** - распределенная система запросов на T-SQL. Поддерживает две модели ресурсов: **serverless** (для непредсказуемых, "взрывных" нагрузок) и **dedicated** (зарезервированная вычислительная мощность для предсказуемой производительности и стоимости).
- **Apache Spark for Azure Synapse** - обработка данных, ETL и машинное обучение без ручного управления кластерами.
- **Единая работа с data lake**: таблицы, определенные поверх файлов в data lake, могут читать и SQL, и Spark. Файлы Parquet, CSV, TSV и JSON можно исследовать напрямую.
- **Встроенная интеграция данных**: движок и интерфейс те же, что у Azure Data Factory (см. раздел про pipelines).
- **Synapse Studio** - единый интерфейс для загрузки, исследования, подготовки, оркестрации и визуализации данных, а также мониторинга ресурсов, пользователей и использования.

Важное уточнение из официальной документации: тем, кто только начинает работать с data warehousing, Microsoft рекомендует начинать с **Microsoft Fabric Data Warehouse**, а существующие рабочие нагрузки dedicated SQL pool могут перейти в Fabric. Поэтому при изучении Synapse полезно понимать, какие части сервиса относятся к legacy-линейке (dedicated SQL pool), а какие остаются актуальными.

Data Explorer в составе Synapse указан как **preview**: его аналитический движок оптимизирован для логов и IoT-данных с автоматической индексацией свободного текста и полуструктурированных данных.

## Архитектура и ключевые компоненты

### Рабочая область (Synapse workspace) и Synapse Studio

Workspace - основная единица, в которой живут SQL-пулы, Spark-пулы, pipelines и ноутбуки. Все они управляются через Synapse Studio, где есть хабы Develop (SQL-скрипты, ноутбуки), Integrate (pipelines) и Monitor (мониторинг pipeline runs и других выполнений).

Workspace можно связать с Azure Virtual Network. Есть два варианта: обычный workspace и workspace с **managed virtual network** (см. раздел "Безопасность").

### Dedicated SQL pool (ранее SQL DW)

Dedicated SQL pool - это массово-параллельная (MPP) архитектура с разделением **compute и storage**:

- **Control node** - "мозг" архитектуры. Приложения подключаются именно к нему и отправляют T-SQL. Здесь работает distributed query engine, который оптимизирует запрос и разбивает его на параллельные операции.
- **Compute nodes** - выполняют параллельную обработку. Число compute nodes от **1 до 60** и определяется уровнем сервиса (service level). Данные пользователей хранятся в Azure Storage, а не на compute nodes.
- **Data Movement Service (DMS)** - внутренний транспорт, который перемещает данные между compute nodes, когда это нужно для корректного результата запроса.
- **Data warehouse unit (DWU)** - абстракция вычислительной мощности, единица масштабирования. Compute можно масштабировать независимо от объема данных, а приостанавливать без потери данных.
- **Distributions** - базовая единица хранения и параллельной обработки. Запрос делится на **60** маленьких запросов, каждый из которых выполняется на одной distribution. Compute node управляет одной или несколькими distributions: при максимальных ресурсах на каждый node приходится одна distribution, при минимальных все distributions находятся на одном node.

Способы распределения строк таблицы (sharding patterns), поддерживаемые источником: **Hash**, **Round Robin**, **Replicate**. Подробнее - в разделе "Как работает".

Официальные ресурсы для dedicated SQL pool в целом пересекаются с Fabric: по документации, dedicated SQL pool в Synapse workspace не использует logical SQL server, в отличие от "standalone" SQL DW.

### Serverless SQL pool

Каждый workspace содержит предустановленный serverless SQL pool с именем **Built-in**. Он не требует резервирования ресурсов: оплата идет за объем обработанных данных, а не за число узлов. Serverless SQL pool позволяет читать файлы в data lake через функцию **OPENROWSET** и создавать внешние таблицы (external tables). Функция OPENROWSET не поддерживается в dedicated SQL pool.

Serverless SQL pool можно использовать как "логическое хранилище" (logical data warehouse) - слой реляционного доступа поверх источников данных Azure.

### Apache Spark pool

Spark pool в Synapse - это **определение** (metadata), а не работающий кластер. Он описывает имя, размер, поведение масштабирования (scaling) и time to live. Пока пул не используется, ресурсы не потребляются и не тарифицируются. Spark instance создается при подключении к пулу, создании сессии и запуске задания. Для каждого пользователя создается отдельный instance.

### Pipelines (интеграция данных)

Pipelines в Synapse используют тот же data integration engine, что и Azure Data Factory. В pipelines доступны, например, Notebook activity, Spark jobs, stored procedures, SQL scripts и data flows. По документации, можно "принимать данные из 90+ источников" и создавать ETL-пайплайны без выхода из Synapse.

### Модель данных и хранения

Synapse читает и пишет в **Azure Data Lake Storage Gen2** (ADLS Gen2). Таблицы поверх файлов позволяют использовать одни и те же данные из SQL и Spark. Для Spark упомянута поддержка Delta Lake (Linux Foundation).

### Современная архитектура хранилища (modern data warehouse)

В загруженных материалах есть только программа учебного модуля "Explore fundamentals of large-scale analytics" (`modules/d0-training-modules-examine-components-of-modern-data-warehouse.md`): там перечислены темы - архитектура хранилища данных, ингест-пайплайны, аналитические хранилища данных и Microsoft Fabric. Содержания этих разделов (схем, сравнений, ролей сервисов) в crawl нет, поэтому описывать типовую схему "ingest - lake - warehouse - BI" по этим источникам мы не можем. В загруженных материалах нет подробностей об этом.

## Основные понятия (glossary)

| Термин (English) | Определение |
|---|---|
| Azure Synapse Analytics | Сервис аналитики, объединяющий SQL, Spark, Data Explorer, pipelines и интеграции с Power BI, CosmosDB и AzureML |
| Synapse workspace | Рабочая область, в которой создаются пулы, pipelines и ноутбуки |
| Synapse Studio | Веб-интерфейс workspace для разработки, оркестрации, мониторинга и безопасности |
| Dedicated SQL pool (formerly SQL DW) | MPP-хранилище с зарезервированными вычислительными ресурсами |
| Serverless SQL pool | Бессерверный SQL-движок, оплата за объем обработанных данных; встроенный пул называется Built-in |
| Spark pool | Определение Spark-окружения; Spark instance создается при подключении и запуске задания |
| Spark instance | Рабочий экземпляр Spark, создаваемый для пользователя при запуске сессии или задания |
| Control node | Узел dedicated SQL pool, который принимает запросы и координирует параллельное выполнение |
| Compute node | Узел, выполняющий параллельные части запроса; число от 1 до 60 |
| Data Movement Service (DMS) | Внутренний сервис передачи данных между compute nodes |
| Data warehouse unit (DWU) | Единица вычислительной мощности dedicated SQL pool |
| Distribution | Базовая единица хранения и параллельной обработки; запрос делится на 60 distributions |
| Hash distribution | Распределение строк по хэшу значения distribution column |
| Round-robin distribution | Равномерное распределение без оптимизации; удобно для staging-таблиц |
| Replicated table | Полная копия маленькой таблицы на каждом compute node |
| Clustered columnstore index | Индекс columnstore, используемый в примере создания таблицы dedicated SQL pool |
| OPENROWSET | Функция serverless SQL pool для чтения файлов из Azure Storage как набора строк |
| External table | Внешняя таблица, описывающая данные в data lake без их загрузки |
| External data source | Именованная ссылка на хранилище, например на ADLS Gen2 |
| COPY statement | Рекомендуемая команда массовой загрузки данных в dedicated SQL pool |
| Data flow | Визуальное (code-free) преобразование данных в pipelines |
| Managed virtual network | Виртуальная сеть, которой управляет Synapse; создается при создании workspace и неизменяема |
| Managed private endpoint | Приватная конечная точка, доступная только в workspace с managed virtual network |
| IP firewall rule | Правило разрешения или запрета доступа к workspace по IP-адресу |
| Data Explorer pool | Пул для аналитики логов и временных рядов (в источниках указан как preview) |
| Microsoft Fabric Data Warehouse | Более новый корпоративный warehouse на data lake, к которому Microsoft рекомендует переходить |

## Как работает / типовые сценарии

**1. Исследование файлов в data lake (serverless SQL).** Пользователь открывает SQL-скрипт в Develop hub и читает Parquet-файл через OPENROWSET с указанием BULK-пути на ADLS Gen2. Для исследования можно работать в системной базе master, но для пользовательских объектов нужна отдельная база данных (см. раздел "Практика"). Если нужны external data sources и учетные данные, создается отдельная база.

**2. Загрузка в dedicated SQL pool.** Для массовой загрузки рекомендуется команда **COPY**: она позволяет загружать данные с меньшими привилегиями, не открывая ключи учетной записи хранения (используется SAS), задавать соответствие колонок, wildcards и отдельное расположение для ERRORFILE (REJECTED_ROW_LOCATION). Для staging-таблиц источник рекомендует **round-robin**, потому что загрузка в такую таблицу быстрая.

**3. Выбор распределения таблицы в dedicated SQL pool.** По источнику:
- **Hash** - обеспечивает наивысшую производительность для joins и агрегаций на больших таблицах. Важен выбор distribution column (distinctness, data skew, типы запросов).
- **Round robin** - простейший вариант; joins требуют перетасовки данных (reshuffling), что занимает дополнительное время.
- **Replicate** - быстрее всего для маленьких таблиц, но занимает место на каждом node и замедляет запись; для больших таблиц непрактичен.

**4. Spark для подготовки данных.** Пул создается маленьким для разработки и отладки, а большим - для production-нагрузок (рекомендация из документации Spark). Пользователи могут иметь доступ к разным пулам. Если у пула недостаточно capacity, notebook-задание отклоняется, а batch-задание ставится в очередь.

**5. Оркестрация через pipelines.** Типовой сценарий из туториала: в Integrate hub создается pipeline, в его дизайнере добавляется Notebook activity, которому назначается ноутбук workspace; через Add trigger создается расписание (пример - "every 1 hour"); после Publish All pipeline можно запустить вручную через Trigger now, а выполнение отслеживать в Monitor hub (Pipeline runs, список или Gantt).

**6. Логическое хранилище (logical data warehouse).** Serverless SQL pool позволяет создать поверх data lake внешние таблицы и представления для BI-инструментов (например, Power BI). Native external tables по документации работают быстрее, чем внешние таблицы с TYPE=HADOOP. Для dedicated SQL pool native external tables доступны только для Parquet и помечены как public preview; CSV и ORC требуют Hadoop external tables.

## Практика

Ниже - только фрагменты, которые есть в загруженных источниках. Имена учетных записей и пути - примеры из документации; пароли из источников намеренно не воспроизводятся.

**Чтение Parquet-файла через serverless SQL pool** (источник: `docs/d2-azure-synapse-analytics-get-started-analyze-sql-on-demand.md`, URL `.../get-started-analyze-sql-on-demand`; в примере используется учетная запись `contosolake`):

```sql
SELECT
    TOP 100 *
FROM
    OPENROWSET(
        BULK 'https://contosolake.dfs.core.windows.net/users/NYCTripSmall.parquet',
        FORMAT='PARQUET'
    ) AS [result]
```

**Создание отдельной базы для пользовательских объектов** (источник: тот же файл). Важно использовать collation с суффиксом `_UTF8`, так как он нужен для корректной конвертации UTF-8 в VARCHAR; документация отмечает, что `Latin1_General_100_BIN2_UTF8` дает лучшую производительность при чтении Parquet и Azure Cosmos DB:

```sql
CREATE DATABASE DataExplorationDB
    COLLATE Latin1_General_100_BIN2_UTF8
```

**Внешний источник данных** (источник: тот же файл). Учетные данные можно не создавать: тогда используется identity вызывающего пользователя.

```sql
CREATE EXTERNAL DATA SOURCE ContosoLake
WITH ( LOCATION = 'https://contosolake.dfs.core.windows.net')
```

**Чтение по относительному пути через data source** (источник: тот же файл):

```sql
SELECT
    TOP 100 *
FROM
    OPENROWSET(
            BULK '/users/NYCTripSmall.parquet',
            DATA_SOURCE = 'ContosoLake',
            FORMAT='PARQUET'
    ) AS [result]
```

**Права для загрузки COPY** (источник: `docs/d2-azure-synapse-analytics-sql-data-warehouse-quickstart-bulk-load-copy-tsql.md`, URL `.../sql-data-warehouse/quickstart-bulk-load-copy-tsql`; плейсхолдеры `<yourusername>` и `<yourtable>` заменяются вручную):

```sql
GRANT CREATE TABLE TO <yourusername>;
GRANT ALTER ON SCHEMA::dbo TO <yourusername>;
GRANT ADMINISTER DATABASE BULK OPERATIONS TO <yourusername>;
GRANT INSERT ON <yourtable> TO <yourusername>;
```

**Создание целевой таблицы с round-robin и columnstore** (тот же источник; показаны первые колонки и опции таблицы, полный список колонок - в источнике):

```sql
CREATE TABLE [dbo].[Trip]
(
    [DateID] int NOT NULL,
    [MedallionID] int NOT NULL,
    [HackneyLicenseID] int NOT NULL,
    [PickupTimeID] int NOT NULL,
    [DropoffTimeID] int NOT NULL
    -- ... остальные колонки см. источник
)
WITH
(
    DISTRIBUTION = ROUND_ROBIN,
    CLUSTERED COLUMNSTORE INDEX
);
```

**Загрузка через COPY** (тот же источник; пример загружает CSV с разделителем `|`):

```sql
COPY INTO [dbo].[Trip] FROM 'https://nytaxiblob.blob.core.windows.net/2013/Trip2013/'
WITH (
   FIELDTERMINATOR='|',
   ROWTERMINATOR='0x0A'
) OPTION (LABEL = 'COPY: dbo.trip');
```

**Расчет стоимости Spark pool** (текстовый пример из `docs/d2-azure-synapse-analytics-spark-apache-spark-concepts.md`, URL `.../spark/apache-spark-concepts`). Пул из 20 medium-узлов по 8 vCores дает 20 x 8 = 160 vCores; при времени работы около 20 минут расчет в источнике: 160 x 0.3 часа = 48 vCore hours.

**Создание Spark pool и pipeline** выполняется через Azure portal и Synapse Studio. Официальные туториалы (`docs/d2-azure-synapse-analytics-get-started-pipelines.md`, `deep/d2-azure-synapse-analytics-quickstart-create-apache-spark-pool-portal.md`) описывают эти шаги текстом, без CLI-команд. Для Spark pool в источнике упомянуто, что его создание и настройка доступны через portal, а PowerShell-cmdlet `New-AzSynapseSqlPool` (модуль Az.Synapse) - для dedicated SQL pool в workspace. Масштабирование dedicated SQL pool делается через portal (Workload management) или cmdlet `Update-AzSynapseSqlPool`; конкретный пример команды в загруженных материалах не приведен полностью.

## Безопасность и стоимость

### Безопасность

- **Role-based access control (RBAC)** - упоминается в обзоре как способ упростить доступ к аналитическим ресурсам. Права на Spark pools могут назначаться отдельно, так что одни пользователи видят один пул, другие - другой.
- **Managed virtual network** - при создании workspace можно включить Managed workspace Virtual Network, которым управляет Synapse. Преимущества по источнику: не нужно настраивать inbound NSG-правила для management traffic, не нужна подсеть под пиковую нагрузку Spark, а вместе с managed private endpoints защита от data exfiltration. Важно: **эту конфигурацию нельзя изменить после создания workspace**. Data integration и Spark-ресурсы развертываются внутри такой сети; у каждого Spark-кластера своя подсеть. Dedicated SQL pool и serverless SQL pool являются multitenant и находятся вне managed VNet; связь с ними идет через Azure private links, которые создаются автоматически.
- **IP firewall rules** - правила разрешают или запрещают доступ по IP-адресу запроса. Правила на уровне workspace действуют на все публичные endpoints (dedicated SQL pools, serverless SQL pool и development). Максимум - **128 правил**. Опция "Allow Azure Services and resources to access this workspace" считается одним правилом, но по документации разрешает подключения из Azure, включая подписки других клиентов, поэтому нужно строго ограничивать права логинов. Создание IP-правил через portal при создании workspace доступно только для workspace **без** managed VNet.
- **Внешний доступ к данным** - external tables в protected storage работают через SAS credential, Microsoft Entra identity или managed identity workspace. COPY не требует раскрытия ключей учетной записи хранения (используется SAS).

### Стоимость

- **Serverless SQL pool** - оплата за объем данных, обработанных запросом, а не за число узлов.
- **Dedicated SQL pool** - оплачиваются **data warehouse units** и хранение данных, и эти ресурсы тарифицируются отдельно. Пока compute приостановлен, оплачивается только хранение; возобновить compute можно в любой момент. Масштабирование DWU меняет расход. Документация также предупреждает, что создание dedicated SQL pool может стать новым платным сервисом.
- **Spark pool** - создание определения пула не тарифицируется. Billing для Spark instances начинается при запуске виртуальных машин и прекращается, когда instances переходят в состояние terminating. Биллинг prorated per minute, поэтому источник советует выключать instance после работы или ставить короткий timeout. Для маленьких пулов для разработки и больших для production рекомендуется разделять.
- Точные цены, регионально зависящие, в загруженных материалах не приведены (они указаны на странице Azure Synapse Analytics pricing, которая в crawl не загружена). Конкретные тарифы в этом документе не указываются.

## Частые вопросы для собеседования

**1. В чем разница между serverless и dedicated SQL pool?**
Serverless SQL pool не требует резервирования ресурсов: он оплачивается за объем обработанных данных и подходит для непредсказуемых нагрузок, исследования файлов в data lake и создания внешних таблиц. Dedicated SQL pool резервирует вычислительную мощность (DWU) и подходит для предсказуемой производительности и больших хранилищ с распределенными таблицами. Источники: `pages/10-synapse-analytics-overview.md`, `deep/d2-azure-synapse-analytics-get-started-analyze-sql-on-demand.md`.

**2. Что такое distribution и какие способы распределения существуют?**
Distribution - базовая единица хранения и параллельной обработки; запрос делится на 60 параллельных подзапросов. Таблицы распределяются по способам Hash, Round Robin и Replicate. Hash дает лучшую производительность для joins и агрегаций на больших таблицах, round robin - быструю загрузку для staging, replicate - для маленьких таблиц. Источник: `docs/d1-azure-synapse-analytics-sql-data-warehouse-massively-parallel-processing-mpp-architecture.md`.

**3. Как устроена архитектура dedicated SQL pool?**
Приложения подключаются к control node, который оптимизирует запрос и передает работу compute nodes (от 1 до 60). Данные хранятся в Azure Storage, поэтому compute и storage разделены; Data Movement Service перемещает данные между узлами. Источник: тот же файл.

**4. Почему для загрузки в dedicated SQL pool рекомендуют COPY?**
Потому что он позволяет загружать данные пользователям с меньшими привилегиями, не открывая ключи учетной записи хранения (используется SAS), поддерживает wildcards, несколько файлов, пользовательскую обработку строк и колонок и отдельное расположение ошибок (REJECTED_ROW_LOCATION). Источник: `docs/d2-azure-synapse-analytics-sql-data-warehouse-quickstart-bulk-load-copy-tsql.md`.

**5. Что такое Spark pool и когда создается Spark instance?**
Spark pool - это определение с параметрами (имя, размер, масштабирование, time to live), которое ничего не потребляет, пока не используется. Spark instance создается при подключении к пулу, создании сессии и запуске задания, и для каждого пользователя создается отдельный instance. Источник: `docs/d2-azure-synapse-analytics-spark-apache-spark-concepts.md`.

**6. Чем Synapse pipelines отличаются от Azure Data Factory?**
Движок и интерфейс pipelines в Synapse те же, что в ADF, но есть различия: ADF поддерживает cross-region integration runtime для data flows, sharing integration runtime, Power Query activity, global parameters и деплой ARM-шаблонами; в Synapse нет этих возможностей, зато есть мониторинг Spark jobs для data flow через Synapse Spark pools. Источник: `docs/d2-azure-synapse-analytics-data-integration-concepts-data-factory-differences.md`.

**7. Что нельзя изменить в Synapse workspace после создания?**
Конфигурацию managed virtual network: нельзя добавить или убрать ее у существующего workspace. Источник: `docs/d1-azure-synapse-analytics-security-synapse-workspace-managed-vnet.md`.

**8. Чем Synapse отличается от Microsoft Fabric Data Warehouse?**
По официальным источникам, Fabric Data Warehouse - это более новый enterprise-warehouse на data lake, и для новых проектов Microsoft советует начинать именно с него, а существующие dedicated SQL pool нагрузки могут перейти в Fabric. Подробного сравнения архитектур в загруженных материалах нет. Источники: `docs/d1-azure-synapse-analytics-sql-data-warehouse-massively-parallel-processing-mpp-architecture.md`, `pages/10-synapse-analytics-overview.md`.

## Источники

Все файлы лежат в базовой папке курса (`azure-course`); пути относительны к ней.

- `pages/10-synapse-analytics-overview.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is (обзор; в файле есть баннер "Access to this page requires authorization", основной текст доступен)
- `docs/d1-azure-synapse-analytics-overview-what-is.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is (дубликат обзора)
- `docs/d1-azure-synapse-analytics-sql-data-warehouse-massively-parallel-processing-mpp-architecture.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/massively-parallel-processing-mpp-architecture
- `docs/d1-azure-synapse-analytics-sql-overview-difference-between-formerly-sql-dw-workspace.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/overview-difference-between-formerly-sql-dw-workspace
- `docs/d2-azure-synapse-analytics-sql-data-warehouse-create-data-warehouse-portal.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/create-data-warehouse-portal (биллинг DWU, pause и resume)
- `docs/d2-azure-synapse-analytics-sql-data-warehouse-quickstart-bulk-load-copy-tsql.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/quickstart-bulk-load-copy-tsql
- `docs/d2-azure-synapse-analytics-sql-data-warehouse-sql-data-warehouse-restore-active-paused-dw.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-restore-active-paused-dw (только для standalone dedicated SQL pool; использовано минимально)
- `docs/d2-azure-synapse-analytics-spark-apache-spark-concepts.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/spark/apache-spark-concepts
- `deep/d2-azure-synapse-analytics-quickstart-create-apache-spark-pool-portal.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/quickstart-create-apache-spark-pool-portal
- `docs/d2-azure-synapse-analytics-get-started-analyze-sql-on-demand.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/get-started-analyze-sql-on-demand
- `deep/d2-azure-synapse-analytics-sql-develop-openrowset.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/develop-openrowset
- `deep/d2-azure-synapse-analytics-sql-create-use-external-tables.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/create-use-external-tables
- `docs/d2-azure-synapse-analytics-get-started-pipelines.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/get-started-pipelines
- `docs/d2-azure-synapse-analytics-data-integration-concepts-data-factory-differences.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/data-integration/concepts-data-factory-differences
- `docs/d1-azure-synapse-analytics-security-synapse-workspace-managed-vnet.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/security/synapse-workspace-managed-vnet
- `docs/d2-azure-synapse-analytics-security-synapse-workspace-ip-firewall.md` - https://learn.microsoft.com/en-us/azure/synapse-analytics/security/synapse-workspace-ip-firewall
- `modules/d0-training-modules-examine-components-of-modern-data-warehouse.md` - https://learn.microsoft.com/en-us/training/modules/examine-components-of-modern-data-warehouse (только программа модуля, без содержания)

Пропущено или использовано минимально:
- Материалы по Synapse Link (Cosmos DB), Stream Analytics output в Synapse, Databricks-интеграции и Data Explorer pool (`deep/d1-azure-synapse-analytics-data-explorer-data-explorer-create-pool-studio.md` и связанные) - найдены в crawl, но не открывались: в документе Data Explorer описан только по обзору.
- Файлы по загрузке, pools и workspace (`create-workspace`, `sql-create-use-views`, `sql-query-parquet-files` и др.) найдены по именам, но не открывались.
- В crawl нет материалов по `explore-data-warehouse-analytics` в `deep\`: файла с таким именем не найдено. Программа `modules\d0-training-modules-examine-components-of-modern-data-warehouse.md` содержит только оглавление.
