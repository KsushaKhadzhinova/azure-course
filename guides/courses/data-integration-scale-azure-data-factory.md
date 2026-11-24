# Интеграция данных в масштабе с Azure Data Factory

**Источник** https://learn.microsoft.com/en-us/training/paths/data-integration-scale-azure-data-factory

## О курсе

Создание и управление пайплайнами данных в облаке с помощью Azure Data Factory.

- **Уровень:** средний (Intermediate)
- **Роль:** Data Engineer, Data Scientist
- **Продукты и сервисы:** Azure Data Factory
- **Предварительные требования:** Успешный вход на портал Azure; понимание вариантов хранения и вычислений в Azure.

## Чему научитесь

- Компоненты Azure Data Factory и их роль в интеграции данных.
- Методы приема данных между различными хранилищами.
- Типовые трансформации и очистка данных без кода.
- Оркестрация крупномасштабного перемещения и трансформации данных.
- Интеграция пакетов SQL Server Integration Services (SSIS).
- Публикация работы Azure Data Factory между окружениями.

## Модули

1. **Интеграция данных с Azure Data Factory**. Понять, как Azure Data Factory (ADF) автоматизирует перемещение и преобразование данных между хранилищами и вычислительными сервисами: изучить паттерны интеграции (ETL и ELT), процесс работы фабрики, ее компоненты, безопасность, создание linked services, datasets, activities и pipelines, а также типы integration runtime. [guide](../modules/data-integration-azure-data-factory.md)
2. **Приём данных петабайтного масштаба в Azure Data Factory**. Научиться выбирать метод приёма данных в Azure Data Factory, понимать доступные коннекторы, использовать Copy Activity, настраивать self-hosted и Azure integration runtime, а также учитывать требования безопасности при приёме данных. [guide](../modules/petabyte-scale-ingestion-azure-data-factory.md)
3. **Преобразование данных без кода в масштабе с Azure Data Factory**. Научиться выполнять преобразования и очистку данных в Azure Data Factory: визуально, через Mapping Data Flow, с отладкой потоков, подготовкой данных через Wrangling Data Flow, вызовом внешних вычислительных сервисов (например, Azure Databricks) и запуском пакетов SSIS. Модуль отмечает, что Data Factory в Microsoft Fabric является следующим поколением Azure Data Factory. [guide](../modules/code-free-transformation-scale.md)
4. **Оркестрация перемещения и трансформации данных в Azure Data Factory**. Научиться оркестрировать перемещение и трансформацию данных в Azure Data Factory: строить управляющий поток, работать с конвейерами, отлаживать их, добавлять параметры и запускать пакеты SSIS. [guide](../modules/orchestrate-data-movement-transformation-azure-data-factory.md)
5. **Выполнение существующих пакетов SSIS в Azure Data Factory**. Научиться переносить существующие пакеты SQL Server Integration Services (SSIS) в облако через Azure-SSIS integration runtime, настраивать его, запускать пакеты в Azure и оценивать и мигрировать пакеты в Azure. [guide](../modules/execute-existing-ssis-packages-azure-data-factory.md)
6. **Эксплуатация конвейеров Azure Data Factory**. Настроить Git-репозиторий для фабрики разработки, вести ветку функциональности и слияние, развернуть конвейеры через release pipeline (CI/CD), мониторить запуски, настроить Azure Monitor и оповещения, перезапускать конвейеры и понимать основы безопасности Azure Data Factory. [guide](../modules/operationalize-azure-data-factory-pipelines.md)

## Ключевые технологии и понятия

- Pipeline
- Activity
- Linked service
- Dataset
- Integration runtime (IR)
- Parameters
- Managed identity
- ETL / ELT
- Azure Data Factory (ADF)
- Ingestion methods (методы приёма)
- Copy Activity
- Linked service (связанная служба)
- Dataset (набор данных)
- Connectors (коннекторы)

## Для каких ролей полезно

- Data Engineer (DE, инженер данных)
- Data Scientist (DS, специалист по данным)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/data-integration-scale-azure-data-factory
- Модуль «Интеграция данных с Azure Data Factory»: https://learn.microsoft.com/en-us/training/modules/data-integration-azure-data-factory/
- Модуль «Приём данных петабайтного масштаба в Azure Data Factory»: https://learn.microsoft.com/en-us/training/modules/petabyte-scale-ingestion-azure-data-factory/
- Модуль «Преобразование данных без кода в масштабе с Azure Data Factory»: https://learn.microsoft.com/en-us/training/modules/code-free-transformation-scale/
- Модуль «Оркестрация перемещения и трансформации данных в Azure Data Factory»: https://learn.microsoft.com/en-us/training/modules/orchestrate-data-movement-transformation-azure-data-factory/
- Модуль «Выполнение существующих пакетов SSIS в Azure Data Factory»: https://learn.microsoft.com/en-us/training/modules/execute-existing-ssis-packages-azure-data-factory/
- Модуль «Эксплуатация конвейеров Azure Data Factory»: https://learn.microsoft.com/en-us/training/modules/operationalize-azure-data-factory-pipelines/
