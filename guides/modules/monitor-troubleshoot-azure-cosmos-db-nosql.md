# Мониторинг и устранение неполадок Azure Cosmos DB для NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-azure-cosmos-db-nosql/

## Цель модуля

Научиться по коду ответа, метрикам, алертам и диагностическим логам находить причину деградации Azure Cosmos DB для NoSQL: интерпретировать коды ответов и троттлинг (429), отслеживать задержку и загрузку партиций, настраивать алерты Azure Monitor и анализировать логи в Log Analytics.

## Ключевые понятия

- **Коды ответов и substatus** - HTTP-код ответа и дополнительный подкод (например, 1014 для заполненной логической партиции).
- **429 (rate limiting)** - запрос ограничен; возможны четыре причины: Request rate is large, metadata rate limiting, transient service error и TXN_WAIT_FOR_TRANSACTION_END.
- **Server-side latency vs end-to-end latency** - серверная задержка измеряется сервисом; сквозная - видна приложению и включает сеть, повторы и ожидания клиента.
- **Normalized RU Consumption** - процент использования provisioned RU/s; значение - максимум по диапазонам ключей партиций за минуту.
- **Physical partition и logical partition** - физическая партиция хранит до 50 ГБ; логическая (одно значение ключа) ограничена 20 ГБ.
- **Alert rule (правило оповещения)** - состоит из области (scope), условия, групп действий (action group) и сведений; бывает metric, log и activity log.
- **Diagnostic settings (диагностические настройки)** - определяют категории логов и назначение (Log Analytics, Storage, Event Hub).
- **Activity ID** - идентификатор операции, связывающий запрос клиента с записью в логах сервиса.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-azure-cosmos-db-nosql/1-introduction

Деградация в продакшене обычно незаметна: растут задержки и ошибки, а клиенты уже недовольны. Сценарий Contoso: за неделю в логах появляются ответы 429, P99-задержка страницы товара выросла с примерно 20 мс до более чем 100 мс, код не менялся. Модуль разбирает инцидент как дежурный инженер: коды ответов, метрики, алерты, логи.

### 2. Интерпретация кодов ответов и диагностика троттлинга
URL: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-azure-cosmos-db-nosql/2-interpret-response-codes-throttling

Таблица кодов: 400, 401 (неверный заголовок авторизации), 403 (истек токен, заблокирован файрволом, или логическая партиция достигла лимита хранения), 404, 408 и 410 и 429 и 449 и 503 (повторяются SDK и приложением), 409, 412, 413 (элемент больше 2 МБ), 423 (блокировка операции масштабирования), 424 (ошибка в транзакционном батче), 500. Подкод 1014 у 403 означает заполненную логическую партицию. Неуспешные операции тоже тратят RU. SDK .NET по умолчанию повторяет запрос при 429 до 9 раз (всего до 10 попыток) не дольше 30 секунд накопленного ожидания. Эти значения настраиваются: в .NET `MaxRetryAttemptsOnRateLimitedRequests` и `MaxRetryWaitTimeOnRateLimitedRequests`; в Python `retry_throttle_total` и `retry_throttle_backoff_max` (значение 0 не отключает повторы, используйте 1). Причины 429: Request rate is large (поможет больше RU/s, но при перекосе партиций - лишь частично); metadata rate limiting (RU/s не помогает: кэшируйте имена баз и контейнеров, держите один экземпляр клиента); transient service error (503); TXN_WAIT_FOR_TRANSACTION_END (параллельные транзакции на одном ключе партиции; уменьшите объем транзакций или распределите записи). Для диагностики в .NET используйте `response.Diagnostics` и `GetClientElapsedTime()`; в Python - заголовки ответа (`x-ms-request-charge`, `x-ms-activity-id`).

### 3. Мониторинг задержки и загрузки партиций
URL: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-azure-cosmos-db-nosql/3-monitor-latency-partition-utilization

