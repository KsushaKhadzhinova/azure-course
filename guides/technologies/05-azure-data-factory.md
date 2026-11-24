# Azure Data Factory

## Что это и зачем

Azure Data Factory (ADF) - облачный сервис ETL и интеграции данных для масштабируемой serverless-интеграции и трансформации данных. В официальной документации он описан как сервис с code-free UI для авторинга и единой панелью мониторинга и управления. Существующие пакеты SSIS можно перенести в Azure и запускать в ADF с полной совместимостью; SSIS Integration Runtime при этом является полностью управляемым сервисом, поэтому инфраструктура не администрируется вручную (источник: d0-azure-data-factory.md).

Типовая задача из введения: компания собирает игровые логи, которые нужно объединить с справочными данными в on-premises хранилище, обработать Spark-кластером в облаке (Azure HDInsight) и опубликовать результат в Azure Synapse Analytics. Workflow должен выполняться по расписанию и запускаться при появлении файлов в контейнере Blob storage. ADF описывается как платформа, которая решает такие сценарии: она создает и планирует data-driven workflows (pipelines), которые забирают данные из разрозненных хранилищ, и поддерживает как ETL, так и ELT (источник: d1-azure-data-factory-introduction.md / pages/06-data-factory-introduction.md).

Ключевые возможности, перечисленные в обзоре: сжатие данных при Copy activity, широкая поддержка коннекторов, custom event triggers, предпросмотр и валидация данных, настраиваемые data flows, интеграция с Microsoft Entra ID и RBAC (источник: pages/06-data-factory-introduction.md).

Важное замечание: в документации Microsoft указано, что Data Factory in Microsoft Fabric является следующим поколением ADF с более простой архитектурой. Существующие рабочие нагрузки ADF могут быть обновлены до Fabric (источник: pages/06-data-factory-introduction.md, docs/d0-azure-data-factory.md).

## Архитектура и ключевые компоненты

Фабрика (data factory) - ресурс, внутри которого живут компоненты. В подписке может быть один или несколько экземпляров ADF. Основные компоненты (источник: pages/06-data-factory-introduction.md, docs/d0-azure-data-factory-concepts-pipelines-activities.md):

- **Pipelines** - логическая группировка activities, которые вместе выполняют задачу. Activities внутри pipeline можно связывать последовательно или запускать параллельно. Управлять pipeline как набором удобнее, чем каждой activity по отдельности.
- **Activities** - шаги обработки. Три группы: data movement (например, Copy), data transformation (Data Flow, Databricks, HDInsight, Azure Function и т.д.) и control flow (ForEach, If Condition, Lookup, Web и др.).
- **Datasets** - представления структур данных внутри хранилищ; указывают на данные, которые activity использует как input или output.
- **Linked services** - строки подключения: описывают подключение либо к хранилищу данных, либо к вычислительному ресурсу, где выполняется activity.
- **Data flows (mapping data flows)** - графы трансформаций, которые ADF выполняет на Spark-кластере, поднимаемом и останавливаемый по мере необходимости. Управлять кластерами не нужно.
- **Integration runtimes (IR)** - вычислительная инфраструктура, которая связывает activities и linked services. IR задает, где выполняется activity или откуда она диспетчеризуется.
- **Triggers** - определяют, когда запускается pipeline run.

Схема связей: activity принимает ноль и более input datasets и производит один или несколько output datasets. Linked service задает подключение, dataset - структуру данных. Например, Azure Storage linked service содержит строку подключения к storage account, а blob dataset указывает контейнер и папку (источник: docs/d0-azure-data-factory-concepts-pipelines-activities.md, pages/06-data-factory-introduction.md).

Три типа integration runtime (источник: docs/d0-azure-data-factory-concepts-integration-runtime.md):

| IR type | Публичная сеть | Private Link | Возможности |
|---|---|---|---|
| Azure | да | да | Data Flow, data movement, activity dispatch |
| Self-hosted | да | да | data movement, activity dispatch |
| Azure-SSIS | да | да | выполнение SSIS-пакетов |

Azure IR - полностью управляемый serverless-compute в Azure: не нужно заниматься провижинингом, установкой ПО, патчингом и масштабированием. Оплачивается фактическое использование. Для Copy activity можно задать число data integration units (DIU), и размер compute масштабируется автоматически. Если включен Managed Virtual Network, Azure IR поддерживает подключение к хранилищам через Private Link. В Data Factory все исходящие порты открыты (источник: docs/d0-azure-data-factory-concepts-integration-runtime.md).

