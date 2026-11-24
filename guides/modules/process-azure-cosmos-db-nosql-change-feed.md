# Обработка change feed и копирование данных в Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/<юнит>`)

## Цель модуля

Научиться строить событийные интеграции на change feed Azure Cosmos DB (через change feed processor, pull model и триггер Azure Functions), выбирать режим change feed и перемещать данные контейнера в другой контейнер с помощью container copy jobs.

## Ключевые понятия

- **Change feed (лента изменений)** — журнал изменений контейнера, упорядоченный внутри каждого значения partition key; глобального порядка между партициями нет.
- **Latest version mode (режим последней версии)** — режим по умолчанию: фиксирует создание и обновление, возвращает только последнюю версию элемента, удаления не фиксирует; не имеет окна хранения.
- **All versions and deletes mode (режим всех версий и удалений)** — фиксирует создание, обновления, промежуточные версии, удаления и истечения TTL; доступен в пределах окна continuous backup; требует NoSQL API, continuous backup и включения функции на аккаунте.
- **Change feed processor** — библиотека внутри приложения: хранит позицию в lease-документах, распределяет работу между экземплярами; есть в .NET V3 SDK и Java V4 SDK.
- **Pull model** — прямое чтение ленты с сохранением continuation token; доступно в .NET, Java, Python и Node.js; ручное управление опросом, повторами и распределением.
- **Lease container (контейнер аренд)** — контейнер с ключом `/id`, где хранится позиция обработчика.
- **Change feed estimator** — оценка отставания потребителя (количество ожидающих изменений) по каждой аренде.
- **At-least-once delivery** — гарантия доставки «не менее одного раза»: позиция продвигается только после успешной обработки батча, поэтому обработчики должны быть идемпотентными.
- **Azure Functions trigger for Azure Cosmos DB** — платформа выполняет процессор и вызывает функцию для каждого батча.
- **Container copy job (задание копирования контейнера)** — серверное задание переноса данных в новый контейнер (например, с другим partition key); может быть offline (запись в источник остановлена) или online (режим All versions and deletes, нужна явная команда завершения). Функция находится в публичном preview.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/1-introduction
Опрос контейнера тратит RU даже без изменений, не видит удаления и не сохраняет промежуточные версии. Change feed решает эти задачи: изменения упорядочены внутри partition key, потребители читают инкрементально и могут возобновлять работу с сохраненной позиции. Сценарий Contoso: обновление копий названия категории в документах товаров и перенос каталога на иерархический partition key.

### 2. Understand the change feed
Источник: https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/2-understand-change-feed
Change feed включен на каждом контейнере и не отключается. Четыре свойства: порядок гарантируется внутри значения partition key; изменения в одной транзакционной области (batch, хранимая процедура, bulk) имеют одинаковую метку времени и могут прийти в любом порядке; ленту можно читать параллельно по feed ranges; несколько независимых потребителей читают одну ленту со своими позициями. Чтение тратит RU контейнера. Процессор создает lease-документы; pull model не требует lease-контейнера, но требует сохранения токенов. Сравнение: процессор автоматически опрашивает и распределяет работу, pull model — вручную; pull model может читать один partition key, процессор — нет. Continuation token и lease несовместимы между собой. В мультирегиональных аккаунтах с несколькими регионами записи элементы идут по метке времени разрешения конфликтов; в режиме по умолчанию изменение может быть отброшено, если в другом регионе пришло более новое изменение того же элемента. Estimator запускают отдельно; проверку можно делать примерно раз в минуту.

