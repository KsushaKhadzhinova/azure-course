# Знакомство с Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/

## Цель модуля

Понять назначение Azure Databricks как единой платформы для data engineering, data science, machine learning и аналитики: создать workspace, освоить интерфейс, основные рабочие нагрузки, ключевые понятия и инструменты управления данными (Unity Catalog и Microsoft Purview).

## Ключевые понятия

- **Azure Databricks** - облачная платформа на базе Apache Spark, объединяющая data engineering, data science, ML и BI.
- **Data lakehouse (озеро-хранилище)** - подход, который совмещает масштабируемость data lake и возможности data warehouse; часто организуется по медальонной архитектуре (medallion architecture).
- **Delta Lake** - слой хранения с транзакциями ACID, контролем схемы и версионированием; формат таблиц по умолчанию в Azure Databricks.
- **Unity Catalog** - централизованное управление доступом, поиском, lineage, аудитом и мониторингом качества данных и AI-объектов.
- **Metastore** - верхний уровень метаданных Unity Catalog; обычно один на регион, его могут использовать несколько workspace.
- **Workspace (рабочая область)** - среда, в которой хранятся notebooks, jobs, compute и другие объекты.
- **Control plane / Compute plane** - управляющий слой, которым владеет Databricks, и слой вычислений (для classic compute в вашей подписке, для serverless - в аккаунте Databricks).
- **Cluster (кластер)** - вычислительный ресурс с driver node и worker nodes; может быть с фиксированным размером или auto-scale.
- **Serverless / Classic compute** - полностью управляемые вычисления против вычислений, настраиваемых пользователем.
- **Databricks Runtime** - собственная сборка Apache Spark с улучшениями и библиотеками; имеет жизненный цикл (Beta, GA, LTS, EoS, EoL).
- **Lakeflow Jobs** - автоматизация и оркестрация задач (job содержит tasks).
- **SQL warehouse** - вычислительный ресурс для SQL-аналитики (serverless, pro или classic).
- **MLflow** - открытая платформа управления жизненным циклом ML (эксперименты, модели, развертывание).
- **Microsoft Purview** - сервис управления данными: discovery, классификация, lineage; интегрируется с Unity Catalog.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/01-introduction

Azure Databricks объединяет инженерию данных, науку о данных и ML в одном workspace. Он подключается к источникам (Azure SQL Database, Amazon S3, Google Cloud Storage, SAP, Oracle и др.). Описаны понятия data lakehouse, medallion architecture, Delta Lake и Unity Catalog.

### 2. Get started with Azure Databricks
https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/02-azure-databricks

Workspace создается через портал, ARM/Bicep/Terraform, PowerShell или Azure CLI. Указываются имя, регион, тариф (pricing tier) и тип workspace. Описан интерфейс: главная страница, боковая панель (SQL, Data Engineering, AI/ML), кнопка + New и поиск. Genie Code (бывший Databricks Assistant) помогает писать и исправлять код, работает в режиме Agent и с согласия пользователя запускает код.

### 3. Identify Azure Databricks workloads
https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/03-workloads

Основные нагрузки: инженерия данных (Spark, Python, R, Scala, SQL), машинное обучение (MLflow, TensorFlow, PyTorch, Scikit-learn), SQL-аналитика через SQL warehouses (требуется Premium) и потоковая обработка.

### 4. Understand key concepts
https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/04-key-concepts

Разобраны workspaces, notebooks (ячейки code и Markdown, magic commands), clusters (driver и worker nodes, типы compute), Databricks Runtime (жизненный цикл версий), Lakeflow Jobs, Delta Lake, Databricks SQL, SQL warehouses (serverless, pro, classic) и MLflow.

### 5. Data governance using Unity Catalog and Microsoft Purview
https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/05-data-governance-using-unity-catalog-and-microsoft-purview

Unity Catalog управляет доступом, lineage, аудитом и качеством. Трехуровневая схема `catalog.schema.object`; таблицы бывают managed и external. Права выдаются через SQL `GRANT`. Microsoft Purview сканирует Unity Catalog, классифицирует данные и показывает lineage в Data Map.

### 6. Exercise - Explore Azure Databricks
https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/06-exercise-explore-databricks

Практическое задание (около 45 минут): интерфейс workspace, загрузка примера данных в volume Unity Catalog, работа с notebook (Python, SQL magic commands, Markdown) с помощью Genie Code. Нужна подписка Azure с правами администратора.

### 7. Module assessment
https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/07-knowledge-check

Проверка знаний (около 3 минут). Текст в источнике не приведен.

### 8. Summary
https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/08-summary

Модуль: создание workspace, основные нагрузки, инструменты Unity Catalog и Microsoft Purview, ключевые концепции Azure Databricks.

## Важные команды / код / настройки

**Создание workspace (Azure CLI):**
```
az databricks workspace create \
    --resource-group myresourcegroup \
    --name mydatabricksws \
    --location westus2 \
    --sku premium
```

**Создание workspace (PowerShell):**
```
New-AzDatabricksWorkspace -Name mydatabricksws -ResourceGroupName myresourcegroup -Location westus2 -ManagedResourceGroupName databricks-group -Sku premium
```

**Права в Unity Catalog (SQL):**
```
GRANT CREATE TABLE ON SCHEMA mycatalog.myschema TO `finance-team`;
```

**Настройки при создании workspace (из источника):**
- Pricing tier: Premium (RBAC, Unity Catalog, SQL, Mosaic AI, serverless compute и др.) или Trial (14 дней бесплатно на Premium). Standard больше недоступен для новых workspace с 1 апреля 2026 года.
- Workspace type: Serverless (предварительно настроенные serverless compute и хранилище, рекомендуется для быстрого старта) или Hybrid (Classic) (compute и storage в вашей подписке).
- Managed Resource Group name - необязательно; создается автоматически.

**Жизненный цикл Databricks Runtime:** Beta - для ознакомления, не для production; GA - около 6 месяцев обновлений под тем же номером версии; LTS - исправления и безопасность около 3 лет; EoS - без поддержки, версия недоступна при создании или обновлении compute; EoL - выведена из эксплуатации. Обновление обычно применяется перезапуском кластера.

**Иерархия Unity Catalog:** `catalog.schema.table_or_other_object`.

## Что запомнить

- Azure Databricks - платформа на Apache Spark для инженерии данных, ML и аналитики в одном workspace.
- Delta Lake дает ACID и версионирование и является форматом таблиц по умолчанию.
- Unity Catalog - централизованное управление доступом и lineage в трехуровневой схеме `catalog.schema.object`.
- Microsoft Purview сканирует Unity Catalog, классифицирует данные и показывает lineage.
- Serverless compute и serverless SQL warehouses снимают управление инфраструктурой; classic - для полного контроля настроек.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/
- В источнике упоминаются (без ссылок в тексте): Azure Databricks Documentation; Getting started with Azure Databricks; Microsoft Purview Documentation; Databricks Unity Catalog.