Self-hosted IR нужен для копирования между облаком и хранилищем в приватной сети, для dispatch activity на вычислительных ресурсах в on-premises или Azure Virtual Network. Документация рекомендует относиться к источнику данных за файрволом как к on-premises, даже при ExpressRoute, и использовать self-hosted IR, даже если хранилище находится в IaaS VM в Azure (источник: docs/d1-azure-data-factory-create-self-hosted-integration-runtime.md, docs/d0-azure-data-factory-concepts-integration-runtime.md).

Azure-SSIS IR - управляемый кластер Azure VM, выделенный для выполнения SSIS-пакетов. Каталог SSISDB размещается в Azure SQL Database или Azure SQL Managed Instance (источник: docs/d0-azure-data-factory-concepts-integration-runtime.md, units/...-3-understand-azure-ssis-integration-runtime.md).

## Основные понятия (glossary)

| Термин (English) | Определение |
|---|---|
| Data factory | Экземпляр сервиса ADF, контейнер для всех компонентов; в подписке может быть несколько фабрик. |
| Pipeline | Логическая группа activities, выполняющих задачу; управляется как единое целое. |
| Activity | Шаг обработки в pipeline: movement, transformation или control. |
| Copy activity | Activity, которая читает данные из source data store, выполняет сериализацию, сжатие, маппинг колонок и пишет в sink. |
| Dataset | Описание структуры и расположения данных, на которые ссылается activity. |
| Linked service | Строка подключения к хранилищу или вычислительному ресурсу; аналог connection string. |
| Integration runtime (IR) | Вычислительная среда, на которой выполняются activities или куда они диспетчеризуются. |
| Azure IR | Управляемый serverless IR в Azure. |
| Self-hosted IR | IR, установленный на машине клиента для доступа к приватным источникам. |
| Azure-SSIS IR | IR для выполнения SSIS-пакетов в Azure. |
| Data integration unit (DIU) | Мера мощности одного блока Azure IR: комбинация CPU, памяти и сетевых ресурсов. Применяется только к Azure IR. |
| Mapping data flow | Визуальный граф трансформаций, исполняемый на Spark-кластере ADF. |
| Trigger | Механизм, который запускает pipeline run. |
| Pipeline run | Экземпляр выполнения pipeline с уникальным GUID (pipeline run ID). |
| Parameter | Пары ключ-значение только для чтения, задаются в pipeline; значения передаются при запуске из trigger или вручную. |
| Variable | Переменная внутри pipeline для временных значений; используется вместе с параметрами. |
| Control flow | Оркестрация: цепочки, ветвление, параметры, циклы (ForEach). |
| Activity dependency | Условие, по которому следующая activity запускается: Succeeded, Failed, Skipped, Completed. |
| Managed identity | Идентификатор, которым фабрика аутентифицируется в других сервисах без хранения секретов (источник: units/...-8-security). |
| Managed Virtual Network | Виртуальная сеть, управляемая ADF, для приватного доступа через Private Link. |
| SSISDB | Каталог SSIS-проектов и пакетов, размещаемый в Azure SQL Database или SQL Managed Instance. |

Источники для глоссария: pages/06-data-factory-introduction.md, docs/d0-azure-data-factory-concepts-pipelines-activities.md, docs/d0-azure-data-factory-concepts-integration-runtime.md, docs/d1-azure-data-factory-copy-activity-performance.md, docs/d1-azure-data-factory-concepts-pipeline-execution-triggers.md, units/d0-training-modules-operationalize-azure-data-factory-pipelines-8-security.md.

## Как работает / типовые сценарии

**Общий процесс.** Согласно DataCamp-руководству и обзорной документации, построение pipeline выглядит так: создать linked services (вкладка Manage), создать datasets (Author), добавить activities в pipeline, опубликовать (Publish), затем запустить вручную (Trigger Now) или через trigger (pages/08-datacamp-azure-data-factory.md). Без публикации изменения остаются черновиками и не могут быть запущены (pages/08-datacamp-azure-data-factory.md).

**Этапы сценария по официальной документации** (источник: pages/06-data-factory-introduction.md):

