# Написание скриптов для Azure Cosmos DB (SQL API) с Azure CLI

**Источник:** https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/

## Цель модуля

Администрировать ресурсы Azure Cosmos DB для NoSQL из Azure CLI: создавать аккаунт, базы и контейнеры, управлять индексной политикой и throughput, переключать режим throughput, менять регионы и инициировать отработку отказа (failover).

## Ключевые понятия

- **Azure CLI** - набор команд для управления ресурсами Azure; для Cosmos DB есть встроенные команды, часть новых возможностей поставляется как расширения.
- **`az cosmosdb`** - группа команд для управления аккаунтом.
- **`az cosmosdb sql`** - подгруппа для ресурсов NoSQL API: базы данных и контейнеры.
- **Индексная политика (indexing policy)** - задается при создании контейнера через `--idx` (имя JSON-файла или строка JSON).
- **Throughput (standard / autoscale)** - пропускная способность контейнера или базы; может переключаться между manual и autoscale.
- **Failover priority** - приоритет регионов для отработки отказа; регион с приоритетом 0 - основной, его смена инициирует ручной failover.
- **Multi-region write** - включение записи во все регионы аккаунта.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/1-introduction

Azure CLI содержит команды для основных административных сценариев Cosmos DB; новые возможности доступны как расширения. Модуль учит просматривать аргументы, группы и подгруппы команд, создавать аккаунт, базы и контейнеры, управлять индексной политикой и throughput, инициировать failover и управлять регионами.

### 2. Создание ресурсов
URL: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/2-create-resources

Команда `az cosmosdb create` создает аккаунт и требует имя (глобально уникальное) и группу ресурсов; по умолчанию создается аккаунт NoSQL. Можно задать уровень консистентности по умолчанию (например, Eventual), включить бесплатный уровень и регион через `--locations`. Базы и контейнеры создаются в подгруппе `az cosmosdb sql`; для контейнера обязателен `--partition-key-path`.

### 3. Управление индексными политиками
URL: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/3-manage-index-policies

Индексная политика задается при создании контейнера аргументом `--idx`: либо именем JSON-файла, либо строкой JSON. Если политика не задана, используется политика по умолчанию. Пример политики: режим `consistent`, `automatic: true`, включенные пути `/*`, исключенные `/headquarters/*` и путь `_etag`. Модуль предупреждает, что экранирование строк JSON в Bash и PowerShell работает по-разному.

### 4. Настройка provisioned throughput для базы и контейнера
URL: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/4-configure-database-container-provisioned-throughput

Подгруппа `throughput` с командой `update` есть у контейнеров и баз. Примеры: контейнер переводится на 1000 RU/s, база - на 4000 RU/s.

### 5. Переход между standard и autoscale throughput
URL: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/5-migrate-standard-autoscale-throughput

Команда `az cosmosdb sql container throughput migrate` с аргументом `--throughput-type` (`autoscale` или `manual`) переключает режим контейнера. Максимум autoscale меняется через `throughput update` с `--max-throughput`. Минимум autoscale показывает `throughput show` с запросом `resource.minimumThroughput`. Вернуть контейнер на ручной режим можно той же командой миграции.

### 6. Смена приоритета регионов для failover
URL: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/6-change-region-failover-priority

Команда `az cosmosdb update` добавляет регионы (`--locations regionName=... failoverPriority=... isZoneRedundant=...`), включает автоматический failover (`--enable-automatic-failover`), включает multi-region write (`--enable-multiple-write-locations`) и удаляет регионы: все регионы, не перечисленные в `--locations`, удаляются. Смена приоритетов выполняется командой `az cosmosdb failover-priority-change` с `--failover-policies`, где нужно перечислить все регионы. Во время операции с регионами другие изменения аккаунта запрещены, пока операция не завершится.

### 7. Инициация failover
URL: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/7-initiate-failovers

Смена региона с приоритетом 0 запускает ручной failover. Пример: переключение приоритетов `westus2=0` и `eastus=1`. Изменение приоритета региона, не равного 0, failover не запускает.

