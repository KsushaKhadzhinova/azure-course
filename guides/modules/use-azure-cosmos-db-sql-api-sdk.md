# Использование SDK Azure Cosmos DB SQL API

**Источник:** https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/

## Цель модуля

Научиться подключать SDK Azure Cosmos DB for NoSQL (.NET, Python, JavaScript) через пакетный менеджер, создавать клиент и работать с базами и контейнерами, использовать один экземпляр клиента, а также настраивать режим подключения, уровень согласованности и предпочтительные регионы.

## Ключевые понятия

- **SDK для Cosmos DB for NoSQL** - библиотеки для .NET (`Microsoft.Azure.Cosmos`, NuGet), Python (`azure-cosmos`, PyPI) и JavaScript (`@azure/cosmos`, npm). Также есть Java и Go, но в модуле они не рассматриваются.
- **CosmosClient** - клиентское представление аккаунта и основной класс SDK.
- **Database / DatabaseProxy** - клиентское представление базы данных (в Python и JavaScript - через CosmosClient).
- **Container / ContainerProxy** - клиентское представление контейнера. Python-классы DatabaseProxy и ContainerProxy не следует создавать напрямую: их получают через CosmosClient.
- **Connection mode (режим подключения)** - Direct (по умолчанию в .NET: запросы идут напрямую к узлам данных) или Gateway (все запросы идут через шлюз; единственный режим в Python и JavaScript).
- **Consistency level на клиенте** - можно только ослабить согласованность для чтения, но не ужесточить и не применить к записи.
- **ApplicationRegion / ApplicationPreferredRegions (.NET), preferred_locations (Python), preferredLocations (JavaScript)** - предпочтительные регионы для клиента.
- **Singleton client (одиночный клиент)** - один экземпляр CosmosClient на все время работы приложения.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/1-introduction

SDK есть для .NET, Java, Python, JavaScript (Node.js) и Go. В модуле рассматриваются .NET, Python и JavaScript. Цели: подключить библиотеки через пакетный менеджер и подключиться к аккаунту из приложения.

### 2. Understand the SDK
https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/2-understand-sdk

Для каждого языка описаны библиотека и ее основные классы: `CosmosClient`, `Database`, `Container` (.NET и JavaScript) и `CosmosClient`, `DatabaseProxy`, `ContainerProxy` (Python). Библиотеки открыты и размещаются на GitHub (azure/azure-cosmos-dotnet-v3, Azure/azure-sdk-for-python, Azure/azure-sdk-for-js).

### 3. Import from package manager
https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/3-import-from-package-manager

Установка через dotnet CLI (NuGet), pip (PyPI) и npm. Без указания версии ставится последняя стабильная версия; для preview версии нужно указать версию явно. Версия записывается в csproj, requirements.txt или package.json.

### 4. Connect to an online account
https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/4-connect-to-online-account

Создание CosmosClient тремя способами: строка подключения, endpoint с ключом и endpoint с токен-учетными данными (Microsoft Entra ID, рекомендуется). Клиент подключается к аккаунту только при первой операции. Можно прочитать свойства аккаунта (ReadAccountAsync, get_database_account, getDatabaseAccount). Получение базы и контейнера: существующий, создание, создание если не существует (с автомасштабированием до 1000 RU/s в примерах).

### 5. Implement client singleton
https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/5-implement-client-singleton

CosmosClient потокобезопасен, управляет соединениями и кэширует адреса в режиме Direct. Для .NET рекомендуется один экземпляр на AppDomain на все время жизни приложения. В Python и JavaScript создавайте клиент один раз и переиспользуйте (в Azure Functions - через статическую переменную).

### 6. Configure connectivity mode
https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/6-configure-connectivity-mode

Настройки передаются в CosmosClientOptions (.NET), как последний параметр конструктора, или в конструктор (Python, JavaScript). Описаны режимы Direct и Gateway, уровни согласованности (Bounded Staleness, Consistent Prefix, Eventual, Session, Strong) и предпочтительные регионы. Также упомянуты retry policies, таймауты и user agent.

### 7. Exercise - Connect to Azure Cosmos DB for NoSQL with the SDK
https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/7-exercise-connect-to

Практическое задание (около 15 минут): подготовка среды, подключение SDK к аккаунту. Нужна подписка Azure с правами администратора.

### 8. Knowledge check
https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/8-knowledge-check

Проверка знаний (около 5 минут). Текст в источнике не приведен.

### 9. Summary
https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/9-summary

Вы научились подключать SDK через пакетный менеджер, подключаться к существующему аккаунту и читать свойства аккаунта. Для дальнейшего изучения указаны ссылки на документацию, пакеты NuGet, PyPI, npm и репозитории GitHub.

## Важные команды / код / настройки

**Установка пакетов:**
```
dotnet add package Microsoft.Azure.Cosmos
```
```
dotnet add package Microsoft.Azure.Cosmos \
    --version 3.41.1
```
```
pip install azure-cosmos
```
```
pip install azure-cosmos==4.8.0
```
```
npm install @azure/cosmos
```
```
npm install @azure/cosmos@4.1.1
```

**Записи в файлах проекта из источника:** `<PackageReference Include="Microsoft.Azure.Cosmos" Version="3.41.1" />` в csproj (target net8.0); `azure-cosmos==4.8.0` в requirements.txt; `"@azure/cosmos": "^4.1.1"` в package.json.

