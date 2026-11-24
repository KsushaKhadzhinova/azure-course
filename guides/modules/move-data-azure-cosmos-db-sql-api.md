# Перенос данных в Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/move-data-azure-cosmos-db-sql-api/

## Цель модуля

Научиться переносить данные в Azure Cosmos DB for NoSQL и из него с помощью сервисов Azure и открытых инструментов: Azure Data Factory, Kafka Connect, Azure Stream Analytics, Apache Spark (через Synapse Link).

## Ключевые понятия

- **Azure Data Factory (ADF)** - бессерверный сервис извлечения, преобразования и загрузки данных (ETL/ELT). Cosmos DB for NoSQL подключается как linked service.
- **Linked service** - описание подключения к хранилищу; для Cosmos DB в ADF может быть источником (source) или приемником (sink).
- **Managed identity и RBAC** - рекомендуемая аутентификация для ADF: на аккаунте Cosmos DB должны быть включены managed identity и права RBAC.
- **Kafka Connect** - инструмент Apache Kafka для потоковой передачи данных между Kafka и внешними системами; коннектор Azure Cosmos DB работает как source или sink.
- **Topic (топик) и mapping топика на контейнер** - в Kafka все сообщения передаются через топики; каждый топик сопоставляется с контейнером.
- **Azure Stream Analytics output** - вывод результатов потоковой обработки в Cosmos DB for NoSQL (поддерживается только NoSQL API).
- **Upsert** - запись, которая вставляет элемент или обновляет существующий с тем же `id`.
- **Azure Synapse Link / analytical storage** - аналитическое хранилище Cosmos DB, доступ к которому дает Spark в Azure Synapse Analytics; HTAP-подход (гибрид транзакционной и аналитической обработки).
- **Azure Cosmos DB Spark connector** - коннектор `cosmos.olap` (чтение из аналитического хранилища) и `cosmos.oltp` (запись в транзакционное хранилище).

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/move-data-azure-cosmos-db-sql-api/1-introduction

После создания аккаунта часто нужно перенести в него данные. Модуль рассматривает сервисы Azure и открытые инструменты для переноса данных в Cosmos DB for NoSQL и из него. Цели: переносить данные сервисами Azure и через Spark или Kafka.

### 2. Move data by using Azure Data Factory
https://learn.microsoft.com/en-us/training/modules/move-data-azure-cosmos-db-sql-api/2-move-data-by-using-azure-data-factory

ADF извлекает, преобразует и загружает данные без серверов. Для Cosmos DB настраивается linked service (через портал или JSON). При чтении (source) задается SQL-запрос, при записи (sink) - режим записи, например upsert.

### 3. Move data by using a Kafka connector
https://learn.microsoft.com/en-us/training/modules/move-data-azure-cosmos-db-sql-api/3-move-data-by-using-kafka-connector

Коннектор Kafka для Cosmos DB - открытый проект microsoft/kafka-connect-cosmosdb на GitHub (JAR устанавливается вручную). Нужно задать четыре свойства подключения и соответствие топиков контейнерам. Для записи создаются топики и отправляются сообщения, которые попадают в сопоставленный контейнер. Для чтения настраивается source-коннектор, и данные из change feed публикуются в топик Kafka.

### 4. Move data by using Stream Analytics
https://learn.microsoft.com/en-us/training/modules/move-data-azure-cosmos-db-sql-api/4-move-data-by-using-stream-analytics

Azure Stream Analytics обрабатывает потоки в реальном времени и может записывать результаты в Cosmos DB for NoSQL. Настраиваются alias выхода, аккаунт, ключ, база и контейнер (они должны существовать заранее). Результаты записываются как JSON, элементы upsert-ятся по `id`.

### 5. Move data by using the Azure Cosmos DB Spark connector
https://learn.microsoft.com/en-us/training/modules/move-data-azure-cosmos-db-sql-api/5-move-data-by-using-spark-connector

Azure Synapse Link дает HTAP: аналитика над данными Cosmos DB без нагрузки на транзакционную часть. Сначала включается analytical storage на уровне аккаунта и контейнера. Затем Spark читает данные (DataFrame или Spark-таблица) и записывает их в контейнер (append или streaming с checkpoint). Запись в транзакционный контейнер расходует RU и влияет на рабочую нагрузку.

### 6. Exercise: Migrate existing data using Azure Data Factory
https://learn.microsoft.com/en-us/training/modules/move-data-azure-cosmos-db-sql-api/6-exercise-migrate-existing-data-using-azure-data-factory

Практическое задание (около 15 минут) по миграции существующих данных через Azure Data Factory. Нужна подписка Azure с правами администратора; в инструкции: создать resource group, настроить локальное окружение и включить resource providers.

### 7. Knowledge check
https://learn.microsoft.com/en-us/training/modules/move-data-azure-cosmos-db-sql-api/7-knowledge-check

Проверка знаний (около 5 минут). Текст в источнике не приведен.

### 8. Summary
https://learn.microsoft.com/en-us/training/modules/move-data-azure-cosmos-db-sql-api/8-summary

Перенос данных в Cosmos DB и из него выполняется сервисами Azure (Data Factory, Stream Analytics) и открытыми платформами (Apache Spark, Apache Kafka).

