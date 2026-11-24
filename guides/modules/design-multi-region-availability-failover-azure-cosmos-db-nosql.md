# Проектирование доступности и аварийного переключения между регионами для Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/

## Цель модуля

Научиться настраивать аккаунт Azure Cosmos DB for NoSQL и его клиенты для работы в нескольких регионах: выбирать зональную и региональную избыточность, добавлять регионы и направлять чтения в ближайший регион, включать запись в нескольких регионах, разрешать конфликты записи и выбирать подходящую операцию аварийного переключения (failover).

## Ключевые понятия

- **Partition set (набор партиций)** - реплика-наборы с одинаковыми значениями partition key в разных регионах; репликация между ними - глобальная.
- **Zone redundancy (зональная избыточность)** - реплики распределяются по зонам доступности внутри региона; задается для каждого региона.
- **Regional redundancy (региональная избыточность)** - защита от потери всего региона; настраивается добавлением регионов.
- **RTO (Recovery Time Objective)** - допустимое время простоя.
- **RPO (Recovery Point Objective)** - допустимый объем потерянных последних данных; определяется уровнем согласованности (strong - 0; session, consistent prefix, eventual - менее 15 минут; bounded staleness - по версиям или времени).
- **Failover priority (приоритет переключения)** - порядок, в котором регионы становятся новым регионом записи; 0 - текущий регион записи.
- **Preferred region list (список предпочтительных регионов)** - список регионов в SDK для чтения и записи.
- **Hub region (хаб-регион)** - регион создания аккаунта при записи в нескольких регионах; остальные - satellite.
- **Tentative и confirmed write (неподтвержденная и подтвержденная запись)** - запись в satellite-регионе сначала неподтверждена, затем подтверждается хабом.
- **_ts и crts** - серверное время записи и время разрешения конфликта или подтверждения отсутствия конфликта в хаб-регионе.
- **Conflict resolution policy (политика разрешения конфликтов)** - last writer wins (по `_ts` или числовому пути) или custom (merge stored procedure, иначе - conflict feed); задается при создании контейнера.
- **Conflict feed (лента конфликтов)** - список конфликтов, которые нужно разрешить вручную.
- **Change write region (смена региона записи)** - плановая операция при здоровых регионах; данные не теряются.
- **Forced failover (принудительное переключение, Offline region)** - операция клиента при отказе региона; возможна потеря непереплицированных записей.
- **Service-managed failover (автоматическое переключение сервисом)** - переключение по решению Microsoft; может занять час и более.
- **PPAF (Per-partition automatic failover)** - переключение только затронутых партиций, примерно за 3 минуты.
- **Circuit breaker и hedging** - клиентская маршрутизация при ошибках одной партиции и отправка дублирующих запросов в другой регион.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/1-introduction

Сценарий: каталог товаров Contoso в одном регионе, высокая задержка чтения из Европы и Азии. Нужно понять, что будет при отказе региона, и настроить аккаунт и клиенты. Модуль: репликация и стоимость, регионы и чтения, запись в нескольких регионах, конфликты, операции failover, PPAF.

### 2. Explore global distribution and availability
https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/2-explore-global-distribution

Описаны реплика-наборы и партиции; при одном регионе записи репликация односторонняя, при нескольких - в обе стороны. Зональная избыточность синхронна внутри региона и настраивается по регионам; региональная защищает от потери региона. Стоимость: провизионированный throughput умножается на число регионов (T x N RU/s). RPO зависит от согласованности; serverless работает только в одном регионе.

### 3. Add regions and route reads
https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/3-add-regions-configure-reads

Регион добавляется через портал (Replicate data globally, Manage regions) или `az cosmosdb update --locations`. Без настройки предпочтительных регионов клиент читает и пишет в основной регион. В SDK задается список `ApplicationPreferredRegions` (.NET) или `preferred_locations` (Python). Список перечитывается каждые 5 минут. Отключать endpoint discovery не рекомендуется.

### 4. Configure multi-region writes
https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/4-configure-multi-region-writes