### 3. Implement a change feed consumer
Источник: https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/3-implement-change-feed-processor
Компоненты: monitored container (`productMeta`), lease container (`/id`), compute instance (уникальное имя), delegate. В .NET обработчик получает `ChangeFeedProcessorContext`, фильтрует по свойству `type` и запускается через `GetChangeFeedProcessorBuilder` с именем процессора, `WithInstanceName`, `WithLeaseContainer`, `WithErrorNotification` (без последнего ошибки чтения нигде не появятся). Разные имена процессора с общим lease-контейнером дают независимые позиции. В Python SDK процессора нет: цикл читает ленту, сохраняет continuation token через `by_page()` после обработки страницы. Токен сохраняется только после обработки батча. Для распределения работы читаются `read_feed_ranges()` (один feed range — одна физическая партиция); диапазоны меняются при разбиении партиций, поэтому их нужно периодически перечитывать. Чтение одного partition key поддерживается pull model. Начальная позиция: процессор по умолчанию начинает с текущего момента; `WithStartTime(DateTime.MinValue.ToUniversalTime())` или `start_time="Beginning"` читают историю. Начальная позиция действует только до появления lease или токена. Ошибки: at-least-once; необработанное исключение повторяет весь батч; постоянно падающее изменение блокирует диапазон, поэтому ошибки нужно перехватывать и записывать в отдельное хранилище ошибок. Таймаут клиента должен быть больше 5-секундного серверного таймаута. Не запускайте асинхронную работу без await внутри обработчика. Масштабирование: экземпляры с одним именем процессора и lease-контейнером делят аренды; аренда истекает через 60 секунд, интервал получения — 13 секунд. Для мультирегиональных аккаунтов клиент должен использовать глобальный endpoint. Права: роль Cosmos DB Built-in Data Contributor; назначения data-plane делаются через `az cosmosdb sql role assignment create`, а не в портале.

### 4. Choose a change feed mode
Источник: https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/4-choose-change-feed-mode
Latest version: фиксирует только итоговое состояние элемента; удаления не видны; нет окна хранения; старт с начала контейнера или с текущего момента (точность времени около 5 секунд). Для учета удалений используется soft delete (флаг `deleted: true` и TTL). All versions and deletes: каждое изменение в порядке возникновения, метаданные `operationType`, `lsn`, `crts`, `previousImageLSN`, `timeToLiveExpired`; предыдущего образа элемента нет. Ограничения: только NoSQL API; continuous backup; включение функции до 30 минут, другие изменения аккаунта во время включения запрещены; несовместимо с partition merge; все чтения идут через gateway mode; доступны только текущий момент или сохраненная позиция, но не начало контейнера или произвольная метка времени. Поддержка SDK: pull model — .NET 3.60.0+, Java 4.81.0+, Python 4.9.1b1+, Node.js 4.1.0+; процессор — .NET 3.60.0+ и Java 4.81.0+; Azure Functions trigger — .NET isolated worker extension 4.16.1+. В .NET — `GetChangeFeedProcessorBuilderWithAllVersionsAndDeletes`, делегат получает `ChangeFeedItem<T>` с `Current` и `Metadata`. Разные приложения могут читать одну ленту в разных режимах, но один потребитель не меняет режим.

### 5. Handle events with Azure Functions
Источник: https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/5-handle-events-azure-functions
Триггер сам запускает процессор, опрашивает ленту, хранит позицию в lease-контейнере и вызывает функцию с батчем. Поддерживается только NoSQL API. В .NET isolated — атрибут `CosmosDBTrigger` с параметрами `%COSMOS_DATABASE_NAME%`, `%COSMOS_CONTAINER_NAME%`, `Connection`, `LeaseContainerName`. Необработанное исключение завершает вызов; политика повторов по умолчанию не настроена; ошибки лучше перехватывать и сохранять в долговечное хранилище до успешного завершения вызова. В Python v2 — декоратор `@app.cosmos_db_trigger`. Identity-based подключение: `COSMOS_CONNECTION__accountEndpoint`, `COSMOS_CONNECTION__credential=managedidentity`, `COSMOS_CONNECTION__clientId`. Локально достаточно `az login` и endpoint в `local.settings.json`. Lease-контейнер лучше создать заранее с ключом `/id`: свойство `CreateLeaseContainerIfNotExists` требует операций control plane, которых нет у роли data plane. Две функции с одинаковыми lease-контейнером и без разных префиксов будут делить аренды; для независимой работы задайте разные префиксы lease-контейнера или отдельные lease-контейнеры. Настройки: `FeedPollDelay` (по умолчанию 5000 мс), `MaxItemsPerInvocation`, `StartFromBeginning`. Режим All versions and deletes доступен только в .NET isolated worker, нужна версия расширения 4.16.1+. Самостоятельный процессор предпочтителен, когда нужны уведомления о получении и освобождении аренд или estimator на собственных арендах; в .NET и Java он поддерживает режим All versions and deletes, в Python и Node.js — нет.