1. Connect and collect - Copy activity переносит данные из on-premises и облачных источников в централизованное хранилище, например Azure Data Lake Storage или Blob storage.
2. Transform and enrich - mapping data flows или внешние activities (HDInsight, Azure Databricks, Machine Learning) преобразуют данные. Data flows выполняются на Spark без необходимости знать Spark.
3. CI/CD and publish - поддерживаются Azure DevOps и GitHub; итог загружается в Azure Synapse Analytics, Azure SQL Database, Azure Cosmos DB и т.д.
4. Monitor - мониторинг через Azure Monitor, API, PowerShell, логи Azure Monitor и панели на портале.

**Копирование.** Copy activity читает данные из source, выполняет сериализацию/десериализацию, сжатие/распаковку, маппинг колонок (по конфигурации input dataset, output dataset и самой activity) и пишет в sink. Нельзя использовать более одного self-hosted IR в одной Copy activity: source и sink должны быть подключены к одному и тому же self-hosted IR. Если self-hosted IR используется для source или sink, оба конца должны быть доступны с сервера, где работает IR (источник: docs/d0-azure-data-factory-copy-activity-overview.md).

**Трансформации.** Mapping data flows содержат категории: schema modifier (например, Derived column, Cast, Aggregate), row modifier (Filter, Sort, Alter row, Assert), multiple inputs/outputs (Conditional split, Union, Exists) и formatters (Flatten, Parse) (источник: units/d0-training-modules-code-free-transformation-scale-3-describe-transformation-types.md). Alter row задает политики insert, delete, update и upsert; условия проверяются по порядку приоритета, и строка получает политику первого совпавшего выражения (там же).

**Control flow.** Поддерживаются Append Variable, Execute Pipeline, Filter, For Each, Get Metadata, If Condition, Lookup, Set Variable, Until, Validation, Wait, Web, Webhook (источник: docs/d0-azure-data-factory-concepts-pipelines-activities.md). Webhook activity вызывает endpoint с callback URL, и pipeline ждет вызова callback перед следующим шагом. Ограничение: мягкий лимит 120 activities на pipeline, включая вложенные activities в контейнерах.

**Зависимости activities.** Для связи A -> B можно задать условие: Succeeded (B выполняется, если A успешна), Failed, Completed (успех или провал) и Skipped. Если activity X падает, следующая в цепочке Y получает статус Skipped (docs/d0-azure-data-factory-concepts-pipelines-activities.md).

**Триггеры.** Три типа: Schedule trigger (по календарному расписанию), Tumbling window trigger (периодические непересекающиеся окна с сохранением состояния) и Event-based trigger (Storage event - появление или удаление файла в Blob storage; Custom event - события из Event Grid). Сравнение Tumbling window и Schedule (источник: docs/d1-azure-data-factory-concepts-pipeline-execution-triggers.md):

- Backfill: Tumbling window поддерживает запуск за прошлые окна; Schedule - нет.
- Retry: Tumbling window по умолчанию имеет retry policy 0 либо заданную пользователем и автоматически повторяет при ошибках 400, 429 и 500; Schedule не поддерживает повторы.
- Concurrency: Tumbling window позволяет задать от 1 до 50 параллельных запусков; Schedule не поддерживает.
- Статус: run Tumbling window отражает состояние запущенного pipeline run; Schedule считается успешным, если pipeline run стартовал ("fire and forget").

Связь pipeline и trigger - n:m (кроме tumbling window): несколько триггеров могут запускать один pipeline, один триггер может запускать несколько pipeline. Триггер нужно явно запустить (start), иначе он не будет срабатывать (docs/d0-azure-data-factory-concepts-pipelines-activities.md, docs/d1-azure-data-factory-concepts-pipeline-execution-triggers.md).

**Параметры.** Pipeline run создается передачей аргументов параметрам pipeline. Аргументы передаются вручную или в определении trigger. Datasets и linked services тоже являются типизированными, переиспользуемыми параметрами (pipeline parameters, источник: pages/06-data-factory-introduction.md).

