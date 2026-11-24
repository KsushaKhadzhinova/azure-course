# Настройка учетных записей хранения Azure (Storage accounts)

**Источник:** https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/

## Цель модуля

Научиться настраивать учетные записи хранения (storage accounts) и выбирать подходящий тип хранилища: понимать возможности и сценарии использования Azure Storage, создавать storage account, выбирать стратегию репликации и настраивать безопасный сетевой доступ к конечным точкам (endpoints). Модуль готовит к экзамену AZ-104.

## Ключевые понятия

- **Azure Storage** - облачное хранилище: объектное (Blob), файловое (Files), очереди (Queue), таблицы (Table). Данные шифруются.
- **Storage account (учетная запись хранения)** - контейнер для сервисов хранения; определяет тип аккаунта, избыточность и настройки доступа.
- **Standard и Premium** - два базовых типа general-purpose аккаунтов: Standard на HDD (дешевле за ГБ), Premium на SSD (стабильно низкая задержка). Конвертировать нельзя, нужно создать новый аккаунт и перенести данные.
- **General-purpose v2 (GPv2)** - рекомендуемый тип для большинства сценариев; поддерживает Blob, Queue, Table и Files. Legacy GPv1 и BlobStorage рекомендуется обновить до GPv2.
- **Hierarchical namespace (HNS)** - включает Data Lake Storage Gen2 и требуется для SFTP.
- **Replication (репликация)** - LRS, ZRS, GRS, RA-GRS, GZRS, RA-GZRS: защита от отказов оборудования, зон, регионов.
- **Endpoint (конечная точка)** - базовый URL сервиса, например `mystorageaccount.blob.core.windows.net`.
- **Custom domain (пользовательский домен)** - сопоставление собственного домена через CNAME.
- **Service endpoint** - сохраняет публичную конечную точку, но ограничивает доступ конкретными VNet и подсетями.
- **Private endpoint** - приватный IP из VNet для storage account; трафик идет по магистрали Microsoft.
- **Storage Service Encryption (SSE)** - шифрование всех данных в покое.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/1-introduction

Сценарий: крупной e-commerce компании нужно хранить и отдавать множество изображений товаров с высокой масштабируемостью и надежностью, а также быстро восстанавливать данные после сбоя. Цели модуля: сценарии использования, выбор типа хранения и создание аккаунта, стратегия репликации, безопасный сетевой доступ.

### 2. Implement Azure Storage
https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/2-implement-azure-storage

Данные делятся на три категории: данные виртуальных машин (managed disks и файлы), неструктурированные (Blob и Data Lake) и структурированные (Table, Cosmos DB, Azure SQL Database). Перечислены преимущества: долговечность и доступность, шифрование и гранулярный доступ, масштабируемость, управляемость, доступ по HTTP/HTTPS через SDK, CLI и PowerShell. Также упомянуты SFTP и NFSv3 для Blob и выбор авторизации через Microsoft Entra ID (RBAC) вместо ключей доступа.

### 3. Explore Azure Storage services
https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/3-explore-azure-storage-services

Blob Storage - объектное хранилище для больших объемов неструктурированных данных (раздача изображений, стриминг, резервное копирование). Azure Files - сетевые файловые шары по SMB и NFS. Queue Storage - очереди сообщений до 64 КБ для асинхронной обработки (пример: миниатюры изображений через Azure Functions). Table Storage - схемно-свободное NoSQL-хранилище; упомянут Azure Cosmos DB Table API.

### 4. Determine storage account types
https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/4-determine-storage-account-kinds

Standard (HDD) - минимальная стоимость за ГБ; Premium (SSD) - низкая задержка для дисков VM и нагрузок вроде баз данных. Варианты: Standard general-purpose v2, Premium block blobs, Premium file shares, Premium page blobs. Для уже существующих legacy-аккаунтов рекомендуется обновление до GPv2 (через портал, CLI или PowerShell).

### 5. Determine replication strategies
https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/5-determine-replication-strategies

