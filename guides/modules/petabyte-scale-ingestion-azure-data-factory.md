# Приём данных петабайтного масштаба в Azure Data Factory

**Источник:** https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/

## Цель модуля

Научиться выбирать метод приёма данных в Azure Data Factory, понимать доступные коннекторы, использовать Copy Activity, настраивать self-hosted и Azure integration runtime, а также учитывать требования безопасности при приёме данных.

## Ключевые понятия

- **Azure Data Factory (ADF)** - сервис интеграции данных для приёма, трансформации и оркестрации данных; предлагает более 100 коннекторов.
- **Ingestion methods (методы приёма)** - Copy Activity (без кода, без трансформации), вычислительные ресурсы (Databricks, HDInsight, Azure Batch, Azure Functions и др.), пакеты SSIS.
- **Copy Activity** - действие для копирования данных между источником и приёмником без трансформации; поддерживает более 100 нативных коннекторов.
- **Linked service (связанная служба)** - описание целевого хранилища данных или вычислительного сервиса.
- **Dataset (набор данных)** - описание структуры и расположения данных внутри связанной службы.
- **Connectors (коннекторы)** - объекты ADF, которые подключают связанные службы и наборы данных к источникам и приёмникам (Azure, базы данных, NoSQL, файлы, REST/ODBC, сервисы и приложения).
- **Integration runtime (IR, среда интеграции)** - мост между действиями и связанными службами. Типы: Azure IR (облако), self-hosted IR (частная сеть), Azure-SSIS IR.
- **Self-hosted integration runtime** - устанавливается на локальной Windows-машине или VM; нужен для копирования между облаком и частной сетью.
- **Azure integration runtime** - управляемая среда в облаке; выполняет Data Flows и Copy Activity между облачными хранилищами; тип Managed.
- **Azure-SSIS IR** - среда для нативного выполнения пакетов SSIS (lift and shift).
- **Data Factory in Microsoft Fabric** - следующее поколение ADF с упрощенной архитектурой и встроенным ИИ.
- **Virtual network (VNet), NSG, service tags** - сетевые инструменты защиты среды интеграции.
- **Managed identity** - управляемая идентичность фабрики для аутентификации в Azure SQL Database и других ресурсах.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/1-introduction

Первый этап интеграции данных - приём данных из систем в целевое или промежуточное хранилище. ADF предлагает разные методы приёма и подключается более чем к сотне коннекторов; выбор зависит от навыков команды. Для любого метода нужна инфраструктура через integration runtime, а также безопасность данных в хранилищах и при передаче. Цели: описать методы приёма, коннекторы, Copy Activity, управление self-hosted IR, настройку Azure IR и вопросы безопасности. Упомянуто, что Data Factory в Microsoft Fabric - следующее поколение ADF; существующие нагрузки ADF можно перевести на Fabric Data Factory.

### 2. Методы приёма данных
Источник: https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/2-list-ingestion-methods

- **Copy Activity** - код-free конвейеры без трансформации при извлечении; подходит для новых проектов с простым извлечением в промежуточное хранилище.
- **Вычислительные ресурсы**: ADF вызывает платформы обработки для сложных расчетов, а результат возвращается в конвейер. Примеры соответствий: HDInsight (Hive, Pig, Spark, MapReduce, Hadoop Streaming); Azure Batch (пользовательские действия); Azure Machine Learning (Execute Pipeline); Azure SQL, Azure Synapse Analytics, SQL Server (хранимые процедуры); Azure Databricks (Notebook, Jar, Python); Azure Function (Azure Function activity).
- **SSIS-пакеты**: для lift and shift существующих SSIS-нагрузок создается Azure-SSIS Integration Runtime, который выполняет пакеты нативно и позволяет управлять ими в ADF.

### 3. Коннекторы
Источник: https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/3-describe-connectors

