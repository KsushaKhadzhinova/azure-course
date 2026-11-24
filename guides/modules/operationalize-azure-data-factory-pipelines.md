# Эксплуатация конвейеров Azure Data Factory

**Источник:** https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/<юнит>`)

> Примечание из исходника: Data Factory в Microsoft Fabric — следующее поколение Azure Data Factory с упрощенной архитектурой; существующие ADF-нагрузки можно перевести в Fabric.

## Цель модуля

Настроить Git-репозиторий для фабрики разработки, вести ветку функциональности и слияние, развернуть конвейеры через release pipeline (CI/CD), мониторить запуски, настроить Azure Monitor и оповещения, перезапускать конвейеры и понимать основы безопасности Azure Data Factory.

## Ключевые понятия

- **Git integration (интеграция с Git)** — подключение фабрики к Azure Repos или GitHub; авторинг сохраняется в ветки, а не сразу в сервис.
- **Collaboration branch (ветка совместной работы)** — обычно `main`; публиковать в сервис можно только из нее.
- **Publish branch `adf_publish`** — ветка, куда ADF сохраняет ARM-шаблоны при публикации; имя можно изменить через `publish_config.json`.
- **ARM template (шаблон Resource Manager)** — описание фабрики; при CI/CD разворачивается в тестовую и продуктивную фабрики.
- **ARM parameter configuration (`arm-template-parameters-definition.json`)** — пользовательская настройка того, какие свойства параметризуются.
- **Linked templates (связанные шаблоны)** — набор шаблонов `ArmTemplate_master.json`, `ArmTemplate_0.json` и т. д. для больших фабрик.
- **Hotfix (QFE)** — срочное исправление в продуктиве, которое делается в отдельной ветке от коммита, развернутого в продуктив.
- **Azure Monitor / diagnostic settings** — отправка журналов ADF в Storage Account, Event Hub или Log Analytics; ADF хранит данные запусков только 45 дней.
- **Integration Runtime (IR)** — вычислительная среда ADF; тип IR должен совпадать во всех окружениях CI/CD.
- **Managed identity (управляемая идентичность)** — аутентификация без хранения секретов; системная или пользовательская.
- **Customer-managed keys (CMK)** — собственные ключи шифрования в Key Vault; настраиваются только для пустой фабрики.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/1-introduction
ADF интегрируется с Azure DevOps и GitHub для контроля версий и непрерывной интеграции и доставки; есть визуальный и программный мониторинг. Предварительные требования: вход в портал, работа с группами ресурсов, понимание компонентов ADF, опыт Copy Activity.

### 2. Understand the language support in Azure Data Factory
Источник: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/2-understand-language-support-azure-data-factory
Помимо UI, ADF управляется через SDK (.NET, Python), REST API, PowerShell, шаблоны ARM и data flow scripts. Для Python нужны пакеты `azure-mgmt-resource`, `azure-mgmt-datafactory` и `azure-identity`. Data flow script — метаданные трансформаций mapping data flow, видимые по кнопке «script».

### 3. Manage source control of Azure Data Factory solutions
Источник: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/3-manage-source-control-solutions
Без Git единственный способ сохранить изменения — Publish All, который сразу публикует в сервис. Git дает историю, откат, частичные сохранения, совместную работу с ревью и ускоряет загрузку фабрики (примерно в 10 раз). Четыре способа подключения: кнопка на домашней странице, канва авторинга, management hub (Git configuration), при создании фабрики. Ветки: создание feature-ветки, pull request в collaboration-ветку, публикация только из нее. Публикация по умолчанию генерирует ARM-шаблоны в `adf_publish`; свой путь задается файлом `publish_config.json` в корне (`"publishBranch"`). Файл читается при загрузке фабрики, нужно обновить браузер. Рекомендации: читать могут все, публиковать — только участники с ролью Data Factory Contributor на группе ресурсов; запретить прямые коммиты в collaboration-ветку. Секреты (пароли) не хранятся в Git: используйте Key Vault или managed identity. Отключение Git не удаляет содержимое репозитория.

### 4. Continuous integration and deployment
Источник: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/4-continuous-integration-deployment
CI/CD — перенос конвейеров между окружениями (dev, test, prod) через ARM-шаблоны. Жизненный цикл: разработка в dev → feature-ветка → pull request → merge в main → публикация в dev → развертывание в UAT через release → развертывание в prod. Только dev связан с Git; test и prod обновляются только через Azure Pipelines или ARM. Release pipeline: артефакт — ветка `adf_publish`; задача ARM Template Deployment (файлы `ARMTemplateForFactory.json` и `ARMTemplateParametersForFactory.json` в папке фабрики), режим Incremental (Complete удаляет ресурсы, которых нет в шаблоне). Секреты берутся из Key Vault: задача Azure Key Vault до деплоя; агенту нужны права Get и List. Активные триггеры нельзя обновить при деплое: их останавливают и запускают заново (PowerShell-скрипт или PrePostDeploymentScript.Ver2.ps1, который останавливает только измененные триггеры). Вручную можно экспортировать ARM-шаблон (Manage → ARM template → Export) и импортировать его в тестовую или продуктивную фабрику через Import ARM Template. Настраивать параметризацию можно через `arm-template-parameters-definition.json` (лимит 256 параметров не меняется). Правила записи: тип `=`/`-`/`|` и тип `string`, `securestring` и др.; `*` параметризует свойства только первого уровня. Большие фабрики используют связанные шаблоны (linkedTemplates, `ArmTemplate_master.json`), которые нужно загрузить в storage account. Hotfix: найти коммит, развернутый в продуктиве, создать hotfix-ветку от него, исправить, экспортировать ARM-шаблон, положить в publish-ветку, развернуть, перенести исправление в dev. Автоматическая публикация: пакет `@microsoft/azure-data-factory-utilities` (скрипт `build`, Node.js 20.x) в YAML-пайплайне сборки; артефакт сборки используется релизом вместо `adf_publish`. Лучшие практики: Git только для dev; разные Key Vault для окружений с одинаковыми именами секретов; IR одного типа во всех окружениях; без пробелов в именах ресурсов (например, `Pipeline_1`); для общих self-hosted IR можно использовать отдельную фабрику с linked IR; приватные endpoint с другими свойствами в разных окружениях вызывают ошибку деплоя.

### 5. Monitor Azure Data Factory pipelines
Источник: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/5-monitor
Мониторинг доступен в Monitor (Studio или портал). Список запусков: имя конвейера, начало и конец, длительность, запустивший триггер, статус (Failed, Succeeded, In Progress, Canceled, Queued), аннотации, параметры, ошибка, тип запуска (Original, Rerun, Rerun (Latest)), Run ID. Обновление — кнопкой Refresh (автообновления нет). Подробности запуска показывают активности: тип (Copy, ExecuteDataFlow, AzureMLExecutePipeline), входной и выходной JSON, статус, IR, ошибка. Gantt view показывает запуски на временной шкале. ADF хранит данные запусков только 45 дней; для дольше — Azure Monitor. Варианты назначения: Storage Account (срок — через lifecycle management), Event Hub, Log Analytics (сложные запросы, алерты, мониторинг нескольких фабрик). Настройка: Diagnostic settings → Add diagnostic setting → Send to Log Analytics; режим Resource-Specific (из-за лимита 500 колонок). Таблицы: ADFActivityRun, ADFPipelineRun, ADFTriggerRun, ADFSandboxActivityRun, ADFSandboxPipelineRun, таблицы SSIS. AllMetrics — метрики для алертов. Данные появляются в Log Analytics с задержкой до 15 минут. Примеры KQL: доступность конвейеров (`ADFPipelineRun`), топ-5 сбоев активностей за 24 часа (`ADFActivityRun`), последний статус запуска (`argmax`).

### 6. Set up alerts for Azure Data Factory
Источник: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/6-set-up-alerts
Оповещения строятся по метрикам: сбои конвейеров, размер фабрики, загрузка IR (CPU, память, число узлов, очередь), запуски активностей и SSIS. Путь: Monitor → Alerts & metrics → New alert rule. Указываются имя, серьезность, критерий, логика (все конвейеры или конкретные активности/конвейеры/тип ошибки), action group для email, SMS, push и голосовых уведомлений.

### 7. Rerun Azure Data Factory pipelines
Источник: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/7-rerun-azure-data-factory-pipelines
Повторный запуск с начала — кнопка Rerun у запуска (можно выбрать несколько). С конкретной активности — Rerun from activity в представлении активностей. Для упавших, истекших по времени или отмененных активностей — Rerun from failed activity. История повторов доступна в списке и для отдельного запуска.

### 8. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/8-knowledge-check
Проверка знаний (в исходнике текст отсутствует).

### 9. Understand Azure Data Factory security
Источник: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/8-security
RBAC: Data Factory Contributor (группа ресурсов и выше; публикация), Reader (только просмотр и мониторинг, без публикации), Contributor на фабрике (изменения через PowerShell и SDK, но без кнопок Publish). Для Git: Data Factory Contributor только малой группе на группе ресурсов. Managed identity: системная (живет вместе с фабрикой) или пользовательская (общая для ресурсов); роль на целевом ресурсе, например Storage Blob Data Reader для чтения из Data Lake Storage. Секреты — в Key Vault (отдельный Key Vault на окружение, одинаковые имена секретов). Для Git-интеграции секреты публикуются напрямую в сервис. CMK: ключ в Key Vault с Soft Delete и Purge Protection; фабрика и Key Vault в одном тенанте и регионе; CMK задается только для пустой фабрики. Принцип наименьших привилегий: узкий scope, регулярный аудит через Azure Monitor.

### 10. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/9-summary
Модуль охватил интеграцию ADF с Azure DevOps и GitHub, Git-конфигурацию, feature-ветки, release pipeline, визуальный мониторинг, Azure Monitor, оповещения, повторные запуски и безопасность ADF.

## Важные команды / код / настройки

Конфигурация публикации (`publish_config.json` в корне collaboration-ветки):

```json
{
    "publishBranch": "factory/adf_publish"
}
```

Пакет для автоматической публикации (`package.json` в корне репозитория):

```json
{
    "scripts": {
        "build": "node node_modules/@microsoft/azure-data-factory-utilities/lib/index"
    },
    "dependencies": {
        "@microsoft/azure-data-factory-utilities": "^1.0.0"
    }
}
```

Ссылка на секрет Key Vault в файле параметров (для деплоя):

```json
{
    "parameters": {
        "azureSqlReportingDbPassword": {
            "reference": {
                "keyVault": {
                    "id": "/subscriptions/<subId>/resourceGroups/<resourcegroupId> /providers/Microsoft.KeyVault/vaults/<vault-name> "
                },
                "secretName": " < secret - name > "
            }
        }
    }
}
```

Остановка триггеров перед деплоем (PowerShell, Azure PowerShell task):

```powershell
$triggersADF = Get-AzDataFactoryV2Trigger -DataFactoryName $DataFactoryName -ResourceGroupName $ResourceGroupName

