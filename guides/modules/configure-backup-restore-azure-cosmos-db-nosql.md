# Настройка резервного копирования и восстановления в Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/<юнит>`)

## Цель модуля

Выбрать режим резервного копирования (periodic или continuous) и уровень хранения, включить continuous backup для нового и существующего аккаунта, выполнить point-in-time recovery (восстановление на момент времени) и проверить результат, а также понять, когда нужен Azure Backup для Azure Cosmos DB.

## Ключевые понятия

- **Periodic backup (периодическое резервное копирование)** — полные снимки по интервалу; по умолчанию интервал 4 часа и хранятся последние две копии. Интервал 1–24 часа, хранение от двойного интервала до 720 часов (30 дней). Восстановление требует обращения в службу поддержки.
- **Continuous backup (непрерывное резервное копирование)** — потоковое сохранение изменений; восстановление на любую секунду внутри окна хранения без обращения в поддержку. Миграция с periodic на continuous необратима.
- **Уровни хранения continuous backup** — `Continuous7Days` (7 дней, хранение бесплатно), `Continuous30Days` (30 дней, платное), `Continuous35Days` (35 дней, тариф как у 30 дней). Если уровень не указан, используется `Continuous30Days`.
- **Restore timestamp / latest restorable timestamp** — момент времени в UTC, на который можно восстановить данные; самая поздняя восстанавливаемая точка.
- **Same-account restore (восстановление в тот же аккаунт)** — восстанавливает только удаленную базу данных или контейнер в исходный аккаунт.
- **New-account restore (восстановление в новый аккаунт)** — создает отдельный аккаунт с состоянием на момент восстановления; нужен для живого, но поврежденного ресурса.
- **Azure Backup for Azure Cosmos DB** — хранение резервных копий в Backup vault с долгим сроком (до 10 лет), неизменяемостью и изоляцией от аккаунта. Функция находится в public preview.
- **Full и incremental backup** — в vault полная копия задает цепочку, инкрементальная хранит только изменения; полная копия должна быть раз в неделю.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/1-introduction
Решения о резервном копировании определяют скорость восстановления, глубину (насколько назад можно вернуться) и то, кто может выполнить восстановление. Модуль сравнивает режимы, включает continuous backup, выполняет point-in-time recovery и описывает Azure Backup для Azure Cosmos DB.

### 2. Evaluate backup options
Источник: https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/2-evaluate-backup-options
Резервные копии выполняются в фоне, не расходуют provisioned throughput, зашифрованы ключами Microsoft. Periodic — по умолчанию; восстановление создает новый аккаунт в регионе записи. Continuous — резервные копии во всех регионах аккаунта, асинхронно в пределах 100 секунд в стабильном состоянии; избыточность хранения не настраивается (LRS, либо ZRS при включенных зонах доступности). Условия для continuous: API for NoSQL, MongoDB, Gremlin или Table (Cassandra не поддерживается); на контейнерах не должен был отключаться Azure Synapse Link. Ограничения восстановления: в новом аккаунте не возвращаются правила брандмауэра, конфигурация виртуальной сети, private endpoints и RBAC-назначения на уровне данных; не восстанавливаются хранимые процедуры, триггеры и UDF. Cross-subscription restore для нативного восстановления не поддерживается. Аналитическое хранилище в резервные копии не входит.

### 3. Configure continuous backup
Источник: https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/3-configure-continuous-backup
Политика задается при создании аккаунта (Azure CLI, Azure PowerShell, Bicep, портал) или миграцией существующего аккаунта из periodic. Миграция необратима и требует права `Microsoft.DocumentDB/databaseAccounts/write`. Во время миграции `type` остается `Periodic`, а `migrationState` имеет статус `InProgress`. После завершения `migrationState` становится `null`, `type` — `Continuous`. Проверяется применённая политика и `latest restorable timestamp`, которое для контейнера может появиться не сразу после массовой загрузки. Для аккаунта и базы данных используется наименьший из таймстампов.