**Сценарии Azure-SSIS.** Lift-and-shift существующих SSIS-пакетов: Azure-SSIS IR выполняет пакеты, развернутые в каталог SSISDB (Project Deployment Model), либо пакеты в файловой системе, Azure Files или MSDB на SQL Managed Instance (Package Deployment Model). При provisioning задаются размер узла (включая число ядер), число узлов, сервер Azure SQL для SSISDB, тир сервиса базы данных и максимальное число параллельных выполнений на узел (источник: units/...-3-understand-azure-ssis-integration-runtime.md). Расположение IR рекомендуется выбирать рядом с сервером, где размещается SSISDB (там же).

## Практика (steps, commands, code only from sources)

**1. Пошаговый pipeline из DataCamp (сторонний источник, не Microsoft).** Шаги создания первого pipeline: создать ADF через Create a resource -> Data Factory; создать linked services для источника (например, Azure Blob Storage) и назначения (например, Azure SQL Database) через Manage; создать datasets через Author (для источника тип, соответствующий формату, например Delimited Text; для назначения - Table); создать pipeline, добавить activity Copy data (вкладки Source, Sink, Mapping); нажать Publish; запустить через Add Trigger -> Trigger Now или создать trigger (время или событие появления файла) (источник: pages/08-datacamp-azure-data-factory.md). В этом руководстве кода нет.

**2. Тот же сценарий в Microsoft Learn (Copy activity).** Путь: Author canvas -> + -> Pipeline -> перетащить Copy Data из группы Move and Transform -> на вкладке Source создать dataset (например, Amazon S3 с форматом DelimitedText), указать linked service с access key и secret key, нажать Preview Data для проверки; на вкладке Sink выбрать ADLS Gen2 (источник: units/d0-training-modules-petabyte-scale-ingestion-azure-data-factory-4-use-copy-activity.md, https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/4-use-copy-activity - URL см. в Источниках).

**3. Пример JSON pipeline с Copy activity** (источник: docs/d1-azure-data-factory-concepts-pipeline-execution-triggers.md):

```json
{
    "name": "copyPipeline",
    "properties": {
        "activities": [
            {
                "type": "Copy",
                "typeProperties": {
                    "source": { "type": "BlobSource" },
                    "sink": { "type": "BlobSink" }
                },
                "name": "CopyBlobtoBlob",
                "inputs": [ { "referenceName": "sourceBlobDataset", "type": "DatasetReference" } ],
                "outputs": [ { "referenceName": "sinkBlobDataset", "type": "DatasetReference" } ]
            }
        ],
        "parameters": {
            "sourceBlobContainer": { "type": "String" },
            "sinkBlobContainer": { "type": "String" }
        }
    }
}
```

**4. Ручной запуск pipeline через Azure PowerShell** (источник: docs/d1-azure-data-factory-concepts-pipeline-execution-triggers.md):

```powershell
Invoke-AzDataFactoryV2Pipeline -DataFactory $df -PipelineName "Adfv2QuickStartPipeline" -ParameterFile .\PipelineParameters.json -ResourceGroupName "myResourceGroup"
```

Альтернативы для запуска, перечисленные в документации: .NET SDK (client.Pipelines.CreateRunWithHttpMessagesAsync), Python SDK, REST API. Microsoft рекомендует использовать модуль Az вместо AzureRM (там же).

**5. Реконфигурация Azure-SSIS IR (Stop - Set - Start)** (источник: docs/d1-azure-data-factory-manage-azure-ssis-integration-runtime.md):

```powershell
Stop-AzDataFactoryV2IntegrationRuntime -DataFactoryName $DataFactoryName -Name $AzureSSISName -ResourceGroupName $ResourceGroupName
Set-AzDataFactoryV2IntegrationRuntime -DataFactoryName $DataFactoryName -Name $AzureSSISName -ResourceGroupName $ResourceGroupName -NodeCount 5
Start-AzDataFactoryV2IntegrationRuntime -DataFactoryName $DataFactoryName -Name $AzureSSISName -ResourceGroupName $ResourceGroupName
```

Первая команда освобождает все узлы и останавливает биллинг. Вторая масштабирует IR до пяти узлов. Третья выделяет узлы для выполнения SSIS-пакетов. В UI редактировать и удалять Azure-SSIS IR можно только в остановленном состоянии (там же).

**6. Выполнение SSIS-пакетов.** Пакеты создаются в SSDT, при этом выбирается шаблон Integration Services Project (Azure-Enabled). Существующий проект можно включить через Azure-Enabled Project Wizard. Для автоматизации в скриптах и CI/CD используется AzureDTExec: он отправляет выполнение в Azure-SSIS IR, создавая и запуская pipeline ADF, в отличие от локального dtexec (источник: units/d0-training-modules-execute-existing-ssis-packages-azure-data-factory-5-run.md). Команды AzureDTExec в источниках не приведены полностью.

