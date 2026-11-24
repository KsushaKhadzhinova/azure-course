# Оркестрация перемещения и трансформации данных в Azure Data Factory

**Источник:** https://learn.microsoft.com/en-us/training/modules/orchestrate-data-movement-transformation-azure-data-factory/

## Цель модуля

Научиться оркестрировать перемещение и трансформацию данных в Azure Data Factory: строить управляющий поток, работать с конвейерами, отлаживать их, добавлять параметры и запускать пакеты SSIS.

## Ключевые понятия

- **Pipeline (конвейер)** - логическая группа действий (activities), которые вместе выполняют задачу; управляется, развертывается и планируется как единое целое.
- **Control flow (управляющий поток)** - оркестрация действий: последовательность, ветвление, циклы, параметры, передача состояния, запуск других конвейеров.
- **Группы действий** - перемещение данных (Copy), трансформация (Data Flow, Azure Function, Spark и др.), управляющие (Get metadata, For Each, Execute Pipeline).
- **Dependency conditions (условия зависимости)** - Succeeded, Failed, Skipped, Completed.
- **Debug run (отладочный запуск)** - тестовый запуск конвейера без публикации, с возможностью точки останова (Debug Until).
- **Parameters и global parameters** - параметры конвейера, связанных служб, потоков данных и глобальные константы, переопределяемые для окружений в CI/CD.
- **Azure-SSIS integration runtime** - среда выполнения пакетов SSIS в Azure.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/orchestrate-data-movement-transformation-azure-data-factory/1-introduction

Цели модуля: понимать управляющий поток, работать и отлаживать конвейеры, добавлять параметры, запускать пакеты. Предварительно нужны: вход в портал Azure, создание групп ресурсов, понимание Azure Data Factory и действия Copy.

### 2. Понимание управляющего потока
URL: https://learn.microsoft.com/en-us/training/modules/orchestrate-data-movement-transformation-azure-data-factory/2-understand-control-flow

Управляющий поток включает цепочки действий (свойство `dependsOn`), ветвление (If Condition; Switch для нескольких ветвей - до 25 именованных случаев и ветка по умолчанию), параметры конвейера, передачу состояния между действиями, циклы (ForEach - может запускать действия параллельно; Until - цикл do-until). Конвейеры запускаются по требованию, по событию (например, появление blob) или по расписанию. Execute Pipeline запускает один конвейер из другого. Для дельта-загрузок используются Lookup и гибкое расписание. Web activity вызывает REST-эндпоинт, Get metadata получает метаданные данных.

### 3. Работа с конвейерами
URL: https://learn.microsoft.com/en-us/training/modules/orchestrate-data-movement-transformation-azure-data-factory/3-work-pipelines

Конвейер - логическая группа действий, которую можно развертывать и планировать одним целым. Действия делятся на: перемещение (Copy), трансформацию (Data Flow, Azure Function, Spark и др.), управление (get metadata, For Each, Execute Pipeline). Действия могут зависеть друг от друга с условиями Succeeded, Failed, Skipped и Completed; независимые действия могут выполняться параллельно.

### 4. Отладка конвейеров
URL: https://learn.microsoft.com/en-us/training/modules/orchestrate-data-movement-transformation-azure-data-factory/4-debug-pipelines

Отладочный запуск не требует публикации изменений. Он реально выполняет конвейер (например, Copy записывает данные), поэтому удобно использовать тестовые папки. Результаты каждого действия видны на вкладке Output. После успешной отладки нужно нажать Publish all. Отладка потока данных (Data Flow Debug) поднимает Spark-кластер, который тарифицируется почасово, включая TTL, поэтому debug-режим стоит выключать. Debug Until задает точку останова. История отладочных запусков хранится 15 дней (вкладка Monitor). Для сложных сценариев может понадобиться тестирование в клонированной песочнице.

### 5. Добавление параметров в компоненты Data Factory
URL: https://learn.microsoft.com/en-us/training/modules/orchestrate-data-movement-transformation-azure-data-factory/5-add-parameters-components

Связанные службы можно параметризовать (например, имя базы на одном SQL-сервере или имя пользователя); встроенная параметризация есть примерно для 50 типов коннекторов, включая Azure SQL Database, Blob Storage, Data Lake Storage Gen2, Azure Cosmos DB for NoSQL, Azure Databricks, SQL Server и др. Для других коннекторов параметры задаются через JSON. Глобальные параметры - константы для выражений конвейера, обращение через `pipeline().globalParameters.<name>`; в CI/CD их можно переопределять для каждого окружения (через ARM-шаблон, режим Git). Параметры потоков данных задаются в настройках потока и передаются из конвейера через Execute Data Flow activity; значения можно задавать выражением конвейера, выражением потока или литералом.

### 6. Выполнение пакетов SSIS
URL: https://learn.microsoft.com/en-us/training/modules/orchestrate-data-movement-transformation-azure-data-factory/6-execute-packages

Azure-SSIS integration runtime выполняет пакеты из SSISDB (Project Deployment Model) и из файловой системы, Azure Files или MSDB (Package Deployment Model). Инструменты SSDT и SSMS позволяют развертывать и запускать пакеты в Azure, а также проверять их совместимость до миграции.

### 7. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/orchestrate-data-movement-transformation-azure-data-factory/7-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 8. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/orchestrate-data-movement-transformation-azure-data-factory/8-summary

Модуль охватил управляющий поток, конвейеры, отладку, параметры и выполнение пакетов. В источнике отмечено, что Data Factory в Microsoft Fabric - следующее поколение Azure Data Factory, а существующие конвейеры можно мигрировать в Fabric Data Factory.

## Важные команды / код / настройки

Выражения и настройки, упомянутые в источнике:

- Ссылка на глобальный параметр: `pipeline().globalParameters.<parameterName>`.
- Зависимость действия: свойство `dependsOn` с условием Succeeded, Failed, Skipped или Completed.
- Switch: до 25 именованных случаев плюс ветка по умолчанию.
- Параметризация связанной службы в JSON: в окне создания связанной службы раздел Advanced, флажок "Specify dynamic contents in JSON format"; либо кнопка {} в Management hub для уже созданной службы.
- Глобальные параметры в CI/CD: в Manage hub выбрать ARM template и включить "Include global parameters in an ARM template" (только в режиме Git).
- Для Data Flow Debug: включить режим отладки потока и выключить его после работы; для тестирования записи в приемник запускайте поток из конвейера.

## Что запомнить

- Конвейер объединяет действия, которые развертываются и планируются вместе.
- Условия зависимостей (Succeeded, Failed, Skipped, Completed) определяют порядок выполнения; независимые действия идут параллельно.
- Debug запускает конвейер реально: данные копируются, поэтому используйте тестовые папки.
- Выключайте Data Flow Debug, так как сессия тарифицируется почасово.
- Параметры и глобальные параметры позволяют переиспользовать конвейеры и переопределять их для окружений.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/orchestrate-data-movement-transformation-azure-data-factory/
- What is Data Factory in Microsoft Fabric?; migration planning guide; Parameterize linked services in Azure Data Factory (упомянуты в источнике, URL не приведены)
