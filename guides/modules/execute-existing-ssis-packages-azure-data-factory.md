# Выполнение существующих пакетов SSIS в Azure Data Factory

**Источник:** https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/

## Цель модуля

Научиться переносить существующие пакеты SQL Server Integration Services (SSIS) в облако через Azure-SSIS integration runtime, настраивать его, запускать пакеты в Azure и оценивать и мигрировать пакеты в Azure.

## Ключевые понятия

- **SSIS (SQL Server Integration Services)** - платформа для ETL-решений; состоит из управляющего потока (control flow) и потока данных (data flow). Пакеты (packages) входят в проекты (projects).
- **Azure-SSIS integration runtime (IR)** - вычислительная среда Azure Data Factory, которая нативно выполняет пакеты SSIS. Связывает действия (activities) и связанные службы (linked services).
- **SSISDB** - каталог SSIS, размещаемый в Azure SQL Database или Azure SQL Managed Instance; используется моделью развертывания проектов (Project Deployment Model).
- **Package Deployment Model** - модель, при которой пакеты хранятся в файловой системе, Azure Files или в MSDB; для нее SSISDB не создается, а настраиваются package stores.
- **Azure-Enabled Project** - проект SSDT, подготовленный для запуска в Azure.
- **AzureDTExec** - утилита командной строки, которая отправляет выполнение пакета в Azure-SSIS IR через конвейер Azure Data Factory с действием Execute SSIS Package.
- **Миграционные блокеры (migration blockers)** - проблемы совместимости, которые не дают пакету работать на Azure-SSIS IR; информационные проблемы (informative issues) касаются частично поддерживаемых или устаревших функций.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/1-introduction

Azure Data Factory позволяет перенести (lift and shift) решения SSIS в облако. В тексте урока указано, что Data Factory в Microsoft Fabric - следующее поколение Azure Data Factory, и для новых проектов его рекомендуется рассматривать; существующие нагрузки Azure Data Factory, включая Azure-SSIS IR, продолжают работать. Предварительные требования: вход в портал Azure, создание групп ресурсов, понимание Azure Data Factory и действия Copy.

### 2. Описание SQL Server Integration Services
URL: https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/2-describe-sql-server-integration-services

SSIS - компонент SQL Server, управляющий выполнением ETL-рабочих процессов через службу Windows. Пакеты можно запускать по требованию или по расписанию. Проект - единица развертывания (начиная с SQL Server 2012), может содержать параметры проекта и диспетчеры подключений на уровне проекта. Пакет содержит управляющий поток, в котором может быть задача Data Flow.

### 3. Azure-SSIS integration runtime
URL: https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/3-understand-azure-ssis-integration-runtime

Расположение Azure-SSIS IR желательно выбирать там же, где находится сервер Azure SQL Database или Azure SQL Managed Instance с SSISDB. Если SSISDB еще не существует, а источники находятся on-premises, рекомендуется создать сервер в регионе виртуальной сети, связанной с локальной сетью. Если регионы не совпадают, сначала создается IR, затем настраивается соединение виртуальных сетей между регионами. IR выполняет пакеты из SSISDB (Project Deployment Model) и пакеты из файловой системы, Azure Files или MSDB (Package Deployment Model). При создании указываются размер узла и число узлов, сервер для SSISDB (и уровень службы для Azure SQL Database), максимальное число параллельных выполнений на узел. После включения IR пакеты можно развертывать и мониторить через SSMS или SSDT.

### 4. Настройка Azure-SSIS integration runtime
URL: https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/4-set-up-azure-ssis-integration-runtime

Создание IR в интерфейсе Azure Data Factory: вкладка Manage, раздел Integration runtimes, + New, плитка "Lift-and-shift existing SSIS packages to execute in Azure". Страницы мастера: General settings (имя, описание, расположение, размер и число узлов, Edition/License Standard или Enterprise, Azure Hybrid Benefit), Deployment settings (создание SSISDB или package stores, подписка, сервер, аутентификация Microsoft Entra или SQL, уровень службы), Advanced settings (параллельные выполнения на узел, кастомизация, подключение к виртуальной сети, self-hosted IR как прокси), Summary и Finish.

