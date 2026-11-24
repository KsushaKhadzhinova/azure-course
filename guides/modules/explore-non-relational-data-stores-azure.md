# Нереляционные хранилища данных в Azure и Azure Cosmos DB

**Источник:** https://learn.microsoft.com/en-us/training/modules/explore-non-relational-data-stores-azure/

## Цель модуля

Понять, чем нереляционные (NoSQL) хранилища отличаются от реляционных, описать ключевые возможности Azure Cosmos DB, выбрать один из пяти API Cosmos DB под существующие навыки и данные, а также знать, когда Cosmos DB подходит и когда нет.

## Ключевые понятия

- **NoSQL-базы данных** - хранят данные в структурах вроде документов, графов, key-value и column-family, а не в реляционных таблицах.
- **Azure Cosmos DB** - полностью управляемая (PaaS) облачная БД для нереляционных данных с глобальным масштабированием.
- **Schema-agnostic (без жесткой схемы)** - элементы одного контейнера могут иметь разную структуру.
- **Account / Database / Container / Item** - четыре уровня иерархии ресурсов Cosmos DB.
- **Partition key и логическая партиция** - свойство, распределяющее данные; каждая логическая партиция вмещает до 20 GB.
- **Request Unit (RU/s)** - единица стоимости операций; 1 RU примерно равен чтению одного элемента 1 KB по ID и partition key.
- **Dedicated / Shared / Serverless throughput** - варианты выделения пропускной способности: на контейнер, на базу (до 25 контейнеров), либо оплата за фактически потребленные RU без предварительного резервирования (serverless ограничен одним регионом Azure).
- **Autoscale** - автоматическая подстройка RU/s в пределах заданного максимума.
- **Уровни согласованности** - strong, bounded staleness, session, consistent prefix, eventual.
- **Fabric mirroring** - репликация операционных данных Cosmos DB для NoSQL в Microsoft Fabric без ETL и без расхода RU.
- **API Cosmos DB** - интерфейсы совместимости: NoSQL, MongoDB, Table, Apache Cassandra, Apache Gremlin.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/explore-non-relational-data-stores-azure/1-introduction

Реляционная модель бывает слишком жесткой и требует тонкой настройки производительности. NoSQL-модели хранят данные как документы, графы, key-value или column-family. Azure Cosmos DB - масштабируемый облачный сервис для NoSQL-данных.

### 2. Описание Azure Cosmos DB
Источник: https://learn.microsoft.com/en-us/training/modules/explore-non-relational-data-stores-azure/2-describe-azure-cosmos-db

- Cosmos DB - PaaS: инфраструктура, обновления и резервное копирование ведутся Microsoft.
- Иерархия: account (без ограничения объема данных и throughput), database (логическое пространство имен), container (основная единица хранения и масштабирования; здесь задаются partition key, throughput, indexing policy и TTL), items (документы, строки, узлы или ребра в зависимости от API).
- Партиционирование: ключ с большим числом значений и равномерным распределением важен для сбалансированной пропускной способности.
- Индексы создаются автоматически для всех свойств; схему заранее задавать не нужно.
- Глобальное распределение: регионы добавляются в любой момент; при multi-region writes пользователи пишут в ближайший регион. По источнику, у аккаунтов с multi-region writes SLA доступности 99.999%; чтение и запись укладываются в 10 мс на 99-м перцентиле, средняя задержка чтения обычно 4 мс или меньше, записи - 5 мс или меньше.
- Уровни согласованности: **Strong** - каждое чтение видит последнюю запись; **Bounded staleness** - чтения отстают на настраиваемый интервал (по времени или числу версий); **Session** - согласованность в пределах клиентской сессии, самый используемый уровень; **Consistent prefix** - чтения не видят записи вне порядка, но могут быть устаревшими; **Eventual** - реплики сходятся со временем, самая слабая гарантия и самая высокая доступность.
- Варианты throughput: **Dedicated** - выделен контейнеру; **Shared** - задается на уровне базы и делится между контейнерами (до 25); **Serverless** - без предварительного резервирования, оплата за потребленные RU, подходит для непредсказуемого трафика, ограничен одним регионом.
- Autoscale: задается максимум RU/s, емкость подстраивается автоматически.
- Подходит для IoT и телеметрии, игр, розницы и e-commerce, web и mobile приложений. Не подходит для сложных многотабличных join (лучше Azure SQL Database) и для крупных аналитических нагрузок (рекомендован Microsoft Fabric).

