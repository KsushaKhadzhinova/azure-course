# Подключение к Azure Cosmos DB for NoSQL с помощью SDK

**Источник:** https://learn.microsoft.com/en-us/training/modules/connect-azure-cosmos-db-nosql-sdk/

## Цель модуля

Научиться устанавливать и настраивать SDK Azure Cosmos DB for NoSQL для .NET и Python: создавать `CosmosClient` как синглтон, выбирать способ аутентификации и режим подключения, настраивать таймауты, повторные попытки и регионы, работать с эмулятором для офлайн-разработки и диагностировать ошибки подключения. Сквозной пример модуля — веб-API компании Contoso.

## Ключевые понятия

- **CosmosClient** — клиент уровня аккаунта; точка входа в SDK. Владеет пулом соединений и кэшем маршрутов, поэтому его создают один раз и переиспользуют.
- **Database / DatabaseProxy** и **Container / ContainerProxy** — легковесные дескрипторы базы и контейнера, получаемые от родительского объекта без сетевых вызовов.
- **Account key** — долгоживущий секрет; подходит для локальных инструментов и эмулятора.
- **Microsoft Entra ID** — рекомендуемая аутентификация для workload в Azure; `DefaultAzureCredential` подходит для разработки, а для production лучше конкретный credential, например `ManagedIdentityCredential`.
- **Direct mode** — запросы идут по TCP напрямую к репликам; поддерживается только в .NET и Java SDK.
- **Gateway mode** — все запросы идут через HTTPS-шлюз на порту 443; единственный режим для Python SDK.
- **Cosmos DB emulator** — локальная реализация протокола NoSQL API для разработки без облачного аккаунта.
- **429 (Too Many Requests)** — превышение лимита запросов; SDK повторяет такие запросы автоматически.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/connect-azure-cosmos-db-nosql-sdk/1-introduction

Введение: почему важна правильная настройка клиента (лишняя задержка, исчерпание пула соединений, непонятные ошибки под нагрузкой). Модуль охватывает установку SDK, аутентификацию, синглтон, режим подключения, эмулятор и диагностику. Примеры даны на C# и Python.

### 2. Understand and import the SDK
https://learn.microsoft.com/en-us/training/modules/connect-azure-cosmos-db-nosql-sdk/2-understand-import-sdk

Иерархия классов повторяет иерархию ресурсов: аккаунт содержит базы, база содержит контейнеры. Пакеты: NuGet `Microsoft.Azure.Cosmos` (.NET) и PyPI `azure-cosmos` (Python). Выбор аутентификации между ключами и Entra ID. Пакет `azure-identity` нужен для `DefaultAzureCredential`.

### 3. Connect using a client singleton
https://learn.microsoft.com/en-us/training/modules/connect-azure-cosmos-db-nosql-sdk/3-connect-client-singleton

Один `CosmosClient` на аккаунт в каждом домене приложения, переиспользуемый весь срок жизни процесса. Примеры регистрации синглтона: в DI для ASP.NET Core и Azure Functions, на уровне модуля в Python и через lifespan в FastAPI. Получение `Database` и `Container` не делает сетевых запросов. Клиент нужно закрывать (Dispose или close) при остановке приложения.

### 4. Configure connectivity mode and settings
https://learn.microsoft.com/en-us/training/modules/connect-azure-cosmos-db-nosql-sdk/4-configure-connectivity-mode

Сравнение direct и gateway режимов и выбор по сетевому окружению. Настройки `CosmosClientOptions`: `RequestTimeout`, `MaxRetryAttemptsOnRateLimitedRequests`, `MaxRetryWaitTimeOnRateLimitedRequests`. Для Python — `read_timeout`, `retry_total`, `retry_backoff_max`. Предпочитаемые регионы: `ApplicationPreferredRegions` (.NET) и `preferred_locations` (Python). Режим фиксируется при запуске процесса.

### 5. Enable offline development with the emulator
https://learn.microsoft.com/en-us/training/modules/connect-azure-cosmos-db-nosql-sdk/5-enable-offline-development-emulator

Эмулятор работает локально и не тарифицирует RU. Доступны Windows-установщик, Windows-контейнер и Linux-контейнер; рекомендуемый вариант — Linux vNext emulator (Docker, только gateway-режим, без учета RU и без direct mode). Подключение к `https://localhost:8081/` с известным локальным ключом. Сертификат эмулятора нужно импортировать и доверять ему, а не отключать проверку TLS. Рекомендуется явно переключать цель (эмулятор или Azure) через переменные окружения.

### 6. Handle connection errors, logging, and parallelism
https://learn.microsoft.com/en-us/training/modules/connect-azure-cosmos-db-nosql-sdk/6-handle-errors-logging-parallelism

Автоматические повторы SDK по кодам 408, 410, 429, 449 и 503 (с ограничениями для чтений, записей и запросов). Ошибки 400, 401, 403, 404 и 500 требуют действий приложения. Для записей с неизвестным результатом решение о повторе принимает приложение. Логирование: в .NET — кастомный `RequestHandler`, в Python — модуль `logging` (уровень INFO для `azure.cosmos`). Параллелизм: `MaxConcurrency` и `MaxBufferedItemCount` для cross-partition запросов, асинхронный клиент `azure.cosmos.aio` в Python.

### 7. Exercise - Connect an app to Azure Cosmos DB
https://learn.microsoft.com/en-us/training/modules/connect-azure-cosmos-db-nosql-sdk/7-exercise-connect-app

Практика (около 30 минут): создать приложение на C# или Python, подключить его к локальному эмулятору, посмотреть трафик SDK и затем подключить то же приложение к аккаунту Azure. Нужна подписка Azure.

### 8. Module assessment
https://learn.microsoft.com/en-us/training/modules/connect-azure-cosmos-db-nosql-sdk/8-knowledge-check

