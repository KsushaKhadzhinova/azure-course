# Безопасность Azure Cosmos DB (SQL API)

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-security-azure-cosmos-db-sql-api/

## Цель модуля

Настроить сетевой контроль доступа, рассмотреть варианты шифрования данных, использовать RBAC (роли Azure и встроенные роли данных), подключаться с Microsoft Entra ID и понять Always Encrypted.

## Ключевые понятия

- **Shared responsibility (модель общей ответственности)** - клиент отвечает за патчи серверов, TLS и надежные учетные записи; Azure Cosmos DB обеспечивает защиту облачной части.
- **IP firewall (IP-фильтр)** - ограничивает доступ списком IPv4-адресов или CIDR-диапазонов; запросы с других адресов получают 403. Сам фильтр не заменяет токен авторизации.
- **HMAC-авторизация** - авторизация по ключам аккаунта (primary/secondary key) или по токенам ресурсов.
- **Azure RBAC (управляющий доступ)** - роли на уровне управления (аккаунт, базы, контейнеры, throughput); назначаются через IAM. Не используются для операций с данными.
- **Data plane RBAC (встроенные роли данных)** - роли Entra ID для операций с данными: Cosmos DB Built-in Data Reader и Cosmos DB Built-in Data Contributor.
- **Encryption at rest и in transit** - все данные шифруются на диске и при передаче (AES-256) ключами, которыми управляет сервис; можно использовать собственные ключи (customer-managed keys).
- **Always Encrypted** - клиентское шифрование чувствительных свойств; сервис не получает ключи расшифровки. Ключи (CMK) хранятся в Azure Key Vault, ключи данных (DEK) - в базе.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/implement-security-azure-cosmos-db-sql-api/1-introduction

Безопасность данных - общая ответственность клиента и поставщика. Источник перечисляет подход Azure Cosmos DB по требованиям: сетевая безопасность (IP-фильтры), авторизация HMAC, RBAC и Active Directory, глобальная и локальная репликация, восстановление удаленных данных (онлайн-резервные копии примерно за 30 дней), шифрование в покое, HTTPS и TLS 1.2, журналы аудита, геоограничения для суверенных регионов. Модуль учит сетевому контролю, шифрованию, RBAC, Entra ID и Always Encrypted.

### 2. Сетевой контроль доступа
URL: https://learn.microsoft.com/en-us/training/modules/implement-security-azure-cosmos-db-sql-api/2-implement-network-level-access-control

По умолчанию аккаунт доступен со всех IP. После включения фильтра доступ разрешен только для указанных IPv4 или CIDR-диапазонов, остальные получают 403 Forbidden. Для работы из портала нужны опции "Allow access from Azure Portal" и добавление текущего IP. Опция "Accept connections from within Azure datacenters" открывает доступ широкому списку адресов Azure (в том числе от других подписок), поэтому ее стоит использовать только без статических IP или подсетей VNet. Также возможна комбинация с подсетями VNet через service endpoint. Настройка: портал (Firewall and virtual networks), шаблоны ARM, Azure CLI или PowerShell (свойство `ipRangeFilter`). Типичные проблемы: портал не видит данные без опции Allow access from Azure Portal; общий 403 в SDK; запросы из подсети с service endpoint не имеют публичного IP и отклоняются фильтром IP - для них нужен список контроля доступа; частные IP в списке разрешенных недопустимы. Диагностика: журналы диагностики с кодами 403.

### 3. Варианты шифрования данных
URL: https://learn.microsoft.com/en-us/training/modules/implement-security-azure-cosmos-db-sql-api/3-review-data-encryption-options

Основные базы хранятся на SSD, вложения и резервные копии - в Azure Blob Storage. Все данные шифруются в покое и при передаче (сквозное шифрование) без дополнительной платы и без включения настройки. Используется AES-256 с ключами сервиса, которыми управляет Microsoft; также доступны собственные ключи клиента. Шифрование и расшифровка выполняются на лету без влияния на производительность. Ключи хранятся отдельно от зашифрованных данных.