### 4. Perform point-in-time recovery
Источник: https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/4-perform-point-time-recovery
Выбор цели: same-account restore для удаленного ресурса (дешевле, данные между аккаунтами не переносятся) и new-account restore для живого ресурса с неверными данными или для удаленного аккаунта. Same-account restore не перезаписывает существующий ресурс; родительская база восстанавливается раньше контейнера; одновременно выполняется не более трех операций восстановления. Точку восстановления находят через event feed (события Create, Replace, Delete по базам и контейнерам; отдельные элементы не фиксируются). При восстановлении `--disable-ttl` отключает TTL, чтобы восстановленные элементы не удалились сразу. Для new-account restore рекомендуется `--public-network-access Disabled`, так как правила сети не наследуются. После восстановления проверяются статус (`Creating` → `Online`), конкретные элементы и количество, восстанавливаются сетевые настройки, role assignments, хранимые процедуры, триггеры и UDF. Клиенты перезапускаются, так как session и continuation-токены становятся недействительными, а change feed начинается заново.

### 5. Describe Azure backup for Azure Cosmos DB
Источник: https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/5-describe-azure-backup-for-cosmos-db
Нативное хранение ограничено 35 днями и предназначено для оперативного восстановления. Azure Backup добавляет долгое хранение (до 10 лет), неизменяемость, изоляцию от управления аккаунтом и централизованное управление. Vault хранит данные в geo-redundant хранилище. Резервные копии выполняются на уровне аккаунта (без восстановления отдельных элементов). Политика содержит еженедельную полную копию и инкрементальные копии в остальные дни (RPO — 1 день). Требуется, чтобы аккаунт уже работал в native continuous backup. Ограничения preview: API for NoSQL и MongoDB (на RU), не поддерживаются национальные облака, восстановление между регионами, иерархические partition keys, per-partition automatic failover, network security perimeter, serverless и целевые аккаунты с лимитом пропускной способности; до 2500 партиций (около 125 ТБ). Стоимость: фиксированная плата за защищаемый экземпляр, ежемесячная плата за объем в vault, плата за восстановление по объему.

### 6. Exercise - Recover from a recovery point
Источник: https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/6-exercise-recover-recovery-point
Практика (около 45 минут): включить continuous backup, удалить данные из каталога CosmicWorks и восстановить контейнер на выбранный момент. Доступны варианты на C# и Python. Нужна подписка Azure.

### 7. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/7-knowledge-check
Проверка знаний (в исходнике текст отсутствует).

### 8. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/8-summary
Защита аккаунта строится на сопоставлении режима, уровня хранения и пути восстановления с действиями команды. Модуль охватывает сравнение режимов, включение continuous backup, проверку политики и latest restorable timestamp, выбор между same-account и new-account restore, а также описание vaulted backup.

## Важные команды / код / настройки

Создание аккаунта с continuous backup (Azure CLI):

```bash
az cosmosdb create `
    --name "contoso-catalog" `
    --resource-group "contoso-data" `
    --backup-policy-type "Continuous" `
    --continuous-tier "Continuous7Days" `
    --default-consistency-level "Session" `
    --locations regionName="West US"
```

Создание аккаунта (Azure PowerShell):

```powershell
$parameters = @{
    ResourceGroupName = 'contoso-data'
    Name              = 'contoso-catalog'
    Location          = 'West US'
    ApiKind           = 'Sql'
    BackupPolicyType  = 'Continuous'
    ContinuousTier    = 'Continuous7Days'
}
New-AzCosmosDBAccount @parameters
```

Bicep:

```bicep
resource catalogAccount 'Microsoft.DocumentDB/databaseAccounts@2025-04-15' = {
  name: 'contoso-catalog'
  properties: {
    // Other required properties omitted for brevity
    backupPolicy: {
      type: 'Continuous'
      continuousModeProperties: {
        tier: 'Continuous7Days'
      }
    }
  }
}
```

Миграция существующего аккаунта из periodic (Azure CLI):

```bash
az cosmosdb update `
    --resource-group "contoso-data" `
    --name "contoso-reporting" `
    --backup-policy-type "Continuous" `
    --continuous-tier "Continuous7Days"
```

Миграция (Azure PowerShell):

```powershell
$parameters = @{
    ResourceGroupName = 'contoso-data'
    Name              = 'contoso-reporting'
    BackupPolicyType  = 'Continuous'
    ContinuousTier    = 'Continuous7Days'
}
Update-AzCosmosDBAccount @parameters
```