## Важные команды / код / настройки

**Linked service в ADF (Managed Identity):**
```
{
    "name": "<example-name-of-linked-service>",
    "properties": {
        "type": "CosmosDb",
        "typeProperties": {
            "accountEndpoint": "https://<cosmos-account-name>.documents.azure.com:443/",
            "authenticationType": "ManagedIdentity"
        }
    }
}
```

**Source в ADF (чтение с фильтром):**
```
{
    "source": {
        "type": "CosmosDbSqlApiSource",
        "query": "SELECT id, categoryId, price, quantity, name FROM products WHERE price > 500",
        "preferredRegions": [
            "East US",
            "West US"
        ]
    }
}
```

**Sink в ADF (upsert):**
```
"sink": {
    "type": "CosmosDbSqlApiSink",
    "writeBehavior": "upsert"
}
```

**Kafka - свойства подключения коннектора:** `connect.cosmos.connection.endpoint` (URI аккаунта), `connect.cosmos.master.key` (ключ аккаунта), `connect.cosmos.databasename` (имя базы), `connect.cosmos.containers.topicmap` (соответствие топиков и контейнеров в формате CSV).

Пример соответствия топиков контейнерам:
```
prodlistener#products,custlistener#customers
```

**Создание топика и запуск producer (из источника):**
```
kafka-topics --create \
    --zookeeper localhost:2181 \
    --topic prodlistener \
    --replication-factor 1 \
    --partitions 1

kafka-console-producer \
    --broker-list localhost:9092 \
    --topic prodlistener
```

**Source-коннектор Kafka Connect (фрагмент конфигурации JSON):** класс `com.azure.cosmos.kafka.connect.source.CosmosDBSourceConnector`, `tasks.max: 1`, конвертеры JsonConverter, `connect.cosmos.task.poll.interval: 100`, `connect.cosmos.offset.useLatest: false`, а также четыре свойства подключения, перечисленные выше. Ключ из примера в источнике здесь не приводится, нужно подставить свой.

**Azure Stream Analytics - настройки выхода Cosmos DB:** Output alias, Account ID (endpoint URI), Account Key, Database, Container name. База и контейнер должны существовать заранее.

**Synapse Link - включение analytical storage (Azure CLI):**
```
az cosmosdb create --name <name> --resource-group <resource-group> --enable-analytical-storage true
```
```
az cosmosdb sql container create --resource-group <resource-group> --account <account> --database <database> --name <name> --partition-key-path <partition-key-path> --throughput <throughput> --analytical-storage-ttl -1
```

**Azure PowerShell:**
```
New-AzCosmosDBAccount -ResourceGroupName <resource-group> -Name <name>  -Location <location> -EnableAnalyticalStorage true
New-AzCosmosDBSqlContainer -ResourceGroupName <resource-group> -AccountName <account> -DatabaseName <database> -Name <name> -PartitionKeyPath <partition-key-path> -Throughput <throughput> -AnalyticalStorageTtl -1
```

**Spark в Azure Synapse Analytics (PySpark):**
```
productsDataFrame = spark.read.format("cosmos.olap")\
    .option("spark.synapse.linkedService", "cosmicworks_serv")\
    .option("spark.cosmos.container", "products")\
    .load()
```
```
create table products_qry using cosmos.olap options (
    spark.synapse.linkedService 'cosmicworks_serv',
    spark.cosmos.container 'products'
)
```
```
productsDataFrame.write.format("cosmos.oltp")\
    .option("spark.synapse.linkedService", "cosmicworks_serv")\
    .option("spark.cosmos.container", "products")\
    .mode('append')\
    .save()
```
Потоковая запись с checkpoint:
```
query = productsDataFrame\
    .writeStream\
    .format("cosmos.oltp")\
    .option("spark.synapse.linkedService", "cosmicworks_serv")\
    .option("spark.cosmos.container", "products")\
    .option("checkpointLocation", "/tmp/runIdentifier/")\
    .outputMode("append")\
    .start()

query.awaitTermination()
```

## Что запомнить

- Для ADF используйте linked service с `ManagedIdentity`; на аккаунте должны быть включены managed identity и RBAC.
- В ADF source читает по SQL-запросу, sink пишет с режимом, например `upsert`.
- В Kafka каждый топик сопоставляется с контейнером (формат `topic#container`), коннектор source публикует изменения из change feed.
- Stream Analytics пишет в Cosmos DB for NoSQL как upsert по `id`; контейнер и база должны существовать заранее.
- Для аналитики без нагрузки на транзакции включайте analytical storage (Synapse Link) на аккаунте и контейнере, а запись через Spark `cosmos.oltp` расходует RU.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/move-data-azure-cosmos-db-sql-api/
- В источнике упоминаются (без ссылок в тексте): Copy and transform data in Azure Cosmos DB for NoSQL by using Azure Data Factory; Kafka Connect for Azure Cosmos DB; Azure Cosmos DB output from Azure Stream Analytics; Configure and use Azure Synapse Link for Azure Cosmos DB; Interact with Azure Cosmos DB using Apache Spark 3 in Azure Synapse Link.
- Репозиторий коннектора: https://github.com/microsoft/kafka-connect-cosmosdb
