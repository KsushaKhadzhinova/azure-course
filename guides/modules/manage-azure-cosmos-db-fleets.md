# Управление парком аккаунтов Azure Cosmos DB (fleets)

**Источник:** https://learn.microsoft.com/en-us/training/modules/manage-azure-cosmos-db-fleets/

## Цель модуля

Организовать многоарендную среду из множества аккаунтов Azure Cosmos DB для NoSQL в fleet, создать fleetspace и зарегистрировать в нем аккаунты из разных подписок, настроить общий пул throughput и отслеживать использование и стоимость по всему парку через fleet analytics.

## Ключевые понятия

- **Fleet (парк)** - верхнеуровневая группировка аккаунтов, которые могут находиться в разных подписках и группах ресурсов; соответствует одному многоарендному приложению. Регион самого fleet не меняет регионы аккаунтов.
- **Fleetspace (пространство парка)** - логическая группа аккаунтов внутри fleet; задает `serviceTier` и `dataRegions` (фиксируются при создании) и границы совместного использования пула.
- **Fleetspace account (аккаунт в fleetspace)** - регистрация существующего аккаунта; аккаунт не перемещается и не копируется. Аккаунт принадлежит ровно одному fleetspace и одному fleet.
- **Pool (пул throughput)** - опциональная настройка fleetspace: общий запас RU/s, которым могут пользоваться ресурсы всех аккаунтов fleetspace сверх выделенного throughput.
- **Fleet analytics** (превью) - экспорт почасовых данных о стоимости, использовании и конфигурации всех аккаунтов в Delta Lake-таблицы Fabric OneLake или Azure Data Lake Storage Gen2.
- **DimResource** - таблица-измерение, связывающая `ResourceId` с парком, подпиской, аккаунтом, регионом, базой и контейнером.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/manage-azure-cosmos-db-fleets/1-introduction

Изоляция через отдельный аккаунт на каждого клиента сохраняет безопасность, но усложняет эксплуатацию при сотнях аккаунтов: перерасход throughput и разрозненная статистика. Fleets оставляют изоляцию аккаунтов и добавляют уровень управления с общим пулом throughput и аналитикой. В сценарии компания Contoso имеет более 200 клиентов с отдельными аккаунтами в нескольких подписках.

### 2. Понимание fleet
URL: https://learn.microsoft.com/en-us/training/modules/manage-azure-cosmos-db-fleets/2-understand-azure-cosmos-db-fleets

Описаны проблемы многих аккаунтов: переразмеривание (каждый аккаунт рассчитан на свой пик) и фрагментированная видимость (метрики Azure Monitor привязаны к аккаунту). Партиционирование (иерархические или синтетические ключи) не подходит, если изоляция должна быть физической. Модель ресурсов: fleet, fleetspace, fleetspace account, пулы и fleet analytics. Лимиты по умолчанию: 3000 аккаунтов в fleetspace, 1 000 000 RU/s пула, 5000 RU/s пула на одну физическую партицию (повышаются через обращение в поддержку). Fleet analytics в тексте помечена как превью. Fleet подходит, если нужна изоляция на уровне аккаунта, аккаунтов много, они в разных подписках и активность неравномерна.

### 3. Создание и организация fleet
URL: https://learn.microsoft.com/en-us/training/modules/manage-azure-cosmos-db-fleets/3-create-organize-fleet

Порядок: создать fleet, затем fleetspace внутри него, затем зарегистрировать аккаунты. Команды: `az cosmosdb fleet`, `az cosmosdb fleetspace`, `az cosmosdb fleetspace account`; `az cosmosdb fleet analytics` поставляется в расширении cosmosdb-preview. Fleetspace задает `fleetspaceApiKind` (NoSQL), `serviceTier` (GeneralPurpose или BusinessCritical) и `dataRegions`; `serviceTier` и `dataRegions` нельзя изменить после создания, а минимум и максимум пула можно. Регистрация аккаунта требует `globalDatabaseAccountProperties.armLocation` и `resourceId`. Аккаунт, уже зарегистрированный в fleetspace, нельзя добавить в другой без удаления регистрации. Организовывать fleet надо по приложению, а fleetspace - по сочетанию регионов и типа записи.

### 4. Настройка throughput парка с помощью пулов
URL: https://learn.microsoft.com/en-us/training/modules/manage-azure-cosmos-db-fleets/4-configure-fleet-throughput-pools

Выделенный throughput (dedicated RU/s) остается гарантированным; ресурс сначала расходует его, а при превышении берет из пула вместо получения 429. Вход в выделенный throughput для пулов - 100-1000 RU/s autoscale. Физическая партиция может потреблять не больше минимума из двух величин: выделенный throughput + 5000 RU/s или 10 000 RU/s (даже при свободном пуле). Пул по умолчанию работает в режиме autoscale: минимум не меньше 100 000 RU/s и кратен 1000; максимум не более чем в 10 раз больше минимума и не меньше минимума. Оплата - по наивысшему значению за каждый час, для каждого региона; простой пул оплачивается по минимуму. Совместный пул возможен, если у аккаунтов одинаковый набор регионов и тип записи (General purpose - одна запись, Business critical - мульти-регион запись). Проверка работы пула: метрика FleetspaceAutoscaledThroughput на уровне парка; на уровне аккаунта - Total Requests и Total Request Units с разбивкой по Capacity Type.

### 5. Мониторинг парка с помощью fleet analytics
URL: https://learn.microsoft.com/en-us/training/modules/manage-azure-cosmos-db-fleets/5-monitor-fleet-analytics