Проверочный тест (около 5 минут). Вопросы и ответы в источнике не приведены.

### 9. Summary
https://learn.microsoft.com/en-us/training/modules/connect-azure-cosmos-db-nosql-sdk/9-summary

Итоги: установка SDK, синглтон `CosmosClient`, выбор аутентификации и режима подключения, работа с эмулятором, диагностика ошибок и логирование. Список дополнительных ресурсов: документация .NET SDK v3, Python SDK, лучшие практики для .NET SDK, диагностика, документация по эмулятору и RBAC с Microsoft Entra ID.

## Важные команды / код / настройки

**Установка:**

```
dotnet add package Microsoft.Azure.Cosmos
dotnet add package Microsoft.Azure.Cosmos --version 3.62.1
pip install azure-cosmos
pip install azure-cosmos==4.16.3
```

Для .NET нужен явный пакет `Newtonsoft.Json` версии 13.0.4 или выше (для SDK 3.54.0 и новее). Для Entra ID: `dotnet add package Azure.Identity` и `pip install azure-identity`.

**Синглтон клиента (.NET, DI):**

```
builder.Services.AddSingleton<CosmosClient>(_ =>
    new CosmosClient(
        accountEndpoint: builder.Configuration["CosmosDb:Endpoint"],
        tokenCredential: new DefaultAzureCredential()
    ));
```

**Синглтон клиента (Python, FastAPI lifespan):**

```
cosmos_client: CosmosClient | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global cosmos_client
    cosmos_client = CosmosClient(
        url="https://<account>.documents.azure.com:443/",
        credential=DefaultAzureCredential()
    )
    yield
    cosmos_client.close()

app = FastAPI(lifespan=lifespan)
```

**Получение дескрипторов (без сетевых вызовов):**

```
database = client.get_database_client("cosmicworks")
container = database.get_container_client("product")
```

**Режим подключения:**

- .NET: `CosmosClientOptions { ConnectionMode = ConnectionMode.Direct }` или `ConnectionMode.Gateway`.
- Python: `connection_mode='Gateway'` (значение по умолчанию); direct не поддерживается.

**Таймауты и повторы (.NET, значения по умолчанию в скобках):**

- `RequestTimeout` (6 секунд) — время ожидания ответа на один запрос, а не на всю операцию.
- `MaxRetryAttemptsOnRateLimitedRequests` (9) — число повторов до ошибки 429.
- `MaxRetryWaitTimeOnRateLimitedRequests` (30 секунд) — суммарное время ожидания повторов при 429.

Пример из источника: `RequestTimeout = TimeSpan.FromSeconds(3)`, `MaxRetryAttemptsOnRateLimitedRequests = 5`, `MaxRetryWaitTimeOnRateLimitedRequests = TimeSpan.FromSeconds(15)`.

**Python-параметры клиента:** `read_timeout=30`, `retry_total=5`, `retry_backoff_max=15`, `preferred_locations=["West US", "East US"]`. Параметр `connection_timeout` отвечает за установку соединения. `retry_write` включается явно и только если приложение допускает дубликаты.

**Регионы (.NET):** `ApplicationPreferredRegions = new List<string> { "West US", "East US" }`. Нельзя одновременно задавать `ApplicationRegion`.

**Эмулятор (Linux vNext, HTTPS):**

```
docker run \
  --detach \
  --name cosmos-emulator \
  --publish 8081:8081 \
  --publish 8080:8080 \
  --publish 1234:1234 \
  mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-latest \
  --protocol https
```

Endpoint: `https://localhost:8081/`. Ключ эмулятора — публичный well-known ключ из документации:
`C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==`

Не используйте `DangerousAcceptAnyServerCertificateValidator` или `connection_verify=False`: они отключают проверку сертификата и для Azure.

**Переключение цели (Python, из источника):** переменная `COSMOS_TARGET` со значениями `Emulator` или `Azure`; `COSMOS_ENDPOINT` задает адрес. Для Azure используется `DefaultAzureCredential()`, для эмулятора — ключ эмулятора и режим Gateway.

**Логирование (Python):**

```
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s"
)
```

Для подробной диагностики: `logging_enable=True` при создании клиента и `logging.getLogger("azure.cosmos").setLevel(logging.DEBUG)`. В production рекомендуется WARNING или INFO.

**Параллельные cross-partition запросы (.NET):** `MaxConcurrency = 5`, `MaxBufferedItemCount = 1000`. Значение меньше 0 (например, -1) отдает решение SDK. Значение больше числа посещаемых партиций не повышает пропускную способность.

## Что запомнить

- Создавайте один `CosmosClient` на аккаунт и переиспользуйте его; не создавайте клиент на каждый запрос.
- Для production в Azure используйте Microsoft Entra ID, а для эмулятора — его локальный ключ и режим Gateway; переключение цели должно быть явным.
- Режим direct (только .NET и Java) быстрее, но требует открытого исходящего TCP; в ограниченных сетях нужен gateway (порт 443).
- SDK сам повторяет 429 и другие переходные ошибки, но записи с неизвестным результатом и ошибки 400, 401, 403, 404 приложение должно обработать само.
- Эмулятор vNext не учитывает RU, не поддерживает direct mode и серверный JavaScript; финальные проверки проводите на аккаунте Azure.

## Связанные материалы

- Azure Cosmos DB for NoSQL .NET SDK (v3).
- Azure Cosmos DB for NoSQL Python SDK.
- Best practices for Azure Cosmos DB .NET SDK.
- Diagnose and troubleshoot issues using the .NET SDK.
- What is the Azure Cosmos DB emulator?
- Connect to Azure Cosmos DB for NoSQL using role-based access control and Microsoft Entra ID.
