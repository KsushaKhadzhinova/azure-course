# Описание сервисов хранения Azure

**Источник:** https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/

## Цель модуля

Научиться сравнивать сервисы Azure Storage, понимать типы учетных записей хранения, уровни доступа Blob, варианты избыточности и способы переноса данных в Azure и внутри него (AzCopy, Azure Storage Explorer, Azure File Sync, Azure Migrate, Azure Data Box).

## Ключевые понятия

- **Storage account (учетная запись хранения)** - уникальное пространство имен для данных Azure Storage, доступное по HTTP/HTTPS.
- **Azure Blobs** - объектное хранилище для текстовых и бинарных данных; включает Data Lake Storage Gen2 для аналитики.
- **Azure Files** - управляемые файловые ресурсы (SMB и NFS), которые можно монтировать из облака и локальной среды.
- **Azure Queues** - хранилище сообщений для асинхронного взаимодействия компонентов; сообщения до 64 KB.
- **Azure Disks** - блочные тома для виртуальных машин Azure (managed disks).
- **Azure Tables** - NoSQL-хранилище для структурированных нереляционных данных.
- **Access tiers (уровни доступа)** - Hot, Cool, Cold, Archive; различаются стоимостью хранения, стоимостью доступа и задержкой.
- **LRS (Locally redundant storage)** - три копии в одном дата-центре региона primary; самый дешевый вариант.
- **ZRS (Zone-redundant storage)** - синхронная репликация в трех зонах доступности primary-региона.
- **GRS / GZRS** - гео-избыточность: копии в парном вторичном регионе (GRS: LRS в обоих регионах; GZRS: ZRS в primary и LRS в secondary).
- **RA-GRS / RA-GZRS** - варианты с возможностью читать данные из вторичного региона до failover.
- **RPO (Recovery Point Objective)** - интервал между последней записью в primary-регион и последней записью в secondary; данные в secondary могут быть не самыми свежими.
- **AzCopy** - утилита командной строки для копирования и синхронизации blob и файлов (синхронизация односторонняя).
- **Azure Storage Explorer** - графическое приложение для управления данными Azure Storage; использует AzCopy внутри.
- **Azure File Sync** - двусторонняя синхронизация файловых серверов Windows с Azure Files, с облачным тирингом.
- **Azure Migrate** - хаб для оценки и миграции локальной инфраструктуры, приложений и данных в Azure.
- **Azure Data Box** - физическое устройство для переноса больших объемов данных (до 80 TB полезной емкости).

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/1-introduction

Модуль знакомит с сервисами Azure Storage, учетными записями хранения, уровнями blob, вариантами избыточности и способами переноса данных. Цели: сравнивать сервисы, описывать уровни хранения и избыточность, типы учетных записей, инструменты перемещения файлов (AzCopy, Storage Explorer, File Sync) и варианты миграции (Azure Migrate, Azure Data Box).

### 2. Учетные записи хранения
Источник: https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/2-accounts

- Тип учетной записи определяет доступные сервисы, варианты избыточности и сценарии использования.
- **Standard general-purpose v2** - стандартный тип для Blob (включая Data Lake Storage), Queue, Table и Azure Files; поддерживает все варианты избыточности. Рекомендуется для большинства сценариев. Для NFS в Azure Files нужен тип premium file shares.
- **Premium block blobs** - Blob Storage для block и append blobs (LRS, ZRS); для высокой частоты транзакций и низкой задержки.
- **Premium file shares** - только Azure Files (LRS, ZRS); поддерживает SMB и NFS.
- **Premium page blobs** - только page blobs (LRS).
- Имя учетной записи: 3-24 символа, только строчные буквы и цифры, уникальное в Azure.
- Эндпоинты: Blob `https://<account>.blob.core.windows.net`, Data Lake Storage Gen2 `https://<account>.dfs.core.windows.net`, Azure Files `https://<account>.file.core.windows.net`, Queue `https://<account>.queue.core.windows.net`, Table `https://<account>.table.core.windows.net`.

### 3. Избыточность хранилища
Источник: https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/3-redundancy

- В primary-регионе данные всегда реплицируются трижды; варианты: LRS и ZRS.
- **LRS** защищает от отказа стойки и дисков в одном дата-центре, дает не менее 11 девяток durability; при аварии всего дата-центра возможна потеря данных.
- **ZRS** синхронно реплицирует данные по трем зонам доступности (не менее 12 девяток durability); данные доступны при недоступности одной зоны. Рекомендуется для высокой доступности внутри региона.
- **GRS** - LRS в primary и асинхронная копия LRS во вторичном регионе; не менее 16 девяток durability.
- **GZRS** - ZRS в primary и LRS во вторичном регионе; рекомендуется для максимальной согласованности, доступности и аварийного восстановления; не менее 16 девяток durability.
- Вторичный регион назначается по парам регионов Azure. По умолчанию данные в нем не читаются до failover.
- Репликация в secondary асинхронная, поэтому при потере primary возможна потеря данных; интервал - RPO.
- **RA-GRS** и **RA-GZRS** позволяют читать данные из вторичного региона; при этом данные могут быть не самыми свежими из-за RPO.

### 4. Сервисы хранения Azure
Источник: https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/4-describe-azure-storage-services

