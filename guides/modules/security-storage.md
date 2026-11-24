# Безопасность Azure Storage

**Источник:** https://learn.microsoft.com/en-us/training/modules/security-storage/

## Цель модуля

Научиться планировать и внедрять меры безопасности для ресурсов Azure Storage по принципам Zero Trust: аутентификация и авторизация через Microsoft Entra ID, управление ключами доступа учетной записи, выбор метода доступа к Azure Files, Blobs, Tables и Queues, защита данных (soft delete, резервные копии, версионирование, immutable storage, point-in-time restore), шифрование с BYOK через Azure Key Vault и двойное шифрование на уровне инфраструктуры.

## Ключевые понятия

- **Zero Trust** - принцип "никогда не доверяй, всегда проверяй": каждый запрос на доступ проверяется по идентичности.
- **Microsoft Entra ID** - облачный сервис идентичности; авторизация через Azure RBAC - предпочтительный метод для Blob, File, Queue и Table.
- **Azure RBAC** - ролевая модель доступа; роли данных (например, Storage Blob Data Reader) дают доступ к данным, а роли управления (Owner, Contributor) - только к учетной записи.
- **Shared Key (ключ учетной записи)** - авторизация по ключу учетной записи; дает полный доступ и рекомендуется избегать.
- **SAS (Shared access signature)** - делегированный доступ по токену; user delegation SAS (на основе Microsoft Entra) рекомендуется, service SAS и account SAS подписываются ключом учетной записи.
- **Anonymous access (анонимный доступ)** - публичное чтение контейнеров и blob; по умолчанию рекомендуется отключать.
- **Managed identity (управляемая идентичность)** - идентичность ресурса Azure, не требующая хранения учетных данных в коде.
- **Identity-based authentication over SMB** - доступ к Azure Files по SMB через AD DS, Microsoft Entra Domain Services или Microsoft Entra Kerberos.
- **Access keys (ключи доступа)** - два 512-битных ключа на учетную запись; ротируются по очереди.
- **Key expiration policy (политика срока ключей)** - напоминание о ротации ключей; проверяется встроенной политикой Azure Policy.
- **Soft delete (мягкое удаление)** - восстановление удаленных контейнеров и blob в течение срока хранения.
- **Blob versioning (версионирование)** - автоматическое сохранение предыдущих версий blob при перезаписи.
- **Point-in-time restore (восстановление на момент времени)** - откат набора блочных blob к состоянию в прошлом.
- **Immutability policy (неизменяемость, WORM)** - запрет удаления и перезаписи данных на заданный интервал; legal hold.
- **Snapshot (снимок)** - ручное сохранение состояния blob в момент времени.
- **BYOK (Bring Your Own Key)** - импорт собственного ключа из on-premises HSM в Azure Key Vault.
- **KEK (Key Exchange Key)** - RSA-HSM ключ в Key Vault с операцией import, которым защищается передаваемый ключ.
- **Key Transfer Blob (.byok)** - файл с зашифрованным ключом, который создает BYOK-инструмент производителя HSM.
- **Infrastructure encryption (double encryption)** - второе шифрование 256-bit AES на уровне инфраструктуры хранилища с отдельным ключом Microsoft.
- **Encryption scope (область шифрования)** - возможность включить infrastructure encryption для части данных внутри учетной записи.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/1-introduction

Модуль рассчитан на администраторов хранилищ, которые защищают данные клиентов, финансовые записи и интеллектуальную собственность. Цели: применять Zero Trust к Azure Storage; настраивать контроль доступа по идентичности через Microsoft Entra ID; управлять жизненным циклом ключей доступа и их ротацией; выбирать метод аутентификации для Azure Files, Blob, Tables и Queues; внедрять защиту данных (soft delete, резервные копии, версионирование, immutable storage, point-in-time restore); настраивать BYOK через Azure Key Vault; включать infrastructure encryption (двойное шифрование).

### 2. Azure Storage
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/2-azure-storage

