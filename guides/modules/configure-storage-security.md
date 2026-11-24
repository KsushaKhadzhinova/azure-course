# Настройка безопасности Azure Storage

**Источник:** https://learn.microsoft.com/en-us/training/modules/configure-storage-security/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/configure-storage-security/<юнит>`)

## Цель модуля

Настроить shared access signature (SAS) с нужными URI и параметрами, настроить шифрование Azure Storage, внедрить customer-managed keys (CMK) и предложить меры по улучшению безопасности хранилища. Модуль относится к подготовке к экзамену AZ-104.

## Ключевые понятия

- **Encryption at rest (шифрование данных в покое)** — Storage Service Encryption (SSE) с 256-битным AES шифрует все данные при записи и расшифровывает при чтении; без дополнительной платы и без снижения производительности.
- **Encryption in transit (шифрование при передаче)** — параметр Secure transfer required; для существующих аккаунтов рекомендуется явно запретить TLS 1.0 и 1.1.
- **Platform-managed keys (PMK)** — ключи, которые создаются, хранятся и управляются Azure; используются по умолчанию.
- **Customer-managed keys (CMK)** — ключи, которыми управляет клиент, хранятся в Azure Key Vault или Managed HSM; BYOK — импорт собственного ключа.
- **Infrastructure encryption (инфраструктурное шифрование)** — двойное шифрование на уровне сервиса и инфраструктуры двумя алгоритмами и двумя ключами; может включаться для аккаунта или encryption scope.
- **Shared Key** — авторизация с помощью ключа доступа аккаунта (два 512-битных ключа на аккаунт).
- **Shared access signature (SAS)** — URI, предоставляющий ограниченный доступ к ресурсам хранилища на заданное время.
- **User delegation SAS** — SAS, защищенный учетными данными Microsoft Entra; поддерживается для Blob Storage и Data Lake Storage.
- **Service-level / account-level SAS** — SAS на конкретные ресурсы сервиса или на более широкий набор операций аккаунта (например, создание файловых систем).
- **Stored access policy (сохраненная политика доступа)** — серверная политика, которая группирует SAS и позволяет отзывать права без перегенерации ключей аккаунта.
- **Storage Insights и Microsoft Defender for Storage** — Insights — пассивный мониторинг и история; Defender — активное обнаружение угроз (сканирование на malware, обнаружение чувствительных данных, аномальная активность).

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/1-introduction
Компания хранит в Azure Storage чувствительные данные, включая персональные. Нужно предоставить безопасный доступ внутренним пользователям и внешним разработчикам. Предварительное условие: навыки работы в портале Azure.

### 2. Review Azure Storage security strategies
Источник: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/2-review-strategies
Перечислены механизмы: шифрование в покое и при передаче, модели шифрования (ключи сервиса, CMK в Key Vault, CMK на собственном оборудовании, client-side шифрование), авторизация через Microsoft Entra ID с managed identities (рекомендуется вместо Shared Key), RBAC на уровне аккаунта, Storage Analytics. Анонимный доступ по умолчанию отключен на новых аккаунтах и рекомендуется оставлять отключенным для аккаунтов с чувствительными данными.

### 3. Create shared access signatures
Источник: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/3-create-shared-access-signatures
SAS — безопасный способ делиться ресурсами без раскрытия ключей аккаунта. Виды: user delegation SAS, account-level SAS и service-level SAS; для серверного контроля — stored access policy. Рекомендации: всегда использовать HTTPS; предпочитать stored access policy (отзыв без смены ключей); задавать короткий срок действия для SAS без политики; заранее продлевать SAS; ставить время начала минимум за 15 минут до текущего (учитывается clock skew до 15 минут); выдавать минимальные права; проверять данные, записанные по SAS; не использовать SAS там, где лучше middle-tier сервис или публичный контейнер.

### 4. Identify URI and SAS parameters
Источник: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/4-identify-uri-sas-parameters
Разобран пример URI service-level SAS. Параметры: ресурсный URI (`restype`, `comp`), версия `sv`, сервис `ss`, время начала `st` (опционально), время окончания `se`, ресурс `sr`, права `sp`, диапазон IP `sip`, протокол `spr`, подпись `sig` (HMAC-SHA256, Base64).

