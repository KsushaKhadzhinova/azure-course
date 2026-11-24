# Настройка ресурсов Azure Cosmos DB: throughput, консистентность и TTL

**Источник:** https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/

## Цель модуля

Научиться оценивать требования к throughput и консистентности и настраивать параметры аккаунта и контейнера Azure Cosmos DB для NoSQL так, чтобы сбалансировать стоимость и производительность.

## Ключевые понятия

- **Request unit (RU)** - единица стоимости операции, объединяющая CPU, IOPS и память. Каждая операция (чтение, запись, запрос) потребляет RU.
- **RU/s** - пропускная способность в request units в секунду.
- **Provisioned vs serverless** - provisioned резервирует RU/s и оплачивается независимо от использования; serverless оплачивает только фактически потребленные RU, без резервирования.
- **Standard vs autoscale** - standard держит фиксированный RU/s; autoscale масштабируется автоматически между 10% заданного максимума и самим максимумом.
- **Dynamic scaling** - autoscale применяется по партициям и регионам, а не равномерно ко всему ресурсу. По умолчанию включен для аккаунтов, созданных после 25 сентября 2024 года.
- **Dedicated vs shared throughput** - dedicated выделяет RU/s одному контейнеру; shared - пул RU/s на уровне базы, которым пользуются все ее контейнеры, без гарантий для отдельного контейнера.
- **Пять уровней консистентности** - Strong, Bounded staleness, Session (по умолчанию), Consistent prefix, Eventual.
- **Time to live (TTL)** - автоматическое истечение данных через заданное число секунд после последнего изменения.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/1-introduction

Баланс между стоимостью throughput и гарантиями чтения: лишний throughput означает оплату простоя, недостаток - ограничение запросов (rate limiting). Модуль проходит путь от оценки RU до выбора модели throughput, области его действия, уровня консистентности и TTL.

### 2. Оценка throughput и требований в RU
URL: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/2-evaluate-throughput-request-unit-requirements

Для нового приложения обычно начинают с serverless, а затем выбирают модель по мере развития нагрузки. Ориентиры: чтение 1-КБ элемента по ID и ключу партиции около 1 RU при session, consistent prefix или eventual; strong и bounded staleness стоят вдвое больше. Создание или удаление такого элемента около 5 RU, обновление около 10 RU (при менее чем пяти индексированных свойствах). Оценка RU/s: сумма по операциям (частота в секунду × RU на запрос). Точнее измерять: в .NET - свойство `RequestCharge`, в Python - заголовок `x-ms-request-charge`; для постраничных запросов суммируются затраты всех страниц.

### 3. Выбор модели throughput
URL: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/3-choose-throughput-model

Provisioned подходит для устойчивой и высокоутилизируемой нагрузки; serverless - для редкой, пиковой или непредсказуемой. Autoscale стоит 1,5 стандартной ставки за 100 RU/s для аккаунта с одним регионом записи; при равном максимуме выгоднее, когда средняя почасовая нагрузка ниже примерно 66% от фиксированного значения. У аккаунта с несколькими регионами записи standard и autoscale стоят одинаково, поэтому autoscale предпочтительнее. Переключение standard/autoscale возможно у контейнера в любой момент; переход аккаунта serverless на provisioned необратим, а обратно - только через новый аккаунт и миграцию данных.

Матрица выбора:

| Характер трафика | Модель |
|---|---|
| Стабильный, предсказуемый, высокая утилизация | Provisioned, standard |
| Переменный или всплесковый, но устойчивый | Provisioned, autoscale |
| Редкий, пакетный, с простоями | Serverless |

### 4. Настройка throughput на уровне базы и контейнера
URL: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/4-configure-throughput-scope

Dedicated throughput (на контейнер) дает предсказуемость и изоляцию; shared (на базу) дешевле для множества легких контейнеров, но не гарантирует ресурсы каждому. Shared-база содержит не более 25 контейнеров. Минимум: 400 RU/s для standard; для autoscale минимальный максимум 1000 RU/s (масштабирование 100-1000 RU/s). Авторы модуля рекомендуют начинать с dedicated throughput на уровне контейнера; shared - продвинутая опция. Область действия (scope) после создания контейнера не меняется: для смены нужно создать новый контейнер и перенести данные (можно задачей копирования контейнера). Квота по умолчанию - 1 000 000 RU/s на контейнер или shared-базу.

### 5. Оценка и настройка уровней консистентности
URL: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/5-evaluate-configure-consistency

Пять уровней от сильного к слабому: Strong, Bounded staleness, Session, Consistent prefix, Eventual. Session - значение по умолчанию и подходит большинству приложений: клиент видит собственные записи (через session token, который SDK кэширует и передает автоматически). Strong и bounded staleness стоят в два раза больше RU на чтение. Аккаунты с несколькими регионами записи не могут использовать strong. Ограничения bounded staleness: для одного региона минимум 10 операций записи или 5 секунд; для нескольких регионов - 100 000 операций или 300 секунд. Переопределение уровня на запрос может только ослабить консистентность, но не усилить (кроме превью-API `ReadConsistencyStrategy` в .NET SDK v3.46+). Session token привязан к партиции; при переходе между клиентами его нужно передать, например через cookie.

