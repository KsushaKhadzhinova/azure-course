# Настройка Azure Files и Azure File Sync

**Источник:** https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/

## Цель модуля

Научиться выбирать хранилище для файловых шар, сравнивать Azure Files с Blob Storage, настраивать файловые шары, снапшоты и soft delete, работать с Azure Storage Explorer и понимать, как Azure File Sync кэширует шары на локальных Windows Server. Модуль готовит к экзамену AZ-104.

## Ключевые понятия

- **Azure Files** - полностью управляемые файловые шары в облаке, доступные по протоколам SMB, NFS и REST.
- **Azure File Sync** - сервис, который кэширует несколько шар Azure Files на локальном Windows Server или в облачной VM.
- **Storage Sync Service** - основной ресурс Azure, который управляет синхронизацией; работает в одном регионе.
- **Sync group (группа синхронизации)** - связка одной cloud endpoint и нескольких server endpoints.
- **Cloud endpoint** - Azure file share, участвующая в синхронизации (только одна на группу).
- **Server endpoint** - путь NTFS на зарегистрированном Windows Server (не системный том).
- **Azure File Sync Agent** - фоновая служба Windows на каждом сервере для синхронизации.
- **Cloud tiering (многоуровневое хранение)** - на сервере хранятся только недавно используемые данные, старые переносятся в Azure Files.
- **File share snapshot (снапшот шары)** - инкрементальная, доступная только для чтения копия шары на момент времени.
- **Soft delete (обратимое удаление)** - удаленные файлы и шары сохраняются и могут быть восстановлены в течение срока хранения.
- **Azure Storage Explorer** - standalone-приложение для работы с данными Azure Storage на Windows, macOS и Linux.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/1-introduction

Azure Files предоставляет полностью управляемые файловые шары; Azure File Sync кэширует их на Windows Server. Сценарий: организации с офисами в разных регионах нужен центральный репозиторий документов с актуальными версиями. Цели: выбор хранилища для шар, сравнение с blob, настройка шар, снапшотов и soft delete, работа с Storage Explorer.

### 2. Compare storage for file shares and blob data
https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/2-compare-files-to-blobs

Azure Files - бессерверная PaaS-шара с иерархией папок, шифрованием, доступом из любой точки и интеграцией с Microsoft Entra или AD DS identities. Одна шара вмещает до 100 TiB, размер файла до 4 TiB. Blob Storage - плоское пространство имен, доступ через контейнеры, подходит для стриминга и произвольного доступа. Azure Files подходит для lift-and-shift приложений, которые используют файловый API.

### 3. Manage Azure file shares
https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/3-manage-file-shares

Шара не поддерживает SMB и NFS одновременно, но в одном аккаунте можно создать шары обоих типов. Уровни: Premium (SSD, provisioned, аккаунт FileStorage), Transaction Optimized, Hot и Cool (HDD, pay-as-you-go, GPv2). Способы аутентификации: identity-based через SMB (AD DS, Microsoft Entra Domain Services, Microsoft Entra Kerberos), access key (полный доступ, избегать использования), SAS-токен (для REST-доступа из кода). Для SMB важен порт 445.

### 4. Create file share snapshots
https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/4-create-file-share-snapshots

Снапшоты - инкрементальные, только для чтения, с уникальной меткой времени в URI. До 200 снапшотов на шару. Сохраняются до удаления, удаление шары удаляет и все снапшоты. Azure Backup может закрепить снапшоты от случайного удаления. Полное восстановление требует только последнего снапшота. Снапшоты создаются через PowerShell или Azure CLI, в том числе по расписанию.

### 5. Implement soft delete for Azure Files
https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/5-implement-file-sync

Soft delete включается на уровне storage account и может быть включен для новых или существующих шар. Срок хранения удаленных данных задается от 1 до 365 дней. Применение: восстановление после случайного удаления, откат после неудачного обновления, защита от программ-вымогателей (ransomware), соответствие требованиям хранения, непрерывность бизнеса.

### 6. Use Azure Storage Explorer
https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/6-identify-components