**.NET - создание клиента с Microsoft Entra ID (managed identity):**
```
using Azure.Identity;
using Microsoft.Azure.Cosmos;
string accountEndpoint = "https://<youraccountname>.documents.azure.com:443/";
DefaultAzureCredential credential = new DefaultAzureCredential();
CosmosClient client = new CosmosClient(accountEndpoint, credential);
```

**.NET - работа с базой и контейнером:**
```
Database database = client.GetDatabase("cosmicworks");
Database database = await client.CreateDatabaseIfNotExistsAsync("cosmicworks");
Container container = database.GetContainer("products");
Container container = await database.CreateContainerIfNotExistsAsync(
    new ContainerProperties(chatContainerName, "/categoryId"),
    ThroughputProperties.CreateAutoscaleThroughput(1000)
);
```

**Python - импорт и создание клиента:**
```
from azure.cosmos import CosmosClient, PartitionKey, ThroughputProperties, ContainerProxy, exceptions
```
```
connection_string = "AccountEndpoint=https://dp420.documents.azure.com:443/;AccountKey=<key>"
client = CosmosClient.from_connection_string(connection_string)
```
```
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
endpoint = "https://dp420.documents.azure.com:443/"
client = CosmosClient(url=endpoint, credential=credential)
```

**Python - база и контейнер:**
```
database = client.get_database_client("cosmicworks")
database = client.create_database_if_not_exists("cosmicworks")
container = database.get_container_client("products")
container = database.create_container(
    id="products",
    partition_key=PartitionKey(path="/categoryId"),
    throughput=ThroughputProperties(auto_scale_max_throughput=1000)
)
```

**JavaScript - импорт и клиент:**
```
const { CosmosClient, Database, Container } = require("@azure/cosmos");
const { DefaultAzureCredential } = require("@azure/identity");
const credential = new DefaultAzureCredential();
const client = new CosmosClient({ endpoint, aadCredentials: credential });
```

**JavaScript - база и контейнер:**
```
const database = client.database("cosmicworks");
const { resource: container } = await database.containers.createIfNotExists({
    id: "products",
    partitionKey: {
        paths: ["/categoryId"]
    },
    maxThroughput: 1000
});
```

**Режим подключения (.NET):**
```
CosmosClientOptions options = new ()
{
    ConnectionMode = ConnectionMode.Gateway
};
```
Значение по умолчанию - `ConnectionMode.Direct`.

**Согласованность и регионы (.NET):**
```
CosmosClientOptions options = new ()
{
    ConsistencyLevel = ConsistencyLevel.Eventual
};
```
```
CosmosClientOptions options = new ()
{
    ApplicationRegion = "westus"
};
```
```
CosmosClientOptions options = new CosmosClientOptions()
{
    ApplicationPreferredRegions = new List<string> { "westus", "eastus" }
};
```

**Python - согласованность, регион и таймаут:**
```
client = CosmosClient(
    url="https://dp420.documents.azure.com:443/",
    credential="<key>",
    consistency_level=ConsistencyLevel.Eventual
)
```
```
client = CosmosClient(
    url="https://dp420.documents.azure.com:443/",
    credential="<key>",
    preferred_locations=["West US", "East US"]
)
```
```
client = CosmosClient(
    url="https://dp420.documents.azure.com:443/",
    credential="<key>",
    connection_timeout=10
)
```

**JavaScript - согласованность, регион и таймаут:**
```
const client = new CosmosClient({
  endpoint: "https://dp420.documents.azure.com:443/",
  key: "<key>",
  consistencyLevel: ConsistencyLevel.Eventual
});
```
```
const client = new CosmosClient({
  endpoint: "https://dp420.documents.azure.com:443/",
  key: "<key>",
  connectionPolicy: {
    preferredLocations: ["West US", "East US"]
  }
});
```
```
const client = new CosmosClient({
  endpoint: "https://dp420.documents.azure.com:443/",
  key: "<key>",
  connectionPolicy: {
    requestTimeout: 10000
  }
});
```

В источнике для примеров используется вымышленный endpoint и образец ключа; здесь ключ заменен на `<key>`.

## Что запомнить

- Устанавливайте SDK через пакетный менеджер языка (`dotnet add package`, `pip install`, `npm install`); для preview указывайте версию явно.
- Предпочтительно подключаться через Microsoft Entra ID (токен-учетные данные), а не через строку подключения с ключом.
- Клиент подключается лениво: первая операция устанавливает соединение, а создание объекта еще ничего не проверяет.
- Создавайте один CosmosClient на приложение и переиспользуйте его; при каждом запросе новый клиент теряет кэш адресов и соединения.
- Согласованность на клиенте можно только ослабить для чтения; режим Direct по умолчанию в .NET, в Python и JavaScript доступен только Gateway.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/use-azure-cosmos-db-sql-api-sdk/
- В источнике упоминаются (без ссылок в тексте): Azure Cosmos DB .NET SDK v3 for NoSQL; Microsoft.Azure.Cosmos Namespace; Microsoft.Azure.Cosmos | NuGet; Azure/azure-cosmos-dotnet-v3 (GitHub); Azure Cosmos DB Python SDK for API for NoSQL; Azure/azure-sdk-for-python (GitHub); azure-cosmos (PyPI); Azure Cosmos DB Node.js SDK for API for NoSQL; Azure/azure-sdk-for-js (GitHub); @Azure/cosmos (npm).
