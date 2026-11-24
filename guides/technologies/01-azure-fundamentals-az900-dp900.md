# Azure Fundamentals (AZ-900) и Data Fundamentals (DP-900)

## Что это и зачем

AZ-900 (Microsoft Azure Fundamentals) и DP-900 (Microsoft Azure Data Fundamentals) - вводные курсы Microsoft, которые дают базовые знания об облачных концепциях, архитектуре Azure, управлении и governance, а также о данных: реляционных и нереляционных, аналитике и потоковой обработке. Курс DP-900T00 описан как введение в основные концепции данных и связанные сервисы данных Azure; курс рассчитан на начинающих и связан с сертификацией Microsoft Certified: Azure Data Fundamentals [1].

Серия Introduction to Cloud Infrastructure состоит из четырех учебных путей и прямо соотнесена с экзаменом AZ-900: Describe cloud concepts, Describe Azure architecture and services, Describe Azure management and governance и Apply Azure skills in guided projects [3][4][5]. Пути для DP-900 (Core data concepts, Relational data, Non-relational data, Analytics) ведут к сертификации Azure Data Fundamentals [6][7][8][9].

Важное ограничение: загруженные страницы в основном содержат структуру курсов, список модулей и цели обучения. Полные тексты описаний AZ-900 о моделях облака, модели shared responsibility, регионах и ценообразовании в них представлены лишь частично. Такие пробелы в документе отмечены явно.

## Архитектура и ключевые компоненты

### Модели облачных сервисов (IaaS, PaaS, SaaS)

Материалы описывают три типа облачных сервисов на примере SQL-сервисов Azure [19]:

- IaaS: SQL Server on Azure Virtual Machines. Виртуальная машина в Azure с установленным SQL Server. Такой подход виртуализирует инфраструктуру (compute, storage, networking) и подходит для lift and shift миграции.
- PaaS: Azure SQL Managed Instance и Azure SQL Database. Для Managed Instance автоматизированы обновления ПО, резервное копирование и другие задачи обслуживания. Azure SQL Database описан как полностью управляемый и масштабируемый PaaS-сервис.
- SaaS: Microsoft Fabric описан как унифицированная SaaS-платформа аналитики, объединяющая хранение, data engineering, data warehousing и отчетность в одном workspace [14].

Azure Cosmos DB описан как полностью управляемый NoSQL-сервис, то есть PaaS. Microsoft берет на себя provisioning серверов, патчинг, обновления и резервное копирование [18].

### Иерархия управления: Azure Resource Manager

Azure Resource Manager (ARM) - служба развертывания и управления Azure. Она принимает запросы из API, инструментов и SDK, аутентифицирует и авторизует их, затем передает нужному сервису. Все возможности портала доступны и через PowerShell, Azure CLI, REST API и SDK [20].

Уровни области управления (scope), от верхнего к нижнему [20]:

1. Management groups (группы управления).
2. Subscriptions (подписки).
3. Resource groups (группы ресурсов).
4. Resources (ресурсы).

Настройки, применённые на верхнем уровне, наследуются нижними. Например, политика, назначенная на подписку, действует на все её resource groups и ресурсы [20].

### Management groups

Management groups - governance-уровень над подписками. Условия, применённые к группе управления, наследуются всеми подписками внутри неё [22]:

- В одном каталоге может быть до 10 000 management groups.
- Дерево management groups поддерживает до шести уровней вложенности (без учета корня и уровня подписки).
- У каждой группы и подписки может быть только один родитель.
- Все подписки и группы в одном каталоге образуют единую иерархию с корнем - root management group.
- По умолчанию корень называется "Tenant root group", его ID совпадает с Microsoft Entra tenant ID.
- Новые подписки по умолчанию попадают в корневую группу.
- Назначение роли на management group наследуется всем подпискам и ресурсам под ней, например роль VM Contributor даёт права на все VM в иерархии [22].

### Resource groups и ресурсы

Resource group - контейнер для связанных ресурсов решения. Основные правила [20]:

- Все ресурсы группы должны иметь общий жизненный цикл: их развертывают, обновляют и удаляют вместе.
- Каждый ресурс может находиться только в одной resource group.
- Ресурсы могут находиться в регионах, отличных от региона группы, но рекомендуется использовать один регион.
- Теги, назначенные группе, не наследуются ресурсами внутри неё.
- Удаление resource group удаляет все ресурсы в ней.
- В одной resource group можно развернуть до 800 экземпляров каждого типа ресурса; некоторые типы из этого лимита исключены.
- Ресурс может подключаться к ресурсам в других группах, например веб-приложение к базе данных в другой группе.

Регион resource group определяет, где хранятся её метаданные. Это важно для требований соответствия (compliance). Control-plane операции маршрутизируются через регион группы, но data-plane запросы к ресурсам идут напрямую к их endpoint-ам [20].

### Регионы, зоны доступности и резервирование

Понятия регион, Availability Zone и region pair в загруженных материалах раскрыты в основном через резервирование Azure Storage и отказоустойчивость Resource Manager:

- Availability Zone - физически разделённое место внутри региона. Zone-redundant storage (ZRS) синхронно реплицирует данные по трём availability zones в основном регионе [17].
- Region pair - для аккаунта хранения Azure назначает парный вторичный регион на основе region pairs [17].
- Resource Manager использует availability zones и резервный регион (backup region) для повышения устойчивости обработки запросов [20].

Подробной схемы регионов Azure и модели shared responsibility в загруженных материалах нет.

### Хранилища и базы данных

Azure Storage хранит данные в трёх копиях в основном регионе, а варианты резервирования задают доступность, долговечность и стоимость [17]. Azure Cosmos DB организован в иерархии: account -> database -> container -> items [18]. Azure SQL - семейство сервисов на основе SQL Server: SQL Server on VM (IaaS), Managed Instance и SQL Database (PaaS) [19].

### Аналитические компоненты

Типовая архитектура аналитики включает ingestion и обработку, аналитическое хранилище, аналитическую модель и визуализацию [15]:

- Ingestion и обработка: данные из транзакционных хранилищ, файлов и потоков загружаются в data lake или реляционный data warehouse через ETL или ELT. Обработка часто выполняется распределёнными системами на multi-node кластерах. Ingestion включает batch-обработку статичных данных и real-time обработку потоков [15].
- Аналитическое хранилище: relational data warehouse, file-based data lake или data lakehouse [15].
- Аналитическая модель: semantic model (tabular модель, на которой работают Power BI и Microsoft Fabric) [15][14].
- Визуализация: отчеты, дашборды, интерактивные среды для исследования данных [15].

Azure предоставляет две основные платформы для крупномасштабной аналитики: Microsoft Fabric и Azure Databricks [15].

## Основные понятия (glossary)

