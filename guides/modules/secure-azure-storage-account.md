# Защита учетной записи Azure Storage

**Источник:** https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/

## Цель модуля

Научиться защищать данные в учетной записи Azure Storage: понимать встроенное шифрование, выбирать способ авторизации (Microsoft Entra ID, ключи учетной записи, SAS), ограничивать сетевой доступ, включать защиту от угроз (Microsoft Defender for Storage), аудировать доступ и использовать механизмы безопасности Azure Data Lake Storage Gen2.

## Ключевые понятия

- **Storage Service Encryption (SSE)** — автоматическое шифрование данных при записи (AES-256, FIPS 140-2); отключить нельзя.
- **Encryption in transit** — защита передачи данных через HTTPS и параметр Secure transfer required.
- **CORS (Cross-Origin Resource Sharing)** — правила межсайтовых запросов; по умолчанию отключено.
- **Microsoft Entra ID и RBAC** — рекомендуемая авторизация для данных и управления.
- **Managed identity** — учетная запись ресурса Azure без хранимых секретов.
- **Storage account keys** — два ключа (primary и secondary) с полным доступом к учетной записи.
- **Shared access signature (SAS)** — токен с ограниченными правами и сроком действия: user delegation, service и account SAS.
- **Private endpoint** — частный IP-адрес в виртуальной сети для доступа к учетной записи.
- **Microsoft Defender for Storage** — защита от необычной активности и угроз.
- **ACL (POSIX-like)** — списки контроля доступа в Azure Data Lake Storage Gen2.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/1-introduction

Введение: Blob, Azure Files, Table storage и Data Lake Storage строятся на Azure Storage и наследуют его механизмы безопасности. Сценарий: аудит безопасности, в ходе которого нужно показать, что данные соответствуют политике Contoso.

### 2. Explore Azure Storage security features
https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/2-storage-security-features

Шесть направлений: защита данных в покое (SSE, AES-256, шифрование дисков ВМ через Azure Disk Encryption с Key Vault), защита при передаче (HTTPS, secure transfer required по умолчанию), CORS (по умолчанию отключено), RBAC с Microsoft Entra ID (рекомендуется, с управляемыми identity), аудит через журналы Azure Monitor (рекомендованы вместо Storage Analytics logs).

### 3. Understand storage account keys
https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/3-storage-account-keys

Shared Key — простой способ авторизации, подписывающий каждый запрос ключом. Ключи учетной записи дают полный доступ, поэтому их используют только для доверенных внутренних приложений. Ротация: переключить приложения на вторичный ключ, перегенерировать первичный, переключить приложения на новый первичный, перегенерировать вторичный. После перегенерации старый ключ и подписанные им SAS перестают работать. Shared Key можно полностью отключить параметром Allow storage account key access.

### 4. Understand shared access signatures
https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/4-shared-access-signatures

Для внешних клиентов используется SAS с ограниченными правами и временем действия. Типы: user delegation SAS (подписан учетными данными Microsoft Entra, рекомендуется), service SAS (для одного сервиса, подписан ключом учетной записи) и account SAS (для нескольких сервисов и операций, подписан ключом). Два шаблона: прокси-сервис с аутентификацией и легкий сервис, который выдает SAS клиенту для прямого доступа.

### 5. Control network access to your storage account
https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/5-control-network-access

По умолчанию доступ разрешен из любой сети. Варианты: private endpoint (частный IP в виртуальной сети, трафик идет по приватной линии Microsoft), ограничение публичного доступа выбранными сетями или IP, полный запрет публичного доступа (Disable). Создание private endpoint не отключает публичный endpoint автоматически. Установка правила deny по умолчанию блокирует доступ, если сначала не настроены разрешающие правила.

### 6. Understand advanced threat protection for Azure Storage
https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/6-advanced-threat-protection