Серверная задержка делится по режиму подключения: Server Side Latency Direct (TCP, только .NET и Java SDK) и Server Side Latency Gateway (HTTPS; для Python, Node.js, Go). Старая общая метрика Server Side Latency устарела. Фильтры: DatabaseName, CollectionName, OperationType, Region, PublicAPIType. Normalized RU Consumption (%) - максимум по диапазонам партиций за минуту; 100 % не всегда проблема. Throttled Request Percentage показывает долю запросов, отклоненных из-за превышения лимита. Для производственной нагрузки 1-5 % запросов с 429 при приемлемой сквозной задержке - нормальны, если партиции распределены равномерно. Под autoscale метрика показывает 100 %, если диапазон использует весь лимит в течение одной секунды, но масштабирование до максимума происходит только при 100 % в течение пяти секунд подряд. Метрика по партициям (Insights > Throughput > Normalized RU Consumption (%) By PartitionKeyRangeID): если все диапазоны высоки - нужна большая пропускная способность; если один диапазон на 100 %, а остальные ниже 30 % - горячая партиция. Метрики Physical Partition Count, Physical Partition Size и Physical Partition Throughput. Физическая партиция хранит до 50 ГБ; логическая партиция ограничена 20 ГБ, и пропускная способность этот лимит не решает. Соглашение о доступности и SLA: серверная задержка менее 10 мс для point read и point write по прямому подключению.

### 4. Настройка алертов Azure Monitor
URL: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-azure-cosmos-db-nosql/4-configure-azure-monitor-alerts

Правило состоит из области (аккаунт), условия (сигнал, логика, порог), групп действий и сведений. Типы: metric (метрики, например троттлинг, задержка, RU, рост хранилища), log (запросы к Log Analytics, например логическая партиция близка к 20 ГБ; требует диагностических настроек), activity log (события управления: ротация ключей, добавление или отключение региона, изменение throughput). Пример алерта на 429: метрика Total Requests с измерением StatusCode = 429; порог - более 100 запросов за 5 минут. Важно: Total Requests считается с агрегацией Count, а Total Request Units - с Total; для правила с порогом 100 используется Total Requests. Порог следует выбирать относительно ожидаемого трафика (пример: при 5000 запросах за 5 минут разумный порог около 500). Динамические пороги подходят для метрик с суточной динамикой. Правило активируется примерно через 10 минут после создания.

### 5. Анализ диагностических логов в Log Analytics
URL: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-azure-cosmos-db-nosql/5-analyze-diagnostic-logs

Метрики собираются автоматически бесплатно, логи - только после создания диагностической настройки, и оплачиваются по объему. Категории для API NoSQL: DataPlaneRequests, QueryRuntimeStatistics (текст запроса по умолчанию обфусцирован), PartitionKeyStatistics (приблизительный объем по ключам), PartitionKeyRUConsumption (RU по ключу в секунду), ControlPlaneRequests (изменения аккаунта), DataPlaneRequests5M и DataPlaneRequests15M (агрегаты). Режим назначения: resource-specific (рекомендуется; таблицы с префиксом CDB, например CDBDataPlaneRequests) или Azure diagnostics (общая таблица AzureDiagnostics, устаревший вариант). Запросы KQL: поиск операций с 429 и средней стоимостью RU, поиск горячего ключа по CDBPartitionKeyRUConsumption, аудит изменений через CDBControlPlaneRequests, связь записи лога с клиентом по ActivityId. Полный текст запросов включается в Settings > Features (Diagnostics full-text query) - это передает параметры запросов (часто персональные данные) в лог-хранилище, поэтому включайте только на время анализа. Чтобы снизить стоимость: включайте нужные категории, используйте агрегаты 5M/15M, отключайте настройку после расследования и удаляйте ее до удаления аккаунта.

### 6. Упражнение: диагностика троттлинга и настройка алерта
URL: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-azure-cosmos-db-nosql/6-exercise-diagnose-alert

