# Защита, оптимизация и развертывание решений Azure Cosmos DB

**Источник** https://learn.microsoft.com/en-us/training/paths/secure-optimize-deploy-azure-cosmos-db-solutions

## О курсе

Эксплуатация Azure Cosmos DB for NoSQL в продуктивной среде: безопасность, резервное копирование, регионы, индексы и диагностика.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB, Azure Backup, Azure Monitor
- **Предварительные требования:** Прохождение пути Design and develop Azure Cosmos DB database solutions или эквивалентный опыт работы с Azure Cosmos DB for NoSQL; базовые знания идентификаторов Azure, назначения ролей и виртуальных сетей.

## Чему научитесь

- Аутентификация через Microsoft Entra ID вместо ключей учетной записи; разделение прав control plane и data plane.
- Выбор между периодическим и непрерывным резервным копированием.
- Добавление регионов и маршрутизация чтения и записи.
- Настройка индексной политики под рабочую нагрузку.
- Диагностика дорогих запросов и инцидентов по метрикам сервиса.
- Управление мультитенантной средой через fleets.

## Модули

1. **Безопасность Azure Cosmos DB for NoSQL**. Научиться защищать приложение и аккаунт Azure Cosmos DB for NoSQL: выбирать аутентификацию (Microsoft Entra и managed identity, ключи с ротацией), разделять control-plane и data-plane права и назначать роли RBAC, настраивать сетевые ограничения (IP firewall, service endpoints, private endpoints) и маскировать чувствительные поля (dynamic data masking). [guide](../modules/secure-azure-cosmos-db-nosql.md)
2. **Настройка резервного копирования и восстановления в Azure Cosmos DB for NoSQL**. Выбрать режим резервного копирования (periodic или continuous) и уровень хранения, включить continuous backup для нового и существующего аккаунта, выполнить point-in-time recovery (восстановление на момент времени) и проверить результат, а также понять, когда нужен Azure Backup для Azure Cosmos DB. [guide](../modules/configure-backup-restore-azure-cosmos-db-nosql.md)
3. **Проектирование доступности и аварийного переключения между регионами для Azure Cosmos DB for NoSQL**. Научиться настраивать аккаунт Azure Cosmos DB for NoSQL и его клиенты для работы в нескольких регионах: выбирать зональную и региональную избыточность, добавлять регионы и направлять чтения в ближайший регион, включать запись в нескольких регионах, разрешать конфликты записи и выбирать подходящую операцию аварийного переключения (failover). [guide](../modules/design-multi-region-availability-failover-azure-cosmos-db-nosql.md)
4. **Проектирование и оптимизация стратегии индексации в Azure Cosmos DB for NoSQL**. Подобрать индексную политику под соотношение чтения и записи контейнера, добавить составные и пространственные индексы, вычисляемые свойства (computed properties) и глобальные вторичные индексы (global secondary indexes), а также измерить стоимость каждого изменения в request units (RU). [guide](../modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql.md)
5. **Анализ и настройка производительности запросов в Azure Cosmos DB for NoSQL**. Научиться диагностировать дорогие запросы Azure Cosmos DB for NoSQL по их метрикам (request charge, server-side query metrics, index metrics, распределение по физическим партициям) и применять исправление, которое указывают эти метрики. [guide](../modules/analyze-tune-query-performance-azure-cosmos-db-nosql.md)
6. **Мониторинг и устранение неполадок Azure Cosmos DB для NoSQL**. Научиться по коду ответа, метрикам, алертам и диагностическим логам находить причину деградации Azure Cosmos DB для NoSQL: интерпретировать коды ответов и троттлинг (429), отслеживать задержку и загрузку партиций, настраивать алерты Azure Monitor и анализировать логи в Log Analytics. [guide](../modules/monitor-troubleshoot-azure-cosmos-db-nosql.md)
7. **Управление парком аккаунтов Azure Cosmos DB (fleets)**. Организовать многоарендную среду из множества аккаунтов Azure Cosmos DB для NoSQL в fleet, создать fleetspace и зарегистрировать в нем аккаунты из разных подписок, настроить общий пул throughput и отслеживать использование и стоимость по всему парку через fleet analytics. [guide](../modules/manage-azure-cosmos-db-fleets.md)

## Ключевые технологии и понятия

- Microsoft Entra authentication
- Managed identity (управляемая идентичность)
- DefaultAzureCredential / ManagedIdentityCredential
- Principal object ID vs client ID
- Account keys (ключи аккаунта)
- Key rotation (ротация ключей)
- Control plane
- Data plane
- Built-in data roles
- Scope (область назначения)
- IP firewall / virtual network service endpoints
- Private endpoint
- publicNetworkAccess / disableLocalAuth
- Dynamic data masking (DDM)

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/secure-optimize-deploy-azure-cosmos-db-solutions
- Модуль «Безопасность Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/secure-azure-cosmos-db-nosql/
- Модуль «Настройка резервного копирования и восстановления в Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/configure-backup-restore-azure-cosmos-db-nosql/
- Модуль «Проектирование доступности и аварийного переключения между регионами для Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/design-multi-region-availability-failover-azure-cosmos-db-nosql/
- Модуль «Проектирование и оптимизация стратегии индексации в Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/design-optimize-indexing-strategy-azure-cosmos-db-nosql/
- Модуль «Анализ и настройка производительности запросов в Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/analyze-tune-query-performance-azure-cosmos-db-nosql/
- Модуль «Мониторинг и устранение неполадок Azure Cosmos DB для NoSQL»: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-azure-cosmos-db-nosql/
- Модуль «Управление парком аккаунтов Azure Cosmos DB (fleets)»: https://learn.microsoft.com/en-us/training/modules/manage-azure-cosmos-db-fleets/
