# Azure Functions

## Что это и зачем

Azure Functions - это serverless-сервис для запуска кода по событию. По описанию Microsoft, он позволяет строить приложения с меньшим объемом кода, без необходимости разворачивать и поддерживать серверы, и с более низкой стоимостью: инфраструктура облака предоставляет нужные ресурсы, а разработчик сосредотачивается на коде ([pages/05-azure-functions-overview.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview)).

Типовые сценарии из загруженных материалов:
- обработка загрузки файлов: запуск кода при появлении или изменении файла в Blob Storage;
- обработка данных в реальном времени: захват и преобразование данных из потоков событий и IoT до записи в хранилище;
- регулярные задачи по расписанию, например очистка данных по таймеру;
- REST API на HTTP-триггерах;
- реакция на изменения в базе данных (создание или обновление документа);
- обработка очередей сообщений: Azure Queue Storage, Service Bus, Event Hubs;
- stateful-рабочие процессы через Durable Functions;
- интеграция с SaaS через managed connectors (Microsoft 365, Teams, SharePoint) ([pages/05-azure-functions-overview.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview)).

Жизненный цикл разработки включает четыре этапа: написание кода, локальная разработка и отладка, развертывание через CLI, CI/CD или IDE, мониторинг через Azure Monitor и Application Insights ([pages/05-azure-functions-overview.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview)).

## Архитектура и ключевые компоненты

