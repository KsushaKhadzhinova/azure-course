# Архитектура Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-architecture/

## Цель модуля

Понять архитектуру Azure Databricks для инженерии данных: иерархию аккаунта, workspace и metastore, разделение control plane и compute plane, типы хранилищ (workspace storage, Unity Catalog managed storage, external storage, default storage) и принципы выбора между ними.

## Ключевые понятия

- **Account** — верхний уровень управления Azure Databricks: identity, workspaces, metastores, биллинг и политики.
- **Workspace** — изолированная среда совместной работы: ingestion, исследование, задания и обучение моделей.
- **Metastore (Unity Catalog)** — контейнер метаданных и прав доступа; региональный, работает на уровне аккаунта.
- **Three-level namespace** — `<catalog>.<schema>.<object>`.
- **Control plane** — управляемые Azure Databricks сервисы (веб-приложение, оркестрация, планирование заданий); данные не обрабатывает.
- **Compute plane** — среда обработки данных: serverless (в аккаунте Azure Databricks) или classic (в подписке клиента).
- **Storage credential** — объект Unity Catalog с механизмом аутентификации (managed identity или service principal).
- **External location** — связка облачного пути и storage credential.
- **Managed storage** — хранилище, которым управляет Unity Catalog для managed tables и volumes.
- **Default storage** — полностью управляемое хранилище Azure Databricks для serverless workspaces.
- **Hive metastore (legacy)** — старый метастор уровня workspace, доступный как каталог `hive_metastore`.
- **DBFS** — устаревшая распределенная файловая система (DBFS root и mounts), рекомендуется не использовать.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-architecture/1-introduction

Введение: архитектура определяет, где находятся данные, как распределяются вычисления и как компоненты взаимодействуют. Описаны control и compute planes, а также три варианта хранения: default storage, external storage и Unity Catalog managed storage.

### 2. Understand Azure Databricks architecture
https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-architecture/2-understand-azure-databricks-architecture

Иерархия: account → workspaces и metastores → catalog → schema → объекты. Metastore регионален и работает на уровне аккаунта, в отличие от legacy Hive metastore уровня workspace. Control plane выполняет оркестрацию, но не обрабатывает данные; compute plane — serverless или classic (в виртуальной сети workspace в подписке; в портале называется Hybrid workspaces). Workspace storage содержит файлы workspace и системные данные (результаты запросов, результаты заданий, историю ноутбуков, планы запросов, логи кластеров). DBFS root и mounts — устаревший паттерн.

### 3. Understand Unity Catalog managed storage
https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-architecture/3-understand-unity-catalog-managed-storage

Managed storage хранит данные managed tables и managed volumes; Unity Catalog управляет жизненным циклом. При DROP managed table файлы сохраняются на 7 дней, затем безвозвратно удаляются асинхронно. Уровни назначения: metastore, catalog (рекомендуется) и schema. Порядок разрешения: schema → catalog → metastore. Фактический путь включает подкаталоги `__unitystorage/catalogs/<uuid>` или `__unitystorage/schemas/<uuid>`. Unity Catalog запрещает пересечение путей managed storage с другими managed-местами, external tables и external volumes.

### 4. Understand external storage
https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-architecture/4-understand-external-storage

External locations связывают облачный путь (ADLS-контейнер, S3 только для чтения, Cloudflare R2) с storage credential. Credential — managed identity (рекомендуется, без секретов) или service principal (с ручной ротацией секретов). External tables и volumes оставляют файлы у владельца, а managed storage locations позволяют указать, где Unity Catalog хранит управляемые данные. Workspace binding ограничивает использование external location или credential конкретными workspace (например, продакшен-credential только в продакшен-workspace).

### 5. Understand default storage
https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-architecture/5-understand-default-storage

Default storage — полностью управляемое хранилище, которое создается автоматически для serverless workspaces. Создавать каталоги на default storage можно только в serverless workspaces; доступ к ним требует serverless compute, классические кластеры не могут читать или писать такие каталоги. Управление доступом через SQL GRANT. Каталоги по умолчанию доступны из workspace, где созданы. Прямой доступ к файлам внешними инструментами (чтение файлов Delta или Iceberg) не поддерживается; BI-инструменты подключаются через ODBC и JDBC.

### 6. Module assessment
https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-architecture/6-knowledge-check

Проверочный тест (около 5 минут). Вопросы и ответы в источнике не приведены.

### 7. Summary
https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-architecture/7-summary

Итоги: иерархия аккаунта, разделение control и compute planes, варианты хранения (default storage, external locations, managed storage) и роль Unity Catalog в управлении данными.

## Важные команды / код / настройки

В источнике нет команд и кода. Упомянутые настройки и правила:

- **Три уровня имен:** `<catalog-name>.<schema-name>.<object-name>`.
- **Legacy-каталог:** `hive_metastore.<schema-name>.<table-name>`.
- **Подкаталоги managed storage:** `__unitystorage/catalogs/<uuid>` и `__unitystorage/schemas/<uuid>`.
- **Срок хранения файлов удаленной managed table:** 7 дней, затем асинхронная очистка.
- **Порядок разрешения managed storage:** schema → catalog → metastore; без хранилища на одном из уровней managed tables и volumes создать нельзя.
- **Storage credential:** рекомендуется Azure managed identity; service principal требует ручного управления секретами.
- **Workspace binding:** ограничивает доступ к external location и credential конкретными workspace.
- **Default storage:** только serverless workspaces; для доступа нужен serverless compute.
- **Устаревшее:** DBFS root и DBFS mounts; рекомендуются Unity Catalog managed tables и volumes.
- **Безопасность:** для workspace storage account можно включить firewall.

## Что запомнить

- Control plane управляет и оркестрирует, compute plane обрабатывает данные; serverless compute работает в аккаунте Azure Databricks, classic — в вашей подписке.
- Metastore Unity Catalog регионален и управляет правами на уровне аккаунта; используйте трехуровневое имя catalog.schema.object.
- Managed storage: Unity Catalog управляет жизненным циклом; рекомендуемый уровень назначения — catalog.
- External location = облачный путь + storage credential; предпочтительна managed identity.
- Default storage удобен для новых serverless-нагрузок, но требует serverless compute и не подходит для прямого доступа к файлам.

## Связанные материалы

- Модуль о создании и настройке внешнего хранилища (упоминается в уроке 4 как следующий модуль курса).
- Документация Unity Catalog, managed и external storage (упоминается в уроках 3 и 4).