### 6. Move data with container copy jobs
Источник: https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/6-move-data-container-copy-jobs
Смена partition key требует переноса данных в контейнер с новым ключом. Container copy job создается на целевом аккаунте, читает change feed исходного контейнера и пишет в заранее созданный целевой контейнер. Компute освобождается после 15 минут простоя. Задание копирует один контейнер; задания в одном аккаунте выполняются последовательно. Offline copy: читает latest version, запись в источник должна быть остановлена, дополнительных настроек аккаунта не нужно, завершается сам. Online copy: читает all versions and deletes, запись разрешена; нужны continuous backup, режим All versions and deletes, возможность `EnableOnlineContainerCopy` (через `az cosmosdb update`); после включения подождать не менее 30 минут; надбавка 50–100% на replace и delete в источнике; завершается командой `az cosmosdb copy complete`. Команды — в расширении `cosmosdb-preview` (`az extension add --name cosmosdb-preview`). Целевой контейнер создается заранее со всеми настройками (ключ, уникальные ключи, пропускная способность, политика индексации). Копирование между аккаунтами требует managed identity с ролью Cosmos DB Built-in Data Contributor на цели. Прогресс — `az cosmosdb copy show` (total и processed). Для online: когда processed достигает total, остановить запись в источник, подождать 5–10 минут и выполнить `az cosmosdb copy complete`. Вычислительные ресурсы по умолчанию: два экземпляра по 4 vCPU и 16 ГБ на аккаунт, общие для всех заданий. Пропускная способность цели — не менее двух значений пропускной способности источника на время копирования; SLA не предусмотрен. Ограничения: доступен не во всех регионах (задание выполняется в регионе записи целевого аккаунта); смена региона записи прерывает задание; container-level TTL не копируется, item-level `ttl` сохраняется с пересчетом; при смене ключа конфликтуют элементы с одинаковым id и разными ключами, которые после смены совпадут; лимит 20 ГБ на логическую партицию сохраняется (ошибка 403); при включенном partition merge задание не работает, а для online-копии аккаунт с завершенным merge в истории не подходит.

### 7. Exercise - Process changes and copy data
Источник: https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/7-exercise-process-changes-copy-data
Практика (около 45 минут): синхронизация денормализованных данных через change feed, обработка изменений в Azure Functions и копирование данных в контейнер с другим partition key. Варианты на C# и Python. Нужна подписка Azure.

### 8. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/8-knowledge-check
Проверка знаний (в исходнике текст отсутствует).

### 9. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/9-summary
Контейнер можно использовать как источник событий и переносить его данные при изменении дизайна. Денормализованные названия категорий синхронизируются автоматически, а каталог может перейти на новый partition key без перестройки конвейера.

## Важные команды / код / настройки

Обработчик и запуск процессора (.NET):

```csharp
static async Task HandleChangesAsync(
    ChangeFeedProcessorContext context,
    IReadOnlyCollection<ProductMetaItem> changes,
    CancellationToken cancellationToken)
{
    Console.WriteLine($"Lease {context.LeaseToken} consumed {context.Headers.RequestCharge} RU.");

    foreach (ProductMetaItem item in changes)
    {
        if (item.type != "category")
        {
            continue;
        }

        await SyncCategoryNameAsync(item, cancellationToken);
    }
}
```

```csharp
Container monitoredContainer = client.GetContainer("cosmicworks", "productMeta");
Container leaseContainer = client.GetContainer("cosmicworks", "leases");

ChangeFeedProcessor processor = monitoredContainer
    .GetChangeFeedProcessorBuilder<ProductMetaItem>(
        processorName: "categoryNameSync",
        onChangesDelegate: HandleChangesAsync)
    .WithInstanceName("catalog-worker-1")
    .WithLeaseContainer(leaseContainer)
    .WithErrorNotification(HandleErrorAsync)
    .Build();

await processor.StartAsync();
await processor.StopAsync();
```

Чтение ленты в Python (pull model):

```python
import time

monitored = database.get_container_client("productMeta")

continuation = load_checkpoint()

while True:
    if continuation:
        changes = monitored.query_items_change_feed(continuation=continuation)
    else:
        changes = monitored.query_items_change_feed(start_time="Beginning")

    pages = changes.by_page()
    for page in pages:
        for item in page:
            if item["type"] == "category":
                sync_category_name(item)

        continuation = pages.continuation_token
        save_checkpoint(continuation)

    time.sleep(5)
```

Чтение по feed range и по одному partition key:

```python
ranges = list(monitored.read_feed_ranges())

changes = monitored.query_items_change_feed(
    start_time="Beginning",
    feed_range=ranges[0],
)

changes = monitored.query_items_change_feed(
    start_time="Beginning",
    partition_key="category",
)
```