### 3. API Azure Cosmos DB
Источник: https://learn.microsoft.com/en-us/training/modules/explore-non-relational-data-stores-azure/3-cosmos-db-apis

API выбирается при создании аккаунта и определяет формат данных, язык запросов и клиентские библиотеки; внутренний формат хранения един. Главная выгода - переносимость существующих приложений. Пять поддерживаемых API:

- **Cosmos DB for NoSQL** - нативный API, JSON-документы, SQL-подобный запрос. Рекомендуется для высоких нагрузок с SLA 99.999%, мгновенным автомасштабированием и автоматическим failover между регионами (ранее назывался SQL API). Поддерживает Fabric mirroring.
- **Cosmos DB for MongoDB** - совместим с драйверами MongoDB, хранит данные в BSON, использует MongoDB Query Language (например, `db.products.find({id: 123})`). Для полного набора возможностей MongoDB Microsoft рекомендует отдельный сервис Azure DocumentDB.
- **Cosmos DB for Table** - модель "ключ-значение" в таблицах, как Azure Table Storage; строки идентифицируются парой PartitionKey и RowKey; дает большую масштабируемость, глобальное распределение и автоматические вторичные индексы.
- **Cosmos DB for Apache Cassandra** - совместим с Apache Cassandra, column-family модель, язык CQL; подходит для миграции Cassandra-нагрузок.
- **Cosmos DB for Apache Gremlin** - графовая модель (вершины и ребра), язык Gremlin; подходит для соцсетей, рекомендаций, обнаружения мошенничества и иерархий организаций.
- Azure Cosmos DB for PostgreSQL - отдельное предложение, которое уходит на вывод из эксплуатации и не рекомендуется для новых проектов.

### 4. Упражнение: исследование Azure Cosmos DB
Источник: https://learn.microsoft.com/en-us/training/modules/explore-non-relational-data-stores-azure/4-exercise-explore-cosmos-db

Практическая работа (15 минут): самостоятельно исследовать Azure Cosmos DB. Требуется подписка Azure с административным доступом.

### 5. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/explore-non-relational-data-stores-azure/5-knowledge-check

Итоговый тест модуля (3 минуты). Содержимое вопросов в исходных материалах не приведено.

### 6. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/explore-non-relational-data-stores-azure/6-summary

Azure Cosmos DB - глобально масштабируемое решение для нереляционных данных. Модуль научил описывать ключевые возможности, определять API и подготавливать экземпляр Cosmos DB. Для дальнейшего развития упоминается сертификация Azure Data Fundamentals.

## Важные команды / код / настройки

- Запрос для Cosmos DB for NoSQL: `SELECT * FROM customers c WHERE c.id = "joe@litware.com"`.
- Запрос для Cosmos DB for MongoDB: `db.products.find({id: 123})`.
- Адрес строки Cosmos DB for Table: `https://endpoint/Customers(PartitionKey='1',RowKey='124')`.
- Запрос для Cosmos DB for Apache Cassandra: `SELECT * FROM Employees WHERE ID = 2` (CQL).
- Gremlin для Cosmos DB for Apache Gremlin: `g.addV('employee').property('id', '3').property('firstName', 'Alice')`, `g.V('3').addE('reports to').to(g.V('1'))`, `g.V().hasLabel('employee').order().by('id')`.
- Лимиты и параметры: логическая партиция до 20 GB; Shared throughput - до 25 контейнеров; serverless - один регион Azure.

## Что запомнить

- Cosmos DB - PaaS для нереляционных данных с гибкой схемой, глобальным распределением и низкой задержкой.
- Четыре уровня иерархии: account, database, container, items; partition key выбирается на уровне контейнера.
- Пять уровней согласованности позволяют выбрать компромисс между строгостью и задержкой; session - самый распространенный.
- Выбор throughput: dedicated, shared или serverless; serverless не подходит для многорегиональных сценариев.
- API выбирается под существующие навыки и данные: NoSQL (нативный), MongoDB, Table, Cassandra, Gremlin.
- Cosmos DB не подходит для сложных join между таблицами и для крупной аналитики.

## Связанные материалы

- Azure Data Fundamentals (сертификация Microsoft)
