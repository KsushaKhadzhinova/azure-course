# Мониторинг ответов и событий Azure Cosmos DB (SQL API)

**Источник:** https://learn.microsoft.com/en-us/training/modules/monitor-responses-events-azure-cosmos-db-sql-api/

## Цель модуля

Научиться отслеживать состояние запросов к Azure Cosmos DB for NoSQL по HTTP-кодам ответов: распознавать частые коды, диагностировать транзитные ошибки (503 и сетевые таймауты) и ограничение скорости (429), настраивать алерты Azure Monitor и аудировать безопасность аккаунта.

## Ключевые понятия

- **HTTP status code** — код результата операции; показывает успех или причину сбоя.
- **Транзитная ошибка (transient error)** — временная ошибка сети или сервиса, обычно решаемая повтором (503, TransportException).
- **429 (Request rate too large)** — запросы превысили provisioned RU/s; ответ содержит заголовок `x-ms-retry-after-ms`.
- **Request Units (RU/s)** — единица стоимости операций; лимит задается provisioned throughput.
- **Hot partition** — логическая партиция, которая потребляет непропорционально много RU и вызывает 429.
- **Metadata requests** — операции со списками, созданием и изменением баз и контейнеров; у них есть отдельный системный лимит.
- **Azure Monitor alerts** — правила оповещения по метрикам и журналам активности.
- **Activity logs и Azure Resource logs** — журналы операций управления и диагностики.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/monitor-responses-events-azure-cosmos-db-sql-api/1-introduction

Введение: HTTP-коды, которые возвращают REST-операции, показывают состояние запроса. Модуль охватывает частые коды, транзитные ошибки, ограничение скорости, алерты и аудит безопасности.

### 2. Review common response codes
https://learn.microsoft.com/en-us/training/modules/monitor-responses-events-azure-cosmos-db-sql-api/2-review-common-response-codes

Коды по операциям: создание документа (201, 400, 403, 409, 413), ReadFeed (400 при неверном override уровня согласованности), получение (304, 400, 404), замена (400, 404, 409, 413), патч (400, 412), удаление (204, 404), запрос (400 для неверного синтаксиса). Общие коды: 200 — успех; 408 — таймаут, включая превышение времени выполнения хранимой процедуры, триггера или UDF; 429 — превышение provisioned throughput; 500 — внутренняя ошибка, обратиться в поддержку; 503 — сервис недоступен, повтор безопасен.

### 3. Understand transient errors
https://learn.microsoft.com/en-us/training/modules/monitor-responses-events-azure-cosmos-db-sql-api/3-understand-transient-errors

Код 503 может быть вызван сетевыми проблемами или недоступностью сервиса; обычно достаточно повторить операцию, а при сохранении проблемы обратиться в поддержку Azure. Рассмотрены три причины: заблокированные порты (Gateway по HTTPS на 443; Direct по TCP на диапазонах 10000–20000 для публичных endpoints или 0–65535 для private endpoints), клиентские сетевые таймауты (TransportException с ReceiveTimeout, их разбирают как 408) и сбой сервиса (проверить страницу состояния Azure).

### 4. Review rate-limiting errors
https://learn.microsoft.com/en-us/training/modules/monitor-responses-events-azure-cosmos-db-sql-api/4-review-rate-limiting-errors

Три причины 429. (1) Высокая частота запросов: доля 429 до 1–5% считается нормальной; выше 5% — признак горячей партиции или нехватки RU/s; анализируйте отчеты Insights (Total Requests by Status Code, Normalized RU Consumption by PartitionKeyRangeID) и логи диагностики. Решения: сменить партиционный ключ (миграцией в новый контейнер), увеличить RU/s, оптимизировать дорогие запросы. (2) Метаданные: увеличение RU/s не помогает; рекомендуются backoff, один экземпляр CosmosClient и кэширование имен баз и контейнеров. (3) Временная ошибка сервиса: повтор запроса; при сохранении — обращение в поддержку.

### 5. Configure Alerts
https://learn.microsoft.com/en-us/training/modules/monitor-responses-events-azure-cosmos-db-sql-api/5-configure-alerts

Алерты Azure Monitor могут отправлять email или запускать Azure Functions и отслеживают доступность, отклик и журнал активности. Пример: оповещение при более чем 1000 ответах 429 за 15 минут, проверка каждые 5 минут, уведомление на admins@contoso.com. Сигнал — Total Request Units, фильтр по StatusCode = 429. Алерт активируется до 10 минут после создания. Типичные сценарии: смена ключей аккаунта, рост данных или индекса, нормализованное потребление RU/s, добавление или отключение региона, создание, удаление и изменение баз и контейнеров, изменение пропускной способности.

