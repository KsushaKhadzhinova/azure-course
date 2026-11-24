# Роли и обязанности специалистов по данным и сервисы Azure

**Источник:** https://learn.microsoft.com/en-us/training/modules/explore-roles-responsibilities-world-of-data/

## Цель модуля

Познакомиться с ролями, которые организации назначают специалистам по данным, с их задачами и с сервисами Microsoft Azure, которые эти роли используют.

## Ключевые понятия

- **Database administrator (DBA)** - администрирует базы (on-premises и в облаке): права доступа, резервные копии, восстановление, доступность и производительность.
- **Data engineer** - строит инфраструктуру и конвейеры интеграции данных, очистку и трансформацию, отвечает за конфиденциальность и мониторинг пайплайнов.
- **Data analyst** - исследует данные, строит аналитические модели, отчеты и визуализации.
- **AI engineer** - встраивает AI-функции в приложения и рабочие процессы, работает с LLM и ML-конвейерами; с ним работают в тесной связке data engineers и data analysts.
- **PaaS и SaaS** - модели облачной поставки: PaaS (Microsoft управляет инфраструктурой), SaaS (готовый продукт как сервис).
- **OneLake** - общее хранилище Microsoft Fabric, на котором работают все его компоненты.
- **Data lake (озеро данных)** - Blob-хранилище с иерархическим пространством имен.
- **Semantic model (семантическая модель)** - слой в Power BI и Fabric, определяющий меры, связи и бизнес-логику.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/explore-roles-responsibilities-world-of-data/1-introduction

Объем данных, которые создают системы и устройства, вырос; появились новые роли и подходы. Модуль описывает роли, их задачи и сервисы Azure для них.

### 2. Роли в мире данных
URL: https://learn.microsoft.com/en-us/training/modules/explore-roles-responsibilities-world-of-data/2-explore-job-roles

Четыре ключевые роли: database administrator, data engineer, data analyst, AI engineer. В одной организации одна персона может совмещать роли. Администратор БД отвечает за проектирование, внедрение и обслуживание БД, резервное копирование и восстановление, безопасность и права доступа. Инженер данных проектирует загрузку и трансформацию данных, хранилища, мониторинг пайплайнов. Аналитик данных ищет тренды и связи, строит модели и отчеты. AI-инженер строит решения на LLM и ML, например chat-over-your-data, генерацию контента и автоматическую классификацию; работает с Microsoft Foundry. В тексте отмечено, что ИИ-инструменты помогают в каждой роли, но архитектурные решения, оценку качества и ответственное внедрение остаются за человеком. Не рассмотрены, но существуют роли data scientist и data architect.

### 3. Сервисы данных
URL: https://learn.microsoft.com/en-us/training/modules/explore-roles-responsibilities-world-of-data/3-data-services

Обзор сервисов Azure для данных:

- **Azure SQL** - семейство реляционных сервисов на движке SQL Server: Azure SQL Database (PaaS), Azure SQL Managed Instance (почти полная совместимость, больше гибкости), Azure SQL VM (полный контроль и ответственность).
- **Открытые СУБД в Azure** - Azure Database for MySQL и Azure Database for PostgreSQL.
- **Azure Cosmos DB** - глобальная NoSQL-база с несколькими API; документы JSON, пары ключ-значение, колоночные семейства и графы.
- **Azure Storage** - Blob containers, file shares, tables; на основе Blob строятся data lake.
- **Azure Data Factory** - конвейеры переноса и трансформации данных (ETL); в Fabric - Fabric Data Factory.
- **Microsoft Fabric** - единая SaaS-платформа аналитики: ингестия, Lakehouse, Warehouse, Real-Time Intelligence, наука о данных, Power BI, базы данных; общий слой OneLake. Copilot помогает писать пайплайны, SQL и код ноутбуков.
- **Fabric IQ** - контекст бизнес-сущностей на основе OneLake и семантических моделей Power BI (в тексте указано, что workload и элемент ontology в превью).
- **Power BI** - платформа бизнес-аналитики и визуализации, встроена в Fabric.
- **Azure Databricks** - аналитическая платформа на Apache Spark, оптимизирована для Delta Lake.
- **Azure Stream Analytics** - движок потоковой обработки: вход, запрос, выход.
- **Azure Data Explorer** - аналитика логов и телеметрии с временными метками.
- **Microsoft Purview** - управление данными на уровне предприятия: карта данных и отслеживание происхождения (lineage).
- **Microsoft Foundry** - PaaS для операций ИИ, моделей и разработки приложений.

### 4. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/explore-roles-responsibilities-world-of-data/4-knowledge-check

Тест модуля с выбором лучшего ответа. Вопросы в источнике не приведены.

### 5. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/explore-roles-responsibilities-world-of-data/5-summary

Работа с данными требует знания многих технологий; организации распределяют задачи по ролям. Модуль научил определять роли специалистов по данным и облачные сервисы, которые они используют. Следующий шаг в источнике - сертификация Azure Data Fundamentals.

## Важные команды / код / настройки

В источнике команд и кода нет. Упомянутые настройки и продукты:

- Microsoft Copilot in Azure - помощь в генерации T-SQL и диагностике Azure SQL Database.
- Azure Cosmos DB extension for Visual Studio Code - AI-помощник для запросов (preview).
- Hierarchical namespace - включает иерархию папок в Blob-хранилище для data lake.

## Что запомнить

- Четыре роли: администратор БД, инженер данных, аналитик данных, AI-инженер; роли могут совмещаться.
- Azure SQL Database, Managed Instance и SQL VM различаются степенью управляемости и ответственностью.
- Microsoft Fabric объединяет аналитику на одном хранилище OneLake и работает по модели SaaS.
- Azure Data Factory и Fabric Data Factory используются для ETL-конвейеров.
- Microsoft Purview помогает с управлением данными, каталогом и lineage.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/explore-roles-responsibilities-world-of-data/
- Сертификация Azure Data Fundamentals (упомянута в источнике, URL не приведен)
