# Интеграции Azure Databricks с сервисами Microsoft

**Источник:** https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/

## Цель модуля

Понять семь интеграций Azure Databricks с сервисами Microsoft (Microsoft Fabric, Power BI, Visual Studio Code, Power Platform, Copilot Studio, Microsoft Purview и Microsoft Foundry), их принципы работы, сценарии применения и вопросы безопасности и управления доступом.

## Ключевые понятия

- **Unity Catalog** - центральный уровень управления во всех интеграциях; механизм применения правил зависит от сервиса-потребителя.
- **Mirrored Azure Databricks Catalog (Fabric)** - элемент Fabric, который отражает структуру каталога и создает ярлыки OneLake на Delta-таблицы без копирования данных.
- **OneLake** - хранилище Fabric; Azure Databricks может писать в него по пути ABFS.
- **Credential passthrough** - передача удостоверения пользователя в хранилище; в Azure Databricks не поддерживается на serverless compute.
- **DirectQuery и Import** - режимы Power BI: запросы к Databricks в реальном времени или загрузка данных в модель.
- **OAuth и service principal** - способы аутентификации: удостоверение пользователя передается дальше (и применяются его права) или используются фиксированные учетные данные приложения.
- **Declarative Automation Bundles** (бывшие Databricks Asset Bundles) - описание заданий и конвейеров в YAML для развертывания.
- **Databricks Connect** - подключение локальной среды Python к удаленному кластеру для отладки.
- **Genie space** - интерфейс на естественном языке к данным Databricks, доступный через MCP.
- **Managed MCP Servers** - функция Azure Databricks для подключения инструментов ИИ к Genie и функциям Unity Catalog (в превью).
- **Runtime lineage** - происхождение данных, которое Unity Catalog записывает при выполнении ноутбуков и передает в Purview.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/1-introduction

Azure Databricks интегрируется с Fabric, Power BI, VS Code, Power Platform, Copilot Studio, Purview и Foundry. Интеграции сохраняют политики управления, но механизмы их применения различаются: одни передают удостоверение пользователя, другие используют service principal. Модуль рассматривает семь интеграций.

### 2. Интеграция с Microsoft Fabric
URL: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/2-integration-databricks-microsoft-fabric

Связь двусторонняя. Fabric читает таблицы Unity Catalog без копирования: элемент Mirrored Azure Databricks Catalog создает ярлыки OneLake; короткоживущие учетные данные обновляются каждый час. Важно: Fabric выполняет авторизацию от имени пользователя, который настроил подключение, а не от имени пользователей, которые запрашивают данные, поэтому политики Unity Catalog для потребителей Fabric не действуют. Для настройки нужна привилегия EXTERNAL USE SCHEMA на схемах. Ограничения: нет доступа к представлениям, материализованным представлениям, потоковым таблицам, каталогам Delta Sharing и таблицам с фильтрами строк или масками столбцов; поддерживаются только Delta-таблицы; не работает с рабочими пространствами с private endpoints или IP access lists; lineage Unity Catalog не отслеживает операции в Fabric. Запись из Databricks в OneLake: путь `abfss://<workspace>@onelake.dfs.fabric.microsoft.com/<lakehouse>.lakehouse/Files/`; аутентификация через Microsoft Entra credential passthrough (нужен premium-workspace) или service principal (работает и на serverless compute); service principal нужна роль в рабочем пространстве Fabric. Для обеих схем важно: OneLake security можно включить для элемента зеркала, а для построчной фильтрации на уровне пользователя рекомендуется DirectQuery в Power BI.

### 3. Интеграция с Power BI
URL: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/3-integration-databricks-power-bi

