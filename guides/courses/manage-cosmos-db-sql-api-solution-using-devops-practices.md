# Управление решением Azure Cosmos DB для NoSQL с помощью практик DevOps

**Источник** https://learn.microsoft.com/en-us/training/paths/manage-cosmos-db-sql-api-solution-using-devops-practices

## О курсе

Автоматизация типовых задач управления Azure Cosmos DB через командную строку и Azure Resource Manager.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB, Azure Resource Manager
- **Предварительные требования:** Опыт создания облачных приложений на Microsoft C# или аналогичном языке программирования.

## Чему научитесь

- Управление аккаунтами, базами данных и контейнерами через командную строку.
- Автоматизированное развертывание ресурсов через Azure Resource Manager.

## Модули

1. **Написание скриптов для Azure Cosmos DB (SQL API) с Azure CLI**. Администрировать ресурсы Azure Cosmos DB для NoSQL из Azure CLI: создавать аккаунт, базы и контейнеры, управлять индексной политикой и throughput, переключать режим throughput, менять регионы и инициировать отработку отказа (failover). [guide](../modules/write-scripts-for-azure-cosmos-db-sql-api.md)
2. **Создание шаблонов ресурсов для Azure Cosmos DB for NoSQL**. Научиться автоматизировать создание ресурсов Azure Cosmos DB for NoSQL (аккаунт, база данных, контейнер) с помощью шаблонов Azure Resource Manager (ARM, JSON) и Bicep, а также управлять throughput и политиками индексации через шаблоны. [guide](../modules/create-resource-template-for-azure-cosmos-db-sql-api.md)

## Ключевые технологии и понятия

- Azure CLI
- `az cosmosdb`
- `az cosmosdb sql`
- Индексная политика (indexing policy)
- Throughput (standard / autoscale)
- Failover priority
- Multi-region write
- Azure Resource Manager (ARM) template
- Bicep
- Microsoft.DocumentDB/databaseAccounts
- Microsoft.DocumentDB/databaseAccounts/sqlDatabases
- Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers
- dependsOn (JSON) / parent (Bicep)
- autoscaleSettings.maxThroughput

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/manage-cosmos-db-sql-api-solution-using-devops-practices
- Модуль «Написание скриптов для Azure Cosmos DB (SQL API) с Azure CLI»: https://learn.microsoft.com/en-us/training/modules/write-scripts-for-azure-cosmos-db-sql-api/
- Модуль «Создание шаблонов ресурсов для Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/