### 5. Запуск пакетов SSIS в Azure Data Factory
URL: https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/5-run

В SQL Server Data Tools (SSDT) выбирается шаблон Integration Services Project (Azure-Enabled) или открывается существующий проект через мастер Azure-Enabled Project Wizard (версия целевой платформы - SQL Server 2017). Мастер SSIS in ADF Connection Wizard подключает проект к Azure-SSIS IR и к хранилищу Azure Storage, куда пакеты загружаются в Azure Files. Перед запуском настраиваются параметры проекта и аутентификация (например, Windows Authentication). Пакеты запускаются из SSDT командой "Execute in Azure" или "Execute Package in Azure". Для автоматизации в скриптах и CI/CD используется AzureDTExec.

### 6. Миграция пакетов SSIS в Azure Data Factory
URL: https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/6-migrate

Перед миграцией пакеты оцениваются: SSDT через Azure-Enabled Project умеет оценивать один пакет или весь проект и формирует отчет, который можно экспортировать в CSV. Задания SQL Server Agent можно мигрировать через SSMS с помощью SSIS Job Migration Wizard (только для пакетов в файловой системе). Есть четыре места хранения пакетов: SSISDB, файловая система, MSDB и SSIS Package store. Способ миграции зависит от места хранения (см. раздел ниже). Azure Database Migration Service не переносит SSISDB в Azure SQL Database; проекты переразворачиваются через мастер развертывания SSIS из SSMS или через SSIS DevOps Tools. Data Migration Assistant, который мог оценивать пакеты SSIS, выведен из эксплуатации 16 июля 2025 года.

### 7. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/7-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 8. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/8-summary

Что такое SSIS, что такое Azure-SSIS IR, как его настроить, как запускать пакеты в Azure и как мигрировать пакеты. В конце указано: ресурсы в собственной подписке нужно удалять (по одному или удалив группу ресурсов), чтобы не платить за них.

## Важные команды / код / настройки

Таблица миграции по типу хранения:

| Тип хранения пакетов | Способ миграции |
|---|---|
| SSIS Catalog (SSISDB) | Переразвернуть проекты через SSDT или SSMS в SSISDB на Azure SQL Database или Azure SQL Managed Instance |
| File System | Переразвернуть пакеты на файловых ресурсах или Azure Files через dtinstall, dtutil или копирование вручную; либо использовать виртуальную сеть или self-hosted IR |
| MSDB database in SQL Server | Экспортировать пакеты в файловую систему, на файловые ресурсы или в Azure Files через SSMS или dtutil |
| SSIS Package store | Экспортировать в package store Azure-SSIS IR через SSMS или dtutil, либо переразвернуть через dtinstall, dtutil или копирование |

Утилиты и инструменты, упомянутые в источнике: SSMS, SSDT, dtinstall, dtutil, SSIS Job Migration Wizard, SSIS DevOps Tools, AzureDTExec (вместо dtexec для выполнения в Azure).

Основные параметры создания Azure-SSIS IR: Name, Description, Location (рекомендуется совпадать с сервером SSISDB), Node Size, Node Number, Edition/License (Standard или Enterprise), Save Money (Azure Hybrid Benefit), Catalog Database Service Tier (Basic, Standard, Premium или elastic pool), Maximum Parallel Executions Per Node.

## Что запомнить

- Azure-SSIS IR выполняет существующие пакеты SSIS в Azure без их переписывания.
- Расположение IR должно совпадать с расположением сервера SSISDB, чтобы не тратить трафик между регионами.
- Перед миграцией оцените пакеты в SSDT: блокеры нужно устранить, информационные проблемы - учесть.
- Для автоматизации запуска используйте AzureDTExec; пакеты в Azure можно запускать и из SSDT.
- После работы удаляйте неиспользуемые ресурсы, чтобы не платить за них.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/
- Migrate SQL Server Agent jobs to ADF with SSMS; Run SSIS packages with the AzureDTExec utility; Data Migration Assistant overview; Migrate SQL Server workloads to Azure SQL (названия из источника, URL не приведены)
- Microsoft Fabric Data Factory (упомянута в источнике как следующее поколение Azure Data Factory)