LRS - самый дешевый и наименее надежный вариант (3 копии в одном датацентре). ZRS - синхронно в трех зонах доступности одного региона. GRS - асинхронно во вторичный регион; RA-GRS дает чтение из вторичного региона. GZRS сочетает ZRS и GRS, RA-GZRS добавляет чтение из вторичного региона. Microsoft рекомендует GZRS для требовательных приложений, а RA-GZRS - для чтения из вторичного региона при региональной аварии.

### 6. Access storage
https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/6-access-storage

Имя аккаунта формирует поддомен endpoint. Пример: объект `myblob` в контейнере `mycontainer` доступен по адресу `mystorageaccount.blob.core.windows.net/mycontainer/myblob`. Пользовательский домен настраивается через CNAME (например, `blobs.contoso.com` указывает на `contosoblobs.blob.core.windows.net`).

### 7. Secure storage endpoints
https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/7-secure-storage-endpoints

Настройки сетевого доступа находятся в разделе Firewalls and virtual networks. Можно разрешить публичные IP-диапазоны и подсети. Подсети и VNet должны находиться в том же регионе или регионе-паре, что и аккаунт. Service endpoints подходят для разработки; private endpoints - для production с полной изоляцией. Рекомендуется проверять ограничения доступа после настройки.

### 8. Module assessment
https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/8-knowledge-check

Проверка знаний (около 3 минут). Вопросы-сценарии: настройка безопасного доступа, стратегия репликации, выбор самого дешевого решения для временных данных сенсоров. Варианты ответов в источнике не приведены.

### 9. Summary and resources
https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/9-summary-resources

Azure Storage предлагает четыре сервиса данных: Blob, Files, Queue и Table. Выбор типа аккаунта и стратегии репликации зависит от требований приложения. Для дальнейшего изучения рекомендуются обзор storage account, статья о избыточности и модули по созданию аккаунта и приватному доступу.

## Важные команды / код / настройки

В источнике команд и кода нет. Ниже настройки и значения, которые приведены в тексте:

**Формат endpoint:**
- Blob: `<storage-account>.blob.core.windows.net`
- Table: `<storage-account>.table.core.windows.net`
- Queue: `<storage-account>.queue.core.windows.net`
- File: `<storage-account>.file.core.windows.net`

**Типы аккаунтов и избыточность (из таблицы источника):**

| Тип аккаунта | Сервисы | Варианты избыточности |
|---|---|---|
| Standard general-purpose v2 | Blob (включая Data Lake), Queue, Table, Azure Files | LRS, GRS, RA-GRS, ZRS, GZRS, RA-GZRS |
| Premium block blobs | Blob (включая Data Lake) | LRS, ZRS |
| Premium file shares | Azure Files (SMB и NFS) | LRS, ZRS |
| Premium page blobs | Только page blobs | только LRS |

**Гарантии долговечности из источника:** GRS и GZRS - не менее 99,99999999999999% (16 девяток).

**Настройки сетевого доступа:** Firewalls and virtual networks; разрешенные публичные IP-диапазоны; подсети и VNet в том же регионе или регионе-паре; private endpoint vs service endpoint.

**CNAME для пользовательского домена (пример):** `blobs.contoso.com` -> `contosoblobs.blob.core.windows.net`.

**Протоколы и порты:** SFTP для Blob требует включенного hierarchical namespace; NFSv3 позволяет Linux монтировать контейнер. SMB использует порт 445 (в источнике модуля Azure Files указано, что исходящий 445 часто блокируется провайдерами).

## Что запомнить

- Тип аккаунта (Standard или Premium) нельзя поменять после создания: переносится только через новый аккаунт и копирование данных.
- Рекомендуемый тип для большинства сценариев - General-purpose v2.
- Для защиты от сбоя зоны используйте ZRS или GZRS; для защиты от сбоя региона - GRS или GZRS.
- Для чтения из вторичного региона без failover выбирайте RA-GRS или RA-GZRS.
- Для production с полной сетевой изоляцией используйте private endpoints; service endpoints подходят для разработки и простых сценариев.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/
- В источнике упоминаются (без ссылок в тексте): Storage account overview; Azure storage redundancy; модуль Create an Azure storage account; модуль Design and implement private access to Azure Services (Azure Private Link и virtual network service endpoints); Exam AZ-104.