**Function app и hosting plan.** Function app - единица развертывания и управления. При создании приложения нужно выбрать hosting option, который определяет: способ масштабирования, ресурсы каждого экземпляра, поддержку функций вроде Virtual Network и поддержку Linux-контейнеров. Фундаментом служит инфраструктура App Service ([docs/d2-azure-azure-functions-functions-scale.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).

Варианты размещения по данным Microsoft Learn:

| Вариант | Характеристика (из источников) |
|---|---|
| Flex Consumption plan | Рекомендуемый вариант. Быстрое событийное масштабирование, интеграция с виртуальной сетью, оплата по факту использования |
| Premium plan | Всегда прогретые инстансы, неограниченная длительность выполнения, интеграция с VNet |
| Dedicated plan | Запуск в существующем App Service plan с предсказуемым масштабированием и стоимостью |
| Container Apps | Полностью настраиваемые контейнеры в Azure Container Apps |
| Consumption plan (legacy) | Устаревший serverless-план, только Windows для новых приложений; для новых приложений рекомендуется Flex Consumption |

Источник: [pages/05-azure-functions-overview.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview) и [docs/d2-azure-azure-functions-functions-scale.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale).

**Triggers и bindings.** Триггер определяет, как запускается функция. У функции должен быть ровно один триггер. Input binding передает данные в функцию, output binding записывает данные во внешний сервис. Триггер по сути является особым типом входного binding. Bindings необязательны, функция может иметь несколько входов и выходов. Функция получает данные через параметры и отправляет данные через возвращаемое значение ([docs/d0-azure-azure-functions-functions-triggers-bindings.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings)).

**Durable Functions.** Расширение Azure Functions для построения stateful-рабочих процессов в serverless-среде. Разработчик пишет orchestrator, activity и entity functions. Runtime Durable Functions управляет состоянием, чекпоинтами, повторами и восстановлением ([docs/d0-azure-azure-functions-durable-durable-functions-overview.md](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview)).

**Scale controller.** Компонент, который следит за экземплярами host на которых работает приложение и решает, когда добавлять или удалять экземпляры на основе текущей производительности ([docs/d2-azure-azure-functions-functions-monitoring.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-monitoring)).

**Host и language worker.** Telemetry генерируется и host-процессом Functions, и language-specific worker процессом, где выполняется код функции ([docs/d2-azure-azure-functions-functions-monitoring.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-monitoring)).

## Основные понятия (glossary)

| Термин (English) | Определение |
|---|---|
| Azure Functions | Serverless-сервис для запуска кода по событиям, без управления серверами |
| Function app | Единица развертывания и управления, содержащая одну или несколько функций и один hosting plan |
| Trigger | Событие, которое запускает выполнение функции. Каждая функция имеет ровно один триггер |
| Input binding | Декларативное подключение, которое передает данные в функцию (например, из хранилища) |
| Output binding | Декларативное подключение, которое записывает результат функции во внешний сервис |
| Binding expressions | Выражения в описании binding, позволяющие получать метаданные события прямо в сигнатуре метода (упоминаются в примере Event Hubs trigger) |
| Hosting option / plan | Способ размещения (Flex Consumption, Premium, Dedicated, Container Apps, Consumption) |
| Flex Consumption plan | Рекомендуемый serverless-план на Linux с VNet и выбором размера памяти |
| Premium plan | План с прогретыми инстансами (always-ready) и неограниченной длительностью выполнения |
| Dedicated plan | Запуск функций в App Service plan по тарифам App Service |
| Consumption plan | Legacy serverless-план с оплатой за выполнение; для новых приложений рекомендуется Flex Consumption |
| Always-ready instances | Заранее подготовленные инстансы, которые уменьшают задержку холодного старта; оплачиваются, даже если функции не выполняются |
| Cold start | Задержка при подготовке нового инстанса, когда приложение масштабировано до нуля |
| Scale controller | Компонент, принимающий решения о добавлении и удалении инстансов |
| Durable Functions | Расширение для stateful-рабочих процессов в serverless-среде |
| Orchestrator function | Функция, описывающая логику workflow; не должна выполнять I/O |
| Activity function | Функция, выполняющая отдельную задачу, вызываемую из orchestrator |
| Entity function | Функция, управляющая небольшим состоянием (упоминается в описании Durable Functions) |
| Orchestration trigger | Binding, который запускает orchestrator и получает события оркестрации |
| Task hub | Логический контейнер состояния Durable Functions (упоминается как отдельная тема) |
| Durable Task Scheduler | Рекомендуемый бэкенд хранения состояния Durable Functions |
| Access key | Общий секрет для авторизации HTTP-запросов к функциям |
| Managed identity | Identity Microsoft Entra ID, которым платформа управляет без секретов |
| Identity-based connection | Подключение к сервису по identity вместо строки подключения |
| AzureWebJobsStorage | Обязательная настройка подключения к storage-аккаунту, которое использует host |
| Application Insights | Сервис мониторинга, с которым интегрированы Functions |
| OpenTelemetry Exporter | Рекомендуемый способ экспорта телеметрии в Application Insights |

Источники определений: [pages/05-azure-functions-overview.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview), [docs/d2-azure-azure-functions-functions-scale.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale), [docs/d0-azure-azure-functions-functions-triggers-bindings.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings), [docs/d0-azure-azure-functions-durable-durable-functions-overview.md](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview), [docs/d1-azure-azure-functions-durable-durable-functions-bindings.md](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-bindings), [docs/d2-azure-azure-functions-functions-identity-based-connections-tutorial.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-identity-based-connections-tutorial), [docs/d2-azure-azure-functions-function-keys-how-to.md](https://learn.microsoft.com/en-us/azure/azure-functions/function-keys-how-to), [docs/d2-azure-azure-functions-functions-monitoring.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-monitoring).

Примечание: определения "Entity function", "Task hub" и "Always-ready" даны в источниках лишь кратко; подробностей о task hubs и entities в загруженных материалах нет.

## Как работает / типовые сценарии

**Модель выполнения.** Триггер получает событие, Functions host запускает код функции на языковом worker-процессе, функция возвращает результат или записывает данные через output binding. Сложные решения могут состоять из многих функций, которые масштабируются независимо ([training: change feed, 2-understand-azure-function-bindings](https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/2-understand-azure-function-bindings)).

**Пример из источников.** HTTP-триггер с output binding в очередь Storage: функция отвечает на HTTP-запрос и одновременно кладет сообщение в очередь ([docs/d0-azure-azure-functions-functions-triggers-bindings.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings)).

**Таймер.** Timer trigger запускает функцию по расписанию в формате cron-выражения. В примере из источника выражение `0 */5 * * * *` означает запуск каждые пять минут ([docs/d1-azure-azure-functions-functions-bindings-timer.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer)).

**Event Hubs.** Триггер Event Hubs срабатывает на событие в потоке event hub. Для настройки нужен доступ на чтение к event hub; сообщение передается в функцию как строка. Для планов Consumption и Premium масштабирование выполняется через Target Based Scaling ([docs/d1-azure-azure-functions-functions-bindings-event-hubs-trigger.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-event-hubs-trigger)).

**Cosmos DB.** Для Azure Cosmos DB поддерживаются три типа binding: trigger (срабатывает при готовой пачке документов из change feed), input (чтение элементов по point read или SQL-запросу) и output (запись элементов в контейнер). Эти binding поддерживаются только для NoSQL API ([training: change feed](https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/2-understand-azure-function-bindings)).

**Durable Functions: паттерны.** Quickstart из источника демонстрирует два паттерна: function chaining (последовательный вызов activities) и fan-out/fan-in (параллельный вызов activities с последующей агрегацией результатов) ([docs/d1-azure-azure-functions-durable-quickstart-python-vscode.md](https://learn.microsoft.com/en-us/azure/azure-functions/durable/quickstart-python-vscode)).

**Ограничения orchestrator.** Единственный dispatcher-поток выполняет весь код orchestrator на одном инстансе хоста, поэтому код должен быть эффективным и не выполнять I/O. Orchestrator не должен использовать bindings кроме orchestration trigger; для работы с другими сервисами нужно вызывать activity. Orchestrator не должен объявляться как async. Поддержки poison messages в orchestration trigger нет. Возвращаемые значения сериализуются в JSON и сохраняются в таблице истории оркестрации в Azure Table Storage ([docs/d1-azure-azure-functions-durable-durable-functions-bindings.md](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-bindings)).

**Когда не использовать Durable Functions.** Для долгих сценариев, где Durable Functions не применимы, источник рекомендует Dedicated plan ([docs/d2-azure-azure-functions-functions-scale.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)). Выбор между Durable Functions и отдельными Durable Task SDK описан в статье Choose your hosting model, текст которой в загруженных материалах не раскрыт.

**Длительные HTTP-запросы.** HTTP-триггер отвечает не дольше 230 секунд, что связано с idle timeout Azure Load Balancer. Для более долгой обработки источник рекомендует async-паттерн Durable Functions или немедленный ответ с отложенной работой ([docs/d2-azure-azure-functions-functions-scale.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).

## Практика (steps, commands, code only from sources)

**Поддерживаемые языки.** C#, Java, JavaScript, PowerShell, Python, Go; для других языков, например Rust, доступны custom handlers ([pages/05-azure-functions-overview.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview)). Для Durable Functions поддержаны C#, JavaScript, TypeScript, Python, PowerShell и Java ([docs/d0-azure-azure-functions-durable-durable-functions-overview.md](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview)). Python поддерживается только на Linux ([docs/d2-azure-azure-functions-functions-scale.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).

**Локальный запуск Durable-примера (Python, из quickstart):**

Запуск локальных зависимостей через Docker:

```
docker run -d --name dtsemulator -p 8080:8080 -p 8082:8082 \
  mcr.microsoft.com/dts/dts-emulator:latest

docker run -d --name azurite -p 10000:10000 -p 10001:10001 -p 10002:10002 \
  mcr.microsoft.com/azure-storage/azurite
```

Файл `local.settings.json`:

```
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "DURABLE_TASK_SCHEDULER_CONNECTION_STRING": "Endpoint=http://localhost:8080;TaskHub=default;Authentication=None"
  }
}
```

Запуск и вызов (PowerShell, из quickstart):

```
func start
$response = Invoke-RestMethod -Method POST -Uri http://localhost:7071/api/StartChaining
$response
Invoke-RestMethod -Uri $response.statusQueryGetUri
```

Источник: [docs/d1-azure-azure-functions-durable-quickstart-python-vscode.md](https://learn.microsoft.com/en-us/azure/azure-functions/durable/quickstart-python-vscode). Dashboard Durable Task Scheduler доступен на http://localhost:8082 ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/durable/quickstart-python-vscode)).

**Создание проекта и публикация (Core Tools, из справочника):**

```
func init --worker-runtime dotnet --csx
func azure functionapp publish <APP_NAME>
```

Источник: [docs/d1-azure-azure-functions-functions-reference-csharp.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-csharp). Для Go в справочнике описан `func azure functionapp publish <APP_NAME>` для деплоя в существующее function app ([docs/d1-azure-azure-functions-functions-reference-go.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-go)).

**Пример trigger и output binding (C# isolated, из обзора триггеров):**

```
[Function("HttpExample")]
public MultiResponse Run([HttpTrigger(AuthorizationLevel.Function, "get", "post")] HttpRequest req)
```

```
public class MultiResponse
{
    [QueueOutput("outqueue", Connection = "AzureWebJobsStorage")]
    public string[] Messages { get; set; }
    public IActionResult HttpResponse { get; set; }
}
```

Источник: [docs/d0-azure-azure-functions-functions-triggers-bindings.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings).

**Пример Node.js v4 (из обзора триггеров):** функция `app.http` с `extraOutputs` и `output.storageQueue`, строка подключения задается через app setting `MyStorageConnectionAppSetting` ([docs/d0-azure-azure-functions-functions-triggers-bindings.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings)).

**Ключи доступа (из how-to):** key можно получить через портал, Azure CLI или Azure PowerShell; программно - через ARM API List Function Keys и List Host Keys ([docs/d2-azure-azure-functions-function-keys-how-to.md](https://learn.microsoft.com/en-us/azure/azure-functions/function-keys-how-to)). Ключ передается в URL через `?code=` или в заголовке `x-functions-key` ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/function-keys-how-to)).

**Подключения без секретов (из статьи о connections):** для storage-аккаунта со стандартными Azure DNS-адресами используется настройка `AzureWebJobsStorage__accountName` ([docs/d2-azure-azure-functions-functions-identity-based-connections-tutorial.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-identity-based-connections-tutorial)). Полный набор настроек для конкретных сервисов в загруженных материалах не приведен.

Конкретные команды развертывания Flex Consumption, Bicep и Azure CLI в загруженных материалах есть только частично, поэтому в этом разделе они не воспроизведены.

## Безопасность и стоимость

**Безопасность.**
- Приложение работает на инфраструктуре App Service, которая обновляет VM и runtime, изолирует приложения и шифрует секреты. Строки подключения и секреты передаются только внутри Azure ([docs/d2-azure-azure-functions-security-concepts.md](https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts)).
- Никогда не хранить секреты в коде функции. По умолчанию секреты хранятся в application settings, которые шифруются Azure. Для централизованного управления рекомендуется Key Vault references ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts)).
- Managed identity: system-assigned привязана к приложению и удаляется вместе с ним, у приложения может быть только одна; user-assigned - отдельный ресурс, который может назначаться нескольким приложениям ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts)).
- Identity-based connections: Microsoft рекомендует managed identities; shared secrets - "последнее средство" ([docs/d2-azure-azure-functions-functions-identity-based-connections-tutorial.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-identity-based-connections-tutorial)). Таблица: managed identity - Highest, Key Vault - High, shared secret - Low.
- Для HTTP-эндпоинтов источник перечисляет слоистый подход: HTTPS, access keys, App Service Authentication/Authorization, Azure API Management, виртуальная сеть, изоляция ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts)).
- Access keys: типы Function, Host, Master (`_master`, административный доступ к runtime REST API) и System. Ключи шифруются при хранении; по умолчанию в Blob Storage через AzureWebJobsStorage ([docs/d2-azure-azure-functions-function-keys-how-to.md](https://learn.microsoft.com/en-us/azure/azure-functions/function-keys-how-to)). Удаление функции не удаляет и не ротирует ключи; для отзыва ключ нужно явно ротировать или удалить ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/function-keys-how-to)).
- Административные эндпоинты `/admin` можно отключить свойством сайта `functionsRuntimeAdminIsolationEnabled` ([docs/d2-azure-azure-functions-security-concepts.md](https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts)).
- CORS задается на уровне приложения; wildcard источник рекомендует не использовать ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts)).
- Триггеры и bindings не валидируют данные; код должен проверять входные данные и параметризовать SQL-запросы ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts)).
- Для Consumption можно задать дневной лимит GB-sec; при его достижении выполнение останавливается ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts)).

