# Разработка AI-решений с Azure Cosmos DB для NoSQL

**Источник** https://learn.microsoft.com/en-us/training/paths/develop-ai-solutions-azure-cosmos-db

## О курсе

Основа данных для AI-приложений, векторный поиск и оптимизация запросов в Azure Cosmos DB for NoSQL.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB
- **Предварительные требования:** Программирование на Python; базовое понимание сервисов Azure и облачных вычислений; знакомство со структурами JSON-документов; понимание концепций машинного обучения, включая эмбеддинги и поиск по сходству.

## Чему научитесь

- Модель ресурсов Cosmos DB, интеграция SDK, CRUD-операции и SQL-запросы для AI-приложений.
- Хранение векторных эмбеддингов и similarity-запросы с функцией VectorDistance.
- Оптимизация производительности запросов: анализ паттернов запросов и настройка индексов.

## Модули

1. **Построение запросов к Azure Cosmos DB для NoSQL**. Научиться подключаться к Azure Cosmos DB для NoSQL через SDK, выполнять CRUD-операции с элементами и писать эффективные SQL-запросы, которые минимизируют потребление Request Units (RU). Модуль рассчитан на создание AI-приложений, которые хранят и извлекают JSON-документы. [guide](../modules/build-query-azure-cosmos-db.md)
2. **Реализация векторного поиска в Azure Cosmos DB for NoSQL**. Научиться хранить векторные эмбеддинги в контейнерах Azure Cosmos DB for NoSQL, настраивать векторные политики и индексы, выполнять запросы похожести с функцией VectorDistance, комбинировать векторный поиск с фильтрами и гибридным (full-text) поиском и обновлять эмбеддинги через change feed. [guide](../modules/implement-vector-search-azure-cosmos-db.md)
3. **Оптимизация производительности запросов в Azure Cosmos DB**. Научиться снижать задержку и стоимость запросов (RU) в Azure Cosmos DB for NoSQL для AI-приложений: настраивать range, composite и tuple индексы под шаблоны поиска, выбирать тип векторного индекса (flat, quantizedFlat, diskANN), строить политику индексации, которая балансирует чтение и запись, и выбирать уровень согласованности (consistency level). [guide](../modules/optimize-query-performance-azure-cosmos-db.md)

## Ключевые технологии и понятия

- Account (аккаунт)
- Database (база данных)
- Container (контейнер)
- Item (элемент)
- Partition key
- Request Units (RU/s)
- Manual и Autoscale throughput
- Системные свойства
- Point read
- Single-partition vs cross-partition запрос
- Parameterized query
- Embedding (эмбеддинг)
- Vector policy (векторная политика)
- dataType

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/develop-ai-solutions-azure-cosmos-db
- Модуль «Построение запросов к Azure Cosmos DB для NoSQL»: https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/
- Модуль «Реализация векторного поиска в Azure Cosmos DB for NoSQL»: https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/
- Модуль «Оптимизация производительности запросов в Azure Cosmos DB»: https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/