Формат метаданных удаления в режиме All versions and deletes:

```json
{
  "metadata": {
    "operationType": "delete",
    "lsn": 17,
    "crts": 1735689600,
    "previousImageLSN": 16,
    "timeToLiveExpired": false,
    "id": "3E4CEACD-D007-46EB-82D7-31F6141752B2",
    "partitionKey": {
      "type": "category"
    }
  }
}
```

Триггер Azure Functions (.NET isolated):

```csharp
[Function("SyncCategoryName")]
public async Task Run(
    [CosmosDBTrigger(
        databaseName: "%COSMOS_DATABASE_NAME%",
        containerName: "%COSMOS_CONTAINER_NAME%",
        Connection = "COSMOS_CONNECTION",
        LeaseContainerName = "leases")] IReadOnlyList<ProductMetaItem> changes,
    FunctionContext context)
{
    if (changes is null)
    {
        return;
    }

    foreach (ProductMetaItem item in changes.Where(c => c.type == "category"))
    {
        try
        {
            await SyncCategoryNameAsync(item);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to sync category {id}", item.id);
            await WriteFailedChangeAsync(item, ex);
        }
    }
}
```

Триггер Azure Functions (Python v2):

```python
import logging
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="SyncCategoryName")
@app.cosmos_db_trigger(
    arg_name="changes",
    database_name="%COSMOS_DATABASE_NAME%",
    container_name="%COSMOS_CONTAINER_NAME%",
    connection="COSMOS_CONNECTION",
    lease_container_name="leases",
)
def sync_category_name(changes: func.DocumentList) -> None:
    for item in changes:
        if item["type"] != "category":
            continue
        try:
            sync_category(item)
        except Exception as error:
            logging.exception("Failed to sync category %s", item["id"])
            write_failed_change(item, error)
```

Настройки подключения с managed identity:

| Настройка | Значение |
|---|---|
| COSMOS_CONNECTION__accountEndpoint | https://<account-name>.documents.azure.com:443/ |
| COSMOS_CONNECTION__credential | managedidentity |
| COSMOS_CONNECTION__clientId | Client ID user-assigned managed identity |

Команды копирования контейнера:

```bash
az extension add --name cosmosdb-preview

az cosmosdb copy create `
    --resource-group $destinationAccountRG `
    --job-name $jobName `
    --dest-account $destinationAccount `
    --src-account $sourceAccount `
    --dest-nosql database=$destinationDatabase container=$destinationContainer `
    --src-nosql database=$sourceDatabase container=$sourceContainer

# Online job: добавить --mode Online
# Прогресс: az cosmosdb copy show
# Завершение online-задания: az cosmosdb copy complete
```

Включение online copy: `az cosmosdb update` с capability `EnableOnlineContainerCopy` на исходном аккаунте (подождать 30 минут).

Команды назначения ролей: `az cosmosdb sql role assignment create` (роль Cosmos DB Built-in Data Contributor).

## Что запомнить

- Change feed включен всегда; порядок гарантируется внутри значения partition key, а не между ними.
- Latest version фиксирует только итоговое состояние и не показывает удаления; All versions and deletes — все версии и удаления в пределах окна continuous backup.
- Обработчики должны быть идемпотентными: доставка «не менее одного раза»; постоянно падающее изменение нужно вынести в отдельное хранилище ошибок.
- Триггер Azure Functions — самый короткий путь к непрерывному потребителю, в том числе для Python; lease-контейнер с ключом `/id` создавайте заранее.
- Container copy job переносит данные в контейнер с новым partition key; offline требует остановки записи, online — дополнительных настроек аккаунта и команды завершения; целевой контейнер нужно создать заранее.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/process-azure-cosmos-db-nosql-change-feed/
- Документация: Change feed in Azure Cosmos DB; Change feed modes; Change feed processor; Change feed pull model; Azure Cosmos DB trigger for Azure Functions; Container copy jobs (упоминаются в уроке 9).
- Связанный модуль: Design data partitioning strategy (`design-data-partitioning-strategy`) — модель с контейнером productMeta и change feed для ссылочной целостности.
- Связанный модуль: Configure backup and restore (`configure-backup-restore-azure-cosmos-db-nosql`) — continuous backup нужен для режима All versions and deletes.