Azure Storage - облачное хранилище Microsoft: доступ по HTTP/HTTPS через REST API, клиентские библиотеки (.NET, Java, Node.js, Python, Go и другие), Azure PowerShell и CLI, портал и Storage Explorer. Сервисы: Blobs (включая Data Lake Storage Gen2), Files, Elastic SAN, Queues, Tables (в составе Cosmos DB for Table), managed Disks, Container Storage; также Azure NetApp Files. Все данные учетной записи шифруются. Для каждого сервиса есть свой сценарий: Files - "lift and shift" приложений с SMB/NFS; Blobs - потоковая и произвольная выборка, data lake; Queues - асинхронные сообщения (до 64 KB, до миллионов сообщений); Tables - гибкие структурированные данные.

Способы авторизации: Microsoft Entra integration (RBAC) для blob, file, queue и table - рекомендуется; identity-based SMB для Azure Files через AD DS, Entra Domain Services или Entra Kerberos; Shared Key (ключ учетной записи, рекомендуется отказываться по возможности); SAS; Entra Domain Services для Azure NetApp Files. Шифрование: encryption at rest (с возможностью собственных ключей через Key Vault) и client-side encryption в клиентских библиотеках. Избыточность задается при создании учетной записи.

### 3. Контроль доступа к учетным записям
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/3-authorize-requests-azure-storage

Таблица поддержки методов по сервисам: Azure Blobs поддерживает Shared Key, SAS, Microsoft Entra ID и анонимный публичный доступ (не поддерживает AD DS). Azure Files (SMB) - Shared Key, Entra ID через Entra Domain Services или Entra Kerberos, AD DS (с синхронизацией учетных данных в Entra ID), без SAS и анонимного доступа. Azure Files (REST), Queues и Tables - Shared Key, SAS и Entra ID; AD DS и анонимный доступ не поддерживаются.

- **Microsoft Entra ID (рекомендуется)** - RBAC назначает права пользователям, группам и приложениям; ключ не нужно хранить в коде.
- **Entra Domain Services для Azure Files** - RBAC для уровня ресурса, Windows ACL для файлов и каталогов.
- **Active Directory для Azure Files** - SMB-доступ с учетными данными AD из присоединенных машин.
- **Shared Key** - полный доступ к учетной записи; по возможности отключайте.
- **SAS** - три типа: user delegation SAS (на основе Entra, рекомендуется), service SAS и account SAS (оба на ключе учетной записи). Для Blob предпочитайте user delegation SAS.
- **Анонимный доступ** - публичное чтение без авторизации; отключайте на уровне учетной записи, если не требуется.
- Порядок выбора: первый выбор - Entra ID с managed identities для приложений в Azure; второй - Entra ID с service principals; третий - user delegation SAS для Blob; последний - Shared Key, если ничего другого нет; анонимный доступ по умолчанию выключен.

### 4. Жизненный цикл ключей доступа учетной записи
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/4-manage-storage-account-access-keys

- При создании учетной записи Azure генерирует два 512-битных ключа доступа; они используются для Shared Key и для SAS, подписанных ключом.
- Рекомендуется хранить ключи в Azure Key Vault и регулярно их ротировать без прерывания приложений.
- Ключи дают полный доступ к конфигурации и данным учетной записи; их доступ нужно ограничивать и мониторить. По возможности используйте Entra ID для Blob, Queue и Table и SMB с AD DS или Entra Kerberos для Azure Files.
- Для запрета Shared Key отключите его на уровне учетной записи; Conditional Access в Entra ID требует отключения Shared Key. Если Shared Key отключен, но в логах видна авторизация Shared Key, это указывает на использование trusted access.
- Просмотр ключей: портал (Security + networking - Access keys, Show keys, Copy), PowerShell или Azure CLI; доступны key1 и key2 и строки подключения. Обычно используйте key1, key2 резервируйте для ротации. Просмотр требует роль Service Administrator или роль с действием `Microsoft.Storage/storageAccounts/listkeys/action` (Owner, Contributor, Storage Account Key Operator Service Role).
- **Ротация вручную**: обновите строки подключения приложений на secondary-ключ; в портале регенерируйте primary-ключ (кнопка Regenerate) и обновите код на новый primary; повторите для secondary. Важно использовать в приложениях только один ключ одновременно. Регенерация требует действия `Microsoft.Storage/storageAccounts/regeneratekey/action`.
- Регенерация ключа отзывает SAS, подписанные этим ключом; после ротации нужно пересоздать account и service SAS. User delegation SAS на ключи не влияет.
- **Key expiration policy**: кнопка Set rotation reminder в Access keys, включение напоминаний и частота. Встроенная политика Azure Policy "Storage account keys should not be expired" назначается на нужную область и показывает несоответствия в View compliance.