Microsoft Defender for Storage выявляет необычные и потенциально вредоносные попытки доступа к Blob, Azure Files и Data Lake Storage Gen2. Рекомендуется включать план на уровне подписки. Тревоги интегрируются с Microsoft Defender for Cloud; по умолчанию владельцы подписки получают email по тревогам высокой важности. В письме указаны характер аномалии, учетная запись, время, возможные причины, шаги расследования и устранения.

### 7. Explore Azure Data Lake Storage security features
https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/7-adl-enterprise-security-features

Data Lake Storage Gen2 построен на Blob storage и наследует его защиту. Добавляет POSIX-подобные ACL для пользователей, групп и service principal, аутентификацию Microsoft Entra ID OAuth 2.0 и интеграцию с Azure Databricks, HDInsight, Azure Synapse Analytics и Azure Storage Explorer.

### 8. Summary
https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/8-summary

Итоги: многоуровневая модель безопасности. Сетевые правила ограничивают приложения, авторизация идет через Microsoft Entra, ключ учетной записи или SAS, шифрование включено по умолчанию, Microsoft Defender for Storage помогает контролировать системы.

## Важные команды / код / настройки

**Запрос Shared Key (пример из урока 3):**

```
GET https://myaccount.blob.core.windows.net/?restype=service&comp=stats

x-ms-version: 2018-03-28  
Date: Wed, 23 Oct 2018 21:00:44 GMT  
Authorization: SharedKey myaccount:CY1OP3O3jGFpYFbTCBimLn0Xov0vt0khH/E5Gy0fXvg=
```

**Расположение ключей в портале:** Security + networking → Access keys.

**Порядок ротации ключей:** переключить приложения на secondary → перегенерировать primary → переключить на новый primary → перегенерировать secondary.

**Параметры учетной записи:**

- Secure transfer required — включен по умолчанию; отклоняет HTTP и незашифрованный SMB.
- Allow storage account key access — установить Disabled, чтобы запретить Shared Key. Это обязательный шаг для Conditional Access.
- Public network access — Enabled from selected networks, Enabled from all networks или Disable (трафик только через private endpoint).

**Типы SAS:** user delegation SAS (рекомендуется), service SAS и account SAS (оба подписываются ключом учетной записи).

**Defender for Storage (включение на уровне подписки):** Microsoft Defender for Cloud → Environment settings → выбрать подписку → три точки → Edit settings → Storage: On → Save.

**Ограничения и предупреждения из источника:**

- Отключение Shared Key перед этим обязательно для применения Conditional Access. Перед отключением переведите приложения на авторизацию через Microsoft Entra ID (предпочтительно с managed identities). Для рабочих нагрузок с поддержкой OAuth используйте Microsoft Entra ID, для Azure Files по SMB — Kerberos, для случаев, где авторизация через Entra ID невозможна, — user delegation SAS.
- Тарифицирование Defender for Storage: план по учетной записи; сканирование на вредоносное ПО оплачивается за ГБ; защита новых учетных записей начинается до 24 часов после создания.

## Что запомнить

- Шифрование данных в покое включено по умолчанию и не отключается; для дисков ВМ используйте Azure Disk Encryption с Key Vault.
- Рекомендуемая авторизация — Microsoft Entra ID с managed identities; ключи учетной записи дают полный доступ и должны ротироваться.
- Для внешних клиентов используйте user delegation SAS с ограниченными правами и сроком действия.
- Private endpoint не отключает публичный доступ автоматически: явно установите Disable.
- Data Lake Storage Gen2 добавляет ACL, а Microsoft Defender for Storage выявляет аномалии доступа.

## Связанные материалы

- Azure Storage security (упоминается в уроке 2).
- Microsoft Defender for Storage и интеграция с Microsoft Defender for Cloud (упоминаются в уроке 6).
- Azure Storage logs в Azure Monitor (упоминаются в уроке 2).
- Conditional Access для Azure Storage (упоминается в уроке 3).
