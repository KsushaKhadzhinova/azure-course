# Безопасность Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/

## Цель модуля

Научиться защищать приложение и аккаунт Azure Cosmos DB for NoSQL: выбирать аутентификацию (Microsoft Entra и managed identity, ключи с ротацией), разделять control-plane и data-plane права и назначать роли RBAC, настраивать сетевые ограничения (IP firewall, service endpoints, private endpoints) и маскировать чувствительные поля (dynamic data masking).

## Ключевые понятия

- **Microsoft Entra authentication** - аутентификация через Microsoft Entra ID с токенами; рекомендуется по умолчанию для Azure-хостов.
- **Managed identity (управляемая идентичность)** - идентичность, которой управляет Azure; system-assigned привязана к одному ресурсу, user-assigned живет независимо.
- **DefaultAzureCredential / ManagedIdentityCredential** - цепочка источников учетных данных (для локальной разработки) и явная учетная запись managed identity (для развернутого кода).
- **Principal object ID vs client ID** - object ID используется в назначениях ролей, client ID - в коде для выбора user-assigned identity.
- **Account keys (ключи аккаунта)** - primary и secondary read-write и read-only ключи; дают широкий доступ ко всему аккаунту.
- **Key rotation (ротация ключей)** - замена ключа через неактивный слот без простоя зависимых приложений.
- **Control plane** - управление ресурсом (настройки, пропускная способность, ключи, назначения ролей data plane).
- **Data plane** - операции с данными (чтение и запись элементов, запросы, change feed).
- **Built-in data roles** - Cosmos DB Built-in Data Reader и Cosmos DB Built-in Data Contributor.
- **Scope (область назначения)** - `/`, `/dbs/<db>`, `/dbs/<db>/colls/<container>`; на уровне элемента и partition key назначения не бывают.
- **IP firewall / virtual network service endpoints** - правила публичного доступа по IP и по подсетям; правила дополняют друг друга.
- **Private endpoint** - приватный IP в VNet через Azure Private Link; целевой подресурс NoSQL - `Sql`.
- **publicNetworkAccess / disableLocalAuth** - параметры отключения публичного доступа и ключевой аутентификации.
- **Dynamic data masking (DDM)** - маскирование полей в ответах чтения и запросов на стороне сервера; данные в хранилище не меняются.
- **Unmask permission** - право видеть исходные значения маскированных полей.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/1-introduction

Безопасность начинается с решений: кто подключается, какие права у него есть, откуда приходят запросы и какие поля клиентов видно. Модуль идет от Microsoft Entra и managed identity к ключам и ротации, затем к RBAC, сетевым контролям и маскированию. Примеры - на C#, с альтернативами на Python. Сценарий: разработчик Contoso готовит аккаунт к production.

### 2. Implement Microsoft Entra authentication
https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/2-implement-entra-authentication

Для Azure-хостов с поддержкой managed identity используйте Microsoft Entra с managed identity: приложение не хранит ключи. Выбор между system-assigned и user-assigned. Для развернутого кода явно используйте ManagedIdentityCredential, чтобы не было fallback на учетную запись разработчика. Для чтения нужна роль data plane. Успешное чтение элемента подтверждает доступ, а при ошибке проверяются три границы: аутентификация, авторизация и сеть.

### 3. Configure key-based authentication and rotation
https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/3-configure-key-authentication-rotation

Если интеграция требует ключ, выбирайте read-only ключ, когда это достаточно; ключ дает широкий доступ, не ограниченный контейнером. Храните ключ в Azure Key Vault. Ротация: проверить, какой слот используют потребители; перегенерировать неактивный secondary; проверить новое значение; переключить все потребители; проверить; перегенерировать primary. Можно отключить ключевую аутентификацию через `disableLocalAuth`, когда все клиенты перешли на Microsoft Entra.

### 4. Implement role-based access control
https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/4-implement-rbac

Control plane управляет ресурсом (включая ключи и назначения ролей), data plane - данными. Для чтения товаров подходит Cosmos DB Built-in Data Reader, а не Contributor. Назначение выполняется через Azure CLI (az cosmosdb sql role assignment create) с principal object ID и узкой областью `/dbs/cosmicworks/colls/product`. Проверяйте разрешенные и запрещенные операции в nonproduction среде.

### 5. Configure network security
https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/5-configure-network-security

Выбор контроля: private endpoint (приватный IP через Private Link), virtual network service endpoint (разрешенная подсеть), IP firewall (публичные IP или диапазоны CIDR). Опция "Accept connections from within Azure datacenters" не подходит для production. Для private endpoint настраивается private DNS (privatelink.documents.azure.com). Явно отключайте публичный доступ (publicNetworkAccess = Disabled), иначе существующие правила и публичный доступ остаются. Изменения могут распространяться до 15 минут.

### 6. Configure dynamic data masking
https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/6-configure-dynamic-data-masking

DDM маскирует поля (в примере `emailAddress` и `phoneNumber`) в ответах чтения и запросов; данные в хранилище не меняются. Требует Microsoft Entra и managed identity (ключи не поддерживаются). Включение функции на аккаунте необратимо. Разделите identity с маской и identity с правом unmask (через пользовательскую роль). Учтите ограничения: запись работает с исходными данными, backup и материализованные представления видят исходные значения, change feed без unmask недоступен.

### 7. Exercise - Secure an account
https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/7-exercise-secure-account

Практическое задание (около 45 минут): клиент с managed identity в Azure Container Instances проверяет доступ только для чтения и сетевые ограничения. Доступны варианты на C# и Python. Нужна подписка Azure.

### 8. Module assessment
https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/8-knowledge-check

Проверка знаний (около 5 минут). Текст вопросов в источнике не приведен.

### 9. Summary
https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/9-summary