Storage Explorer требует разрешений Azure Resource Manager (управление) и разрешений на уровне данных (Microsoft Entra ID). Подключение возможно к аккаунтам подписки, к общим аккаунтам из других подписок, к Azure Storage Emulator, а также по имени аккаунта и ключу, либо через SAS. Ключи доступа дают доступ ко всему аккаунту, поэтому их нужно хранить безопасно и регулярно перегенерировать.

### 7. Consider Azure File Sync
https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/7-deploy-azure-file-sync

Azure File Sync состоит из пяти компонентов: Storage Sync Service, sync group, cloud endpoint, server endpoint и Azure File Sync Agent. Лимиты: до 100 sync groups на Storage Sync Service, до 99 зарегистрированных серверов, до 50 server endpoints на sync group. Поддерживаются SMB, NFS и FTPS на локальном сервере. Cloud tiering хранит на сервере только часто используемые данные; Azure Backup защищает локальные данные.

### 8. Module assessment
https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/8-knowledge-check

Проверка знаний (около 3 минут). Сценарий: склад с ограниченной пропускной способностью и ПО, которое работает на локальных машинах; предложены cloud tiering, soft delete и снапшоты. Варианты ответов в источнике не приведены.

### 9. Summary and resources
https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/9-summary-resources

Azure Files поддерживает SMB, NFS, client libraries и REST; подходит для lift-and-shift. Есть standard (HDD) и premium (SSD) шары. Снапшоты дают точечные копии; soft delete позволяет восстановить удаленную шару; Storage Explorer - standalone приложение; Azure File Sync кэширует шары на Windows Server. Для изучения рекомендуются документация Azure Files и Azure File Sync, модули по гибридному файловому серверу и проект Azure Files и Azure Blobs.

## Важные команды / код / настройки

В источнике команд и кода нет. Ниже лимиты, уровни и параметры из текста:

**Azure Files:**
- Одна шара: до 100 TiB; файл: до 4 TiB.
- Уровни: Premium (SSD, provisioned billing, аккаунт FileStorage, LRS или ZRS); Transaction Optimized, Hot, Cool (HDD, pay-as-you-go, GPv2, все варианты избыточности из списка LRS, GRS, RA-GRS, ZRS, GZRS, RA-GZRS).
- Порт SMB: 445.
- Одна шара не поддерживает SMB и NFS одновременно.

**Снапшоты шар:**
- До 200 снапшотов на шару.
- Полное восстановление требует только последнего снапшота.

**Soft delete:**
- Включается на уровне storage account.
- Срок хранения: от 1 до 365 дней.

**Azure File Sync:**
- Storage Sync Service: до 100 sync groups, до 99 зарегистрированных серверов, один регион.
- Sync group: одна cloud endpoint, до 50 server endpoints.
- Server endpoint: путь NTFS, не на системном томе; cloud tiering на нем не поддерживается.
- Ограничение: 100 sync groups на Storage Sync Service, 50 server endpoints на sync group.

**Storage Explorer - параметры подключения:** имя аккаунта и ключ доступа (в портале называется key1), либо custom endpoint domain для национальных облаков (выбрать Other в Storage endpoints domain).

## Что запомнить

- Azure Files дает SMB/NFS-шары в облаке, Blob Storage - объектное хранилище с плоским пространством имен.
- Выбирайте identity-based аутентификацию через Microsoft Entra или AD DS; ключи доступа обходят все ограничения и их лучше не раздавать.
- Снапшоты защищают от ошибок приложения и случайного удаления; soft delete сохраняет удаленное на срок от 1 до 365 дней.
- Azure File Sync кэширует шары на Windows Server и поддерживает многоуровневое хранение (cloud tiering) для экономии места.
- Лимиты File Sync: 100 sync groups на сервис, 50 server endpoints на группу, одна cloud endpoint на группу.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/
- В источнике упоминаются (без ссылок в тексте): Azure Files documentation; Azure File Sync documentation; модуль Implement a hybrid file server infrastructure (Azure File Sync и Storage Migration Service); Guided Project - Azure Files and Azure Blobs; Exam AZ-104.
