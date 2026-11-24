# Настройка среды Azure Databricks

**Источник** https://learn.microsoft.com/en-us/training/paths/azure-databricks-data-engineer-set-up-configure-environment

## О курсе

Архитектура Azure Databricks, интеграции, варианты вычислительных ресурсов и организация данных.

- **Уровень:** средний (Intermediate)
- **Роль:** Data Engineer
- **Продукты и сервисы:** Azure Databricks, Unity Catalog
- **Предварительные требования:** Базовые знания аналитики данных; понимание облачных хранилищ; знакомство с SQL и организацией данных.

## Чему научитесь

- Архитектура Azure Databricks: разделение control plane и compute plane.
- Интеграции Azure Databricks с сервисами Microsoft.
- Выбор вычислительных ресурсов для разных нагрузок.
- Трехуровневое пространство имен Unity Catalog: catalogs, schemas и objects.

## Модули

1. **Знакомство с Azure Databricks**. Понять назначение Azure Databricks как единой платформы для data engineering, data science, machine learning и аналитики: создать workspace, освоить интерфейс, основные рабочие нагрузки, ключевые понятия и инструменты управления данными (Unity Catalog и Microsoft Purview). [guide](../modules/explore-azure-databricks.md)
2. **Архитектура Azure Databricks**. Понять архитектуру Azure Databricks для инженерии данных: иерархию аккаунта, workspace и metastore, разделение control plane и compute plane, типы хранилищ (workspace storage, Unity Catalog managed storage, external storage, default storage) и принципы выбора между ними. [guide](../modules/understand-azure-databricks-architecture.md)
3. **Интеграции Azure Databricks с сервисами Microsoft**. Понять семь интеграций Azure Databricks с сервисами Microsoft (Microsoft Fabric, Power BI, Visual Studio Code, Power Platform, Copilot Studio, Microsoft Purview и Microsoft Foundry), их принципы работы, сценарии применения и вопросы безопасности и управления доступом. [guide](../modules/understand-azure-databricks-integrations.md)
4. **Выбор и настройка вычислительных ресурсов в Azure Databricks**. Научиться выбирать тип вычислительного ресурса (serverless, classic, SQL warehouse, job compute, instance pools) для нагрузки, настраивать производительность (узлы, автомасштабирование, завершение работы), функции (Photon, версия Runtime), устанавливать библиотеки и управлять доступом к compute. [guide](../modules/select-and-configure-compute.md)
5. **Создание и организация объектов в Unity Catalog**. Спроектировать и создать структуру Unity Catalog из трёх уровней пространства имён (catalog → schema → таблицы, представления, тома, функции), применить единые соглашения об именах, настроить managed storage, создать таблицы (managed, external, с ключами и ограничениями), представления (стандартные, динамические, материализованные, streaming tables), тома, функции и процедуры, подключить внешние базы через foreign catalog и настроить AI/BI Genie. [guide](../modules/create-and-organize-objects-in-unity-catalog.md)

## Ключевые технологии и понятия

- Azure Databricks
- Data lakehouse (озеро-хранилище)
- Delta Lake
- Unity Catalog
- Metastore
- Workspace (рабочая область)
- Control plane / Compute plane
- Cluster (кластер)
- Serverless / Classic compute
- Databricks Runtime
- Lakeflow Jobs
- SQL warehouse
- MLflow
- Microsoft Purview

## Для каких ролей полезно

- Data Engineer (DE, инженер данных)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/azure-databricks-data-engineer-set-up-configure-environment
- Модуль «Знакомство с Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/
- Модуль «Архитектура Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-architecture/
- Модуль «Интеграции Azure Databricks с сервисами Microsoft»: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/
- Модуль «Выбор и настройка вычислительных ресурсов в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/
- Модуль «Создание и организация объектов в Unity Catalog»: https://learn.microsoft.com/en-us/training/modules/create-and-organize-objects-in-unity-catalog/