- Коннекторы работают с действиями Copy, Data Flow, Lookup, Get Metadata и Delete.
- Поддерживаемые форматы файлов: Avro, Binary, Delimited text, Excel, Iceberg (только как приёмник и только для ADLS Gen2), JSON, ORC, Parquet, XML.
- Категории хранилищ: Azure (Data Lake Storage Gen2, Synapse Analytics); базы данных (Netezza, Greenplum); NoSQL (Cassandra, MongoDB); файлы (FTP, Google Cloud Storage); общие протоколы (REST, ODBC); сервисы и приложения (Dynamics, Salesforce).
- Актуальный список коннекторов ведется на странице обзора коннекторов Microsoft.

### 4. Упражнение: Copy Activity
Источник: https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/4-use-copy-activity

Пример конвейера в ADF Studio: создать pipeline, добавить Copy Data из группы Move and Transform; источник - Amazon S3 с форматом DelimitedText и связанной службой по access key и secret key (Test Connection, затем Create); приёмник - Azure Data Lake Storage Gen2 с выбранным методом аутентификации; Preview Data для проверки источника; Debug для тестового запуска; на вкладке Output через иконку очков открывается мониторинг копирования с метриками Data read/written, throughput и длительностью. Результат проверяется в учетной записи ADLS Gen2.

### 5. Упражнение: self-hosted integration runtime
Источник: https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/5-manage-self-hosted-integration-runtime

- Self-hosted IR выполняет Copy Activity между облачным хранилищем и хранилищем в частной сети, а также трансформации на вычислительных ресурсах в локальной сети или VNet: Azure Function, Custom (Azure Batch), Get Metadata, HDInsight (Hive, Pig, MapReduce, Spark, Streaming - BYOC), Lookup, Machine Learning Execute Pipeline, Stored Procedure, Validation, Web.
- У self-hosted IR нет свойства location: он логически регистрируется в ADF, а вычислительный ресурс предоставляет пользователь.
- Создание: Manage - Integration runtimes - +New - Azure, Self-Hosted - Continue - имя (например, MySelfHostedIR) - Create; скопировать ключ аутентификации, скачать и установить IR на локальной Windows-машине, вставить ключ на странице Register и нажать Register, затем Finish.
- Автоматизация: развертывание через ARM-шаблон или PowerShell; ключ получается отдельной командой.

### 6. Упражнение: Azure integration runtime
Источник: https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/6-set-up-azure-integration-runtime

- Azure IR выполняет Data Flows, Copy Activity между облачными хранилищами и действия диспетчеризации в публичной сети: .NET custom, Azure Function, Databricks Notebook/Jar/Python, Get Metadata, HDInsight (Hive, Pig, MapReduce, Spark, Streaming), Lookup, Stored Procedure, Validation, Web.
- Расположение можно задать явно; по умолчанию autoresolve IR - ADF сам выбирает регион (в том же регионе, если доступен, или ближайший в той же географии) по расположению приемника.
- Создание: Manage - Integration runtimes - +New - Azure - Continue - Azure - имя - Create. Тип в PowerShell - Managed; параметры вычислений не нужны, так как ресурсы эластично управляются облаком.

### 7. Безопасность приёма данных
Источник: https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/7-understand-data-ingestion-security-considerations

