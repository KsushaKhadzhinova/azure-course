# Реляционные СУБД в Azure: обзор и развертывание

**Источник:** https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-relational-database-offerings-azure/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-relational-database-offerings-azure/<юнит>`)

## Цель модуля

Изучить варианты реляционных сервисов баз данных в Azure (Azure SQL и сервисы для открытых СУБД MySQL и PostgreSQL), сравнить их по модели обслуживания, совместимости и сценариям использования и научиться развертывать сервис.

## Ключевые понятия

- **IaaS / PaaS** — IaaS (SQL Server на виртуальных машинах) дает полный контроль над ОС и СУБД; PaaS (Managed Instance, SQL Database, MySQL и PostgreSQL) берет на себя обслуживание, обновления и резервное копирование.
- **SQL Server on Azure VMs** — полноценный SQL Server в виртуальной машине; подходит для lift-and-shift миграции.
- **Azure SQL Managed Instance** — PaaS с почти 100% совместимостью с SQL Server; подходит для переноса экземпляра со всеми базами.
- **Azure SQL Database** — полностью управляемая PaaS-база для новых облачных решений; модели Single Database и Elastic Pool; тариф Hyperscale до 128 ТБ.
- **Serverless compute tier** — вычислительные ресурсы автоматически масштабируются в заданном диапазоне; в General Purpose база может автоматически приостанавливаться.
- **Elastic pool (эластичный пул)** — общие ресурсы для нескольких баз с разной нагрузкой во времени.
- **SQL Database server (логический сервер)** — центральная точка администрирования баз, логинов, правил брандмауэра, аудита и failover-групп.
- **Azure Database for MySQL / PostgreSQL** — PaaS-реализации MySQL (на базе Community Edition) и PostgreSQL; есть варианты Flexible Server.
- **Microsoft Defender for SQL** — расширенная защита: vulnerability assessment и Advanced Threat Protection.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-relational-database-offerings-azure/1-introduction
Azure поддерживает SQL Server, PostgreSQL, MySQL и другие СУБД. Большинство сервисов полностью управляемые, с встроенной высокой доступностью, масштабированием и автоматическим мониторингом и настройкой производительности.

### 2. Describe Azure SQL services and capabilities
Источник: https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-relational-database-offerings-azure/2-azure-sql
Azure SQL — семейство сервисов на базе SQL Server: SQL Server on Azure VMs (IaaS), Azure SQL Managed Instance (PaaS, почти 100% совместимость) и Azure SQL Database (PaaS для новых облачных приложений). Сравнение: по совместимости, архитектуре, доступности, обслуживанию и сценариям. Azure SQL Database — дешевый вариант с минимальным администрированием, но не полностью совместимый с on-premises SQL Server; подходит для новых проектов и систем с переменной нагрузкой. Перечислены возможности: автоматическое обновление и патчинг, point-in-time restore, репликация в другие регионы, Microsoft Defender for SQL (Advanced Threat Protection и аудит в хранилище, например в Azure Storage account), шифрование at rest и in motion, бесплатный уровень с месячными лимитами 100 000 vCore-секунд serverless-вычислений и 32 ГБ хранилища на базу.

### 3. Describe Azure services for open-source databases
Источник: https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-relational-database-offerings-azure/3-azure-database-open-source
MySQL — простая открытая СУБД (популярна в стеке LAMP); PostgreSQL — объектно-реляционная СУБД с расширяемостью и PL/pgSQL. Azure Database for MySQL — PaaS с автоматическими резервными копиями и point-in-time restore до 35 дней (по умолчанию 7). Azure Database for PostgreSQL — PaaS с аналогичными возможностями доступности, масштабирования и безопасности; поддерживается набор расширений; query store сохраняет статистику запросов в базе `azure_sys` (представление `query_store.qs_view`). Варианты Flexible Server дают больше контроля над настройками; в бесплатной учетной записи Azure Flexible Server доступен бесплатно 12 месяцев.

### 4. Exercise: Explore Azure relational database services
Источник: https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-relational-database-offerings-azure/4-exercise-provision-relational-azure-data-services
Практика (около 15 минут): исследование Azure SQL Database. Нужна подписка Azure с правами администратора.

### 5. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-relational-database-offerings-azure/5-knowledge-check
Проверка знаний (в исходнике текст вопросов отсутствует).

### 6. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-relational-database-offerings-azure/6-summary
Модуль: определить варианты Azure SQL, определить варианты для открытых СУБД и развернуть сервис базы данных в Azure. Рекомендованный следующий шаг — сертификация Azure Data Fundamentals.

## Важные команды / код / настройки

В исходниках нет блоков кода. Ключевые параметры из текста:

- Azure SQL Database: модели Single Database и Elastic Pool; тарифы с serverless compute tier и Hyperscale (до 128 ТБ).
- Резервное копирование Azure Database for MySQL: point-in-time restore до 35 дней (по умолчанию 7 дней).
- Бесплатный уровень Azure SQL Database: 100 000 vCore-секунд serverless-вычислений в месяц и 32 ГБ хранилища на базу.
- PostgreSQL: включение query store сохраняет данные в `azure_sys`; запрос через `query_store.qs_view`.

## Что запомнить

- SQL Server on Azure VMs — IaaS с полным контролем; подходит для lift-and-shift и когда нужен доступ к ОС.
- Azure SQL Managed Instance — выбор для большинства миграций с минимальными изменениями приложения.
- Azure SQL Database — для новых облачных решений; возможна совместимость не со всеми функциями on-premises.
- Elastic pool позволяет разделять ресурсы между базами с разной нагрузкой во времени.
- Azure Database for MySQL и PostgreSQL — PaaS с автоматическими бэкапами, высокой доступностью и масштабированием; Flexible Server дает больше настроек.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/explore-provision-deploy-relational-database-offerings-azure/
- Документация: What is Azure SQL Managed Instance? (упоминается в уроке 2).
- Документация: Migration overview: From SQL Server (упоминается в уроке 2).
- Документация: Extensions and modules in Azure Database for PostgreSQL (упоминается в уроке 3).
- Сертификация: Azure Data Fundamentals (упоминается в уроке 6).