Итог: managed identity для Azure-хостов; ключи в Key Vault с ротацией; разделение control plane и data plane и наименьшие роли; private endpoint, service endpoint и IP firewall; маскирование полей с учетом ограничений.

## Важные команды / код / настройки

**Managed identity, system-assigned (C#):**
```
TokenCredential credential = new ManagedIdentityCredential(
    ManagedIdentityId.SystemAssigned);
```

**Managed identity, system-assigned (Python):**
```
from azure.identity import ManagedIdentityCredential
credential = ManagedIdentityCredential()
```

**Managed identity, user-assigned по client ID (C#):**
```
TokenCredential credential = new ManagedIdentityCredential(
    ManagedIdentityId.FromUserAssignedClientId(managedIdentityClientId));
```

**Managed identity, user-assigned по client ID (Python):**
```
from azure.identity import ManagedIdentityCredential
credential = ManagedIdentityCredential(client_id=managed_identity_client_id)
```

**Чтение элемента с Microsoft Entra (C#, фрагмент):**
```
TokenCredential credential = new DefaultAzureCredential();
using CosmosClient client = new CosmosClient(endpoint, credential);
Container container = client.GetContainer("cosmicworks", "product");
ItemResponse<dynamic> response = await container.ReadItemAsync<dynamic>(
    productId,
    new PartitionKey(categoryId));
```

**Встроенные роли data plane:**

| Роль | ID роли | Действия |
|---|---|---|
| Cosmos DB Built-in Data Reader | 00000000-0000-0000-0000-000000000001 | Чтение метаданных, чтение элементов, запросы, change feed |
| Cosmos DB Built-in Data Contributor | 00000000-0000-0000-0000-000000000002 | Метаданные, containers/* и containers/items/* |

Действия Reader: `readMetadata`, `containers/items/read`, `containers/executeQuery`, `containers/readChangeFeed`. Для SDK-запросов нужны `executeQuery` и `readChangeFeed`.

**Назначение роли (Azure CLI):**
```
az cosmosdb sql role assignment create `
    --resource-group '<resource-group>' `
    --account-name '<account-name>' `
    --role-definition-id '00000000-0000-0000-0000-000000000001' `
    --principal-id '<managed-identity-principal-object-id>' `
    --scope '/dbs/cosmicworks/colls/product'
```

**Просмотр назначений:**
```
az cosmosdb sql role assignment list `
    --resource-group '<resource-group>' `
    --account-name '<account-name>'
```

**Права для оператора, который назначает роли (control plane):** `sqlRoleDefinitions/read`, `sqlRoleAssignments/read`, `sqlRoleAssignments/write` в `Microsoft.DocumentDB/databaseAccounts/`.

**Ротация ключей:** регенерировать неактивный ключ, дождаться завершения операции (от 1 минуты до нескольких часов), переключить потребителей, затем регенерировать старый primary. Ключи хранить в Azure Key Vault.

**Отключение ключевой аутентификации:** `disableLocalAuth` = `true` (затрагивает весь аккаунт; сначала проверьте все клиенты на Microsoft Entra).

**Сетевые параметры:**
- Allow access from: Selected networks (IP firewall); CIDR-диапазоны; не использовать 0.0.0.0 "Accept connections from within Azure datacenters" в production.
- Service endpoint: включить `Microsoft.AzureCosmosDB` на подсети и добавить ее в allow rules; аккаунт и VNet в одном тенанте Microsoft Entra.
- Private endpoint: целевой подресурс NoSQL `Sql`; DNS-зона `privatelink.documents.azure.com`.
- Публичный доступ: `publicNetworkAccess` = `Disabled` для закрытого аккаунта.
- Режимы подключения SDK: Direct (C# по умолчанию) - TCP 10 000-20 000 для публичных или service endpoint, 0-65 535 для private endpoint; Gateway (Python) - HTTPS 443.

**DDM - политика маскирования (JSON-фрагмент):**
```
{
  "dataMaskingPolicy": {
    "includedPaths": [
      {
        "path": "/emailAddress",
        "strategy": "Email"
      },
      {
        "path": "/phoneNumber",
        "strategy": "Default"
      }
    ]
  }
}
```
- Стратегия `Email` оставляет первую букву имени пользователя и окончание домена.
- Стратегия `Default` возвращает `XXXX` для строк, `0` для чисел и `false` для логических значений.
- `MaskSubstring` использует `startPosition` и `length`.
- Не маскируйте `id` и partition key (`customerId`); `excludedPaths` поддерживается только при включенном корне `/`.
- Пользовательская роль для unmask: Reader плюс `Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/unmask`; назначается на `/dbs/cosmicworks/colls/customer`.

## Что запомнить

- Для Azure-хостов используйте Microsoft Entra с managed identity; ключи не нужны и не хранятся в коде.
- В развернутом коде выбирайте ManagedIdentityCredential явно, а не DefaultAzureCredential.
- Read-only ключ не ограничивает доступ контейнером: любой владелец ключа получает широкий доступ. Ключи храните в Key Vault и ротируйте через неактивный слот.
- Назначайте роли data plane с минимальными правами и узкой областью (контейнер), используя principal object ID.
- Private endpoint дает приватный доступ; service endpoint и IP-правила все еще используют публичный endpoint. Для закрытого аккаунта отключите публичный доступ.
- Маскирование не защищает запись, бэкапы и прямой запрос к данным; оно дополняет, а не заменяет RBAC и сетевые ограничения.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/
- В источнике упоминаются (без ссылок в тексте): Connect with Microsoft Entra authentication; Rotate account keys; Review data-plane roles and permissions; Configure private endpoints and DNS; Configure virtual network service endpoints; Configure IP firewall rules; Configure dynamic data masking; disable key-based authentication; SDK connectivity modes; Data Explorer authentication.