### 5. Determine Azure Storage encryption
Источник: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/5-determine-storage-service-encryption
Шифрование включено для всех новых и существующих аккаунтов и не может быть отключено; выполняется автоматически и прозрачно. Рекомендуется хранить ключи доступа в Azure Key Vault с регулярной ротацией (например, каждые 90 дней через политику ротации). Описаны варианты: infrastructure encryption, platform-managed keys и customer-managed keys.

### 6. Create customer-managed keys
Источник: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/6-create-customer-managed-keys
CMK дают гибкость и контроль: можно создавать, отключать, аудировать, ротировать ключи и задавать права доступа. Аккаунт хранилища и Key Vault должны быть в одном регионе, но могут быть в разных подписках. Managed HSM соответствует FIPS 140-2 Level 3. В портале выбирается тип шифрования (Microsoft или customer) и ключ (URI или выбор из Key Vault).

### 7. Apply Azure Storage security best practices
Источник: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/7-apply-best-practices
Storage Insights дает единый обзор производительности, емкости и доступности, метрики и логи (задержка, пропускная способность, использование емкости, транзакции). Microsoft Defender for Storage добавляет активное обнаружение угроз: сканирование загрузок blob на malware, обнаружение PII и учетных данных, аномальная активность и репутация хешей.

### 8. Exercise: Manage Azure Storage
Источник: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/8-simulation-storage
Практика (около 50 минут по оценке, в исходнике указано 5 минут на юнит): создание аккаунта хранилища, безопасных blob-контейнеров и файловых ресурсов Azure Files через Storage Browser. Нужна подписка Azure.

### 9. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/9-knowledge-check
Проверка знаний (в исходнике приведен сценарий и вопросы, без ответов).

### 10. Summary and resources
Источник: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/10-summary-resources
Модуль охватил настройку SAS (URI и параметры), определение и настройку шифрования, реализацию CMK, а также stored access policies и улучшения безопасности.

## Важные команды / код / настройки

Пример service-level SAS URI (из модуля):

```
https://myaccount.blob.core.windows.net/?restype=service&comp=properties&sv=2015-04-05&ss=bf&st=2015-04-29T22%3A18%3A26Z&se=2015-04-30T02%3A23%3A26Z&sr=b&sp=rw&sip=168.1.5.60-168.1.5.70&spr=https&sig=F%6GRVAZ5Cdj2Pw4tgU7IlSTkWgn7bUkkAg8P6HESXwmf%4B
```

Параметры SAS: `sv` (версия), `ss` (сервис: `bf` — Blob и Files), `st` (начало UTC, опционально), `se` (окончание UTC), `sr` (ресурс: `b` — blob), `sp` (права: `rw`), `sip` (диапазон IP), `spr` (протокол: `https`), `sig` (подпись).

Настройки из текста:

- Secure transfer required — требовать защищенное соединение; запрет TLS 1.0 и 1.1 для существующих аккаунтов.
- Публичный анонимный доступ отключен по умолчанию для новых аккаунтов; рекомендуется оставлять отключенным для чувствительных данных.
- Для Key Vault — автоматическая ротация ключей (пример: каждые 90 дней).
- Для CMK — аккаунт и Key Vault в одном регионе; Managed HSM для требований FIPS 140-2 Level 3.
- Clock skew — до 15 минут; время начала SAS задавать не менее чем за 15 минут до текущего или не задавать вовсе.

Рекомендованные ограничения для SAS по версии API: для клиентов с версией REST API ранее 2012-02-12 максимальная длительность SAS без stored access policy — 1 час.

## Что запомнить

- Шифрование at rest включено всегда; для ключей выбирается PMK (по умолчанию) или CMK из Key Vault / Managed HSM.
- Предпочтительна авторизация через Microsoft Entra ID и managed identities; Shared Key можно отключить на уровне аккаунта.
- SAS всегда передавать и создавать по HTTPS; отзывать удобнее через stored access policy.
- Минимизируйте права и срок действия SAS: короткий срок ограничивает ущерб при компрометации.
- Для CMK аккаунт и Key Vault должны быть в одном регионе; ключи можно ротировать и аудировать.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/
- Документация: Grant limited access to Azure Storage resources with shared access signatures; Read about Azure Storage encryption for data at rest; Create a SAS for your Azure storage account; Create a service-level SAS; Construct a user delegation SAS; Use customer-managed keys for Azure Storage encryption (упоминаются в уроке 10).
- Самостоятельное обучение: Secure your Azure storage account; Implement Azure Storage security (упоминаются в уроке 10).
- Связанный модуль: Plan and implement security for storage (упоминается в уроке 6).