- **Azure Blobs**: масштабируемое объектное хранилище для изображений, документов, медиа, логов, резервных копий и аналитики; доступ по URL, REST API, CLI, PowerShell и клиентским библиотекам (.NET, Java, Node.js, Python, PHP, Ruby).
- **Уровни доступа blob**: Hot (часто используемые данные), Cool (хранение не менее 30 дней), Cold (не менее 90 дней), Archive (не менее 180 дней, гибкая задержка). Hot, Cool и Cold можно задать на уровне учетной записи; Archive - только на уровне blob. Cool и Cold дешевле хранить, но дороже читать и ниже SLA доступности; Archive - самый дешевый для хранения и самый долгий и дорогой для извлечения (rehydration).
- **Azure Files**: полностью управляемые файловые ресурсы по SMB и NFS; SMB доступен из Windows, Linux и macOS, NFS - из Linux и macOS; управление через CLI, PowerShell, портал и Storage Explorer.
- **Azure Queues**: надежная обмен сообщениями между компонентами; до миллионов сообщений, размер до 64 KB; часто используется с Azure Functions.
- **Azure Disks**: блочные тома (managed disks) для виртуальных машин Azure.
- **Azure Tables**: NoSQL-хранилище структурированных нереляционных данных.
- Общие преимущества: надежность и высокая доступность, шифрование всех данных сервисом, масштабируемость, управляемость (Azure обслуживает оборудование) и доступность по HTTP/HTTPS.

### 5. Миграция данных в Azure
Источник: https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/6-identify-azure-data-migration-options

- **Azure Migrate** - хаб для оценки и миграции локального дата-центра в Azure: единый портал, инструменты Discovery and assessment и Server Migration, интеграция с миграцией баз данных, веб-приложений и продуктами ISV. Работает в реальном времени для инфраструктуры, приложений и данных.
- **Azure Data Box** - физическое устройство для асинхронной передачи больших объемов данных (до 80 TB полезной емкости). Заказывается в портале, доставляется региональным перевозчиком, настраивается через локальный веб-интерфейс; данные загружаются после получения Microsoft. Подходит, когда пропускной способности сети недостаточно (разовая миграция, периодическая загрузка, экспорт из Azure). После импорта диски стираются по стандарту NIST 800-88r1.

### 6. Инструменты перемещения файлов
Источник: https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/7-identify-azure-file-movement-options

- **AzCopy** - командная утилита для загрузки, скачивания, копирования между учетными записями и синхронизации; может работать с другими облаками. Синхронизация односторонняя: источник и назначение задаются явно, двусторонней синхронизации по временным меткам нет.
- **Azure Storage Explorer** - графическое приложение для Windows, macOS и Linux; для операций использует AzCopy.
- **Azure File Sync** - централизует файловые ресурсы в Azure Files, сохраняя работу с Windows Server; двусторонняя синхронизация, доступ по SMB, NFS и FTPS, несколько кэшей по миру, замена отказавшего сервера, облачный тиринг (часто используемые файлы хранятся локально, редкие - в облаке).

### 7. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/8-knowledge-check

Итоговый тест модуля (4 минуты) с выбором лучшего ответа. Содержимое вопросов в исходных материалах не приведено.

### 8. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/9-summary

Модуль охватил учетные записи хранения и их связь с сервисами, blob, варианты избыточности и способы миграции и перемещения данных.

## Важные команды / код / настройки

- Имя учетной записи: 3-24 символа, строчные буквы и цифры, уникальное в Azure.
- Эндпоинты: `https://<storage-account-name>.blob.core.windows.net`, `.dfs.core.windows.net`, `.file.core.windows.net`, `.queue.core.windows.net`, `.table.core.windows.net`.
- Варианты избыточности: LRS, GRS, RA-GRS, ZRS, GZRS, RA-GZRS.
- Минимальный срок хранения для уровней blob: Cool - 30 дней, Cold - 90 дней, Archive - 180 дней.
- Типы учетных записей: Standard general-purpose v2; Premium block blobs (LRS, ZRS); Premium file shares (LRS, ZRS); Premium page blobs (LRS).
- Инструменты: AzCopy (CLI), Azure Storage Explorer (GUI), Azure File Sync (двусторонняя синхронизация Windows Server с Azure Files), Azure Migrate, Azure Data Box (до 80 TB).

## Что запомнить

- Учетная запись хранения определяет доступные сервисы и варианты избыточности; для большинства сценариев рекомендуется Standard general-purpose v2.
- LRS - самый дешевый вариант, но не защищает от отказа дата-центра; ZRS защищает от отказа зоны, GRS и GZRS - от отказа региона.
- RPO означает, что вторичный регион может отставать; RA-GRS и RA-GZRS позволяют читать его, но данные могут быть не самыми свежими.
- Уровни blob: Hot для частого доступа, Cool и Cold для редкого (с минимальным сроком хранения), Archive для долгосрочного архива.
- Для переноса: Azure Migrate - для миграции инфраструктуры, Data Box - для больших объемов при ограниченной сети, AzCopy и Storage Explorer - для отдельных файлов, Azure File Sync - для централизации файловых серверов.

## Связанные материалы

- Store data in Azure (курс Microsoft Learn)
- Microsoft Certified: Azure Data Fundamentals (сертификация)