### 5. Доступ к Azure Files
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/5-select-configure-access-azure-files

- При работе с файлами в портале запросы авторизуются через учетную запись Microsoft Entra или ключ учетной записи; портал показывает метод и позволяет переключаться при наличии прав. Рекомендуется Entra ID.
- Метод можно задать для каждой файловой шары (Data storage - File shares - шара - Browse, поле Authentication method).
- **Доступ через Entra-учетную запись** требует двух условий: роль с доступом к данным файлов и роль Azure Resource Manager Reader (минимум) на уровне учетной записи или выше. Встроенные роли: Storage File Data Privileged Reader (чтение) и Storage File Data Privileged Contributor (чтение, запись, удаление, изменение ACL/NTFS - ACL в портале не меняются, используйте PowerShell или CLI). Для переключения на Entra-пользователя нужны дополнительные действия `readFileBackupSemantics` и `writeFileBackupSemantics`.
- **Доступ через ключ**: нужна роль с `Microsoft.Storage/storageAccounts/listkeys/action` (Reader and Data Access, Storage Account Contributor, Azure Resource Manager Contributor и Owner по возрастанию прав). Использование ключа дает полный доступ и должно быть ограничено.
- При ReadOnly-блокировке учетной записи операция List Keys (POST) запрещена, поэтому доступ к файлам возможен только через Entra-учетные данные. Классические роли Service Administrator и Co-Administrator эквивалентны Owner.
- Настройка по умолчанию: при создании учетной записи (вкладка Advanced, раздел Security, флажок Default to Microsoft Entra authorization in the Azure portal) или позже (Settings - Configuration - Enabled).
- Рекомендации: отдавать предпочтение Entra ID, выдавать минимальные роли (Privileged Reader для чтения), использовать managed identities, условный доступ (Conditional Access), мониторинг через Azure Monitor, по возможности отключить Shared Key.

### 6. Доступ к Azure Blobs через Microsoft Entra ID
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/6-authorize-access-blobs-use-microsoft-entra-id

- Entra ID поддерживается для всех учетных записей general-purpose и Blob во всех публичных регионах и национальных облаках; только для учетных записей, созданных через модель развертывания Azure Resource Manager.
- Рекомендуется managed identities для ресурсов в Azure; для локальных ресурсов - через Azure Arc. Для SAS предпочтительна user delegation SAS.
- Двухэтапный процесс: аутентификация (получение OAuth 2.0 токена) и авторизация (проверка роли RBAC в сервисе Blob).
- Клиентские библиотеки: Azure Identity (рекомендуется для большинства сценариев, DefaultAzureCredential) и MSAL (для продвинутых сценариев, нужен resource ID).
- Resource ID для конкретной учетной записи: `https://<account-name>.blob.core.windows.net` (Azure Global), `https://<account-name>.blob.core.usgovcloudapi.net` (Azure Government), `https://<account-name>.blob.core.chinacloudapi.cn` (Azure China 21Vianet). Общий для всех облаков: `https://storage.azure.com`.
- Права назначаются через RBAC на уровне: отдельного контейнера (самый узкий), учетной записи, группы ресурсов, подписки, группы управления. Роли: Storage Blob Data Owner (полный доступ, включая POSIX ACL для ADLS Gen2), Storage Blob Data Contributor (чтение, запись, удаление), Storage Blob Data Reader (только чтение), Storage Blob Delegator (получение user delegation key). Роли Owner, Contributor и Storage Account Contributor данных blob не дают.
- Azure ABAC позволяет задать условия назначения ролей (например, по имени контейнера, пути blob или тегам).
- Назначение ролей может занимать до 30 минут.
- Портал: выбирает метод по наличию listkeys-права; для доступа через Entra нужны права на данные и на навигацию по ресурсам учетной записи (Reader).
- Рекомендуется отключить Shared Key после миграции, использовать user delegation SAS, включить диагностику и условный доступ.
- Поддержка может быть ограничена при включенном Data Lake Storage Gen2, NFS 3.0 или SFTP.

### 7. Доступ к Azure Tables через Microsoft Entra ID
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/7-authorize-access-tables-use-microsoft-entra-id