| Термин (English) | Определение |
|---|---|
| Azure Resource Manager (ARM) | Служба развертывания и управления Azure; единый слой для запросов из портала, CLI, PowerShell, REST и SDK [20]. |
| Subscription | Область управления и биллинга, в которой размещаются ресурсы; на уровне подписки применяются политики и назначения ролей [20][22]. |
| Management group | Группа управления над подписками; наследует политики и назначения ролей вниз по иерархии [22]. |
| Root management group | Единственная корневая группа каталога, в которую входят все группы и подписки; по умолчанию называется Tenant root group [22]. |
| Resource group | Контейнер связанных ресурсов с общим жизненным циклом; каждый ресурс находится только в одной группе [20]. |
| Resource | Управляемый объект Azure: виртуальная машина, storage account, веб-приложение, база данных, виртуальная сеть и т. д. [20]. |
| Resource provider | Сервис, поставляющий ресурсы Azure, например Microsoft.Compute для виртуальных машин [20]. |
| Tag | Метка для логической организации ресурсов и группировки затрат; не наследуется ресурсами от группы [20]. |
| Declarative syntax / ARM template / Bicep | Декларативное описание желаемой инфраструктуры. ARM-шаблон - JSON-файл, Bicep - язык для декларативного развертывания [20]. |
| Azure Policy | Сервис оценки ресурсов на соответствие бизнес-правилам (policy definitions) и применения эффектов [21]. |
| Policy definition | Бизнес-правило в JSON-формате с условиями и эффектом [21]. |
| Initiative (policySet) | Набор policy definitions, объединённых под общую цель [21]. |
| Policy assignment | Назначение definition или initiative на scope: management group, subscription, resource group или ресурс [21]. |
| Effect | Реакция политики на несоответствующий ресурс: deny, audit, auditIfNotExists, modify, deployIfNotExists и др. [21]. |
| Availability Zone | Физически разделённое место внутри региона Azure, используемое для отказоустойчивости [17]. |
| LRS / ZRS / GRS / GZRS | Варианты резервирования Azure Storage: локальное, зональное, геореплицируемое и геозональное [17]. |
| RPO (recovery point objective) | Интервал между последней записью в основной регион и последней записью в вторичный регион [17]. |
| Relational database | База с таблицами, первичными ключами и SQL; данные нормализуются, чтобы не дублировать значения [12]. |
| Nonrelational database (NoSQL) | Система без реляционной схемы: key-value, document, column family и graph [12]. |
| Structured / semi-structured / unstructured data | Структурированные данные имеют фиксированную схему, полуструктурированные (например, JSON) допускают вариации, неструктурированные (документы, изображения, аудио, видео) не имеют структуры [10]. |
| BLOB | Бинарный большой объект, например изображение, видео, аудио или документ [11]. |
| Parquet / Avro | Оптимизированные файловые форматы: Parquet - колоночный, Avro - строковый [11]. |
| Delta Lake | Открытый формат хранения поверх Parquet с журналом транзакций, обеспечивающий ACID, версионность и надежные обновления в data lake [11][14]. |
| OLTP | Online Transactional Processing: высоконагруженные транзакционные системы с операциями CRUD и семантикой ACID [13]. |
| ACID | Atomicity, Consistency, Isolation, Durability: свойства надежной транзакции [13]. |
| OLAP / semantic model | Агрегированная модель для аналитики с предвычисленными мерами по измерениям [14][15]. |
| Data lake | Файловое хранилище для больших объемов данных, часто в формате файлов [14]. |
| Data warehouse | Реляционное хранилище, оптимизированное для запросов и отчетности [14]. |
| Data lakehouse | Гибрид data lake и data warehouse: гибкое хранение файлов и реляционная семантика запросов [14]. |
| ETL / ELT | Extract, Transform, Load (трансформация до загрузки) и Extract, Load, Transform (трансформация после загрузки) [14][15]. |
| Medallion architecture | Слои Bronze (сырые данные), Silver (очищенные и приведённые к единому виду), Gold (агрегированные, готовые для бизнеса) [14]. |
| Batch processing | Обработка статичных, накопленных данных порциями [15]. |
| Stream processing | Непрерывная обработка событий по мере их поступления; запрос выполняется постоянно (perpetual query) [16]. |
| Windowing | Агрегация событий по временным окнам, например число показаний датчика в минуту [16]. |
| Event Hubs | Сервис приёма больших объемов событий; внутри раздела порядок сохраняется, гарантия доставки - at-least-once [16]. |
| Eventstream / Eventhouse / KQL | Компоненты Fabric Real-Time Intelligence: приём и маршрутизация потоков, БД для событий временных рядов и язык запросов Kusto Query Language [16]. |
| Azure Stream Analytics | PaaS-сервис для потоковых заданий: приём, perpetual query и вывод результатов [16]. |
| Request Unit (RU/s) | Единица пропускной способности Cosmos DB; примерно стоимость чтения одного элемента 1 КБ по ID и partition key [18]. |
| Partition key | Свойство, по которому данные распределяются по логическим разделам; каждый логический раздел до 20 ГБ [18]. |
| Semantic model / DAX | Табличная модель с мерами, написанными на DAX (Data Analysis Expressions) [15]. |

## Как работает / типовые сценарии

### Управление и наследование политик

Policy оценивает ресурсы, сравнивая их свойства с бизнес-правилами [21]. Типовые сценарии из материалов [21]:

- разрешить развертывание ресурсов только в допустимых регионах;
- принудительно применять таксономические теги;
- требовать отправки диагностических логов в Log Analytics workspace;
- блокировать действия по identity, например требовать MFA.

Оценка выполняется при создании или обновлении ресурса в scope с назначением, при новом назначении, при изменении назначенной политики и по стандартному циклу соответствия раз в 24 часа [21]. Политика наследуется вниз по иерархии, а исключения (notScopes) позволяют вывести подресурс из области назначения [21].

