# Модели согласованности в Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/<юнит>`)

## Цель модуля

Научиться оценивать уровни согласованности Azure Cosmos DB, настраивать уровень по умолчанию для аккаунта и переопределять его для отдельных запросов.

## Ключевые понятия

- **Consistency levels (уровни согласованности)** — шкала от строгой до слабой согласованности; их пять: Strong, Bounded Staleness, Session, Consistent Prefix, Eventual.
- **Strong (строгая)** — чтение всегда возвращает последнюю версию; запись подтверждается после фиксации во всех регионах; наибольшая задержка.
- **Bounded Staleness (ограниченное отставание)** — чтения отстают от записей не более чем на заданное число версий K или интервал времени T.
- **Session (сессионная)** — пользователь видит свои записи в рамках одной сессии (SDK-экземпляра или передачи session token); уровень по умолчанию для нового аккаунта.
- **Consistent Prefix (согласованный префикс)** — чтения могут отставать, но не появляются не по порядку.
- **Eventual (eventual)** — самая слабая согласованность; минимальная задержка записи и максимальная доступность, но возможно чтение не по порядку.
- **Session token (токен сессии)** — значение заголовка Session, которое передает сессию между запросами и клиентами.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/1-introduction
Azure Cosmos DB предлагает шкалу уровней согласованности, более тонкую, чем бинарный выбор «строгая/слабая». Цели: настроить уровень по умолчанию для аккаунта и менять уровень для отдельного запроса.

### 2. Understand consistency models
Источник: https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/2-understand
Описаны пять уровней и компромиссы между согласованностью, задержкой записи и доступностью при репликации между регионами. Strong: самая высокая задержка. Bounded Staleness: компромисс между задержкой записи и ограничением отставания; внутри региона записи обеспечивают строгие гарантии. Session: подходит, когда пользователи должны сразу видеть свои операции. Consistent Prefix: важен порядок чтения, а не задержка. Eventual: подходит приложениям без требований к порядку и согласованности.

### 3. Configure default consistency model in the portal
Источник: https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/3-configure-default-consistency-model-portal
Каждый новый аккаунт имеет уровень по умолчанию Session. Уровень для всего аккаунта меняется в портале на панели Default consistency; он применяется ко всем чтениям и запросам контейнеров аккаунта.

### 4. Change consistency model with the SDK
Источник: https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/4-change-consistency-model-sdk
Через `ItemRequestOptions` можно ослабить уровень для одного запроса (уровень можно только ослабить, но не усилить). Аналогично можно задать уровень для всего экземпляра `CosmosClient` через `CosmosClientOptions`.

### 5. Use session tokens
Источник: https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/5-use-session-tokens
При session-согласованности используется session token, который передается между Azure Cosmos DB и клиентом. Обычно SDK управляет токенами сам; токен можно извлечь из заголовка ответа и передать в следующий запрос или другому клиенту.

### 6. Exercise: Configure consistency models in the portal and the Azure Cosmos DB for NoSQL SDK
Источник: https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/6-exercise-configure-consistency-models-portal-sdk
Практика (около 15 минут): настройка уровней согласованности в портале и в SDK. Нужна подписка Azure с правами администратора.

### 7. Knowledge check
Источник: https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/7-knowledge-check
Проверка знаний (в исходнике текст отсутствует).

### 8. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/8-summary
Выбор правильного уровня согласованности определяет поведение Azure Cosmos DB для нагрузки; уровень по умолчанию можно переопределять на уровне запроса.

## Важные команды / код / настройки

Ослабление уровня для одного запроса чтения:

```csharp
ItemRequestOptions options = new()
{ 
    ConsistencyLevel = ConsistencyLevel.Eventual 
};

string id = "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009";

string categoryId = "9603ca6c-9e28-4a02-9194-51cdb7fea816";
PartitionKey partitionKey = new (categoryId);

Product item = await container.ReadItemAsync<Product>(id, partitionKey, requestOptions: options);
```

Ослабление уровня для всего клиента:

```csharp
CosmosClientOptions options = new()
{
    ConsistencyLevel = ConsistencyLevel.Eventual 
};

CosmosClient client = new (endpoint, key, options);
```

Получение и передача session token:

```csharp
ItemResponse<Product> response = await container.CreateItemAsync<Product>(item);
string token = response.Headers.Session;

ItemRequestOptions options = new()
{
    SessionToken = token
};
ItemResponse<Product> readResponse = container.ReadItemAsync<Product>(id, partitionKey, requestOptions: options);)
```

Настройки: уровень по умолчанию для нового аккаунта — Session; меняется на панели Default consistency в портале.

## Что запомнить

- Пять уровней согласованности: Strong, Bounded Staleness, Session, Consistent Prefix, Eventual.
- Уровень по умолчанию для нового аккаунта — Session.
- На уровне запроса (`ItemRequestOptions`) уровень можно только ослабить, не усилить.
- Для клиента уровень задается через `CosmosClientOptions`.
- При Session-согласованности токен сессии (заголовок Session) обычно управляется SDK автоматически.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/
- Документация: Consistency levels in Azure Cosmos DB (упоминается в уроке 8).
- Связанные модули: Try Azure Cosmos DB for NoSQL (`try-azure-cosmos-db-sql-api`), Customize indexes (`customize-indexes-azure-cosmos-db-sql-api`).
