# Знакомство с нереляционными службами данных Azure: Storage и Data Lake

**Источник:** https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-non-relational-data-services-azure/

## Цель модуля

Изучить базовые возможности Azure Storage и Microsoft OneLake для приложений с нереляционными (NoSQL) хранилищами: Blob Storage, Data Lake Storage Gen2, Azure Files и Azure Tables, а также научиться создавать и использовать учетную запись хранения (storage account).

## Ключевые понятия

- **Blob storage (Blob Storage)** - хранение больших объемов неструктурированных данных в виде blob-объектов; blob хранится в контейнере внутри storage account.
- **Block / Page / Append blob** - три типа blob: блочные (для дискретных объектов), страничные (случайный доступ, виртуальные диски VM) и добавляемые (только добавление блоков).
- **Access tiers (уровни доступа)** - Hot, Cool, Cold и Archive: баланс между задержкой доступа и стоимостью хранения.
- **Lifecycle management policy** - политика, которая переводит blob между уровнями по возрасту и может удалять устаревшие blob.
- **Redundancy (избыточность)** - LRS, ZRS, GRS, GZRS, RA-GRS и RA-GZRS: защита данных внутри датацентра, между зонами и между регионами.
- **Azure Data Lake Storage Gen2** - озеро данных на базе Azure Storage с иерархическим пространством имен (hierarchical namespace) и POSIX-ACL.
- **Hierarchical namespace (иерархическое пространство имен)** - включается при создании аккаунта или обновлении; обновление необратимо.
- **Microsoft OneLake** - хранилище, которое автоматически создается для тенантов Microsoft Fabric и построено на Azure Data Lake Storage Gen2 (упоминается в источнике).
- **Azure Files** - облачные сетевые файловые ресурсы (SMB и NFS).
- **Azure Table Storage** - NoSQL-хранилище ключ-значение с PartitionKey и RowKey; таблицы не имеют внешних ключей и связей.
- **Azure Cosmos DB for Table** - более новый сервис с той же моделью ключ-значение, упомянутый в источнике.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-non-relational-data-services-azure/1-introduction

Многим приложениям не нужна жесткая структура реляционной БД, и они используют нереляционное хранение. Azure Storage и Microsoft OneLake предлагают варианты хранения данных в облаке.

### 2. Explore Azure blob storage
https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-non-relational-data-services-azure/2-azure-blob-storage

Blob-объекты хранятся в контейнерах. Рекомендуемый способ входа - Microsoft Entra ID с RBAC. "Папки" в контейнере виртуальные: это лишь разделители "/" в именах blob. Описаны три типа blob, четыре уровня доступа с минимальными сроками хранения, lifecycle management и варианты избыточности.

### 3. Explore Azure Data Lake Storage Gen2
https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-non-relational-data-services-azure/3-azure-data-lake-gen2

Data Lake Gen2 сочетает масштабируемость Blob Storage с иерархической файловой системой, совместимой с аналитическими системами (например, Azure Databricks). Иерархическое пространство имен дает POSIX-ACL на уровне файлов и папок. Включить его можно при создании аккаунта или обновить существующий, но обновление необратимо.

### 4. Explore Azure Files
https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-non-relational-data-services-azure/4-azure-files

Azure Files - облачные сетевые папки, которые заменяют файловые серверы on-premises. Файлы загружаются через портал, AzCopy или синхронизируются через Azure File Sync. Доступны HDD- и SSD-уровни и протоколы SMB (Windows, Linux, macOS) и NFS (только Linux-клиенты, требует SSD и доступа через private endpoint или service endpoint).

### 5. Explore Azure Tables
https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-non-relational-data-services-azure/5-azure-tables

Azure Table Storage хранит полуструктурированные данные: каждая строка имеет уникальный ключ из PartitionKey и RowKey, а столбцы у строк могут отличаться. Данные обычно денормализуют. Партиции независимы и масштабируются; поиск с указанием partition key быстрее. Внутри партиции строки упорядочены по RowKey, что дает быстрые точечные и диапазонные запросы.

### 6. Exercise: Explore Azure Storage
https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-non-relational-data-services-azure/6-exercise-azure-storage

Практическое задание (около 15 минут) по Azure Storage. Нужна подписка Azure с правами администратора.

### 7. Module assessment
https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-non-relational-data-services-azure/7-knowledge-check

Итоговая проверка (около 3 минут). Текст вопросов в источнике не приведен.

### 8. Summary
https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-non-relational-data-services-azure/8-summary

Модуль охватил возможности Blob, Data Lake Gen2, OneLake, Azure Files и Azure Table storage, а также создание и использование storage account. Для дальнейшего изучения источник рекомендует сертификацию Azure Data Fundamentals.

## Важные команды / код / настройки

В источнике команд и кода нет. Ниже приведены параметры и ограничения из текста:

**Blob Storage:**
- Блочный blob: блок до 4000 MiB, до 50 000 блоков, максимум 190,7 TiB.
- Страничный blob: страницы по 512 байт, максимум 8 TiB.
- Добавляемый blob: блок до 4 MiB, максимум чуть больше 195 GiB.
- Hot - по умолчанию; Cool - минимум 30 дней; Cold - минимум 90 дней; Archive - минимум 180 дней. Чтение из Archive может занимать до 15 часов (нужна регидратация).
- Lifecycle management: переход по дням с момента изменения (Hot -> Cool -> Cold -> Archive) и удаление устаревших blob.

**Избыточность:**
- LRS - 3 копии в одном датацентре.
- ZRS - 3 копии в трех зонах доступности основного региона.
- GRS и GZRS - асинхронная репликация во вторичный регион.
- RA-GRS и RA-GZRS - чтение из вторичного региона без failover.

**Azure Files:**
- До 256 TiB в одном аккаунте для SSD с моделью provisioned v2; до 5 PiB для HDD с оплатой по факту.
- Максимальный размер одного файла 4 TiB; квоты могут ограничивать шару.
- До 2000 одновременных handle на файл или каталог.
- NFS-шары: только SSD-уровень, доступ через private endpoint или service endpoint в виртуальной сети; на Windows не поддерживаются.

## Что запомнить

- Blob Storage хранит неструктурированные данные в контейнерах; "папки" в нем виртуальные.
- Уровни Hot/Cool/Cold/Archive имеют минимальные сроки хранения (30/90/180 дней) и штрафы за досрочное удаление.
- Иерархическое пространство имен превращает Blob в Data Lake Gen2 и дает POSIX-ACL; обратно включить его нельзя.
- Azure Files дает сетевые папки в облаке по протоколам SMB и NFS; NFS требует SSD и приватного доступа.
- Azure Table Storage - нереляционное хранилище ключ-значение: ключ = PartitionKey + RowKey, связей и внешних ключей нет.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-non-relational-data-services-azure/
- В источнике упоминаются (без ссылок в тексте): сертификация Azure Data Fundamentals; Azure Cosmos DB for Table; Microsoft OneLake; Azure File Sync; AzCopy.