Включается настройка multi-region writes (портал или `az cosmosdb update --enable-multiple-write-locations true`) без простоя. Цена: нельзя strong consistency. Хаб-регион - регион создания аккаунта. Поля `_ts` и `crts`. Рекомендации: писать в регион происхождения трафика, не использовать случайный или round-robin выбор региона, передавать session token только для чтения, не переписывать один элемент часто.

### 5. Resolve write conflicts
https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/5-resolve-write-conflicts

Типы конфликтов: insert, replace, delete. По умолчанию - last writer wins по `_ts` (удаление всегда побеждает). Можно выбрать числовой путь (например, `/updateSequence`). Custom-политика использует merge stored procedure `resolveConflict` с параметрами incomingItem, existingItem, isTombstone, conflictingItems. Без процедуры конфликты попадают в conflict feed, где их нужно разбирать вручную. Политика задается только при создании контейнера.

### 6. Configure account failover
https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/6-configure-account-failover

Задайте приоритеты переключения (0 - регион записи). Три операции: смена региона записи (плановая, при здоровых регионах, без потерь), принудительное переключение Offline region (секунды, возможна потеря данных), автоматическое переключение сервисом (час и более). Не выполняйте операции управления в затронутом регионе. После восстановления регион возвращается как read region; запись возвращают плановой сменой региона и разбирают conflict feed.

### 7. Configure partition-level failover
https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/7-configure-partition-level-failover

PPAF переключает только затронутые партиции (около 3 минут) и работает для single-write-region аккаунтов. Требования: провизионированный throughput (не serverless), API for NoSQL, согласованность кроме bounded staleness, Direct mode, минимальные версии SDK (.NET 3.62.0, Java 4.79.0, Python 4.16.0, Node.js 4.7.0). PPAF входит в Business Critical и оплачивается отдельно. Включается через Features, с circuit breaker по умолчанию; hedging - опция клиента. Проверка через инъекцию сбоя (EnableDisableChaosFault.ps1 из репозитория ppaf-samples).

### 8. Exercise - Configure regions and failover
https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/8-exercise-configure-regions-failover

Практическое задание (около 45 минут): двухрегионный аккаунт, смена региона записи, включение multi-region writes и тест отказа региона. Нужна подписка Azure.

### 9. Module assessment
https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/9-knowledge-check

Проверка знаний (около 5 минут). Текст вопросов в источнике не приведен.

### 10. Summary
https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/10-summary

Подведены итоги: зональная и региональная избыточность сочетаются; регионы умножают стоимость и снижают RTO, RPO задается согласованностью; список предпочтительных регионов превращает реплицированный аккаунт в низколатентный; multi-region writes исключают strong consistency; политика конфликтов фиксируется при создании контейнера; три операции failover различаются по времени и риску потерь; PPAF переключает только партиции.

## Важные команды / код / настройки

**Добавление регионов (Azure CLI; список задает полный набор регионов):**
```
az cosmosdb update `
    --name "contoso-catalog" `
    --resource-group "contoso-data" `
    --locations regionName="West US 2" failoverPriority=0 isZoneRedundant=True `
    --locations regionName="North Europe" failoverPriority=1 isZoneRedundant=True
```

**Предпочтительные регионы (.NET):**
```
CosmosClientOptions options = new()
{
    ApplicationPreferredRegions = new List<string>
    {
        Regions.NorthEurope,
        Regions.WestUS2
    }
};
CosmosClient client = new(accountEndpoint, new DefaultAzureCredential(), options);
```

**Предпочтительные регионы (Python):**
```
client = CosmosClient(
    ACCOUNT_ENDPOINT,
    credential=DefaultAzureCredential(),
    preferred_locations=["North Europe", "West US 2"],
)
```

**Отключение маршрутизации (не рекомендуется):** .NET - `LimitToEndpoint = true`; Python - `enable_endpoint_discovery=False`.

**Включение multi-region writes (Azure CLI):**
```
az cosmosdb update `
    --name "contoso-catalog" `
    --resource-group "contoso-data" `
    --enable-multiple-write-locations true