- Entra ID для таблиц доступен для всех учетных записей общего назначения во всех публичных регионах и национальных облаках (только для Resource Manager).
- Управляемые идентичности - рекомендуемый подход: не нужно хранить учетные данные.
- Роли RBAC: Storage Table Data Contributor (чтение, запись, удаление сущностей) и Storage Table Data Reader (только чтение).
- Уровни области: отдельная таблица (самый узкий), учетная запись, группа ресурсов, подписка, группа управления.
- Роли Owner, Contributor и Storage Account Contributor доступа к данным таблиц не дают. Роли с действием listKeys дают полный доступ по Shared Key; для усиления создайте пользовательскую роль без этого действия.
- Назначение ролей может занимать до 30 минут.
- Лучшие практики: managed identities, минимальные роли (Reader вместо Contributor, где возможно), назначение на уровне таблицы, отключение Shared Key, пользовательские роли, мониторинг, условный доступ, периодический аудит назначений, разделение dev и prod (разные учетные записи и назначения).

### 8. Доступ к Azure Queues через Microsoft Entra ID
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/8-authorize-access-queue-data-azure-portal

- Entra ID для очередей доступен для всех учетных записей general-purpose; рекомендуется управляемая идентичность.
- Resource ID для очередей: `https://<account-name>.queue.core.windows.net` (Azure Global), `https://<account-name>.queue.core.usgovcloudapi.net` (Azure Government), `https://<account-name>.queue.core.chinacloudapi.cn` (Azure China 21Vianet). Общий: `https://storage.azure.com`.
- Роли RBAC: Storage Queue Data Contributor (полный доступ к сообщениям), Storage Queue Data Reader (только просмотр), Storage Queue Data Message Processor (peek, получение и удаление сообщений для worker-приложений), Storage Queue Data Message Sender (только добавление сообщений).
- Уровни области: отдельная очередь, учетная запись, группа ресурсов, подписка, группа управления.
- Роли управления (Owner, Contributor, Storage Account Contributor) данных очередей не дают.
- Портал, PowerShell и CLI поддерживают вход учетными данными Entra; в портале выбор метода зависит от наличия listkeys-права.
- Лучшие практики: managed identities; минимальные роли (Reader для просмотра, Message Sender для постановки в очередь, Message Processor для worker, Data Contributor только при полном доступе); назначение на уровне очереди; отключение Shared Key; повторы с экспоненциальной задержкой при сбоях аутентификации; разделение окружений.

### 9. Защита данных от угроз: soft delete, резервные копии, версионирование, immutable storage
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/9-recommendations-basic-data-protection

- Базовый набор защиты: блокировка Azure Resource Manager на учетную запись (защищает от удаления учетной записи, но не контейнеров и blob); container soft delete для восстановления контейнеров; для Blob - версионирование (blob versioning) при каждой перезаписи; для Data Lake Storage Gen2 - ручные снимки.
- Варианты защиты: ARM-блокировка учетной записи; immutability policy на версию blob или на контейнер (для соответствия требованиям, WORM); container soft delete (минимум 7 дней); blob versioning вместе с container и blob soft delete; blob soft delete (минимум 7 дней); point-in-time restore для набора блочных blob (не удаляйте контейнеры, удаляйте отдельные blob); blob snapshot (альтернатива версионированию по стоимости или для hierarchical namespace); копирование во вторую учетную запись (object replication только для Blob, AzCopy и Azure Data Factory поддерживают Blob и Data Lake).
- Таблица по ресурсам: ARM-блокировка защищает только учетную запись; immutability policy на версию или контейнер защищает учетную запись, контейнер, объект от удаления и перезаписи; container soft delete - контейнер от удаления; blob versioning, blob soft delete и point-in-time restore - объект от удаления и перезаписи; snapshot - только от перезаписи; копирование во вторую учетную запись - контейнер и объекты.
- Особенности: учетную запись нельзя удалить, если в ней есть контейнер с version-level immutable storage; контейнер нельзя удалить, если в нем есть blob (независимо от блокировки); перезапись текущей версии создает новую версию; при legal hold или заблокированной time-based retention политике на уровне контейнера учетная запись также защищена от удаления; blob versioning и point-in-time restore не поддерживаются для Data Lake Storage Gen2.
- Восстановление: учетная запись - в течение 14 дней (если создана через Resource Manager и не пересоздана с тем же именем); контейнер - через container soft delete; из второй учетной записи; версия blob; soft-deleted blob; снимок; набор блочных blob на момент времени (если point-in-time restore включен и точка в пределах срока хранения; хранилище не скомпрометировано).
- Стоимость: включение большинства функций бесплатно, но удаленные и версии данных тарифицируются; point-in-time restore включает версионирование, soft delete и change feed; оплата за операцию восстановления; копии во второй учетной записи добавляют емкость, транзакции и при другом регионе - исходящий трафик.
- Аварийное восстановление: при геоизбыточности (GRS, GZRS) можно вручную переключиться на вторичный регион; customer-managed failover не поддерживается для учетных записей с hierarchical namespace.
- Рекомендации: комбинировать несколько механизмов; регулярно проверять восстановление; планировать сроки хранения с учетом стоимости; использовать immutability для WORM; мониторить через Azure Monitor и Azure Policy; управлять жизненным циклом версий и снимков; геоизбыточность для критичных данных; Azure Backup for Azure Files.