Azure Policy и Azure RBAC различаются: Policy проверяет состояние ресурса независимо от того, кто его меняет, а RBAC управляет действиями пользователей на разных scope. Даже если пользователь имеет право на действие, Policy блокирует создание или изменение, если результат не соответствует правилам [21].

### Иерархия подписок и доступ

Одно назначение роли на management group позволяет пользователю получить доступ ко всем подпискам внутри неё, вместо скриптов RBAC по каждой подписке [22]. Политика, ограничивающая регионы для VM, применённая к группе Corp, наследуется всеми подписками её потомков [22].

### Аналитический поток: от источника до отчета

Типовой конвейер аналитики [14][15]: данные из операционных систем извлекаются и загружаются в data lake (ETL или ELT), затем структурируются в таблицы data warehouse или lakehouse, агрегируются в semantic model и, наконец, используются для отчетов и дашбордов. Data scientists работают с файлами в data lake, аналитики запрашивают таблицы warehouse, а бизнес-пользователи потребляют агрегированные данные модели [14].

### Потоковая обработка

Типовой поток событий [16]:

1. Событие генерирует данные (сигнал датчика, сообщение, запись в лог).
2. Данные попадают в streaming source (например, Event Hubs, IoT Hub, Kafka или папка в ADLS Gen2).
3. Perpetual query выбирает, проецирует или агрегирует события, например по окнам.
4. Результат пишется в sink: файл, таблицу, real-time дашборд или очередь для downstream-обработки.

Варианты реализации: Microsoft Fabric Real-Time Intelligence, Spark Structured Streaming (в Azure Databricks и Fabric) и Azure Stream Analytics [16].

### Типы баз данных и типовые сценарии выбора

- Транзакционные (OLTP) задачи, такие как перевод денег, требуют ACID. Пример из материалов: перевод 40 долларов со счета A (100) на счет B (50) должен выполниться как одна неделимая операция [13].
- Реляционные БД подходят для структурированных данных со связями и SQL. Azure SQL Database - вариант для новых облачных решений, Managed Instance - для миграций с минимальными изменениями, SQL Server on VM - для полного контроля и lift and shift [19].
- Cosmos DB подходит для гибкой схемы, глобального распространения и низкой задержки: IoT и телеметрия, игры, каталоги и заказы в ритейле, персонализация в web и mobile. Для сложных многотабличных join лучше Azure SQL Database, для крупной аналитики - Microsoft Fabric [18].

## Практика (steps, commands, code only from sources)

В загруженных материалах нет пошаговых CLI- или PowerShell-команд для AZ-900 и DP-900. Страницы курсов содержат ссылки на бесплатные аккаунты (Pay as you go или Try Azure free на 30 дней) и список лабораторных заданий, но сами шаги не приведены [1][2][3][4][5].

Из источников доступны следующие фрагменты.

Формат назначения custom role на management group, из документации по management groups [22]:

```
"AssignableScopes": [
      "/providers/microsoft.management/managementGroups/ContosoCorporate"
]
```

Важно использовать ID группы, а не отображаемое имя: такая ошибка распространена, потому что оба поля задаются пользователем [22].

Пример полуструктурированных данных (JSON) из модуля Identify data formats [10]:

```
{
  "firstName": "Joe",
  "lastName": "Jones",
  "contact":
  [
    { "type": "home", "number": "555 123-1234" },
    { "type": "email", "address": "joe@litware.com" }
  ]
}
```

Этот пример показывает гибкость схемы: у каждого клиента может быть свой набор полей [10].

Подробные учебные упражнения, например Create account и Explore Cosmos DB, относятся к модулям, которые в загруженном материале описаны только заголовками, поэтому конкретные шаги здесь не воспроизводятся.

## Безопасность и стоимость

### Безопасность