### 4. RBAC
URL: https://learn.microsoft.com/en-us/training/modules/implement-security-azure-cosmos-db-sql-api/4-use-role-based-access-control-rbac

Azure RBAC задает управляющий доступ, но не операции с данными. Встроенные роли: DocumentDB Account Contributor (управление аккаунтами), Cosmos DB Account Reader (чтение), Cosmos Backup Operator (восстановление и настройка резервного копирования, без доступа к данным), CosmosRestoreOperator (восстановление при непрерывном резервном копировании), Cosmos DB Operator (создание аккаунтов, баз и контейнеров, без доступа к данным и Data Explorer). Назначение ролей - через IAM в портале, поддерживаются и пользовательские роли. SDK можно заблокировать от изменения свойств аккаунта, баз, контейнеров и throughput; тогда такие изменения выполняются через ARM-шаблоны, PowerShell, CLI, REST или Management Library.

### 5. Доступ к ресурсам аккаунта через Microsoft Entra ID
URL: https://learn.microsoft.com/en-us/training/modules/implement-security-azure-cosmos-db-sql-api/5-access-account-resources-using-azure-active-directory

Встроенный RBAC для данных: аутентификация запросов Entra ID и авторизация через разрешения на уровне операций. Модель разрешений покрывает операции с данными (create, read, replace, upsert, delete, executeQuery, readChangeFeed, executeStoredProcedure, manageConflicts и readMetadata) и не покрывает управление ресурсами. Определения ролей: встроенные (`Cosmos DB Built-in Data Reader` с ID 00000000-0000-0000-0000-000000000001; `Cosmos DB Built-in Data Contributor` с ID 00000000-0000-0000-0000-000000000002) или пользовательские (scope: `/`, `/dbs/<db>`, `/dbs/<db>/colls/<container>`). Назначение ролей задает роль, принципала, scope. В SDK вместо ключа передается TokenCredential (например, ClientSecretCredential). Data Explorer портала пока не поддерживает RBAC для данных; для этого используется Azure Cosmos DB Explorer с параметром `?feature.enableAadDataPlane=true`. Журналы DataPlaneRequest содержат aadPrincipalId_g и aadAppliedRoleAssignmentId_g. Для RBAC-only можно отключить ключи (`disableLocalAuth` = true). Лимиты: 100 определений ролей и 2000 назначений на аккаунт; роли назначаются только удостоверениям того же арендатора; группы из более 200 не разрешаются; токен передается с каждым запросом, увеличивая размер полезной нагрузки.

Пример инициализации SDK (.NET):

```csharp
TokenCredential servicePrincipal = new ClientSecretCredential(
    "<azure-ad-tenant-id>",
    "<client-application-id>",
    "<client-application-secret>");
CosmosClient client = new CosmosClient("<account-endpoint>", servicePrincipal);
```

### 6. Always Encrypted
URL: https://learn.microsoft.com/en-us/training/modules/implement-security-azure-cosmos-db-sql-api/6-understand-always-encrypted

Данные шифруются на клиенте, поэтому сервис не получает ключи расшифровки. Ключи-обертки (CMK) хранятся в Azure Key Vault. Ключи данных (DEK) создаются SDK и хранятся в базе данных (на уровне базы, их можно делить между контейнерами). Политика шифрования задается на уровне контейнера при создании и не меняется; путь - только верхнего уровня (`/property`); ID и ключ партиции зашифровать нельзя. Типы: deterministic (одинаковое значение дает одинаковый шифротекст; поддерживает равенство в фильтрах, но уязвим к анализу шаблонов) и randomized (безопаснее, фильтрация невозможна). Для массивов шифруются все элементы; для объектов - только листовые значения. Чтение по id и ключу партиции, запросы и change feed расшифровываются автоматически. Фильтрация только по равенству (`WHERE c.property = @Value`). Если клиент не имеет ключа на часть свойств, он может запрашивать только остальные.