Пример ослабления одного чтения в .NET:

```csharp
ItemRequestOptions options = new()
{
    ConsistencyLevel = ConsistencyLevel.Eventual
};
```

Пример на Python для всего клиента:

```python
client = CosmosClient(
    url=endpoint,
    credential=credential,
    consistency_level="Eventual")
```

### 6. Настройка time to live для хранения данных
URL: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/6-configure-time-to-live-data-retention

TTL удаляет элементы через заданное число секунд после последнего изменения фоновой задачей, которая использует свободные RU. Истекший элемент сразу перестает возвращаться в запросах, даже до физического удаления. Свойство контейнера `DefaultTimeToLive`: не задано или `null` - TTL выключен; `-1` - TTL включен, но без истечения по умолчанию; положительное целое n - истечение через n секунд (максимум 2 147 483 647). TTL на элементе (`ttl`) действует только при включенном TTL контейнера и переопределяет его. Удалить переопределение на элементе можно удалением свойства `ttl`, а не присвоением `null`. TTL-удаления не попадают в change feed по умолчанию; для их учета используйте режим "all versions and deletes".

Таблица поведения:

| DefaultTimeToLive контейнера | ttl элемента | Результат |
|---|---|---|
| 1000 | не задан | Истекает через 1000 с |
| 1000 | 2000 | Истекает через 2000 с |
| 1000 | -1 | Не истекает |
| -1 | 2000 | Истекает через 2000 с (только этот элемент) |
| не задан | 2000 | Не истекает (TTL выключен на уровне контейнера) |

### 7. Упражнение: настройка throughput и консистентности
URL: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/7-exercise-configure-throughput-consistency

Практика (около 30 минут) на C# или Python: настройка autoscale, консистентности и TTL, измерение RU-затрат операций. Нужна подписка Azure.

### 8. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/8-knowledge-check

Итоговый тест модуля (около 5 минут). Вопросы в источнике не приведены.

### 9. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/9-summary

Краткое резюме: RU как единица throughput, выбор модели по форме трафика, компромисс scope throughput между стоимостью и изоляцией, пятиуровневая шкала консистентности (сильнейший нужный уровень ставится по умолчанию, слабее - переопределяется на чтения), TTL как настройка жизненного цикла данных.

## Важные команды / код / настройки

Выделение throughput на уровне базы (.NET):

```csharp
Database database = await client.CreateDatabaseIfNotExistsAsync(
    id: "cosmicworks",
    throughputProperties: ThroughputProperties.CreateManualThroughput(400));
```

Autoscale на контейнере (.NET):

```csharp
Container container = await database.CreateContainerIfNotExistsAsync(
    containerProperties: properties,
    throughputProperties: ThroughputProperties.CreateAutoscaleThroughput(autoscaleMaxThroughput: 1000));
```

То же на Python:

```python
database = client.create_database_if_not_exists(
    id="cosmicworks",
    offer_throughput=400)

container = database.create_container_if_not_exists(
    id="product",
    partition_key=PartitionKey(path="/categoryId"),
    offer_throughput=ThroughputProperties(auto_scale_max_throughput=1000))
```

Azure CLI: `az cosmosdb sql container create` с `--throughput` (standard) или `--max-throughput` (autoscale); для TTL в CLI используется `--ttl`.

Ослабление консистентности для чтения (.NET, один запрос):

```csharp
ItemRequestOptions options = new()
{
    ConsistencyLevel = ConsistencyLevel.Eventual
};

Product item = await container.ReadItemAsync<Product>(
    id: "0A7E57DA-C73F-467F-954F-17B7AFD6227E",
    partitionKey: new PartitionKey("4F34E180-384D-42FC-AC10-FEC30227577F"),
    requestOptions: options);
```

Чтение нескольких элементов с ослаблением (Python):

```python
items = container.read_items(
    items=[("0A7E57DA-C73F-467F-954F-17B7AFD6227E", "4F34E180-384D-42FC-AC10-FEC30227577F")],
    consistency_level="Eventual")
```

Параметры TTL: портал - Scale and Settings, Time to Live; имена свойств: `DefaultTimeToLive` (.NET), `default_ttl` (Python), `--ttl` (CLI).

## Что запомнить

- Один RU - это единая мера стоимости операции; оценку RU/s делайте по частоте операций, а подтверждайте реальным `RequestCharge` или заголовком `x-ms-request-charge`.
- Provisioned выгоден при высокой утилизации, serverless - при редком трафике; autoscale сохраняет гибкость, но не отменяет ограничение запросов (HTTP 429).
- Dedicated throughput на контейнер - разумная отправная точка; shared на уровне базы экономит, но не гарантирует ресурсы.
- Session - разумный уровень по умолчанию; переопределение на запрос может только ослабить консистентность.
- TTL контейнера должен быть включен, иначе TTL элемента не работает.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-resources-throughput-consistency/
- Request units in Azure Cosmos DB, Provision throughput on containers and databases, Choose between standard (manual) and autoscale throughput, Serverless in Azure Cosmos DB, Consistency levels in Azure Cosmos DB, Time to live (TTL) in Azure Cosmos DB, Configure time to live in Azure Cosmos DB for NoSQL (названия из источника, URL не приведены)