**Стоимость (только то, что есть в источниках).**
- Consumption: оплата по числу выполнений, времени выполнения и использованной памяти, агрегированно по всем функциям приложения ([deep/d1-azure-azure-functions-consumption-plan.md](https://learn.microsoft.com/en-us/azure/azure-functions/consumption-plan)). Время опроса runtime для storage queue trigger не тарифицируется ([deep/d2-azure-azure-functions-functions-bindings-storage-queue-trigger.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-queue-trigger)).
- Flex Consumption: оплата за GB-секунды памяти инстансов при выполнении (минус бесплатный грант, сумма которого в источнике не указана) и за число выполнений (минус бесплатный грант). Минимальный оплачиваемый период - 1000 мс, далее округление вверх до 100 мс. Always-ready инстансы оплачиваются, даже если функции не выполняются ([deep/d1-azure-azure-functions-flex-consumption-plan.md](https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-plan)).
- Premium: оплата по core seconds и памяти инстансов; нет платы за выполнение, есть минимальная месячная стоимость активного плана ([deep/d1-azure-azure-functions-functions-premium-plan.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-premium-plan)).
- Dedicated: оплата по тарифам App Service plan ([docs/d2-azure-azure-functions-functions-scale.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).
- Application Insights: есть бесплатный уровень с дневным лимитом; при его превышении новые логи не появляются в запросах, семплирование включено по умолчанию ([docs/d2-azure-azure-functions-functions-monitoring.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-monitoring)).

**Ограничения и сроки (из таблицы service limits, точные значения):**
- Таймаут по умолчанию: Flex Consumption 30 мин, Premium 30 мин, Dedicated 30 мин, Consumption 5 мин; максимум Consumption 10 мин, остальные планы unbounded ([docs/d2-azure-azure-functions-functions-scale.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).
- Макс. размер запроса 210 МБ, длина строки запроса 4096, длина URL 8192 ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).
- Flex Consumption: размеры инстансов 512 МБ, 2048 МБ или 4096 МБ; до 1000 инстансов ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).
- Consumption: до 200 инстансов на Windows и 100 на Linux ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).
- Consumption на Linux выводится из эксплуатации 30 сентября 2028; приложения v3 на Linux в Consumption перестанут работать после 30 сентября 2026. Windows Consumption пока не затронут ([там же](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).
- Поддержка in-process модели C# заканчивается 10 ноября 2026; рекомендуется isolated worker model ([docs/d1-azure-azure-functions-durable-durable-functions-bindings.md](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-bindings)).

## Частые вопросы для собеседования

**1. Что такое Azure Functions и в чем его отличие от обычного приложения на VM?**
Это serverless-сервис, где разработчик пишет код функции, а инфраструктура обеспечивает ресурсы без необходимости управлять серверами ([pages/05-azure-functions-overview.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview)).

**2. Чем отличаются trigger и binding?**
Trigger запускает функцию и обязательно один на функцию. Bindings необязательны и подключают функцию к сервисам: input передает данные, output записывает результат. Триггер - особый тип входного binding ([docs/d0-azure-azure-functions-functions-triggers-bindings.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings)).

**3. Какие hosting plans есть и какой рекомендовать для новых приложений?**
Flex Consumption (рекомендуемый), Premium, Dedicated, Container Apps и Consumption (legacy). Для новых serverless-приложений источник рекомендует Flex Consumption ([docs/d2-azure-azure-functions-functions-scale.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).

**4. Когда выбрать Premium, а когда Dedicated?**
Premium подходит для непрерывно работающих приложений, нужны прогретые инстансы, длительное выполнение или VNet. Dedicated подходит, когда есть недозагруженные VM, нужна предсказуемая оплата или несколько web и function приложений на одном плане ([docs/d2-azure-azure-functions-functions-scale.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).

**5. Что такое Durable Functions и почему orchestrator нельзя делать async?**
Durable Functions - расширение для stateful-workflow с orchestrator, activity и entity. Orchestrator выполняется на одном dispatcher-потоке и не должен выполнять I/O, поэтому объявлять его async запрещено; для работы с внешними сервисами используют activity ([docs/d1-azure-azure-functions-durable-durable-functions-bindings.md](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-bindings)).

**6. Как безопасно передать строку подключения к базе данных функции?**
Не хранить секреты в коде. Предпочтительно использовать managed identity и identity-based connection; если сервис не поддерживает Entra ID, использовать Key Vault references. Shared secret в app settings - последнее средство ([docs/d2-azure-azure-functions-functions-identity-based-connections-tutorial.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-identity-based-connections-tutorial), [docs/d2-azure-azure-functions-security-concepts.md](https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts)).

**7. Какие ключи доступа есть у HTTP-функции и чем они отличаются?**
Function key дает доступ к конкретной функции, host key - ко всем функциям приложения, master key (`_master`) дает административный доступ к runtime REST API, system key используется расширениями и Durable Task API ([docs/d2-azure-azure-functions-function-keys-how-to.md](https://learn.microsoft.com/en-us/azure/azure-functions/function-keys-how-to)).

**8. Сколько времени может выполняться HTTP-функция и как обойти ограничение?**
HTTP-триггер отвечает не дольше 230 секунд из-за idle timeout Azure Load Balancer. Для долгой обработки - async-паттерн Durable Functions или немедленный ответ с отложенной работой ([docs/d2-azure-azure-functions-functions-scale.md](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)).

## Источники

Использованные файлы (пути относительно базовой папки курса `azure-course`):
- `pages/05-azure-functions-overview.md` - https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview
- `docs/d0-azure-azure-functions-functions-triggers-bindings.md` - https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings
- `docs/d0-azure-azure-functions-durable-durable-functions-overview.md` - https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview
- `docs/d1-azure-azure-functions-durable-durable-functions-bindings.md` - https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-bindings
- `docs/d1-azure-azure-functions-durable-quickstart-python-vscode.md` - https://learn.microsoft.com/en-us/azure/azure-functions/durable/quickstart-python-vscode
- `docs/d1-azure-azure-functions-functions-bindings-timer.md` - https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer
- `docs/d1-azure-azure-functions-functions-bindings-event-hubs-trigger.md` - https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-event-hubs-trigger
- `docs/d1-azure-azure-functions-functions-reference-csharp.md` - https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-csharp
- `docs/d1-azure-azure-functions-functions-reference-go.md` - https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-go
- `docs/d2-azure-azure-functions-functions-scale.md` - https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale
- `docs/d2-azure-azure-functions-security-concepts.md` - https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts
- `docs/d2-azure-azure-functions-functions-monitoring.md` - https://learn.microsoft.com/en-us/azure/azure-functions/functions-monitoring
- `docs/d2-azure-azure-functions-function-keys-how-to.md` - https://learn.microsoft.com/en-us/azure/azure-functions/function-keys-how-to
- `docs/d2-azure-azure-functions-functions-identity-based-connections-tutorial.md` - https://learn.microsoft.com/en-us/azure/azure-functions/functions-identity-based-connections-tutorial
- `deep/d1-azure-azure-functions-flex-consumption-plan.md` - https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-plan
- `deep/d1-azure-azure-functions-consumption-plan.md` - https://learn.microsoft.com/en-us/azure/azure-functions/consumption-plan
- `deep/d1-azure-azure-functions-functions-premium-plan.md` - https://learn.microsoft.com/en-us/azure/azure-functions/functions-premium-plan
- `deep/d2-azure-azure-functions-functions-bindings-storage-queue-trigger.md` - https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-queue-trigger (использован только факт о тарификации опроса)
- `units/d0-training-modules-handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed-2-understand-azure-function-bindings.md` - https://learn.microsoft.com/en-us/training/modules/handle-events-azure-functions-azure-cosmos-db-sql-api-change-feed/2-understand-azure-function-bindings

Не использованы, но релевантны по теме (для дальнейшего расширения): `docs/d2-azure-azure-functions-functions-monitoring.md` (использован), `docs/d2-azure-azure-functions-functions-host-json.md`, `docs/d2-azure-azure-functions-functions-best-practices.md`, `docs/d2-azure-azure-functions-functions-identity-access-azure-sql-with-managed-identity.md`, `docs/d2-azure-azure-functions-consumption-plan.md`, `docs/d2-azure-azure-functions-functions-bindings-cosmosdb-v2.md`.

Пропущено: MCP-навигационные и служебные ответы инструментов, а также страницы, требующие авторизации (баннер "Access to this page requires authorization" присутствует во всех загруженных страницах, поэтому текст мог быть неполным).
