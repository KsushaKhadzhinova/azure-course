# Реализация безопасности учётной записи хранения Azure

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-storage-account-security/

## Цель модуля

Настроить базовые параметры безопасности учётной записи хранения (secure transfer, минимальная версия TLS, запрет анонимного доступа, запрет репликации между арендаторами), выбрать модель авторизации (managed identity и RBAC предпочтительны), управлять жизненным циклом SAS-токенов через stored access policies и отключить Shared Key авторизацию с контролем через Azure Policy.

## Ключевые понятия

- **Secure transfer required** - разрешает только HTTPS-подключения, HTTP отклоняется.
- **Minimum TLS version** - минимальная версия TLS для клиентов; рекомендуется 1.2.
- **Allow Blob anonymous access** - разрешение анонимного (публичного) чтения контейнеров и блобов; рекомендуется отключить.
- **Allow cross-tenant replication** - разрешение object replication между арендаторами Microsoft Entra; рекомендуется отключить, если не нужно.
- **Shared Key (account key)** - ключи учётной записи с полным доступом ко всем данным; рекомендуется отключить.
- **Service SAS, Account SAS** - SAS, подписанные ключом учётной записи; отзыв требует ротации ключа (кроме service SAS со stored access policy).
- **User delegation SAS** - SAS, подписанный ключом делегирования Microsoft Entra; единственный тип SAS, который рекомендует Microsoft; ключ делегирования действителен до 7 дней.
- **Managed identity (system-assigned и user-assigned)** - идентичность Azure, которой управляет платформа; `DefaultAzureCredential` использует её автоматически.
- **Stored access policy (сохранённая политика доступа)** - серверная политика на контейнере с идентификатором, сроком и правами; SAS ссылается на неё, и её можно отозвать без ротации ключа.
- **Azure Policy "Storage accounts should prevent shared key access"** - политика, которая аудирует или запрещает Shared Key доступ.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/implement-storage-account-security/1-introduction

Сценарий Contoso: AI-агенты в Azure Functions работают с документами в Blob Storage, ключи учётной записи хранятся в настройках приложения. Задача команды безопасности: закрыть базовые настройки, перейти к identity-based доступу, выдавать отзываемые SAS внешним подрядчикам и отключить ключи через Azure Policy.

### 2. Настройка параметров безопасности учётной записи
Источник: https://learn.microsoft.com/en-us/training/modules/implement-storage-account-security/2-configure-storage-account-security

- **Secure transfer required**: включено по умолчанию для новых учётных записей; старые аккаунты могут разрешать HTTP - проверьте и включите. После включения HTTP-приложения получают ошибку.
- **Minimum TLS version**: установите Version 1.2; клиенты с TLS 1.0 и 1.1 отклоняются; настройка действует на Blob, File, Queue и Table.
- **Allow Blob anonymous access**: по умолчанию отключено для новых учётных записей; отключение на уровне аккаунта переопределяет настройки контейнеров.
- **Allow cross-tenant replication**: отключите, если межарендаторная репликация не нужна; внутриарендаторная репликация продолжит работать.
- Путь в портале: Configuration в разделе Settings учётной записи.

### 3. Выбор модели авторизации
Источник: https://learn.microsoft.com/en-us/training/modules/implement-storage-account-security/3-select-authorization-model

- Три модели: Shared Key (рекомендуется отказаться), SAS (только user delegation SAS рекомендуется), Microsoft Entra ID + RBAC (предпочтительна).
- Shared Key: ключи - два 512-битных секрета с полным доступом; отзыв требует ротации, что ломает все приложения с этим ключом.
- Service SAS подписывается ключом учётной записи; Account SAS - тоже; user delegation SAS подписывается ключом делегирования Microsoft Entra и отзывается отзывом учётных данных Entra.
- RBAC-роли данных: Storage Blob Data Reader (чтение), Storage Blob Data Contributor (чтение, запись, удаление), Storage Blob Data Owner (полный контроль, включая права). Эти роли не дают доступа к управлению учётной записью.
- Для Azure Functions рекомендуется managed identity с ролью Storage Blob Data Reader; `DefaultAzureCredential` получает токены автоматически.
- Назначение: Identity > System assigned > Status: On, затем Access Control (IAM) > Add role assignment; распространение роли может занять до 30 минут.
- System-assigned привязана к одному ресурсу и удаляется вместе с ним; user-assigned существует независимо и может использоваться несколькими ресурсами (например, при переносе в Azure Container Apps).

### 4. Управление доступом через stored access policies
Источник: https://learn.microsoft.com/en-us/training/modules/implement-storage-account-security/4-manage-stored-access-policies

