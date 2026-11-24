# Настройка multi-region write в Azure Cosmos DB (SQL API)

**Источник:** https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/

## Цель модуля

Настроить Azure Cosmos DB для записи во все регионы (multi-region write), выбрать регион записи в .NET SDK и понять, как разрешаются конфликты при одновременном изменении одного элемента в разных регионах.

## Ключевые понятия

- **Multi-region write** - режим, при котором каждый регион аккаунта может принимать операции записи; позволяет масштабировать записи глобально.
- **Strong consistency** - в сценарии multi-region write не поддерживается.
- **Preferred regions (предпочтительные регионы)** - список регионов, в порядке которого SDK пытается выполнять операции при недоступности текущего.
- **Конфликт (conflict)** - ситуация, когда один элемент одновременно меняют в разных регионах. Бывают конфликты вставки (insert), замены (replace) и удаления (delete).
- **Last Write Wins (LWW)** - политика по умолчанию: побеждает элемент с наибольшим значением `_ts` (или другого числового пути, заданного через conflict resolution path); при конфликте удаления побеждает операция удаления.
- **Custom conflict resolution** - собственная логика разрешения конфликтов на основе хранимой процедуры или ручная обработка через conflicts feed.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/1-introduction

Multi-write позволяет масштабировать записи по всему миру. Цели модуля: настроить multi-region write и выбрать регион записи в .NET SDK.

### 2. Понимание multi-region write
URL: https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/2-understand

Каждый регион поддерживает и чтение, и запись. Включение записи во все регионы - операция, не прерывающая доступность приложения. Сохраняются многие возможности одного региона: шкала уровней консистентности, низкая задержка записи, высокая доступность с SLA. Strong consistency не поддерживается. При отказе дата-центра аккаунт продолжает работать, так как SDK пробует другой регион из списка предпочтительных. Настроить можно через Azure CLI, PowerShell, код, шаблоны ARM (JSON/Bicep) или портал Azure. После включения все реплики становятся регионами записи.

### 3. Настройка поддержки нескольких регионов в SDK
URL: https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/3-support-sdk

Если регион не задан, SDK использует основной регион аккаунта (первый в списке, обычно выбранный при создании). Свойство `ApplicationRegion` задает регион, с которым SDK работает; после подключения клиент получает список регионов и упорядочивает их по близости, а при недоступности выбранного переходит к следующим. Свойство `ApplicationPreferredRegions` задает собственный приоритетный список.

### 4. Понимание политик разрешения конфликтов
URL: https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/4-understand-conflict-resolution-policies

Три типа конфликтов: Insert, Replace, Delete. По умолчанию действует Last Write Wins по `_ts`. Можно задать другой числовой путь через conflict resolution path, например `/sortableTimestamp`. Политику можно задать только при создании контейнера.

### 5. Создание пользовательской политики разрешения конфликтов
URL: https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/5-create-custom-conflict-resolution-policy

Custom-политика использует хранимую процедуру с фиксированной сигнатурой из четырех параметров: `incomingItem` (вставляемый или обновляемый элемент), `existingItem` (уже зафиксированный элемент), `isTombstone` (был ли элемент ранее удален) и `conflictingItems` (массив конфликтующих зафиксированных элементов). Альтернатива без процедуры - режим Custom без процедуры: конфликты попадают в conflicts feed, и приложение разрешает их вручную.

### 6. Упражнение: подключение аккаунта multi-region write через SDK
URL: https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/6-exercise-connect-multi-region-write-account-sdk

Практика (нужна подписка Azure с правами администратора): создать группу ресурсов, настроить локальную среду, включить провайдеры ресурсов. Дополнительных шагов в тексте урока нет.

### 7. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/7-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 8. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/8-summary

Включение multi-region write на аккаунте и выбор предпочтительного региона записи в .NET SDK.

## Важные команды / код / настройки

Выбор региона записи через `ApplicationRegion` (.NET):

```csharp
CosmosClientOptions options = new()
{
    ApplicationRegion = Regions.WestUS
};
TokenCredential managedIdentityCredential = new ManagedIdentityCredentialBuilder()
    .clientId("<your-managed-identity-client-id>")
    .build();
using CosmosClient client = new CosmosClient("<your-cosmos-endpoint>", managedIdentityCredential, options);
```

Собственный приоритетный список регионов через `ApplicationPreferredRegions` (.NET):

```csharp
CosmosClientOptions options = new()
{
    ApplicationPreferredRegions = new List<string>
    {
        Regions.WestUS,
        Regions.AustraliaSoutheast,
        Regions.NorthEurope
    }
};
```

То же через `CosmosClientBuilder`: `.WithApplicationRegion(Regions.WestUS)` или `.WithApplicationPreferredRegions(...)`.

Container с политикой Last Write Wins по собственному пути:

```csharp
ContainerProperties properties = new("products", "/categoryId")
{
    ConflictResolutionPolicy = new ConflictResolutionPolicy()
    {
        Mode = ConflictResolutionMode.LastWriterWins,
        ResolutionPath = "/sortableTimestamp",
    }
};
```

Custom-политика со ссылкой на хранимую процедуру:

```csharp
ContainerProperties properties = new(containerName, partitionKey)
{
    ConflictResolutionPolicy = new ConflictResolutionPolicy()
    {
        Mode = ConflictResolutionMode.Custom,
        ResolutionProcedure = $"dbs/{databaseName}/colls/{containerName}/sprocs/{sprocName}",
    }
};
```

Ручное разрешение через conflicts feed: `ConflictResolutionMode.Custom` без `ResolutionProcedure`.

Сигнатура хранимой процедуры разрешения конфликтов:

```javascript
function <function-name>(incomingItem, existingItem, isTombstone, conflictingItems)
```

## Что запомнить

- Multi-region write делает каждый регион записываемым; strong consistency в этом режиме недоступна.
- SDK выбирает регион через `ApplicationRegion` или собственный список `ApplicationPreferredRegions`.
- Политика конфликтов по умолчанию - Last Write Wins по `_ts`; другой числовой путь задается через `ResolutionPath`.
- Политику конфликтов можно задать только при создании контейнера.
- Для сложной логики используйте custom-политику: хранимую процедуру с параметрами `incomingItem`, `existingItem`, `isTombstone`, `conflictingItems` или ручную обработку conflicts feed.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/
- Configure multi-region writes in your applications that use Azure Cosmos DB, Conflict types and resolution policies when using multiple write regions, Manage conflict resolution policies in Azure Cosmos DB (названия из источника, URL не приведены)