Настройка: создать CMK в Key Vault, выдать приложению права (Get, List, Unwrap Key, Wrap Key, Verify, Sign), подключить `AzureKeyVaultKeyStoreProvider` (пакет Microsoft.Data.Encryption.AzureKeyVaultProvider), создать DEK через `CreateClientEncryptionKeyAsync`, создать контейнер с политикой шифрования через `WithClientEncryptionPolicy`. CMK рекомендуется периодически ротировать; новый ключ подключается через `RewrapClientEncryptionKeyAsync`.

## Важные команды / код / настройки

Инициализация SDK с Entra ID (см. выше).

Always Encrypted: инициализация провайдера ключей и клиента:

```csharp
var tokenCredential = new ClientSecretCredential(
    "<aad-app-tenant-id>", "<aad-app-client-id>", "<aad-app-secret>");
var keyStoreProvider = new AzureKeyVaultKeyStoreProvider(tokenCredential);
var client = new CosmosClient("<connection-string>")
    .WithEncryption(keyStoreProvider);
```

Создание DEK:

```csharp
await database.CreateClientEncryptionKeyAsync(
    "my-key",
    DataEncryptionKeyAlgorithm.AEAD_AES_256_CBC_HMAC_SHA256,
    new EncryptionKeyWrapMetadata(
        keyStoreProvider.ProviderName,
        "akvKey",
        "https://<my-key-vault>.vault.azure.net/keys/<key>/<version>"));
```

Ротация CMK:

```csharp
await database.RewrapClientEncryptionKeyAsync(
    "my-key",
    new EncryptionKeyWrapMetadata(
        keyStoreProvider.ProviderName,
        "akvKey",
        " https://<my-key-vault>.vault.azure.net/keys/<new-key>/<version>"));
```

Политика шифрования при создании контейнера:

```csharp
var path1 = new ClientEncryptionIncludedPath
{
    Path = "/property1",
    ClientEncryptionKeyId = "my-key",
    EncryptionType = EncryptionType.Deterministic.ToString(),
    EncryptionAlgorithm = DataEncryptionKeyAlgorithm.AEAD_AES_256_CBC_HMAC_SHA256.ToString()
};
await database.DefineContainer("my-container", "/partition-key")
    .WithClientEncryptionPolicy()
    .WithIncludedPath(path1)
    .Attach()
    .CreateAsync();
```

Фильтр по зашифрованному свойству:

```csharp
var queryDefinition = container.CreateQueryDefinition(
    "SELECT * FROM c where c.property1 = @Property1");
await queryDefinition.AddParameterAsync("@Property1", 1234, "/property1");
```

Роли данных и ID (для назначения через CLI/PowerShell/ARM):

| Роль | ID |
|---|---|
| Cosmos DB Built-in Data Reader | 00000000-0000-0000-0000-000000000001 |
| Cosmos DB Built-in Data Contributor | 00000000-0000-0000-0000-000000000002 |

Лимиты RBAC: 100 определений ролей и 2000 назначений на аккаунт.

## Что запомнить

- Фильтр IP ограничивает сеть, но запрос все равно требует действительного токена авторизации.
- Шифрование в покое и при передаче включено по умолчанию, ключами управляет сервис или клиент.
- Управляющий RBAC (Azure IAM) и data plane RBAC (встроенные роли данных) - разные уровни доступа.
- Для Entra ID в SDK передается TokenCredential вместо ключа; ключи аккаунта можно отключить (`disableLocalAuth`).
- Always Encrypted шифрует свойства на клиенте; deterministic позволяет фильтровать по равенству, randomized - безопаснее, но без фильтрации.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/implement-security-azure-cosmos-db-sql-api/
- Security in Azure Cosmos DB - overview; Configure IP firewall in Azure Cosmos DB; Data encryption in Azure Cosmos DB; Azure role-based access control in Azure Cosmos DB; Configure role-based access control with Microsoft Entra ID for your Azure Cosmos DB account; Use client-side encryption with Always Encrypted for Azure Cosmos DB; Quickstart: Register an application with the Microsoft identity platform (названия из источника, URL не приведены)