Подключение Power BI Desktop к кластеру или SQL warehouse (лучше для DirectQuery); быстрый старт через Partner Connect. Режимы: Import (загрузка в Power BI, нужны обновления) и DirectQuery (запрос к Databricks для каждого визуала, нужен работающий вычислительный ресурс). С февраля 2026 новые подключения используют драйвер ADBC по умолчанию; существующие остаются на ODBC, пока не изменены вручную (`Implementation="2.0"`). Аутентификация: персональный токен (один пользователь), Microsoft Entra ID SSO (права проверяются для каждого пользователя), service principal (фиксированные учетные данные). Power BI Desktop работает только на Windows. Публикация из Catalog Explorer: Publish to Power BI workspace; нужны Unity Catalog и лицензия Power BI Premium (Premium capacity, Premium Per User или Fabric capacity), включенный XMLA-эндпоинт с Read и Write. Комментарии к столбцам передаются как описания. Для DirectQuery с OAuth Unity Catalog проверяет права каждого пользователя. Power BI tasks в рабочих процессах Databricks обновляют семантические модели после обработки данных; требуется Unity Catalog connection.

Таблица режимов доступа: SSO - права проверяются для каждого пользователя и есть аудит по пользователям; фиксированные учетные данные или Import - все видят одни данные; service principal - видна только его активность; персональный токен - только для разработки и тестирования.

### 4. Интеграция с Visual Studio Code
URL: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/4-integration-databricks-vscode

Расширение Databricks для VS Code: разработка локально, выполнение на удаленных кластерах или serverless compute; запуск ноутбуков как Lakeflow Jobs; несколько проектов в одном рабочем пространстве VS Code. Отладка через Databricks Connect: точки останова, просмотр переменных, пошаговое выполнение; поддерживаются файлы Python и ноутбуки по ячейкам. Тесты pytest выполняются на вычислительных ресурсах Databricks. Развертывание через Declarative Automation Bundles (YAML для Lakeflow Jobs, Lakeflow pipelines и MLOps Stacks) с целевыми окружениями. Синхронизация локальных файлов с папкой рабочей области - однонаправленная; изменения в рабочей области не возвращаются. Для продуктивных конвейеров предпочтительны bundles.

### 5. Интеграция с Power Platform
URL: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/5-integration-databricks-power-platform

Коннектор Azure Databricks (премиум-коннектор) подключает Power Apps и Power Automate к Unity Catalog через SQL warehouse; нужны лицензия Power Apps премиум, учетная запись Microsoft Entra ID и значения Server Hostname и HTTP Path. Типы подключения: OAuth (права пользователя) и service principal. Power Apps: canvas-приложения с чтением и записью (создание, обновление, удаление); Dataverse virtual tables, которые не потребляют емкость Dataverse, но не поддерживают OAuth passthrough, в отличие от прямых подключений (быстрее, только для canvas). Power Automate: выполнение SQL, запуск заданий и получение результатов, отмена, список заданий; для больших объемов используйте пакетные операции. Ограничения: нет поддержки государственных облаков; часть формул PowerFx вычисляется только на локальных данных приложения; коннектор подчиняется лимитам запросов; можно добавить коннектор в политику данных Business. Для конкурентной записи полезны функции параллелизма на уровне строк в новых версиях Databricks Runtime.

### 6. Интеграция с Copilot Studio
URL: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/6-integration-databricks-copilot-studio

Два шаблона: таблицы как источники знаний (knowledge sources) и Genie spaces как инструменты. Для источников знаний выбираются каталог и таблицы; агент запрашивает таблицы через SQL warehouse без копирования данных, и Unity Catalog применяет правила. OAuth передает удостоверение пользователя, service principal выполняет все запросы с одинаковыми правами. Genie подключается по MCP: нужно включить Managed MCP Servers preview и указать Genie Space ID; Genie выполняет аналитику, визуализации и объяснения, а не только поиск. Genie-интеграция в публичном превью. Для нее нужен SQL warehouse типа serverless или pro (classic не поддерживается). Коннектор не работает в GCC, GCC High и China Cloud. OAuth требует, чтобы обе платформы были в одном арендаторе Microsoft Entra. Лимиты Power Platform: 100 вызовов API за 60 секунд. Рекомендуется создавать представления для агентов.

### 7. Интеграция с Microsoft Purview
URL: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/7-integration-databricks-microsoft-purview