### 10. Настройка BYOK (Bring Your Own Key)
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/10-bring-your-own-key-specification

- Сценарий: клиент переносит ключ из on-premises HSM в HSM, которая поддерживает Azure Key Vault. Требования: ключ не существует вне HSM в открытом виде; вне HSM ключ всегда защищен ключом, который хранится в HSM Key Vault.
- Термины: **KEK (Key Exchange Key)** - RSA-HSM ключ, созданный в Key Vault; **Wrapping key** - эфемерный AES-ключ, созданный on-premises HSM; **Target key** - переносимый ключ (RSA, EC, AES только в Managed HSM).
- KEK: RSA-HSM размером 4 096 бит (рекомендуется), 3 072 или 2 048; key_ops ограничены `import`; находится в том же vault, куда импортируется Target key.
- Шаги: 1) создать KEK в Key Vault; 2) скачать публичную часть KEK; 3) с BYOK-инструментом производителя HSM импортировать KEK в целевой HSM и экспортировать Target key, защищенный KEK; 4) импортировать полученный blob в Key Vault через Azure CLI или PowerShell. Результат шага 3 - файл Key Transfer Blob (`.byok`).
- Ограничения HSM: разрешен экспорт через key wrap; Target key помечен CKA_EXTRACTABLE; KEK и wrapping key могут быть CKA_TRUSTED. Настройка исходного HSM - в документации производителя.
- Формат blob: JSON Web Encryption compact serialization (RFC 7516); долгосрочно Microsoft планирует использовать PKCS#11 CKM_RSA_AES_KEY_WRAP, при котором эфемерный AES-ключ обрабатывается двумя HSM.
- Лучшие практики: максимальный размер KEK; только операция import; HSM уровня FIPS 140-2 Level 2 или выше; защищать файл `.byok`; документировать импорт; тестировать процесс на тестовых ключах; планировать ротацию (ключи нельзя экспортировать из Key Vault, но можно импортировать новые версии); для строгих требований - Managed HSM; RBAC с разделением прав на создание KEK и импорт; аудит через Azure Monitor или SIEM; проверить поддержку BYOK-инструмента производителем.

### 11. Двойное шифрование (infrastructure encryption)
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/11-enable-infrastructure-encryption-double-encryption-data

- Azure Storage по умолчанию шифрует все данные учетной записи 256-битным AES (FIPS 140-2). Infrastructure encryption добавляет второй слой 256-битного AES на уровне инфраструктуры с другим алгоритмом и другим ключом.
- Может быть включен для всей учетной записи или для области шифрования (encryption scope). На уровне сервиса используются ключи Microsoft или собственные ключи в Key Vault / Managed HSM; infrastructure encryption всегда использует отдельный ключ Microsoft.
- Включается только при создании учетной записи (general-purpose v2 или premium block blob) и не отключается после создания. Для области шифрования - при ее создании, если на учетной записи не включено.
- Создание в портале: Storage accounts - Add - вкладка Encryption - Enable infrastructure encryption - Enabled - Review + create. Проверка: учетная запись - Settings - Encryption.
- Azure Policy содержит встроенное определение, требующее infrastructure encryption для учетных записей.
- Рекомендации: включать при требованиях compliance (например, HIPAA, PCI-DSS, FedRAMP); учитывать необратимость решения; проверить производительность; сочетать с customer-managed keys; использовать encryption scopes для точечного применения; учитывать при DR, так как восстановленные учетные записи должны быть созданы с этой настройкой; регулярно проверять через Azure Monitor, Azure Security Center и Azure Policy; сочетать с сетевой защитой (private endpoints, firewalls), RBAC, SAS и Microsoft Defender for Storage.