Проверка политики:

```bash
az cosmosdb show `
    --resource-group "contoso-data" `
    --name "contoso-catalog" `
    --query "backupPolicy"
```

Latest restorable timestamp для контейнера:

```bash
az cosmosdb sql retrieve-latest-backup-time `
    --resource-group "contoso-data" `
    --account-name "contoso-catalog" `
    --database-name "cosmicworks" `
    --container-name "product" `
    --location "West US"
```

Получение информации о backup контейнера (Azure PowerShell):

```powershell
$parameters = @{
    ResourceGroupName = 'contoso-data'
    AccountName       = 'contoso-catalog'
    DatabaseName      = 'cosmicworks'
    Name              = 'product'
    Location          = 'West US'
}
Get-AzCosmosDBSqlContainerBackupInformation @parameters
```

Список экземпляров восстанавливаемого аккаунта и событий:

```bash
az cosmosdb restorable-database-account list `
    --account-name "contoso-catalog"

az cosmosdb sql restorable-database list `
    --instance-id "<instance-id>" `
    --location "West US"

az cosmosdb sql restorable-container list `
    --instance-id "<instance-id>" `
    --database-rid "<database-resource-id>" `
    --location "West US"
```

Same-account restore контейнера (Azure CLI):

```bash
az cosmosdb sql container restore `
    --resource-group "contoso-data" `
    --account-name "contoso-catalog" `
    --database-name "cosmicworks" `
    --name "product" `
    --restore-timestamp "2026-09-04T14:10:00Z" `
    --disable-ttl True
```

Same-account restore контейнера (Azure PowerShell):

```powershell
$parameters = @{
    ResourceGroupName     = 'contoso-data'
    AccountName           = 'contoso-catalog'
    DatabaseName          = 'cosmicworks'
    Name                  = 'product'
    RestoreTimestampInUtc = '2026-09-04T14:10:00Z'
    DisableTtl            = $true
}
Restore-AzCosmosDBSqlContainer @parameters
```

Восстановление удаленной базы данных: `az cosmosdb sql database restore` (восстанавливает базу вместе с ее контейнерами).

New-account restore (Azure CLI):

```bash
az cosmosdb restore `
    --resource-group "contoso-data" `
    --target-database-account-name "contoso-catalog-recovered" `
    --account-name "contoso-catalog" `
    --restore-timestamp "2026-09-04T14:10:00Z" `
    --location "West US" `
    --public-network-access Disabled `
    --disable-ttl True
```

Выборочное восстановление: `--databases-to-restore name=cosmicworks collections=product`.

Роли: встроенная роль `CosmosRestoreOperator` (действие restore и чтения для интерфейса восстановления; назначается на подписку или на restorable account resource); для создания нового аккаунта нужно `Microsoft.DocumentDB/databaseAccounts/write` в группе ресурсов (роль Cosmos DB Operator).

Azure Resource Graph для аудита режимов backup — запрос по типу `microsoft.documentdb/databaseAccounts` с полями `properties.backupPolicy.type`, `periodicModeProperties` и `continuousModeProperties.tier` (полный текст запроса — в уроке 2 исходника).

## Что запомнить

- Миграция с periodic на continuous необратима; проверьте условия (особенно Azure Synapse Link) до миграции.
- Всегда явно задавайте уровень `Continuous7Days`/`Continuous30Days`/`Continuous35Days`: без него используется платный 30-дневный уровень.
- Точка восстановления не может быть раньше создания ресурса; проверяйте latest restorable timestamp, а не текущее время.
- Same-account restore восстанавливает только удаленные ресурсы; new-account restore создает новый аккаунт, для которого нужно заново настроить сеть и роли.
- Azure Backup для Azure Cosmos DB добавляет хранение до 10 лет в изолированном vault, но находится в public preview и требует native continuous backup.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/
- Документация: Choosing a backup mode; Periodic backup; Continuous backup and point-in-time restore; Provision an account with continuous backup; Migrate from periodic to continuous mode; Restore a deleted container or database to the same account; Configure restore permissions; Azure Backup for Azure Cosmos DB (упоминаются в уроках 2–5).
- Связанный модуль: Try Azure Cosmos DB for NoSQL (`try-azure-cosmos-db-sql-api`).