Практика: включить диагностические логи, вызвать события троттлинга, исследовать их в Azure Monitor и KQL и создать алерт (C# или Python). Нужна подписка Azure.

### 7. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-azure-cosmos-db-nosql/7-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 8. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-azure-cosmos-db-nosql/8-summary

Коды ответов говорят, что сломалось; метрики - что деградирует; алерты - когда смотреть; диагностические логи называют конкретный запрос. Четыре причины 429 требуют разных исправлений. Порог алерта задается относительно ожидаемого трафика.

## Важные команды / код / настройки

Настройка повторов при 429 (.NET):

```csharp
CosmosClient client = new(
    accountEndpoint: endpoint,
    tokenCredential: new DefaultAzureCredential(),
    clientOptions: new CosmosClientOptions
    {
        MaxRetryAttemptsOnRateLimitedRequests = 5,
        MaxRetryWaitTimeOnRateLimitedRequests = TimeSpan.FromSeconds(10)
    });
```

Настройка повторов при 429 (Python):

```python
client = CosmosClient(
    endpoint,
    credential=DefaultAzureCredential(),
    retry_throttle_total=5,
    retry_throttle_backoff_max=10,
)
```

Диагностика при ошибке (.NET):

```csharp
catch (CosmosException ex)
{
    Console.WriteLine($"Status: {ex.StatusCode} SubStatus: {ex.SubStatusCode}");
    Console.WriteLine($"Activity ID: {ex.ActivityId} Charge: {ex.RequestCharge} RU");
    Console.WriteLine($"Retry after: {ex.RetryAfter}");
}
```

Группа действий и правило алерта на 429 (Azure CLI):

```powershell
$actionGroupId = az monitor action-group create `
    --name "dp420-oncall" `
    --resource-group $resourceGroup `
    --short-name "dp420" `
    --action email oncall you@contoso.com `
    --query id `
    --output tsv

az monitor metrics alert create `
    --name "Rate limited requests" `
    --resource-group $resourceGroup `
    --scopes $accountId `
    --condition "count TotalRequests > 100 where StatusCode includes 429" `
    --window-size 5m `
    --evaluation-frequency 1m `
    --action $actionGroupId `
    --description "More than 100 rate-limited requests in five minutes."
```

Диагностическая настройка с категориями (Azure CLI):

```powershell
az monitor diagnostic-settings create `
    --name "cosmos-diagnostics" `
    --resource $accountId `
    --workspace $workspaceId `
    --export-to-resource-specific true `
    --logs '[{"category":"DataPlaneRequests","enabled":true},{"category":"PartitionKeyRUConsumption","enabled":true}]'
```

KQL: операции с 429 и средняя стоимость RU:

```kusto
CDBDataPlaneRequests
| where TimeGenerated >= ago(24h)
| summarize throttledOperations = dcountif(ActivityId, StatusCode == 429),
            totalOperations = dcount(ActivityId),
            totalConsumedRUPerMinute = sum(RequestCharge)
    by DatabaseName, CollectionName, OperationName, RequestResourceType, bin(TimeGenerated, 1min)
| extend averageRUPerOperation = 1.0 * totalConsumedRUPerMinute / totalOperations
| extend fractionOf429s = 1.0 * throttledOperations / totalOperations
| order by fractionOf429s desc
```

KQL: поиск горячего ключа партиции:

```kusto
CDBPartitionKeyRUConsumption
| where TimeGenerated >= ago(24h)
| where CollectionName == "product"
| where isnotempty(PartitionKey)
| summarize sum(RequestCharge) by PartitionKey, OperationName, bin(TimeGenerated, 1s)
| order by sum_RequestCharge desc
```

KQL: связь с конкретным запросом по ActivityId:

```kusto
CDBDataPlaneRequests
| where ActivityId == "<activity-id-from-your-application>"
```

Пороги из источника: 20 ГБ на логическую партицию; 50 ГБ на физическую; 2 МБ на элемент; 10 мс серверная задержка по SLA (point read/write, direct).

## Что запомнить

- Код ответа и substatus говорят, что произошло; повторять стоит только переходные ошибки (408, 410, 429, 449, 503).
- Для 429 сначала определите причину: нехватка RU/s, metadata rate limiting, transient error или TXN_WAIT_FOR_TRANSACTION_END.
- Горячая партиция видна в метриках по PartitionKeyRangeID; одна партиция на 100 % при остальных низких - перекос, а не нехватка throughput.
- Алерт нужно настраивать с порогом, рассчитанным от ожидаемого трафика, иначе его отключат.
- Диагностические логи платные и включаются вручную; используйте resource-specific таблицы и ActivityId для связи с клиентом.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-azure-cosmos-db-nosql/
- Monitor Azure Cosmos DB; Azure Cosmos DB monitoring data reference; Diagnose and troubleshoot request rate too large exceptions; Design resilient applications with Azure Cosmos DB SDKs; Monitor normalized request units; Monitor server-side latency; Create alerts by using Azure Monitor; Monitor data by using diagnostic settings (названия из источника, URL не приведены)
