# Использование change feed в Azure Cosmos DB (SQL API) с помощью SDK

**Источник:** https://learn.microsoft.com/en-us/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/

## Цель модуля

Реализовать change feed processor в .NET SDK для Azure Cosmos DB для NoSQL: написать делегат для обработки пакетов изменений и настроить оценку (estimator) количества непрочитанных изменений.

## Ключевые понятия

- **Change feed processor** - компонент .NET SDK, который читает изменения из контейнера, прост в реализации, масштабируется горизонтально и может работать в разных .NET-средах.
- **Monitored container (отслеживаемый контейнер)** - контейнер, в котором отслеживаются вставки и обновления.
- **Lease container (контейнер аренды)** - хранилище состояния для нескольких потребителей change feed; создается заранее.
- **Host (хост)** - экземпляр клиентского приложения, который реагирует на изменения.
- **Delegate (делегат)** - код приложения, реализующий бизнес-логику для каждого пакета изменений; тип `ChangesHandler<T>`.
- **Change feed estimator** - отдельный процессор-«спутник», который измеряет, сколько изменений еще не прочитано.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/1-introduction

В модуле реализуется change feed processor с делегатом на C# для чтения изменений из контейнера. Цели: создать processor в .NET SDK и написать делегат, обрабатывающий пакет изменений на клиенте.

### 2. Возможности change feed в SDK
URL: https://learn.microsoft.com/en-us/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/2-understand-features-sdk

Процессор поддерживает распределенные сценарии, когда обработка делится между несколькими клиентскими приложениями. Четыре компонента: отслеживаемый контейнер, контейнер аренды, хост и делегат. Контейнер аренды нужно создать до настройки процессора.

### 3. Реализация делегата
URL: https://learn.microsoft.com/en-us/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/3-implement-delegate

Делегат типа `ChangesHandler<T>` принимает `IReadOnlyCollection<T>` с изменениями и `CancellationToken`. Каждое изменение - «снимок» элемента, доставляемый с семантикой at-least-once. Делегат можно написать как именованный метод или как анонимную функцию.

### 4. Реализация change feed processor
URL: https://learn.microsoft.com/en-us/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/4-implement-change-feed-processor

Создание processor: получить builder от отслеживаемого контейнера, указать имя процессора и делегат, задать контейнер аренды и имя хоста, затем запустить `StartAsync` и остановить `StopAsync`. Методы builder: `WithInstanceName`, `WithStartTime`, `WithLeaseContainer`, `WithErrorNotification`, `WithMaxItems`, `WithPollInterval`.

### 5. Реализация оценщика change feed
URL: https://learn.microsoft.com/en-us/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/5-implement-change-feed-estimator

Процессор работает как временной указатель. Если он упирается в ресурсы хоста, нужно масштабирование на несколько хостов. Оценщик (estimator) показывает количество непрочитанных изменений и использует тот же контейнер аренды; делегат типа `ChangesEstimationHandler` получает значение оценки.

### 6. Упражнение: обработка событий change feed с SDK
URL: https://learn.microsoft.com/en-us/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/6-exercise-process-change-feed-events-use-sdk

Практика (нужна подписка Azure с правами администратора): создать группу ресурсов, настроить локальную среду, включить провайдеры ресурсов.

### 7. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/7-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 8. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/8-summary

Реализован базовый change feed processor с делегатом и sidecar-оценщик в .NET SDK.

## Важные команды / код / настройки

Делегат как именованный метод и как анонимная функция:

```csharp
static async Task HandleChangesAsync(
    IReadOnlyCollection<Product> changes,
    CancellationToken cancellationToken
)
{
    // Do something with the batch of changes
}

ChangesHandler<Product> changeHandlerDelegate = HandleChangesAsync;
```

```csharp
ChangesHandler<Product> changeHandlerDelegate = async (
    IReadOnlyCollection<Product> changes,
    CancellationToken cancellationToken
) => {
    foreach(Product product in changes)
    {
        await Console.Out.WriteLineAsync($"Detected Operation:\t[{product.id}]\t{product.name}");
    }
};
```

Создание контейнеров-источника и аренды, builder и запуск процессора:

```csharp
Container sourceContainer = client.GetContainer("cosmicworks", "products");
Container leaseContainer = client.GetContainer("cosmicworks", "productslease");

var builder = sourceContainer.GetChangeFeedProcessorBuilder<Product>(
    processorName: "productItemProcessor",
    onChangesDelegate: changeHandlerDelegate
);

ChangeFeedProcessor processor = builder
    .WithInstanceName("desktopApplication")
    .WithLeaseContainer(leaseContainer)
    .Build();

await processor.StartAsync();
// Wait while processor handles items
await processor.StopAsync();
```

Оценщик изменений:

```csharp
ChangesEstimationHandler changeEstimationDelegate = async (
    long estimation,
    CancellationToken cancellationToken
) => {
    // Do something with the estimation
};

ChangeFeedProcessor estimator = sourceContainer.GetChangeFeedEstimatorBuilder(
    processorName: "productItemEstimator",
    estimationDelegate: changeEstimationDelegate)
    .WithLeaseContainer(leaseContainer)
    .Build();
```

## Что запомнить

- Change feed processor состоит из отслеживаемого контейнера, контейнера аренды, хоста и делегата.
- Контейнер аренды нужно создать до настройки процессора; он хранит состояние между потребителями.
- Делегат получает пакеты изменений с семантикой at-least-once, поэтому обработка должна выдерживать повторы.
- Процессор запускается через `StartAsync` и останавливается через `StopAsync`.
- Estimator показывает, сколько изменений ожидает обработки, и помогает решить, нужно ли масштабировать число хостов.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/
- Change feed in Azure Cosmos DB, Change feed processor in Azure Cosmos DB, Use the change feed estimator (названия из источника, URL не приведены)