$triggersADF | ForEach-Object { Stop-AzDataFactoryV2Trigger -ResourceGroupName $ResourceGroupName -DataFactoryName $DataFactoryName -Name $_.name -Force }
```

Запуск триггеров после деплоя — аналогично, функцией `Start-AzDataFactoryV2Trigger`.

Создание фабрики на Python SDK:

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *
import time

#Create a data factory
subscription_id = '<Specify your Azure Subscription ID>'
rg_name = '<Specify your resource group name>'
df_name = '<Specify your data factory name>'
credentials = DefaultAzureCredential()
adf_client = DataFactoryManagementClient(credentials, subscription_id)

df_resource = Factory(location='eastus')
df = adf_client.factories.create_or_update(rg_name, df_name, df_resource)
while df.provisioning_state != 'Succeeded':
    df = adf_client.factories.get(rg_name, df_name)
    time.sleep(1)
```

Установка пакетов Python SDK:

```bash
pip install azure-mgmt-resource
pip install azure-mgmt-datafactory
pip install azure-identity
```

Запросы KQL в Log Analytics:

```kusto
ADFPipelineRun
| where Status != 'InProgress' and Status != 'Queued'
| where FailureType != 'UserError'
| summarize availability = 100.00 - (100.00 * countif(Status != 'Succeeded') / count()) by bin(TimeGenerated, 1h), _ResourceId
| order by TimeGenerated asc
| render timechart
```