**7. Мониторинг.** В интерфейсе Monitor доступны список pipeline runs (колонки: Pipeline Name, Run Start, Run End, Duration, Triggered By, Status, Annotations, Parameters, Error, Run, Run ID) и activity runs (Activity Name, Activity Type, Integration Runtime, User Properties и др.). Статусы: Failed, Succeeded, In Progress, Canceled, Queued. Список обновляется вручную кнопкой Refresh, автообновление не поддерживается. Доступен Gantt view (units/d0-training-modules-operationalize-azure-data-factory-pipelines-5-monitor.md).

**8. Оповещения (alerts).** Monitor > Alerts & metrics > New alert rule: имя, severity, критерий по метрикам (количество и размер сущностей, runs activity/pipeline/trigger, CPU/память/число узлов/очередь IR, выполнения SSIS-пакетов, старт/стоп SSIS IR), логика (все pipelines или конкретные по типу activity, имени, failure type), action group с email, SMS, push или voice (units/d0-training-modules-operationalize-azure-data-factory-pipelines-6-set-up-alerts.md).

**9. Производительность Copy.** Рекомендуется сначала максимизировать производительность одной Copy activity. При Azure IR начинать с значений по умолчанию для DIU и parallel copy; при self-hosted IR использовать отдельную машину, не совпадающую с хостом хранилища, и начинать с одного узла. После тестового запуска фиксировать достигнутую производительность и фактические значения DIU и parallel copies (docs/d1-azure-data-factory-copy-activity-performance.md).

**10. Производительность Data Flow.** Четыре возможных узких места: время старта кластера, чтение из источника, время трансформаций, запись в sink. Старт кластера обычно занимает 3-5 минут; для последовательных задач его можно сократить через time to live (TTL) интеграционного runtime. Debug mode позволяет тестировать на живом Spark-кластере без ожидания прогрева (docs/d1-azure-data-factory-concepts-data-flow-performance.md).

## Безопасность и стоимость

**Безопасность (источник: units/d0-training-modules-operationalize-azure-data-factory-pipelines-8-security.md):**

- RBAC. Встроенные роли: Data Factory Contributor (создание и публикация, на уровне resource group или выше), Reader (только просмотр и мониторинг, без публикации), Contributor (уровень фабрики; не видит кнопок Publish и Publish All). Для Git-интеграции рекомендуется выдавать Data Factory Contributor небольшой группе.
- Managed identities. Системная (system-assigned) живет вместе с фабрикой; пользовательская (user-assigned) независима. Например, Storage Blob Data Reader назначается managed identity фабрики на storage account, без строк подключения и паролей.
- Azure Key Vault. Для сервисов без поддержки managed identity секреты хранятся в Key Vault. Секреты linked services не сохраняются в Git: изменения linked service с секретом публикуются сразу в сервис, в обход Git-workflow. Для разных окружений рекомендуется отдельный Key Vault на каждое окружение с одинаковыми именами секретов.
- Customer-managed keys (CMK). По умолчанию данные шифруются Microsoft-managed key. CMK настраивается через Key Vault; Key Vault должен иметь Soft Delete и Purge Protection; фабрика и Key Vault должны быть в одном Microsoft Entra tenant и в одном регионе. CMK настраивается только для пустой фабрики.
- Сеть. Self-hosted IR можно развернуть внутри виртуальной сети. Azure-SSIS IR при присоединении к VNet создает сетевые ресурсы, например NSG (units/d0-training-modules-petabyte-scale-ingestion-azure-data-factory-7-understand-data-ingestion-security-considerations.md).
- Self-hosted IR: credentials рекомендуется хранить в Azure Key Vault. Локальное хранение шифруется, но требует разрешить домен interactive authoring в файрволе. Один экземпляр IR можно установить только на одну машину; до четырех узлов на один IR (docs/d1-azure-data-factory-create-self-hosted-integration-runtime.md).
- Сетевые ограничения: в Data Factory все исходящие порты открыты при использовании Azure IR; для ограничения исходящего трафика рекомендуется Azure-SSIS IR в VNet (docs/d0-azure-data-factory-concepts-integration-runtime.md).