Fleet analytics агрегирует данные по часу для всего парка и пишет Delta Lake-таблицы в Fabric OneLake или ADLS Gen2. Сравнение: метрики Azure Monitor (уровень аккаунта, агрегация 1 минута, хранение 93 дня), логи (на запрос, хранение задается пользователем), fleet analytics (весь парк, агрегация 1 час). Настройка: 1) добавить destination (Fabric workspace или storage account) в меню fleet; 2) выдать права службе-принципалу Cosmos DB Fleet Analytics - роль Contributor в рабочем пространстве Fabric или Storage Blob Data Contributor в хранилище. Для Fabric рабочая область должна использовать OneLake по умолчанию и иметь емкость Fabric; для хранилища при создании включается hierarchical namespace. Данные появляются через час; если их нет через 24 часа, сначала проверьте роль. Таблицы фактов: FactRequestHourly, FactResourceUsageHourly, FactAccountHourly, FactMeterUsageHourly, FactFleetHourly. Измерения: DimResource (сопоставление с парком, подпиской, аккаунтом), DimMeter (продукт, название счетчика, базовая цена) и др. Факты без join с DimResource не привязываются к клиенту.

### 6. Упражнение: создание и мониторинг парка
URL: https://learn.microsoft.com/en-us/training/modules/manage-azure-cosmos-db-fleets/6-exercise-create-monitor-fleet

Практика: создать fleet и fleetspace, зарегистрировать два аккаунта в общем пуле throughput, мониторить пул и отправить fleet analytics в Azure Data Lake Storage. Нужна подписка Azure.

### 7. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/manage-azure-cosmos-db-fleets/7-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 8. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/manage-azure-cosmos-db-fleets/8-summary

Fleet группирует аккаунты между подписками; fleetspace - внутри fleet, каждый аккаунт в одном fleetspace и одном fleet. Пул добавляет общие RU/s к выделенным, минимум 100 000 RU/s, с ограничением на физическую партицию. Аккаунты делят пул только при совпадении регионов и уровня службы. Fleet analytics экспортирует данные по часу в Delta Lake, и для привязки к клиенту нужен join с DimResource.

## Важные команды / код / настройки

Создание fleet:

```powershell
az cosmosdb fleet create `
    --resource-group $resourceGroup `
    --fleet-name $fleetName `
    --location $location
```

Тело fleetspace (файл fleetspace.json), в котором указаны `fleetspaceApiKind`, `serviceTier`, `dataRegions` и диапазон пула (в источнике фрагмент JSON приведен без закрывающих скобок; полный текст см. в уроке):

```json
{
  "properties": {
    "fleetspaceApiKind": "NoSQL",
    "serviceTier": "GeneralPurpose",
    "dataRegions": [ "westus2" ],
    "throughputPoolConfiguration": {
      "minThroughput": 100000,
      "maxThroughput": 100000
    }
```

Создание fleetspace:

```powershell
az cosmosdb fleetspace create `
    --resource-group $resourceGroup `
    --fleet-name $fleetName `
    --fleetspace-name $fleetspaceName `
    --body "@fleetspace.json"
```

Получение ID аккаунта:

```powershell
$accountId = az cosmosdb show `
    --subscription "<account-subscription-id>" `
    --resource-group $accountResourceGroup `
    --name $accountName `
    --query "id" `
    --output tsv
```

Регистрация аккаунта в fleetspace: `az cosmosdb fleetspace account create` с `--resource-group`, `--fleet-name`, `--fleetspace-name`, `--fleetspace-account-name` и `--body "@fleetspace-account.json"` (в файле - `globalDatabaseAccountProperties.armLocation` и `resourceId`).

Требование из источника: передавать JSON через `@<файл>`, а не строкой, так как PowerShell удаляет кавычки.

Пример запроса из fleet analytics (самые активные аккаунты за неделю):

```sql
SELECT TOP 100
    DR.[SubscriptionId],
    DR.[AccountName],
    SUM(FRH.[TotalRequestCount]) AS sum_total_requests
FROM
    [FactRequestHourly] FRH
JOIN
    [DimResource] DR
    ON FRH.[ResourceId] = DR.[ResourceId]
WHERE
    FRH.[Timestamp] >= DATEADD(DAY, -7, GETDATE())
    AND ResourceName IN ('Document', 'StoredProcedure')
GROUP BY
    DR.[AccountName],
    DR.[SubscriptionId]
ORDER BY
    sum_total_requests DESC;
```

Ключевые параметры пула:

| Параметр | Значение |
|---|---|
| Минимум пула | не менее 100 000 RU/s, кратен 1000 |
| Максимум пула | не более 10 × минимум и не меньше минимума |
| Пул на физическую партицию | не более 5000 RU/s сверх выделенного |
| Суммарно на физическую партицию | не более 10 000 RU/s (выделенный + пул) |

## Что запомнить

- Fleet - один парк на одно многоарендное приложение; fleetspace задает регионы и тип службы, которые фиксируются при создании.
- Аккаунт принадлежит ровно одному fleetspace и одному fleet; регистрация не перемещает данные.
- Пул добавляет общий запас RU/s поверх выделенного throughput и оплачивается по минимуму даже при простое.
- Совместно использовать пул могут только аккаунты с одинаковыми регионами и типом записи.
- Fleet analytics пишет почасовые Delta-таблицы; для атрибуции по клиентам соединяйте факты с DimResource и не забывайте роль службы Cosmos DB Fleet Analytics.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/manage-azure-cosmos-db-fleets/
- Fleets overview; Fleet pools; Create a fleet; Fleet analytics; Enable fleet analytics; Fleet analytics schema reference; Fleets frequently asked questions (названия из источника, URL не приведены)
