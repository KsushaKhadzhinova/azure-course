# Интегрированный кэш в Azure Cosmos DB

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-integrated-cache/

## Цель модуля

Включить и настроить встроенный (integrated) кэш Azure Cosmos DB для NoSQL, чтобы снизить стоимость повторяющихся операций чтения и запросов без написания собственного клиентского кэша.

## Ключевые понятия

- **Integrated cache** - встроенный in-memory кэш Azure Cosmos DB; не требует собственного кода кэширования.
- **Dedicated gateway (выделенный шлюз)** - ресурс аккаунта, на котором работает кэш; имеет свою конечную точку (endpoint).
- **Gateway mode** - режим подключения SDK, при котором запросы идут через шлюз; по умолчанию используется Direct mode.
- **MaxIntegratedCacheStaleness** - параметр допустимой «устарелости» данных в кэше; по умолчанию 5 минут.
- **Цена операции из кэша** - при попадании в кэш (пока данные не устарели) операция не потребляет RU; RU тратятся на первый вызов.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/implement-integrated-cache/1-introduction

Интенсивные операции чтения накапливают затраты RU; собственный клиентский кэш сложен в поддержке. Модуль учит включать и настраивать integrated cache и отслеживать его работу.

### 2. Какие нагрузки выигрывают от кэша
URL: https://learn.microsoft.com/en-us/training/modules/implement-integrated-cache/2-review-workloads-that-benefit-from-cache

Собственный кэш требует маршрутизации всех запросов через него, масштабирования, инвалидации при обновлении и удалении и усложняет создание элементов. Integrated cache решает эти задачи. Выигрывают нагрузки: с заметно большим числом чтений и запросов, чем записей; с многократным чтением больших элементов; с повторным выполнением дорогих запросов; с горячими ключами партиций при чтении.

### 3. Включение integrated cache
URL: https://learn.microsoft.com/en-us/training/modules/implement-integrated-cache/3-enable-integrated-cache

Два шага: создать выделенный шлюз в аккаунте (портал, раздел Dedicated Gateway; задаются число экземпляров и SKU, которые можно изменить позже) и обновить код SDK. Для .NET SDK нужны три условия: конечная точка шлюза (формат `<account>.sqlx.cosmos.azure.com`), режим Gateway вместо Direct, уровень консистентности Session или Eventual. Рекомендуется аутентификация через managed identity с ролью Cosmos DB Built-in Data Contributor. Для point read и запросов уровень консистентности задается вручную в `ItemRequestOptions` или `QueryRequestOptions`. Затраты RU видны в `RequestCharge`; при запросах суммируются значения по всем страницам.

### 4. Настройка устарелости кэша
URL: https://learn.microsoft.com/en-us/training/modules/implement-integrated-cache/4-configure-cache-staleness

По умолчанию кэш хранит данные 5 минут. Окно устарелости задается через `MaxIntegratedCacheStaleness` в `DedicatedGatewayRequestOptions`: для point read - в `ItemRequestOptions`, для запросов - в `QueryRequestOptions`. В примерах: 15 минут для point read и 120 секунд для запроса.

### 5. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/implement-integrated-cache/5-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 6. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/implement-integrated-cache/6-summary

Создание выделенного шлюза и integrated cache, настройка кэша.

## Важные команды / код / настройки

Клиент с конечной точкой шлюза, режимом Gateway и managed identity:

```csharp
using Azure.Identity;
using Microsoft.Azure.Cosmos;

string endpoint = "https://<cosmos-account-name>.sqlx.cosmos.azure.com/";

CosmosClientOptions options = new()
{
    ConnectionMode = ConnectionMode.Gateway,
    ConsistencyLevel = ConsistencyLevel.Session // or ConsistencyLevel.Eventual
};

// Use DefaultAzureCredential to authenticate with managed identity.
CosmosClient client = new(endpoint, new DefaultAzureCredential(), options);
```

Point read через кэш:

```csharp
ItemRequestOptions requestOptions = new()
{
    ConsistencyLevel = ConsistencyLevel.Session
};
ItemResponse<Product> response = await container.ReadItemAsync<Product>(id, partitionKey, requestOptions: requestOptions);
```

Запрос через кэш и суммирование RU по страницам:

```csharp
QueryRequestOptions queryOptions = new()
{
    ConsistencyLevel = ConsistencyLevel.Eventual
};
FeedIterator<Product> iterator = container.GetItemQueryIterator<Product>(query, requestOptions: queryOptions);
```

Настройка устарелости для point read (15 минут):

```csharp
ItemRequestOptions operationOptions = new()
{
    ConsistencyLevel = ConsistencyLevel.Eventual,
    DedicatedGatewayRequestOptions = new()
    {
        MaxIntegratedCacheStaleness = TimeSpan.FromMinutes(15)
    }
};
```

Настройка устарелости для запроса (120 секунд):

```csharp
QueryRequestOptions queryOptions = new()
{
    ConsistencyLevel = ConsistencyLevel.Eventual,
    DedicatedGatewayRequestOptions = new()
    {
        MaxIntegratedCacheStaleness = TimeSpan.FromSeconds(120)
    }
};
```

Требования к подключению, перечисленные в источнике: endpoint шлюза, `ConnectionMode.Gateway`, уровень консистентности Session или Eventual, роль Cosmos DB Built-in Data Contributor у managed identity.

## Что запомнить

- Integrated cache не требует собственного кода кэша: включается через выделенный шлюз и настройки SDK.
- В кэш попадают point read и запросы; при попадании (пока данные не устарели) RU не списываются.
- Для работы нужны endpoint шлюза, режим Gateway и уровень консистентности Session или Eventual.
- По умолчанию данные в кэше хранятся 5 минут; окно задается через `MaxIntegratedCacheStaleness`.
- Лучше всего кэш подходит для нагрузок с частыми чтениями и повторяющимися запросами.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/implement-integrated-cache/
- Azure Cosmos DB integrated cache - Overview; How to configure the Azure Cosmos DB integrated cache (названия из источника, URL не приведены)