- Azure Policy: все объекты Policy (definitions, initiatives и assignments) зашифрованы at rest [21]. Политики можно использовать для обеспечения безопасности, например через требование диагностических логов или блокировку действий по identity [21].
- Рекомендация: начинать с эффектов audit или auditIfNotExists, а не с deny, modify или deployIfNotExists, чтобы оценить влияние правила [21].
- Управление доступом: Azure RBAC встроен в платформу управления; роли Owner, Contributor, Reader, Resource Policy Contributor и User Access Administrator задают права на Policy и управление назначениями [20][21].
- Корень management group (root): назначение ролей или политик на нём действует на весь каталог, поэтому такие назначения должны быть обязательными (must have) [22].
- Azure SQL Database: шифрование данных at rest и in transit, Microsoft Defender for SQL, аудит событий в хранилище [19].
- Cosmos DB: в прочитанных материалах подробностей о сетевой безопасности и резервном копировании нет; описаны только управляемость сервиса и глобальная репликация [18].
- Microsoft Entra ID и identity-модель в загруженных материалах раскрыты в минимальном объеме; подробностей об этом нет.

### Стоимость и ценообразование

- Azure Cost Management указан как один из модулей пути Describe Azure management and governance (оценка, отслеживание и управление затратами). Подробного описания инструмента в загруженных материалах нет [5].
- Management groups не поддерживают cost management для Microsoft Customer Agreement subscriptions [22].
- Storage: LRS - самый дешёвый вариант; ZRS, GRS и GZRS повышают доступность и долговечность ценой стоимости [17].
- Cosmos DB: три режима throughput. Dedicated - выделенная пропускная способность контейнера. Shared - на уровне базы данных, общая для до 25 контейнеров. Serverless - без предварительной настройки, оплата за потребленные RU; подходит для непредсказуемого трафика и ограничен одним регионом [18].
- Azure SQL Database: Elastic pool помогает снизить затраты, когда нагрузка разных баз меняется во времени; в General Purpose tier база может автоматически приостанавливаться при простое [19].
- Azure SQL Database free tier: 100 000 vCore seconds serverless compute и 32 ГБ хранилища на базу в месяц [19].
- Остальные ценовые данные (калькулятор цен, модели оплаты) в загруженных материалах отсутствуют.

## Частые вопросы для собеседования

**1. Чем IaaS отличается от PaaS и SaaS? Приведите пример из Azure SQL.**
IaaS - это виртуальная машина с установленным SQL Server, где вы управляете ОС, обновлениями и бэкапами; такой подход подходит для lift and shift [19]. PaaS - Azure SQL Managed Instance или Azure SQL Database, где обновления, бэкапы и восстановление автоматизированы [19]. SaaS - Microsoft Fabric как единая SaaS-платформа аналитики [14].

**2. Что такое иерархия scope в Azure и как наследуются настройки?**
Уровни: management group, subscription, resource group, resource. Настройки верхнего уровня наследуются нижними: политика на подписке действует на все её resource groups и ресурсы [20].

**3. Можно ли перенести ресурс между resource groups, и что происходит при удалении группы?**
Ресурс можно перенести в другую группу в любой момент. При удалении resource group удаляются все ресурсы в ней. Каждый ресурс может находиться только в одной группе [20].

**4. Чем Azure Policy отличается от Azure RBAC?**
Policy оценивает состояние ресурса по бизнес-правилам независимо от того, кто его меняет. RBAC управляет действиями пользователей. Вместе они дают полный контроль над scope [21].

**5. Какие варианты резервирования Azure Storage существуют и что означает RPO?**
LRS (3 копии в одном датацентре, более 11 девяток долговечности), ZRS (синхронная репликация по 3 availability zones в основном регионе, 12 девяток), GRS и GZRS (вторичный регион, 16 девяток). RPO - интервал между последней записью в основной регион и вторичный; типичный RPO Azure Storage меньше 15 минут, но SLA на репликацию нет [17].

**6. Что такое ACID и зачем он нужен OLTP-системам?**
ACID - это Atomicity, Consistency, Isolation, Durability. Пример: перевод денег должен быть атомарным, а проверка баланса во время перевода не должна видеть промежуточное состояние. Такие системы обслуживают line-of-business приложения [13].

**7. В чем разница между ETL и ELT, и что такое medallion architecture?**
ETL трансформирует данные до загрузки в аналитическое хранилище, ELT сначала копирует данные и трансформирует их внутри хранилища [15]. Medallion architecture организует данные в lakehouse по слоям Bronze (сырые), Silver (очищенные) и Gold (готовые к бизнес-использованию) [14].