```kusto
ADFActivityRun
| where TimeGenerated >= ago(24h)
| where Status != 'InProgress' and Status != 'Queued'
| where FailureType != 'UserError'
| summarize failureCount = countif(Status != 'Succeeded') by bin(TimeGenerated, 1h), ActivityName
| top 5 by failureCount desc nulls last
| order by TimeGenerated asc
| render timechart
```

```kusto
ADFPipelineRun
| summarize argmax(TimeGenerated, *) by RunId, Status, _ResourceId
```

Фрагмент `arm-template-parameters-definition.json` в исходнике не приведен; в тексте описаны правила синтаксиса (`=`, `-`, `|`, `*`, типы `string`, `securestring`, `int`, `bool`, `object`, `secureobject`, `array`).

Роли: Data Factory Contributor, Reader, Contributor (на фабрике); Storage Blob Data Reader — пример роли managed identity для чтения из Data Lake Storage.

## Что запомнить

- Git подключается только к dev-фабрике; test и prod обновляются через CI/CD или ARM-шаблоны.
- Публикация из collaboration-ветки создает ARM-шаблоны в `adf_publish`; релиз разворачивает их в целевые фабрики в режиме Incremental.
- Секреты хранятся в Key Vault (отдельный на окружение, одинаковые имена секретов), а не в Git; для аутентификации предпочтительна managed identity.
- ADF хранит данные запусков 45 дней; для длительного хранения и алертов используйте diagnostic settings и Log Analytics.
- Перезапуск — от конкретной или упавшей активности; для срочных исправлений — hotfix-ветка от коммита, развернутого в продуктиве.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/
- Документация: Roles and permissions for Azure Data Factory (упоминается в уроке 9).
- Связанный модуль: Configure storage security (`configure-storage-security`) и Secure Azure resources with RBAC (`secure-azure-resources-with-rbac`) — общие принципы доступа и ключей.
- Fabric Data Factory — следующее поколение ADF (упоминается во введении).