```

**Клиент для записи в регионе (.NET):** `ApplicationRegion = Regions.NorthEurope`.

**Клиент для записи в нескольких регионах (Python):**
```
client = CosmosClient(
    ACCOUNT_ENDPOINT,
    credential=DefaultAzureCredential(),
    multiple_write_locations=True,
    preferred_locations=["North Europe", "West US 2"],
)
```

**Политика конфликтов (.NET):**
```
ContainerProperties properties = new("product", "/categoryId")
{
    ConflictResolutionPolicy = new ConflictResolutionPolicy()
    {
        Mode = ConflictResolutionMode.LastWriterWins,
        ResolutionPath = "/updateSequence"
    }
};
```

**Политика конфликтов (Python):**
```
container = database.create_container_if_not_exists(
    id="product",
    partition_key=PartitionKey(path="/categoryId"),
    conflict_resolution_policy={
        "mode": "LastWriterWins",
        "conflictResolutionPath": "/updateSequence",
    },
)
```

**Сигнатура merge stored procedure:** `function resolveConflict(incomingItem, existingItem, isTombstone, conflictingItems)`. Режим custom задается как `Mode = ConflictResolutionMode.Custom` с `ResolutionProcedure = "dbs/cosmicworks/colls/product/sprocs/resolveConflict"`.

**Приоритеты переключения (Azure CLI):**
```
az cosmosdb failover-priority-change `
    --name "contoso-catalog" `
    --resource-group "contoso-data" `
    --failover-policies westus2=0 northeurope=1 japaneast=2
```

**Принудительное переключение (Azure CLI):**
```
az cosmosdb offline-region `
    --name "contoso-catalog" `
    --resource-group "contoso-data" `
    --region "West US 2"
```

**Автоматическое переключение сервисом (Azure CLI; флаг сохраняет старое имя):**
```
az cosmosdb update `
    --name "contoso-catalog" `
    --resource-group "contoso-data" `
    --enable-automatic-failover true
```

**Минимальные значения bounded staleness при нескольких регионах:** 100 000 операций записи или 300 секунд.

**PPAF (Python SDK, hedging):**
```
client = CosmosClient(
    ACCOUNT_ENDPOINT,
    credential=DefaultAzureCredential(),
    preferred_locations=["West US 2", "North Europe"],
    availability_strategy={"threshold_ms": 300, "threshold_steps_ms": 100},
)
```
По умолчанию в Python: circuit breaker - 10 последовательных ошибок чтения, 5 - записи или 90% ошибок; hedging с `availability_strategy=True` - порог 500 мс и шаг 100 мс.

**Инъекция сбоя PPAF:** скрипт `EnableDisableChaosFault.ps1` (`-Enable` и `-Disable`), затрагивает 10% партиций (минимум 1, максимум 10); применение до 15 минут. Метрики портала: Total Requests и PartitionWriteGlobalStatus.

## Что запомнить

- Регион добавляется как изменение конфигурации; без списка предпочтительных регионов клиент читает из основного региона, и новый регион простаивает.
- При записи в нескольких регионах strong consistency недоступна, а конфликты разрешаются политикой, которую нельзя изменить после создания контейнера.
- Смена региона записи безопасна и без потерь, но работает только при здоровых регионах; для аварии используйте forced failover.
- Автоматическое переключение сервисом может занять час и более: это резерв для неконтролируемых аккаунтов.
- PPAF переключает только сбойные партиции, но требует новых версий SDK у всех клиентов и не поддерживает bounded staleness.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/
- В источнике упоминаются (без ссылок в тексте): Distribute your data globally with Azure Cosmos DB; Reliability in Azure Cosmos DB; Manage an Azure Cosmos DB account in the Azure portal; Multi-region writes in Azure Cosmos DB; Conflict types and resolution policies; Configure per-partition automatic failover; репозиторий ppaf-samples (EnableDisableChaosFault.ps1); SDK availability behavior in multiregional environments.