- Stored access policy задаёт идентификатор, время начала и окончания, разрешения; SAS ссылается на неё через `signedidentifier` и не содержит сроков и прав сам по себе.
- Изменение или удаление политики мгновенно влияет на все SAS, которые на неё ссылаются.
- Создание: портал - Containers > нужный контейнер > Access policy > Add policy. До пяти политик на контейнер, очередь, таблицу или файловый ресурс.
- Отзыв: удалить политику или изменить срок на прошлое, либо убрать разрешения.
- Ограничения: работает только с service SAS; для account SAS и user delegation SAS не поддерживается (для user delegation отзыв - через учётные данные Entra).

### 5. Отключение Shared Key и контроль через Azure Policy
Источник: https://learn.microsoft.com/en-us/training/modules/implement-storage-account-security/5-disable-shared-key-enforce-policy

- Перед отключением найдите клиентов, которые используют ключи: метрика Transactions с фильтром Authentication = AccountKey; либо запрос в Azure Monitor Logs к `StorageBlobLogs` с группировкой по `CallerIpAddress` и `UserAgentHeader`.
- Мигрируйте клиентов на managed identity или service principal с RBAC, а внешним клиентам выдавайте user delegation SAS.
- Отключение: Configuration > Allow storage account key access = Disabled. После этого запросы с ключом или SAS, подписанным ключом, получают HTTP 403; user delegation SAS и Entra ID + RBAC продолжают работать.
- Важно для Azure Files: портал по умолчанию использует Shared Key для file shares; без настройки identity-based доступа отключение ломает Azure Files, включая доступ через портал. Blob-only аккаунт Contoso не затронут.
- Azure Policy: "Storage accounts should prevent shared key access". Сначала назначьте в режиме Audit, затем переключите на Deny. Политика не отключает Shared Key на существующих аккаунтах - их нужно исправить вручную или через remediation tasks. Назначение: Azure Policy > поиск политики > Assign; результаты появляются в течение нескольких часов.

### 6. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/implement-storage-account-security/6-knowledge-check

В исходных материалах вопросы не приведены.

### 7. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/implement-storage-account-security/7-summary

Модуль закрыл уровень доступа: базовые настройки (secure transfer, TLS 1.2, запрет анонимного доступа, запрет межарендаторной репликации), identity-based авторизация через managed identity, отзываемые SAS через stored access policies и отключение Shared Key с контролем через Azure Policy. Следующий модуль - сетевая безопасность.

## Важные команды / код / настройки

Команда генерации SAS, ссылающегося на stored access policy (Azure CLI):

```
az storage blob generate-sas \
    --account-name contosodocs \
    --container-name invoices \
    --name document.pdf \
    --policy-name vendor-read-policy \
    --account-key <key>
```

Запрос в Azure Monitor Logs для поиска вызовов с Shared Key или SAS (KQL):

```
StorageBlobLogs
| where AuthenticationType in ("AccountKey", "SAS") and TimeGenerated > ago(7d)
| summarize count() by CallerIpAddress, UserAgentHeader, AccountName
| top 10 by count_ desc
```

Настройки из уроков (портал, раздел Configuration учётной записи и Azure Policy):
- Secure transfer required = Enabled
- Minimum TLS version = Version 1.2
- Allow Blob anonymous access = Disabled
- Allow cross-tenant replication = Disabled
- Allow storage account key access = Disabled
- Политика: "Storage accounts should prevent shared key access" (Audit, затем Deny)
- Роли: Storage Blob Data Reader, Storage Blob Data Contributor, Storage Blob Data Owner
- Лимит stored access policies: 5 на контейнер (или другой ресурс)

## Что запомнить

- Включите secure transfer и TLS 1.2, отключите анонимный доступ и межарендаторную репликацию, если они не нужны.
- Предпочитайте Microsoft Entra ID + RBAC; для Azure Functions используйте managed identity и `DefaultAzureCredential`.
- Из SAS рекомендуется только user delegation SAS; service SAS со stored access policy позволяет отзыв без ротации ключа.
- Перед отключением Shared Key найдите клиентов с AccountKey через метрики или StorageBlobLogs.
- Azure Policy сначала в режиме Audit, потом Deny; существующие аккаунты исправляются отдельно, а Azure Files требует отдельной подготовки.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/implement-storage-account-security/
- Authorize access to data in Azure Storage; Prevent Shared Key authorization for an Azure Storage account (ссылки из урока 7)
- Следующий модуль курса: настройка сетевой безопасности Azure Storage (см. guides/modules/configure-network-security-azure-storage.md)
