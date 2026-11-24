# Миграция SQL-нагрузок в Azure SQL Database

**Источник:** https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/

## Цель модуля

Научиться планировать и выполнять миграцию баз данных SQL Server в Azure SQL Database: выбрать возможности целевой базы, выбрать офлайн- или онлайн-метод миграции (Azure Database Migration Service, BACPAC, транзакционная репликация, bcp, Azure Data Factory), контролировать производительность и подключения.

## Ключевые понятия

- **Azure SQL Database** - PaaS-движок БД; подходит для нагрузок с непредсказуемым использованием, новых БД без истории и сценариев, где не нужны SQL Agent и instance-уровень.
- **Офлайн-миграция (offline)** - миграция с простоем БД.
- **Онлайн-миграция (online)** - миграция с минимальным или нулевым простоем; в источнике единственный онлайн-метод - транзакционная репликация.
- **Azure Database Migration Service (DMS)** - управляемый сервис миграции; рекомендуется для крупных миграций. Работает через self-hosted integration runtime.
- **BACPAC** - сжатый файл с метаданными и данными БД для импорта и экспорта.
- **SqlPackage** - утилита для импорта и экспорта BACPAC; параллельные вызовы ускоряют работу.
- **Transactional replication (транзакционная репликация)** - публикатор (Publisher), подписчик (Subscriber), дистрибьютор (Distributor), статья (Article), публикация (Publication) и подписка (Subscription).
- **bcp** - утилита массового экспорта и импорта данных таблиц.
- **Azure Data Factory** - перенос и преобразование данных (чаще для BI), а не всей БД целиком.
- **Elastic query / elastic jobs** - возможности Azure SQL Database: межбазовые запросы и замена SQL Server Agent.
- **Transient errors (временные ошибки)** - нужно повторять подключение с экспоненциальной задержкой.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/1-introduction

Azure SQL Database - PaaS, миграция на него снимает зависимость от компонентов уровня instance (например, SQL Agent jobs). Сценарий: компания производит велосипеды и запчасти; нужно перенести базы продуктов, складских запасов и HR. Перечислены ситуации, когда лучше Azure SQL Database, а не Managed Instance. Рекомендуется сначала изучить оценку миграции (Assess SQL Server databases for migration to Azure SQL).

### 2. Choose the right Azure SQL Database feature
https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/2-choose-right-sql-database-option-azure

Описаны преимущества: автоматические бэкапы, point-in-time restore, долгосрочное хранение бэкапов до 10 лет, гарантия доступности 99,99%, геовосстановление, active geo-replication, масштабирование, elastic pools, Microsoft Entra, TDE по умолчанию, маскирование и Always Encrypted, модели DTU и vCore (с Azure Hybrid Benefit экономия до 30%). Эксклюзивные функции: Hyperscale, auto-scale в serverless, автонастройка индексов, elastic query, elastic jobs, Query Performance Insights. Таблица инструментов и режимов миграции, рекомендации по производительности и повторным попыткам подключения.

### 3. Use Azure Database Migration Service to migrate to Azure SQL Database
https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/3-migrate-using-azure-migration-extension

Офлайн-миграция через DMS с Azure CLI (расширение datamigration) или PowerShell. Порядок: создать сервис миграции, перенести схему, создать миграцию данных (можно выбрать конкретные таблицы), следить за статусом, при необходимости отменить. Статусы: Preparing for copy, Copying, Copy finished, Rebuilding indexes, Succeeded. Указаны ограничения производительности: масштабировать целевую БД заранее, до 10 параллельных миграций на один self-hosted integration runtime, таблицы с большими blob-колонками могут не мигрировать из-за таймаута.

### 4. Не входит в набор источника
Юнит с номером 4 в собранных материалах отсутствует (в индексе источника нет этой страницы), поэтому здесь он не описан.

### 5. Migrate to Azure SQL Database using BACPAC
https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/5-migrate-using-bacpac

Импорт из файла .bacpac (из Blob Storage или локально). Через портал: Import database, выбор storage account и контейнера, размер БД, учетные данные, отслеживание в Import/Export history. Через SqlPackage быстрее. Для ускорения можно временно поднять уровень сервиса, а после импорта понизить.

### 6. Use an online method to migrate to Azure SQL Database
https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/6-migrate-sql-server-azure-sql-database-online

Транзакционная репликация переносит данные почти в реальном времени после начального снимка. Azure SQL Database выступает push-подписчиком. Настраивается через SSMS или T-SQL на публикаторе, но не через портал. Пример переноса таблицы `[Person].[Person]` из AdventureWorks. Управление и мониторинг репликации выполняются со стороны SQL Server, а не из Azure SQL Database. Для подключения через репликацию нужны логины SQL-аутентификации.

### 7. Move data to Azure SQL Database
https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/7-move-data-sql-database

Частичная миграция: нужны только некоторые таблицы (например, клиенты и продукты, а продажи остаются on-premises). Инструменты: утилита bcp (массовый экспорт и импорт в файлы, нужно знать схему и типы данных, если нет файла формата) и Azure Data Factory (перенос и преобразование данных, чаще для BI).

### 8. Exercise - Migrate a SQL Server database to Azure SQL Database
https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/8-exercise-migrate-sql-database

Практическое задание (около 30 минут). Нужна подписка Azure.

### 9. Module assessment
https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/9-knowledge-check

Проверка знаний (около 8 минут). Текст вопросов в источнике не приведен.

### 10. Summary
https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/10-summary

В сценарии миграция выполнена офлайн и онлайн. Выбор метода зависит от допустимого времени простоя. Дополнительно рекомендуются обзор миграции SQL Server в Azure SQL Database, Azure Database Migration Service и статья о транзакционной репликации.