### 6. Audit security
https://learn.microsoft.com/en-us/training/modules/monitor-responses-events-azure-cosmos-db-sql-api/6-audit-security

Activity logs автоматически фиксируют все операции записи (PUT, POST, DELETE) с указанием инициатора, времени и статуса. Azure Resource logs включаются через Diagnostics settings; с помощью Microsoft Defender for Cloud и Azure Policy можно включить сбор журналов. Рекомендуется включить аудит control plane и настроить алерт на изменение правил брандмауэра аккаунта.

### 7. Exercise: Troubleshoot an application using the Azure Cosmos DB for NoSQL SDK
https://learn.microsoft.com/en-us/training/modules/monitor-responses-events-azure-cosmos-db-sql-api/7-exercise-troubleshoot-application-using-sdk

Практика (около 20 минут): диагностика приложения с помощью SDK. Нужна подписка Azure с правами администратора.

### 8. Knowledge check
https://learn.microsoft.com/en-us/training/modules/monitor-responses-events-azure-cosmos-db-sql-api/8-knowledge-check

Проверочный тест (около 5 минут). Вопросы и ответы в источнике не приведены.

### 9. Summary
https://learn.microsoft.com/en-us/training/modules/monitor-responses-events-azure-cosmos-db-sql-api/9-summary

Итоги: коды ответов, транзитные ошибки, ограничение скорости, алерты и аудит безопасности. Список ссылок на документацию по кодам HTTP, диагностике 503, 408 и 429, алертам и аудиту.

## Важные команды / код / настройки

**Запрос Log Analytics для 429 по операциям (из урока 4):**

```
AzureDiagnostics
| where TimeGenerated >= ago(24h)
| where Category == "DataPlaneRequests"
| summarize throttledOperations = dcountif(activityId_g, statusCode_s == 429), totalOperations = dcount(activityId_g), totalConsumedRUPerMinute = sum(todouble(requestCharge_s)) by databaseName_s, collectionName_s, OperationName, requestResourceType_s, bin(TimeGenerated, 1min)
| extend averageRUPerOperation = 1.0 * totalConsumedRUPerMinute / totalOperations 
| extend fractionOf429s = 1.0 * throttledOperations / totalOperations
| order by fractionOf429s desc
```

**Порты (таблица из урока 3):**

| Режим подключения | Протокол | SDK | Порт |
|---|---|---|---|
| Gateway | HTTPS | Все SDK | NoSQL (443) |
| Direct | TCP | .NET и Java SDK | Публичные/служебные endpoints: 10000–20000; private endpoints: 0–65535 |

**Настройка алерта (из урока 5):**

- Сигнал: Total Request Units, фильтр Split by dimension → StatusCode = 429.
- Порог (Alert Logic Threshold): 1000.
- Aggregation granularity (Period): 15 минут; Frequency of Evaluation: 5 минут.
- Action group: email на admins@contoso.com.

**Заголовок повтора:** `x-ms-retry-after-ms` — рекомендуемое время ожидания перед повтором при 429.

**Повторы SDK:** по умолчанию SDK повторяет 429 десять раз (в тексте урока), после чего ошибка возвращается приложению. Для повтора используйте backoff или заголовок `x-ms-retry-after-ms`.

## Что запомнить

- 429 означает превышение RU/s; доля до 1–5% обычно нормальна, выше 5% — проверьте горячие партиции.
- При 429 от метаданных увеличение RU/s не помогает: используйте один CosmosClient и кэширование.
- 503 безопасно повторять; если ошибка сохраняется, проверьте состояние сервиса и обратитесь в поддержку.
- Для Direct-режима нужны открытые TCP-порты; Gateway работает по HTTPS на порту 443.
- Алерты Azure Monitor на StatusCode = 429 позволяют заметить ограничение скорости до жалоб пользователей; Activity logs фиксируют операции записи для аудита.

## Связанные материалы

- Diagnose and troubleshoot issues when using Azure Cosmos DB .NET SDK.
- Documents (REST API): Create, List (ReadFeed), Get, Replace, Patch, Delete, Query Documents.
- HTTP Status Codes for Azure Cosmos DB.
- Diagnose and troubleshoot Azure Cosmos DB service unavailable exceptions.
- Azure Cosmos DB for NoSQL SDK connectivity modes.
- Diagnose and troubleshoot Azure Cosmos DB .NET SDK request timeout exceptions.
- Diagnose and troubleshoot Azure Cosmos DB request rate too large (429) exceptions.
- Create alerts for Azure Cosmos DB using Azure Monitor.
- Security in Azure Cosmos DB - overview.
- Azure security baseline for Azure Cosmos DB.
- How to audit Azure Cosmos DB control plane operations.