**Стоимость и лимиты (только из источников):**

- Azure IR: вы платите за фактическое использование; масштабирование compute автоматическое (docs/d0-azure-data-factory-concepts-integration-runtime.md).
- Azure-SSIS IR: остановка IR освобождает узлы и останавливает биллинг; управление стоимостью - через остановку и запуск (docs/d0-azure-data-factory-concepts-integration-runtime.md, docs/d1-azure-data-factory-manage-azure-ssis-integration-runtime.md).
- DIU: до 256 на одну Copy activity при Azure IR (docs/d1-azure-data-factory-copy-activity-performance.md).
- Self-hosted IR: до 4 узлов; масштабирование вверх (scale up) работает, только если процессор и память узла недогружены (docs/d1-azure-data-factory-create-self-hosted-integration-runtime.md, docs/d1-azure-data-factory-copy-activity-performance.md).
- Pipeline: мягкий лимит 120 activities (docs/d0-azure-data-factory-concepts-pipelines-activities.md).
- Tumbling window: concurrency от 1 до 50 (docs/d1-azure-data-factory-concepts-pipeline-execution-triggers.md).
- Цены в загруженных материалах не приведены: в документации есть только ссылка на страницу Pricing. Конкретных ценовых цифр в источниках нет.

## Частые вопросы для собеседования

**1. Чем ADF отличается от Fabric Data Factory?**
ADF - зрелый PaaS-сервис с возможностью выделенных Integration Runtime и глубокой интеграцией с on-premises системами. Microsoft Fabric - SaaS-платформа, объединяющая Data Factory, Synapse Analytics и Power BI в одном окружении. Pipelines ADF и Fabric Data Factory очень похожи, навыки переносятся (pages/08-datacamp-azure-data-factory.md; pages/06-data-factory-introduction.md; docs/d0-azure-data-factory.md). Это утверждение DataCamp о переносимости навыков - мнение стороннего автора; подтверждение официальной документации - о наличии пути миграции.

**2. Что такое integration runtime и какие типы бывают?**
IR - вычислительная инфраструктура, которая связывает activities и linked services. Три типа: Azure (serverless, public и Private Link), self-hosted (для приватных сетей и on-premises), Azure-SSIS (выполнение SSIS-пакетов). Таблица возможностей приведена в разделе архитектуры (docs/d0-azure-data-factory-concepts-integration-runtime.md).

**3. В чем разница между linked service и dataset?**
Linked service - строка подключения к хранилищу или вычислительному ресурсу. Dataset - описание структуры данных, ссылающееся на linked service. Пример из документации: Azure Storage linked service задает подключение к storage account, а blob dataset указывает контейнер и папку (pages/06-data-factory-introduction.md).

**4. Чем Tumbling window trigger отличается от Schedule trigger?**
Tumbling window поддерживает backfill, повторы, concurrency 1-50 и отражает состояние запуска pipeline. Schedule trigger не поддерживает backfill и повторы и считается успешным сразу после старта pipeline run (docs/d1-azure-data-factory-concepts-pipeline-execution-triggers.md).

**5. Как безопасно хранить учетные данные в ADF?**
Предпочтительно использовать managed identity с назначением нужной роли на целевом ресурсе, без строк подключения. Для сервисов без поддержки managed identity - Azure Key Vault. Секреты linked services не попадают в Git (units/d0-training-modules-operationalize-azure-data-factory-pipelines-8-security.md).

**6. Как ускорить Copy activity?**
Сначала тюнинг одной Copy activity: для Azure IR - DIU и parallel copy; для self-hosted IR - отдельная машина и масштабирование вверх или до четырех узлов. Параллелизм на уровне pipeline достигается через ForEach, который запускает несколько Copy activity одновременно. Результаты тестов фиксируются, чтобы потом использовать для планирования (docs/d1-azure-data-factory-copy-activity-performance.md).

**7. Как ADF выполняет SSIS-пакеты в облаке?**
Через Azure-SSIS IR: это управляемый кластер Azure VM с каталогом SSISDB на Azure SQL Database или SQL Managed Instance. Пакеты разворачиваются из SSDT или SSMS, автоматизация выполняется через AzureDTExec (units/d0-training-modules-execute-existing-ssis-packages-azure-data-factory-5-run.md, docs/d0-azure-data-factory-concepts-integration-runtime.md).