## Важные команды / код / настройки

**Установка расширения и создание сервиса миграции (Azure CLI):**
```
az extension add --name datamigration
```
```
az datamigration sql-service create \
    --resource-group "<YourResourceGroup>" \
    --sql-migration-service-name "<YourMigrationService>" \
    --location "<YourLocation>"
```

**Миграция схемы:**
```
az datamigration sql-server-schema \
    --action "MigrateSchema" \
    --src-sql-connection-str "Server=<YourSourceServer>;Initial Catalog=<YourSourceDB>;User ID=<YourSourceUser>;Password=<YourSourcePassword>" \
    --tgt-sql-connection-str "Server=<YourTargetServer>.database.windows.net;Initial Catalog=<YourTargetDB>;User ID=<YourTargetUser>;Password=<YourTargetPassword>"
```

**Создание миграции данных (ключевые параметры; полный вызов с параметрами `--source-sql-connection`, `--target-sql-connection`, `--scope`, `--migration-service` приведен в источнике):**
```
az datamigration sql-db create \
    --resource-group "<YourResourceGroup>" \
    --sqldb-instance-name "<YourTargetServer>" \
    --target-db-name "<YourTargetDB>" \
    --source-database-name "<YourSourceDB>" \
    ...
```
Для выборки таблиц добавляется параметр `--table-list "[Person].[Person]" "[Person].[EmailAddress]" "[Sales].[Customer]"`. Пустые таблицы DMS пропускает даже если они выбраны.

**Мониторинг и управление:**
```
az datamigration sql-db show \
    --resource-group "<YourResourceGroup>" \
    --sqldb-instance-name "<YourTargetServer>" \
    --target-db-name "<YourTargetDB>" \
    --expand "MigrationStatusDetails"
```
```
az datamigration sql-db wait \
    --resource-group "<YourResourceGroup>" \
    --sqldb-instance-name "<YourTargetServer>" \
    --target-db-name "<YourTargetDB>" \
    --created
```
```
az datamigration sql-db cancel \
    --resource-group "<YourResourceGroup>" \
    --sqldb-instance-name "<YourTargetServer>" \
    --target-db-name "<YourTargetDB>" \
    --migration-operation-id "<YourMigrationOperationId>"
```

**PowerShell:** `New-AzDataMigrationToSqlDb` с параметрами `-Kind "SqlDb"`, `-SourceSqlConnectionAuthentication SQLAuthentication`, `-TargetSqlConnectionDataSource "<YourTargetServer>.database.windows.net"`, `-MigrationService ...` и при необходимости `-TableList`.

**Импорт BACPAC через SqlPackage:**
```
SqlPackage.exe /a:import /tcs:"Data Source=<server-name>.database.windows.net;Initial Catalog=myMigratedDatabase;User Id=<your_server_admin_account_user_id>;Password=<your_server_admin_account_password>" /sf:AdventureWorks2019.bacpac /p:DatabaseEdition=Premium /p:DatabaseServiceObjective=P6
```

**Транзакционная репликация (порядок T-SQL-скриптов из источника):**
1. `sp_adddistributor` и `sp_adddistributiondb` - создание дистрибьютора и базы `distribution`.
2. `sp_adddistpublisher` и `sp_addsubscriber` (целевой подписчик `<server>.database.windows.net`).
3. `sp_replicationdboption` с `@optname = N'publish'` для базы `AdventureWorks`.
4. `sp_addlogreader_agent` и `sp_addqreader_agent` - агенты Log Reader и Queue Reader.
5. `sp_addpublication` и `sp_addpublication_snapshot` - публикация (в примере `REPL-AdventureWorks`, `@repl_freq = N'continuous'`).
6. `sp_addarticle` - статья для таблицы `Person`.
7. `sp_addsubscription` (тип `Push`, `@subscriber_type = 0`) и `sp_addpushsubscription_agent`.

Полный текст скриптов с параметрами (включая пути, учетные записи и пароль-заглушку) приведен в источнике.

**Повторные попытки подключения (из источника):** первый повтор - не раньше чем через 5 секунд, далее задержка растет экспоненциально до 60 секунд; при временной ошибке SELECT повторяется в новом подключении.

**Прочие настройки из источника:** целевая база для репликации - Business Critical Gen5 8 vCore или Hyperscale; отключить auto update и auto create statistics на время миграции; выбирать высший уровень сервиса для миграции и понижать после нее; до 10 одновременных миграций на один self-hosted integration runtime.

## Что запомнить

- Для миграции с простоем используйте Azure Database Migration Service (рекомендуется для больших миграций), BACPAC или bcp; для миграции без простоя - транзакционную репликацию.
- Транзакционная репликация в Azure SQL Database работает только с логинами SQL-аутентификации и настраивается со стороны SQL Server, а не из портала.
- Перед миграцией временно поднимите уровень целевой БД, а затем понизьте его: это ускоряет перенос.
- Миграция по частям (выбор таблиц в DMS или `--table-list`) позволяет оставить часть данных on-premises.
- Временные ошибки подключения повторяйте с экспоненциальной задержкой (от 5 до 60 секунд).

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/
- В источнике упоминаются (без ссылок в тексте): Migration overview: SQL Server to Azure SQL Database; Azure Database Migration Service; Transactional Replication with Azure SQL Database; Assess SQL Server databases for migration to Azure SQL; SQL Database features; Replication to Azure SQL Database; PowerShell module for data migration; Azure CLI for data migration; модуль Deploy PaaS solutions with Azure SQL.
- Репликация и ошибки подключения: Troubleshoot transient connection errors in SQL Database and SQL Managed Instance.