Purview читает метаданные (базы, таблицы, столбцы, связи) без доступа к данным. Процесс: регистрация источника и сканирование. Hive metastore: сканирование рабочей области, статический lineage из определений представлений, нужна self-hosted integration runtime, без инкрементального сканирования (каждый раз полное). Unity Catalog: полная иерархия metastore, catalog, schema, tables и views; инкрементальная синхронизация; cloud-native Azure integration runtime через SQL warehouse. Runtime lineage: таблицы и столбцы, записанные Unity Catalog в системные таблицы при выполнении ноутбуков; внешние оркестраторы вроде Azure Data Factory в lineage не попадают; сложные трансформации столбцов могут быть не полностью захвачены. Преимущества: единый каталог, согласованное управление, анализ влияния для соответствия требованиям. Во время миграции можно сканировать оба источника.

### 8. Интеграция с Microsoft Foundry
URL: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/8-integration-databricks-microsoft-foundry

Агенты Foundry подключают Genie spaces через Model Context Protocol (MCP) и коннектор Azure Databricks Genie. Агент не выполняет SQL напрямую, а задает вопросы Genie space, который генерирует SQL, выполняет его и возвращает результат. Аутентификация - OAuth Identity Passthrough (Managed OAuth на базе Microsoft Entra ID рекомендуется; Custom OAuth для других провайдеров). Azure Databricks проверяет права на каждый доступ к Genie space; Genie применяет права Unity Catalog. Нужно включить Managed MCP Servers preview в рабочем пространстве. Ограничения: Genie через MCP не хранит историю диалога, поэтому каждый вопрос обрабатывается отдельно; лимит пять вопросов в минуту при вызове из Foundry; интеграция в публичном превью. Стоимость: оплата агента Foundry и серверных вычислений SQL для Genie.

### 9. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/9-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 10. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/10-summary

Интеграции расширяют lakehouse на аналитику (Fabric, Power BI), разработку (VS Code), приложения (Power Platform), ИИ-агентов (Copilot Studio, Foundry) и управление (Purview), сохраняя Unity Catalog как центр управления. Важно понимать модели безопасности, способы аутентификации и ограничения каждой интеграции.

## Важные команды / код / настройки

Путь записи в OneLake из Databricks:

```
abfss://myWorkspace@onelake.dfs.fabric.microsoft.com/myLakehouse.lakehouse/Files/
```

Права для Fabric-подключения к Unity Catalog: `EXTERNAL USE SCHEMA` на схемах с общими таблицами (у пользователя, который настраивает подключение).

Адреса и параметры, упомянутые в тексте:

- Power BI: Server Hostname и HTTP Path из деталей вычислительного ресурса; для драйвера ADBC/ODBC - `Implementation="2.0"` в Advanced Editor.
- Power Platform: Server Hostname и HTTP Path из SQL warehouse.
- Copilot Studio и Foundry: Genie Space ID; включить Managed MCP Servers preview.
- Declarative Automation Bundles: описание в YAML для Lakeflow Jobs, Lakeflow pipelines, MLOps Stacks.

Лимиты, упомянутые в источнике:

| Интеграция | Ограничение |
|---|---|
| Fabric (чтение из Unity Catalog) | Нет представлений, материализованных представлений, потоковых таблиц, Delta Sharing; только Delta; нет private endpoints и IP access lists |
| Power Platform (коннектор) | Лимиты троттлинга; группировать операции |
| Copilot Studio | 100 вызовов API за 60 секунд |
| Genie через Foundry | 5 вопросов в минуту |
| Genie в Copilot Studio | SQL warehouse типа serverless или pro |

## Что запомнить

- Fabric, читающий Unity Catalog, авторизуется от имени настроившего подключение пользователя, поэтому политики Unity Catalog для его потребителей не действуют.
- Для DirectQuery с OAuth в Power BI Unity Catalog проверяет права каждого пользователя; service principal дает одни и те же данные всем.
- Purview сканирует Unity Catalog инкрементально через SQL warehouse; Hive metastore требует self-hosted runtime и полного сканирования.
- Runtime lineage фиксирует только операции, записанные Unity Catalog; Azure Data Factory в нем не видна.
- Genie через MCP (Copilot Studio, Foundry) в публичном превью, не хранит историю диалога и имеет лимиты вызовов.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/understand-azure-databricks-integrations/
- Модуль "Govern Unity Catalog objects" и другие материалы из источника (URL не приведены в тексте уроков)