**8. Чем batch-обработка отличается от потоковой и какие сервисы Azure используются для стриминга?**
Batch обрабатывает статичные данные порциями, stream - события по мере их поступления, с perpetual query и окнами по времени [15][16]. Для приёма событий используют Event Hubs (порядок внутри раздела, at-least-once) или IoT Hub. Для обработки - Azure Stream Analytics, Spark Structured Streaming или Fabric Real-Time Intelligence [16].

## Источники

Все пути указаны относительно базовой папки azure-course.

1. pages/02-dp-900t00-course.md - https://learn.microsoft.com/en-us/training/courses/dp-900t00
2. pages/01-get-started-data-engineering.md - https://learn.microsoft.com/en-us/training/paths/get-started-data-engineering/
3. related/d1-training-paths-microsoft-azure-fundamentals-describe-cloud-concepts.md - https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts
4. related/d1-training-paths-azure-fundamentals-describe-azure-architecture-services.md - https://learn.microsoft.com/en-us/training/paths/azure-fundamentals-describe-azure-architecture-services
5. related/d1-training-paths-describe-azure-management-governance.md - https://learn.microsoft.com/en-us/training/paths/describe-azure-management-governance
6. related/d0-training-paths-azure-data-fundamentals-explore-core-data-concepts.md - https://learn.microsoft.com/en-us/training/paths/azure-data-fundamentals-explore-core-data-concepts
7. related/d0-training-paths-azure-data-fundamentals-explore-relational-data.md - https://learn.microsoft.com/en-us/training/paths/azure-data-fundamentals-explore-relational-data
8. related/d0-training-paths-azure-data-fundamentals-explore-non-relational-data.md - https://learn.microsoft.com/en-us/training/paths/azure-data-fundamentals-explore-non-relational-data
9. related/d0-training-paths-azure-data-fundamentals-explore-data-warehouse-analytics.md - https://learn.microsoft.com/en-us/training/paths/azure-data-fundamentals-explore-data-warehouse-analytics
10. units/d0-training-modules-explore-core-data-concepts-2-data-formats.md - https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/2-data-formats
11. units/d0-training-modules-explore-core-data-concepts-3-file-storage.md - https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/3-file-storage
12. units/d0-training-modules-explore-core-data-concepts-4-databases.md - https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/4-databases
13. units/d0-training-modules-explore-core-data-concepts-5-transactional-data-processing.md - https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/5-transactional-data-processing
14. units/d0-training-modules-explore-core-data-concepts-6-analytical-processing.md - https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/6-analytical-processing
15. units/d0-training-modules-examine-components-of-modern-data-warehouse-2-describe-warehousing.md - https://learn.microsoft.com/en-us/training/modules/examine-components-of-modern-data-warehouse/2-describe-warehousing
16. units/d0-training-modules-explore-fundamentals-stream-processing-3-explore-common-elements.md - https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-stream-processing/3-explore-common-elements
17. units/d0-training-modules-describe-azure-storage-services-3-redundancy.md - https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/3-redundancy
18. units/d0-training-modules-explore-non-relational-data-stores-azure-2-describe-azure-cosmos-db.md - https://learn.microsoft.com/en-us/training/modules/explore-non-relational-data-stores-azure/2-describe-azure-cosmos-db
19. units/d0-training-modules-explore-provision-deploy-relational-database-offerings-azure-2-azure-sql.md - https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-relational-database-offerings-azure/2-azure-sql
20. docs/d0-azure-azure-resource-manager-management-overview.md - https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview
21. docs/d1-azure-governance-policy-overview.md - https://learn.microsoft.com/en-us/azure/governance/policy/overview
22. docs/d0-azure-governance-management-groups-overview.md - https://learn.microsoft.com/en-us/azure/governance/management-groups/overview

Прочитаны, но использованы только как структура курса (без подробностей): modules/d0-training-modules-explore-core-data-concepts.md (https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts), modules/d0-training-modules-describe-azure-storage-services.md (https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services).

Не использованы: папки deep/ и related/ по Data Factory, Functions, Stream Analytics и Databricks относятся к следующему уровню (DP-203 и смежные) и выходят за рамки данного документа. Тексты о shared responsibility, регионах Azure и ценообразовании в загруженных материалах не найдены, поэтому соответствующие разделы документа содержат только то, что есть в источниках.
