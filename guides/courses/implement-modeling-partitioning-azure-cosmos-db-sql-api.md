# Внедрение стратегии моделирования и партиционирования данных в Azure Cosmos DB для NoSQL

**Источник** https://learn.microsoft.com/en-us/training/paths/implement-modeling-partitioning-azure-cosmos-db-sql-api

## О курсе

Моделирование данных и партиционирование контейнеров Azure Cosmos DB для масштабирования и производительности.

- **Уровень:** средний (Intermediate)
- **Роль:** Data Engineer, Developer
- **Продукты и сервисы:** Azure Cosmos DB
- **Предварительные требования:** Знакомство с Azure и порталом Azure; опыт программирования на C#.

## Чему научитесь

- Определение ключевых паттернов доступа и модели сущностей приложения.
- Стратегии управления связями между сущностями (например, клиенты и заказы).
- Партиционирование для масштабирования контейнеров.

## Модули

1. **Реализация нереляционной модели данных в Azure Cosmos DB**. Научиться переносить реляционную модель в нереляционную (NoSQL) модель Azure Cosmos DB for NoSQL: проектировать документы по шаблонам доступа, выбирать между встраиванием (embedding) и ссылками (referencing), подбирать партиционный ключ без горячих партиций и моделировать небольшие справочники. Сквозной пример модуля: перенос интернет-магазина из реляционной БД. [guide](../modules/implement-non-relational-data-model.md)
2. **Стратегия моделирования и партиционирования данных в Azure Cosmos DB**. Научиться моделировать и партиционировать данные для NoSQL-базы (Azure Cosmos DB) на примере перевода реляционной модели интернет-магазина в NoSQL: денормализация, поддержка ссылочной целостности через change feed, объединение сущностей в одном контейнере и денормализация агрегатов. [guide](../modules/design-data-partitioning-strategy.md)

## Ключевые технологии и понятия

- Горизонтальное масштабирование (scale-out)
- Partition key (партиционный ключ)
- Логическая партиция
- Физическая партиция
- Hot partition
- Cross-partition query
- Embedding и referencing
- Entity discriminator
- Лимит физической партиции:
- Лимит логической партиции:
- Партиционный ключ в примере:
- Партиционный ключ для клиентов:
- Партиционный ключ для справочников:
- Запросы для малых справочников:

## Для каких ролей полезно

- Data Engineer (DE, инженер данных)
- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/implement-modeling-partitioning-azure-cosmos-db-sql-api
- Модуль «Реализация нереляционной модели данных в Azure Cosmos DB»: https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/
- Модуль «Стратегия моделирования и партиционирования данных в Azure Cosmos DB»: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/