### 8. Упражнение: настройка provisioned throughput через скрипт Azure CLI
URL: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/8-exercise-adjust-provisioned-throughput-using-azure-cli-script

Практика по настройке throughput скриптом Azure CLI; нужна подписка Azure с правами администратора.

### 9. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/9-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 10. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/10-summary

Использование группы `az cosmosdb` и подгрупп NoSQL для создания и управления ресурсами; `--help` для просмотра аргументов; настройка индексной политики и throughput; failover и управление регионами.

## Важные команды / код / настройки

Создание аккаунта:

```bash
az cosmosdb create \
    --name '<account-name>' \
    --resource-group '<resource-group>' \
    --default-consistency-level 'Eventual' \
    --enable-free-tier 'true'
```

Создание базы и контейнера:

```bash
az cosmosdb sql database create \
    --account-name '<account-name>' \
    --resource-group '<resource-group>' \
    --name '<database-name>'

az cosmosdb sql container create \
    --account-name '<account-name>' \
    --resource-group '<resource-group>' \
    --database-name '<database-name>' \
    --name '<container-name>' \
    --throughput '400' \
    --partition-key-path '<partition-key-path-string>'
```

Контейнер с индексной политикой из файла:

```bash
az cosmosdb sql container create \
    --account-name '<account-name>' \
    --resource-group '<resource-group>' \
    --database-name '<database-name>' \
    --name '<container-name>' \
    --partition-key-path '<partition-key-path-string>' \
    --idx '@.\policy.json' \
    --throughput '400'
```

Изменение throughput контейнера и базы:

```bash
az cosmosdb sql container throughput update \
    --account-name '<account-name>' \
    --resource-group '<resource-group>' \
    --database-name '<database-name>' \
    --name '<container-name>' \
    --throughput '1000'

az cosmosdb sql database throughput update \
    --account-name '<account-name>' \
    --resource-group '<resource-group>' \
    --name '<database-name>' \
    --throughput '4000'
```

Миграция на autoscale и изменение максимума:

```bash
az cosmosdb sql container throughput migrate \
    --account-name '<account-name>' \
    --resource-group '<resource-group>' \
    --database-name '<database-name>' \
    --name '<container-name>' \
    --throughput-type 'autoscale'

az cosmosdb sql container throughput update \
    --account-name '<account-name>' \
    --resource-group '<resource-group>' \
    --database-name '<database-name>' \
    --name '<container-name>' \
    --max-throughput '5000'
```

Минимум autoscale:

```bash
az cosmosdb sql container throughput show \
    --account-name '<account-name>' \
    --resource-group '<resource-group>' \
    --database-name '<database-name>' \
    --name '<container-name>' \
    --query 'resource.minimumThroughput' \
    --output 'tsv'
```

Включение автоматического failover и multi-region write:

```bash
az cosmosdb update \
    --name '<account-name>' \
    --resource-group '<resource-group>' \
    --enable-automatic-failover 'true'

az cosmosdb update \
    --name '<account-name>' \
    --resource-group '<resource-group>' \
    --enable-multiple-write-locations 'true'
```

Смена приоритетов регионов и ручной failover:

```bash
az cosmosdb failover-priority-change \
    --name '<account-name>' \
    --resource-group '<resource-group>' \
    --failover-policies 'westus2=0' 'eastus=1'
```

Помните: в `failover-policies` нужно перечислять все регионы аккаунта.

## Что запомнить

- Аккаунт создается `az cosmosdb create`, базы и контейнеры - `az cosmosdb sql ...`; для контейнера обязателен `--partition-key-path`.
- Индексную политику можно передать файлом или строкой JSON через `--idx`; строку экранируйте с учетом оболочки.
- Throughput меняется на уровне контейнера или базы; autoscale настраивается через `--max-throughput`.
- Регион с приоритетом 0 - основной; смена этого приоритета запускает ручной failover.
- `az cosmosdb update --locations` удаляет регионы, которых нет в списке, поэтому перечисляйте все нужные регионы.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/
- Azure CLI for Azure Cosmos DB; az cosmosdb; az cosmosdb sql (названия из источника, URL не приведены)
