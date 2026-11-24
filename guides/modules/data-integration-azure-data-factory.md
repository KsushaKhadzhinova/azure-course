# Интеграция данных с Azure Data Factory

**Источник:** https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/

## Цель модуля

Понять, как Azure Data Factory (ADF) автоматизирует перемещение и преобразование данных между хранилищами и вычислительными сервисами: изучить паттерны интеграции (ETL и ELT), процесс работы фабрики, ее компоненты, безопасность, создание linked services, datasets, activities и pipelines, а также типы integration runtime.

## Ключевые понятия

- **Pipeline** — конвейер (data-driven workflow), группа activities; запускается по расписанию или триггеру.
- **Activity** — действие: перемещение данных (Copy), преобразование (Mapping Data Flow или внешние вычисления) или управление (Control activities).
- **Linked service** — объект с параметрами подключения к хранилищу или вычислительному сервису, аналог строки подключения.
- **Dataset** — именованное представление данных внутри хранилища: таблица, файл, папка, контейнер.
- **Integration runtime (IR)** — вычислительная инфраструктура, на которой выполняются activities и linked services. Типы: Azure, Self-hosted, Azure-SSIS.
- **Parameters** — пары «ключ-значение» только для чтения, определяются в pipeline и передаются при запуске.
- **Managed identity** — учетная запись, которой управляет Azure; позволяет не хранить учетные данные в определениях сервисов.
- **ETL / ELT** — extract, transform, load (преобразование до загрузки) и extract, load, transform (загрузка исходных данных, затем преобразование).

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/1-introduction

Введение: зачем нужна оркестрация перемещения данных между хранилищами и какие темы охватывает модуль.

### 2. Understand Azure Data Factory
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/2-understand

ADF — облачный сервис интеграции данных и ETL, который оркестрирует перемещение и преобразование. Аналогия с дирижером: ADF сам не всегда выполняет работу, а поручает ее другим сервисам (например, Azure Databricks) и управляет последовательностью. Мониторинг: Azure Monitor, API, PowerShell, Azure Monitor logs и панели состояния в портале. Data Factory в Microsoft Fabric — следующее поколение сервиса.

### 3. Describe data integration patterns
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/3-describe-data-integration-patterns

Интеграция включает сбор данных из источников, очистку и преобразование, загрузку в хранилище. Фазы Extract (источник и данные), Transform (разбиение, объединение, сопоставление полей, агрегация), Load (назначение, запуск, мониторинг). Переход от ETL к ELT: данные сохраняются в исходном формате, структура определяется на этапе преобразования. Два основных паттерна: современное хранилище данных (пакетная загрузка) и продвинутая аналитика (подготовка данных в Data Lake для Azure Databricks или HDInsight).

### 4. Explain the data factory process
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/4-explain-process

Четыре шага pipeline: Connect and collect (подключение и сбор данных), Transform and enrich (преобразование и обогащение), CI/CD and publish (публикация с поддержкой CI/CD через Azure DevOps и GitHub), Monitor (мониторинг успешных и неуспешных запусков).

### 5. Understand Azure Data Factory components
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/5-understand-components

Компоненты: linked services (источники и вычислительные ресурсы), datasets (структуры данных), activities (Copy, Mapping Data Flow, stored procedure, Hive, Pig, ML), pipelines (группировка activities и триггеры), control flow (последовательность, ветвление, циклы, For-each), parameters, Data Flows (визуальные преобразования на управляемом Spark), integration runtime (связывает activity с linked service) и публикация результата для Power BI или ML.

### 6. Azure Data Factory security
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/6-security

Для создания фабрик нужна роль Contributor или Owner (или администратор подписки). Для управления дочерними ресурсами в портале — роль Data Factory Contributor или Contributor на уровне группы ресурсов и выше. Для PowerShell и SDK достаточно Contributor на уровне ресурса и выше. Managed identities: system-assigned (одна на фабрику, удаляется вместе с ней) и user-assigned (отдельный ресурс). Учетные данные, которые нельзя заменить managed identity, хранятся в Azure Key Vault.

### 7. Set-up Azure Data Factory
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/7-set-up

Создание в портале: подписка, группа ресурсов, регион, глобально уникальное имя, версия V2, при необходимости интеграция с Git (URL, имя репозитория, ветка, корневая папка). Также можно развернуть через PowerShell.

### 8. Create linked services
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/8-create-linked-services

Linked service похож на строку подключения. Его можно создать в дизайнере при настройке Copy activity или отдельно (JSON, REST API, SDK). Свойство `connectVia` задает integration runtime; если оно не указано, используется Azure IR по умолчанию. Примеры: Azure SQL Database и Azure Blob Storage с аутентификацией через system-assigned managed identity.

### 9. Create datasets
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/9-create-datasets

Dataset указывает, какие данные использовать как вход или выход activity: таблицы, файлы, папки, документы. Пример из источника: два набора данных типа Binary (InputDataset и OutputDataset) в контейнере `adftutorial` (папки input и output), созданные через PowerShell cmdlet `Set-AzDataFactoryV2Dataset`.

### 10. Create data factory activities and pipelines
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/10-create-activities-pipelines