### 12. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/12-knowledge-check

Итоговый тест модуля (10 минут). Содержимое вопросов в исходных материалах не приведено.

### 13. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/security-storage/13-summary

Модуль показал, как планировать и внедрять меры безопасности для Azure Storage по принципам Zero Trust и defense-in-depth: предпочитать Entra ID ключам и токенам, применять RBAC по сервисам, защищать данные (soft delete, версионирование, point-in-time restore, immutable storage), использовать BYOK и infrastructure encryption для требований соответствия. Ключевые принципы: Zero Trust, defense-in-depth, least privilege, разделение обязанностей (разные ключи на разных уровнях шифрования), готовность к соответствию требованиям.

## Важные команды / код / настройки

- Создание KEK для BYOK: `az keyvault key create --kty RSA-HSM --size 4096 --name KEKforBYOK --ops import --vault-name ContosoKeyVaultHSM`.
- Загрузка публичной части KEK: `az keyvault key download --name KEKforBYOK --vault-name ContosoKeyVaultHSM --file KEKforBYOK.publickey.pem`.
- Формат KEK: RSA-HSM, 4096 бит (рекомендуется), key_ops = import. Для Azure SQL поддерживаются 2 048 или 3 072 бит.
- Встроенная политика Azure Policy: "Storage account keys should not be expired" (ключи не просрочены); также политика, требующая infrastructure encryption.
- Роли Azure RBAC для данных: Storage Blob Data Owner / Contributor / Reader / Delegator; Storage Queue Data Contributor / Reader / Message Processor / Message Sender; Storage Table Data Contributor / Reader; Storage File Data Privileged Reader / Contributor.
- Действия ARM для ключей: `Microsoft.Storage/storageAccounts/listkeys/action` (просмотр ключей), `Microsoft.Storage/storageAccounts/regeneratekey/action` (регенерация).
- Действия ARM для Azure Files: `Microsoft.Storage/storageAccounts/fileServices/readFileBackupSemantics/action`, `Microsoft.Storage/storageAccounts/fileServices/writeFileBackupSemantics/action`.
- Ресурсы для Entra-авторизации: `https://<account-name>.blob.core.windows.net`, `https://<account-name>.queue.core.windows.net`, общий `https://storage.azure.com`.
- Минимальный срок soft delete для контейнеров и blob: 7 дней.
- Infrastructure encryption: настройка в Storage accounts - Add - вкладка Encryption - Enable infrastructure encryption; проверка Settings - Encryption.
- Опция портала: Default to Microsoft Entra authorization in the Azure portal (Advanced - Security или Settings - Configuration).
- Порядок предпочтения авторизации: managed identities в Entra ID; service principals в Entra ID; user delegation SAS; Shared Key только как крайний вариант.

## Что запомнить

- Для Blob, Queue, Table и Azure Files предпочитайте Microsoft Entra ID с RBAC и managed identities вместо ключей учетной записи.
- Ключи доступа дают полный доступ: храните в Key Vault, ротируйте по очереди key1 и key2, включайте напоминания и политику Azure Policy.
- Регенерация ключа отзывает account и service SAS; user delegation SAS на ключ не опирается.
- Защита данных: soft delete (минимум 7 дней), blob versioning, point-in-time restore и immutable storage комбинируйте для защиты от удаления, порчи и вымогательства.
- BYOK: KEK RSA-HSM 4096 бит с operation import, импорт `.byok` blob через CLI или PowerShell, инструмент производителя HSM.
- Infrastructure encryption (двойное шифрование) задается при создании учетной записи и необратимо; для точечного применения используйте encryption scopes.

## Связанные материалы

В исходных материалах модуля раздел со ссылками на дополнительные ресурсы не приведен.
