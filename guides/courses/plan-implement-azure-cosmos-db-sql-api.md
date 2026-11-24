# Планирование и внедрение Azure Cosmos DB для NoSQL

**Источник** https://learn.microsoft.com/en-us/training/paths/plan-implement-azure-cosmos-db-sql-api

## О курсе

Планирование конфигурации и выбор вариантов провизионирования для нового аккаунта Azure Cosmos DB for NoSQL.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB
- **Предварительные требования:** Опыт создания облачных приложений на Microsoft C# или аналогичном языке программирования.

## Чему научитесь

- Варианты конфигурации нового аккаунта Azure Cosmos DB for NoSQL.
- Выбор между вариантами пропускной способности (throughput).
- Миграция данных в Azure Cosmos DB for NoSQL и из него.

## Модули

1. **Планирование ресурсов для Azure Cosmos DB for NoSQL**. Научиться оценивать требования приложения к пропускной способности (throughput) и хранению данных, а также правильно настраивать аккаунт и ресурсы Azure Cosmos DB для NoSQL под новое решение. [guide](../modules/plan-resource-requirements.md)
2. **Настройка пропускной способности Azure Cosmos DB для SQL API**. Сравнить модели предоставления пропускной способности в Azure Cosmos DB (serverless, standard/manual provisioned, autoscale) и научиться выполнять миграцию между standard и autoscale throughput в соответствии с характером нагрузки. [guide](../modules/configure-azure-cosmos-db-sql-api.md)
3. **Перенос данных в Azure Cosmos DB for NoSQL**. Научиться переносить данные в Azure Cosmos DB for NoSQL и из него с помощью сервисов Azure и открытых инструментов: Azure Data Factory, Kafka Connect, Azure Stream Analytics, Apache Spark (через Synapse Link). [guide](../modules/move-data-azure-cosmos-db-sql-api.md)

## Ключевые технологии и понятия

- Request Units (RU)
- RU/s
- Container (контейнер)
- Database (база данных)
- Serverless
- Standard provisioned throughput
- Autoscale provisioned throughput
- Dynamic Autoscale
- Capacity calculator (калькулятор емкости)
- TTL (Time-to-live)
- Request Units (RU/s)
- Provisioned throughput
- Standard (manual) throughput
- Autoscale throughput

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/plan-implement-azure-cosmos-db-sql-api
- Модуль «Планирование ресурсов для Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/plan-resource-requirements/
- Модуль «Настройка пропускной способности Azure Cosmos DB для SQL API»: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/
- Модуль «Перенос данных в Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/move-data-azure-cosmos-db-sql-api/