Три категории activities: перемещение данных (Copy), преобразование (Mapping Data Flow или вычисления в Azure Databricks, Azure Batch, Azure Functions, Azure SQL Database, Azure Machine Learning, HDInsight, Azure-SSIS IR) и управление (Execute Pipeline, ForEach, Web, Lookup, Get Metadata, Until, If Condition, Wait, Append Variable, Filter, Set Variable, Validation, Webhook, Fail). Приведены структуры JSON для execution и control activities, pipeline и пример HDInsight Hive activity с `retry: 3`.

### 11. Manage integration runtimes
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/11-manage-integration-runtimes

IR — вычислительная инфраструктура. Типы: Azure (Data Flow, перемещение данных и диспетчеризация активностей в публичной сети и через частные сети), Self-hosted (перемещение данных и диспетчеризация в частной сети, например on-premises) и Azure-SSIS (выполнение пакетов SSIS). По умолчанию создается Auto-Resolve IR. Правила выбора: копирование между облачными источниками — Azure IR; если один из концов в частной сети — Self-hosted IR; для Lookup и GetMetadata — IR, связанный с linked service хранилища; для Data Flow — IR, связанный с activity.

### 12. Module assessment
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/12-knowledge-check

Проверочный тест (около 3 минут). Вопросы и ответы в источнике не приведены.

### 13. Summary
https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/13-summary

Итоги: ADF автоматизирует регулярное перемещение данных в составе аналитического решения через компоненты и процесс работы сервиса и роли для его настройки и управления. Удаляйте неиспользуемые ресурсы или группу ресурсов после завершения работы.

## Важные команды / код / настройки

**Создание ADF через PowerShell (из урока 7):**

```
# Sign in to Azure
Connect-AzAccount

# Select the target subscription
$SubscriptionId = "add your subscription in the quotes"
Select-AzSubscription -SubscriptionId $SubscriptionId

# Register the Microsoft Azure Data Factory resource provider
Register-AzResourceProvider -ProviderNamespace Microsoft.DataFactory

# Define resource group name and location
$resourceGroupName = "cto_ignite"
$rglocation = "West US 2"

# Create the resource group
New-AzResourceGroup -Name $resourceGroupName -Location $rglocation

# Create Azure Data Factory
Set-AzDataFactoryV2 -ResourceGroupName $resourceGroupName -Name "ctoigniteADF" -Location $rglocation
```

**Linked service Azure SQL Database с managed identity:**

```
{
  "name": "AzureSqlLinkedService",
  "properties": {
    "type": "AzureSqlDatabase",
    "typeProperties": {
      "server": "<server-name>.database.windows.net",
      "database": "ctosqldb",
      "authenticationType": "SystemAssignedManagedIdentity"
    }
  }
}
```

**Linked service Azure Blob Storage с managed identity:** `"type": "AzureBlobStorage"`, `serviceEndpoint` вида `https://ctostorageaccount.blob.core.windows.net/`, `accountKind: StorageV2`.

**Создание dataset через PowerShell (из урока 9):** `Set-AzDataFactoryV2Dataset -DataFactoryName ... -ResourceGroupName ... -Name "InputDataset" -DefinitionFile ".\InputDataset.json"`. Тип `Binary`, `AzureBlobStorageLocation`, контейнер `adftutorial`, папка `input`, файл `emp.txt`.

**Pipeline с HDInsight Hive activity (фрагмент из урока 10):** `"type": "HDInsightHive"`, `"policy": { "retry": 3 }`. Pipeline запускается по расписанию через связанный триггер.

**Роли для управления ADF (урок 6):** Data Factory Contributor; на уровне группы ресурсов и выше — Contributor для портала; для PowerShell и SDK — Contributor на уровне ресурса и выше.

**Типы integration runtime (урок 11):**

| Тип IR | Публичная сеть | Частная сеть |
|---|---|---|
| Azure | Data Flow, Data movement, Activity dispatch | Data Flow, Data movement, Activity dispatch |
| Self-hosted | Data movement, Activity dispatch | Data movement, Activity dispatch |
| Azure-SSIS | SSIS package execution | SSIS package execution |

Свойство `connectVia` в linked service задает IR; без него используется Auto-Resolve.

## Что запомнить

- ADF оркестрирует работу: pipeline вызывает activities, которые могут выполняться самой фабрикой или внешними сервисами.
- Linked service описывает подключение, dataset — структуру данных, activity — действие, pipeline — их последовательность.
- Managed identity позволяет не хранить учетные данные в определениях; для остальных секретов используйте Azure Key Vault.
- Integration runtime определяет, где выполняется activity: Azure IR для облачных данных, Self-hosted для частной сети, Azure-SSIS для пакетов SSIS.
- Паттерн ELT отличается от ETL порядком шагов: сначала загрузка в исходном формате, затем преобразование.

## Связанные материалы

- Connector overview (обзор коннекторов ADF; упоминается в уроке 8).
- Managed identities for Azure Data Factory (упоминается в уроке 6).
- Custom role для Data Factory (упоминается в уроке 6).
- Data Factory in Microsoft Fabric — следующее поколение ADF (упоминается в уроке 2).
- Azure Monitor, Azure Monitor logs и панели состояния в портале (упоминаются в уроках 2 и 4).
