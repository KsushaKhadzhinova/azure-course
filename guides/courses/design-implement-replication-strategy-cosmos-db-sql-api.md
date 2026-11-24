# Проектирование и внедрение стратегии репликации в Azure Cosmos DB для NoSQL

**Источник** https://learn.microsoft.com/en-us/training/paths/design-implement-replication-strategy-cosmos-db-sql-api

## О курсе

Репликация данных по всему миру и управление failover в Azure Cosmos DB for NoSQL.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB
- **Предварительные требования:** Опыт создания облачных приложений на Microsoft C# или аналогичном языке программирования.

## Чему научитесь

- Репликация данных по регионам и автоматические или ручные failover.
- Настройка согласованности (consistency) на «скользящей шкале».
- Запись данных в несколько регионов.

## Модули

1. **Настройка репликации и управление отказоустойчивостью в Azure Cosmos DB**. Научиться распределять данные Azure Cosmos DB по регионам, оценивать стоимость глобальной репликации, настраивать автоматический и ручной failover, а также направлять .NET SDK для NoSQL на конкретный регион. [guide](../modules/configure-replication-manage-failovers-azure-cosmos-db.md)
2. **Модели согласованности в Azure Cosmos DB for NoSQL**. Научиться оценивать уровни согласованности Azure Cosmos DB, настраивать уровень по умолчанию для аккаунта и переопределять его для отдельных запросов. [guide](../modules/use-consistency-models-azure-cosmos-db-sql-api.md)
3. **Настройка multi-region write в Azure Cosmos DB (SQL API)**. Настроить Azure Cosmos DB для записи во все регионы (multi-region write), выбрать регион записи в .NET SDK и понять, как разрешаются конфликты при одновременном изменении одного элемента в разных регионах. [guide](../modules/configure-multi-region-write-azure-cosmos-db-sql-api.md)

## Ключевые технологии и понятия

- Глобальное распределение (global distribution)
- Primary region (основной регион)
- Read-only region (регион только для чтения)
- Replica set / partition set
- Single-write region / multi-region write
- Standard provisioned throughput
- Autoscale
- Automatic failover (автоматический failover)
- Failover priority (приоритет failover)
- ApplicationRegion / ApplicationPreferredRegions
- Consistency levels (уровни согласованности)
- Strong (строгая)
- Bounded Staleness (ограниченное отставание)
- Session (сессионная)

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/design-implement-replication-strategy-cosmos-db-sql-api
- Модуль «Настройка репликации и управление отказоустойчивостью в Azure Cosmos DB»: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/
- Модуль «Модели согласованности в Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/
- Модуль «Настройка multi-region write в Azure Cosmos DB (SQL API)»: https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/
