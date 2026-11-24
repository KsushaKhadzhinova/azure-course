# Настройка репликации и управление отказоустойчивостью в Azure Cosmos DB

**Источник:** https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/

## Цель модуля

Научиться распределять данные Azure Cosmos DB по регионам, оценивать стоимость глобальной репликации, настраивать автоматический и ручной failover, а также направлять .NET SDK для NoSQL на конкретный регион.

## Ключевые понятия

- **Глобальное распределение (global distribution)** - репликация данных account'а между регионами Azure; настраивается при создании или позже.
- **Primary region (основной регион)** - регион, выбранный при создании account'а; без multi-region write это единственный регион для записи.
- **Read-only region (регион только для чтения)** - дополнительный гео-реплицированный регион, в котором можно читать данные.
- **Replica set / partition set** - физическая партиция реализована как набор реплик; реплики с одним и тем же значением partition key в разных регионах образуют partition set и пересылают данные друг другу.
- **Single-write region / multi-region write** - направление потока данных между репликами зависит от того, включена ли запись в несколько регионов.
- **Standard provisioned throughput** - стоимость рассчитывается как RU/s x число регионов.
- **Autoscale** - стоимость: минимальные RU/s x число регионов плюс потребление RU в каждом регионе.
- **Automatic failover (автоматический failover)** - при аварии региона записи запись переносится в один из регионов чтения по приоритету.
- **Failover priority (приоритет failover)** - порядок, в котором регионы чтения становятся регионом записи.
- **ApplicationRegion / ApplicationPreferredRegions** - свойства клиентского SDK для выбора региона запросов чтения.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/1-introduction

Azure Cosmos DB глобально распределена по дизайну: данные могут располагаться ближе к пользователям и оставаться доступными при региональных сбоях. Цели модуля: распределить данные по регионам, настроить автоматический и ручной failover, настроить .NET SDK на конкретный регион.

### 2. Принцип репликации
Источник: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/2-understand-replication

Каждый контейнер имеет partition key, по значению которого данные распределяются по физическим партициям внутри региона. Физическая партиция реализована как replica set. Внутри account'а данные реплицируются между replica sets разных партиций (локальное распределение), а replica sets с одним и тем же значением ключа образуют partition set и пересылают данные между регионами (глобальное распределение).

### 3. Распределение данных по регионам
Источник: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/3-distribute-data-across-regions

- Для нового account'а местоположение, выбранное на вкладке Basics, становится основным регионом; если multi-region write не включен, записи возможны только в нем.
- На вкладке Global Distribution включите гео-избыточность, чтобы добавить регион-пару Azure как первую реплику.
- Для существующего account'а регионы добавляются и удаляются на панели Replicate data globally; репликация начинается после сохранения изменений.

### 4. Оценка стоимости глобального распределения
Источник: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/4-evaluate-cost-distributing-data-globally

- Standard provisioned: `RU/s x число регионов`. Пример: 1 000 RU/s при записи в один регион и репликации в пять других регионов дает 1 000 x (1+5) = 6 000 RU/s.
- Autoscale: `минимальные RU/s x число регионов + потребление RU в каждом регионе`. Пример: autoscale 1 000 RU/s, минимум 100 RU/s, 100 x (1+5) = 600 плюс потребленные RU в час по регионам.

### 5. Политики автоматического failover
Источник: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/5-define-automatic-failover-policies

Account с одним регионом записи уязвим к полному отказу дата-центра. По умолчанию автоматический failover выключен; его нужно включить, затем отсортировать регионы чтения по приоритету и сохранить. В примере: регион записи West US 2, регионы чтения East US (приоритет 1) и UK South (приоритет 2). При сбое West US 2 новым регионом записи станет East US; при сбое East US - UK South.

### 6. Ручной failover
Источник: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/6-perform-manual-failovers

Ручной failover можно запустить через портал Azure, например как часть учений по аварийному восстановлению. Для успешного failover и сохранения согласованности данных нужна связность между регионами, поэтому не запускайте его во время общесервисного сбоя Azure Cosmos DB.

### 7. Настройка региона в SDK
Источник: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/7-configure-sdk-region

Для .NET SDK два способа: свойство `ApplicationRegion` (один регион) и `ApplicationPreferredRegions` (приоритетный список). Примеры используют `DefaultAzureCredential` (Microsoft Entra managed identity), `CosmosClientOptions` и `CosmosClientBuilder` с методами `WithApplicationRegion` и `WithApplicationPreferredRegions`. Имена регионов можно задавать строками (например, "UK South") или константами статического класса `Regions` (например, `Regions.UKSouth`).

### 8. Упражнение: подключение к разным регионам
Источник: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/8-exercise-connect-different-regions-sql-api-sdk

Упражнение (15 минут) на подключение SDK к разным регионам Azure Cosmos DB for NoSQL. Требуется подписка Azure с административным доступом; нужно создать группу ресурсов, настроить локальное окружение и включить resource providers.

### 9. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/9-knowledge-check

Итоговый тест модуля (5 минут). Содержимое вопросов в исходных материалах не приведено.

### 10. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/10-summary

Модуль показал, как оценивать варианты глобального распределения, настраивать и тестировать сценарии failover и читать данные из конкретного региона через .NET SDK.

## Важные команды / код / настройки

- Эндпоинт account'а: `https://<cosmos-account-name>.documents.azure.com:443/`.
- Регион клиента: `CosmosClientOptions options = new() { ApplicationRegion = "UK South" };`, либо `ApplicationRegion = Regions.UKSouth`.
- Список предпочтительных регионов: `ApplicationPreferredRegions = regions` (например, "East Asia", "South Africa North", "West US").
- Построитель клиента: `new CosmosClientBuilder(accountEndpoint, credential).WithApplicationRegion(Regions.UKSouth).Build();` и `.WithApplicationPreferredRegions(new List<string> { Regions.EastAsia, Regions.SouthAfricaNorth, Regions.WestUS })`.
- Аутентификация в примерах: `DefaultAzureCredential credential = new DefaultAzureCredential();` (Microsoft Entra managed identity), клиент: `new CosmosClient(accountEndpoint, credential, options)`.
- Формула стоимости standard provisioned: `RU/s x число регионов`.
- Формула стоимости autoscale: `минимальные RU/s x число регионов + RU по регионам`.
- Настройка failover приоритетов в портале: включить automatic failover, отсортировать регионы чтения, сохранить.

## Что запомнить

- Глобальное распределение настраивается через портал или SDK, CLI и PowerShell; стоимость растет пропорционально числу регионов.
- Стоимость provisioned throughput считается как RU/s x число регионов; для autoscale - минимум RU/s x регионы плюс потребление.
- Автоматический failover по умолчанию выключен и требует настройки приоритетов регионов чтения.
- Ручной failover подходит для учений по аварийному восстановлению, но не во время общесервисного сбоя Azure Cosmos DB.
- .NET SDK направляет запросы чтения через ApplicationRegion или ApplicationPreferredRegions.

## Связанные материалы

- Distribute your data globally with Azure Cosmos DB
- Manage an Azure Cosmos account using the Azure portal