- **Сеть**: VNet защищает ресурсы; self-hosted IR размещают в VNet, а NSG должна разрешать только административный доступ. В Azure-SSIS IR порт 3389 (RDP) открыт по умолчанию на уровне NIC NSG для поддержки Microsoft; ограничьте его NSG уровня подсети. Защита от DDoS - Azure DDoS Protection на VNet с IR; Azure Firewall threat intelligence для блокировки вредоносных IP и доменов; для проверки полезной нагрузки - перенаправление трафика через межсетевой экран (ExpressRoute force tunneling или NVA). Service tags (например, DataFactoryManagement) упрощают правила NSG.
- **Идентичность и доступ**: административные учетные записи должны быть выделенными и контролируемыми; для создания фабрик нужна роль contributor или owner либо администратор подписки. Регистрируйте service principal в Microsoft Entra ID; используйте managed identity фабрики для аутентификации, например в Azure SQL Database. Ограничивайте доступ к данным через RBAC.
- **Защита данных**: ведите список хранилищ с чувствительными данными, изолируйте такие системы, отслеживайте и блокируйте несанкционированную передачу, шифруйте данные при передаче и в покое.
- **Логирование и мониторинг**: централизуйте логи ADF в Azure Monitor и Log Analytics, храните их долго в Azure Storage; включайте virtual network flow logs для VNet с IR (NSG flow logs выводятся из эксплуатации 30 сентября 2027 года); настройте алерты на действия; следуйте стандартам организации (аудит, безопасность, антивирус, сроки хранения).
- Данные о запусках конвейеров ADF хранятся только 45 дней; для более долгого хранения включите diagnostic settings и отправляйте логи в Log Analytics или Storage Account.

### 8. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/8-knowledge-check

Итоговый тест модуля (5 минут). Содержимое вопросов в исходных материалах не приведено.

### 9. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/9-summary

Приём может работать в петабайтном масштабе с методом, подходящим под навыки команды. Copy Activity - самый простой способ настройки. Для передачи данных из локальных серверов требуется self-hosted integration runtime; для выполнения SSIS-пакетов - Azure-SSIS IR. После завершения проекта удалите ресурсы, которые больше не нужны, или всю группу ресурсов, так как работающие ресурсы стоят денег.

## Важные команды / код / настройки

- Создание self-hosted IR (PowerShell): `Set-AzDataFactoryV2IntegrationRuntime -ResourceGroupName $resourceGroupName -DataFactoryName $dataFactoryName -Name $selfHostedIntegrationRuntimeName -Type SelfHosted -Description "selfhosted IR description"`.
- Получение ключа self-hosted IR: `Get-AzDataFactoryV2IntegrationRuntimeKey -ResourceGroupName $resourceGroupName -DataFactoryName $dataFactoryName -Name $selfHostedIntegrationRuntimeName`.
- Создание Azure IR (PowerShell): `Set-AzDataFactoryV2IntegrationRuntime -DataFactoryName "SampleV2DataFactory1" -Name "MySampleAzureIR" -ResourceGroupName "ADFV2SampleRG" -Type Managed -Location "West Europe"`.
- Azure IR через PowerShell создается с `-Type Managed`; расположение (Location) можно задать явно, по умолчанию действует autoresolve.
- Порт RDP 3389 в Azure-SSIS IR открыт по умолчанию на уровне NIC NSG - ограничьте его NSG подсети.
- Service tag для правил NSG: DataFactoryManagement.
- Хранение логов ADF: 45 дней; отправка в Log Analytics или Storage Account через diagnostic settings.
- Пути в Studio: Manage - Integration runtimes - +New; Author - pipeline - Move and Transform - Copy Data; кнопки Preview Data и Debug.

## Что запомнить

- Copy Activity - самый простой метод приёма без трансформации; более 100 коннекторов.
- Self-hosted IR нужен для данных из локальной сети или приватной сети; Azure IR - для облачных источников и приёмников.
- Azure IR по умолчанию использует autoresolve; self-hosted IR не имеет свойства location.
- Безопасность приёма: VNet и NSG, managed identity и Microsoft Entra ID, RBAC, шифрование, логирование и flow logs.
- ADF хранит данные о запусках 45 дней; для долгого хранения настройте diagnostic settings.
- После учебного проекта удаляйте ресурсы, чтобы не платить за простой.

## Связанные материалы

- Upgrade from Azure Data Factory to Data Factory in Microsoft Fabric
- Connectors overview (обзор коннекторов ADF)
- Security considerations for data movement in Azure Data Factory
- Monitor Azure Data Factory