**8. Как мониторить и оповещать о сбоях pipeline?**
Monitor Studio показывает pipeline runs и activity runs с статусами и ошибками, есть Gantt view. Для оповещений создается alert rule по метрикам (например, failed pipelines) с action group для email, SMS, push или voice. Также возможна интеграция с Log Analytics (units/...-5-monitor.md, units/...-6-set-up-alerts.md).

## Источники

Все файлы находятся в базовой папке azure-course.

Основные источники (использованы):

- pages/06-data-factory-introduction.md - https://learn.microsoft.com/en-us/azure/data-factory/introduction
- pages/07-data-integration-scale-data-factory.md - https://learn.microsoft.com/en-us/training/paths/data-integration-scale-azure-data-factory/ (состав учебного пути, использован только как навигация)
- pages/08-datacamp-azure-data-factory.md - https://www.datacamp.com/tutorial/azure-data-factory (сторонний источник; используется для пошагового сценария, отмечен как не-Microsoft)
- pages/09-data-factory-tutorials.md - https://learn.microsoft.com/en-us/azure/data-factory/data-factory-tutorials (только список туториалов, без содержимого; использован для навигации)
- docs/d0-azure-data-factory.md - https://learn.microsoft.com/en-us/azure/data-factory
- docs/d0-azure-data-factory-concepts-integration-runtime.md - https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime
- docs/d0-azure-data-factory-concepts-pipelines-activities.md - https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities
- docs/d0-azure-data-factory-copy-activity-overview.md - https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-overview
- docs/d1-azure-data-factory-concepts-pipeline-execution-triggers.md - https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipeline-execution-triggers
- docs/d1-azure-data-factory-copy-activity-performance.md - https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-performance
- docs/d1-azure-data-factory-concepts-data-flow-performance.md - https://learn.microsoft.com/en-us/azure/data-factory/concepts-data-flow-performance
- docs/d1-azure-data-factory-manage-azure-ssis-integration-runtime.md - https://learn.microsoft.com/en-us/azure/data-factory/manage-azure-ssis-integration-runtime
- docs/d1-azure-data-factory-create-self-hosted-integration-runtime.md - https://learn.microsoft.com/en-us/azure/data-factory/create-self-hosted-integration-runtime
- units/d0-training-modules-execute-existing-ssis-packages-azure-data-factory-3-understand-azure-ssis-integration-runtime.md - https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/3-understand-azure-ssis-integration-runtime
- units/d0-training-modules-execute-existing-ssis-packages-azure-data-factory-5-run.md - https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/5-run
- units/d0-training-modules-code-free-transformation-scale-3-describe-transformation-types.md - https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/3-describe-transformation-types
- units/d0-training-modules-petabyte-scale-ingestion-azure-data-factory-4-use-copy-activity.md - https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/4-use-copy-activity (URL взят из шаблона соседнего файла; проверить при необходимости)
- units/d0-training-modules-petabyte-scale-ingestion-azure-data-factory-7-understand-data-ingestion-security-considerations.md - https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/7-understand-data-ingestion-security-considerations
- units/d0-training-modules-operationalize-azure-data-factory-pipelines-5-monitor.md - https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/5-monitor
- units/d0-training-modules-operationalize-azure-data-factory-pipelines-6-set-up-alerts.md - https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/6-set-up-alerts
- units/d0-training-modules-operationalize-azure-data-factory-pipelines-8-security.md - https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/8-security

Просмотренные, но не использованные по существу:

- docs/d1-azure-data-factory-introduction.md и другие коннекторные страницы docs/d1-azure-data-factory-connector-*.md - сведения о коннекторах уже покрыты общими таблицами; подробностей по отдельным коннекторам в документе нет.
- Страницы SSIS-модуля 4 (set up) и 6 (migrate), а также модули по Synapse-интеграции не загружались полностью: в тексте нет сведений из них.

Примечания о качестве источников: страницы Microsoft Learn в части случаев закрыты для неавторизованного просмотра ("Access to this page requires authorization"), поэтому фрагменты взяты из сохраненного текста статьи. В DataCamp-статье есть внутреннее расхождение (в одном месте "over 90 native connectors", в другом "over 100 native connectors"); в документе не использованы конкретные числа из DataCamp.
