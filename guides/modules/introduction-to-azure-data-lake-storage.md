# Введение в Azure Data Lake Storage

**Источник:** https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-data-lake-storage/

## Цель модуля

Понять назначение озера данных (data lake), возможности Azure Data Lake Storage Gen2 (безопасность, производительность, избыточность), отличия от Blob Storage, этапы обработки больших данных и типовые аналитические сценарии.

## Ключевые понятия

- **Data lake (озеро данных)** - репозиторий данных в исходном формате (обычно blob или файлы), который позволяет хранить структурированные, полуструктурированные и неструктурированные данные.
- **Azure Data Lake Storage Gen2** - масштабируемое, безопасное и экономичное озеро данных для аналитики, построенное на Azure Blob Storage.
- **Hierarchical namespace (иерархическое пространство имён)** - каталоги и поддиректории с метаданными; переименование и удаление каталога выполняются одной атомарной операцией.
- **Azure RBAC и ABAC** - грубый контроль доступа на уровне ролей и уточнение условиями (например, по тегу).
- **POSIX ACL** - детальные права на уровне каталога и файла.
- **Избыточность** - LRS, ZRS, GRS/RA-GRS, GZRS/RA-GZRS.
- **Data swamp (болото данных)** - озеро без управления данными и качества, которое становится бесполезным.
- **Этапы обработки больших данных** - ingest, store, prep and train, model and serve.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-data-lake-storage/1-introduction

Во многих организациях BI-решения на реляционных БД плохо работают с неструктурированными данными из-за стоимости и сложности. Озеро данных решает эту проблему: файловое хранилище с высокой масштабируемостью, из которого данные потребляются в технологиях больших данных, таких как Apache Spark. Azure Data Lake Storage Gen2 - облачная реализация такого озера в Azure.

### 2. Понимание Azure Data Lake Storage Gen2
Источник: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-data-lake-storage/2-azure-data-lake-gen2

- **Открытость**: иерархическая файловая система доступна через открытые API; данные можно использовать в Azure Databricks и Microsoft Fabric без перемещения. Поддерживаются открытые форматы Parquet и Delta Lake.
- **Безопасность**: RBAC (грубый доступ), ABAC (условия на роли), POSIX ACL (файлы и каталоги). Права не наследуются автоматически после создания дочернего элемента; можно задать права по умолчанию для родительского каталога, которые применяются при создании новых элементов. Данные шифруются at rest ключами Microsoft или клиента.
- **Производительность**: иерархия каталогов снижает вычислительные ресурсы и время обработки.
- **Избыточность**: LRS (внутри одного дата-центра), ZRS (между зонами доступности в регионе), GRS/RA-GRS (во вторичный регион), GZRS/RA-GZRS (зоны и регион). Стандартные учётные записи general-purpose v2 поддерживают все варианты, premium block blob - LRS и ZRS в отдельных регионах.
- **Планирование**: учитывайте типы данных, преобразования, кто получает доступ и типовые паттерны доступа, чтобы озеро не превратилось в data swamp.

### 3. Включение Azure Data Lake Storage Gen2 в Azure Storage
Источник: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-data-lake-storage/3-create-data-lake-account

Data Lake Storage Gen2 включается как возможность учётной записи Standard general-purpose v2 (чаще всего) или Premium block blob. При создании аккаунта в портале включается опция **Enable hierarchical namespace** на вкладке Advanced. Для существующего аккаунта доступна миграция (Data Lake Gen2 upgrade), которая необратима.

### 4. Сравнение Azure Data Lake Storage и Azure Blob Storage
Источник: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-data-lake-storage/4-azure-data-lake-and-blob-storage

- Blob Storage хранит объекты в плоском пространстве имён; символ `/` в имени создаёт лишь виртуальные «папки».
- Data Lake Storage Gen2 использует иерархическое пространство имён, поэтому операции с каталогами выполняются атомарно, а не поэлементно.
- Без аналитики (архив, медиа, сайты) можно оставить Blob Storage без иерархического пространства имён.
- Для аналитики включайте Enable hierarchical namespace; приложения могут обращаться к данным и через Blob API, и через API файловой системы Data Lake Storage Gen2.

### 5. Этапы обработки больших данных
Источник: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-data-lake-storage/5-stages-for-processing-big-data

Четыре этапа, общие для архитектур больших данных:
- **Ingest** - приём данных: пакетно через конвейеры Microsoft Fabric, в реальном времени через Azure Event Hubs, Azure Stream Analytics или Microsoft Fabric Real-Time Intelligence.
- **Store** - хранение; Data Lake Storage Gen2 как безопасное и масштабируемое хранилище, совместимое с популярными технологиями.
- **Prep and train** - подготовка данных и обучение моделей: Azure Databricks, Microsoft Fabric, Azure Machine Learning.
- **Model and serve** - представление данных пользователям: Microsoft Power BI, аналитические нагрузки Microsoft Fabric.

### 6. Сценарии аналитики с Data Lake Storage Gen2
Источник: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-data-lake-storage/6-use-cases

- **Big data**: распределённая обработка Apache Spark в Azure Databricks и Microsoft Fabric («три V» - объём, разнообразие, скорость).
- **Хранилище данных**: ETL-конвейеры (например, в Azure Synapse Analytics или Microsoft Fabric) извлекают данные из Azure SQL Database или Azure Cosmos DB, складывают в озеро, затем загружают в хранилище данных и визуализируют в Power BI.
- **Аналитика в реальном времени**: события из Azure Event Hubs обрабатываются Azure Stream Analytics (агрегация по временным окнам) и записываются в Data Lake Storage Gen2.
- **Data science и ML**: Apache Spark и Python; Azure Machine Learning обучает модели на данных из контейнеров Data Lake Storage Gen2.

### 7. Оценка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-data-lake-storage/7-knowledge-check

В исходных материалах вопросы не приведены.

### 8. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-data-lake-storage/8-summary

Data Lake Storage Gen2 - доступное, безопасное, долговечное, масштабируемое и резервируемое облачное хранилище, которое обслуживает Azure Databricks и Microsoft Fabric без перемещения данных.

## Важные команды / код / настройки

Код и команды в уроках не приведены. Настройки и параметры из уроков:
- Тип учётной записи: Standard general-purpose v2 или Premium block blob.
- Параметр: **Enable hierarchical namespace** (вкладка Advanced при создании аккаунта).
- Варианты избыточности: LRS, ZRS, GRS, RA-GRS, GZRS, RA-GZRS.
- Открытые форматы данных: Parquet и Delta Lake.

## Что запомнить

- Data Lake Storage Gen2 - это возможности Blob Storage, включаемые иерархическим пространством имён, а не отдельный сервис.
- Иерархическое пространство имён даёт атомарные операции с каталогами и лучшую производительность аналитики.
- Доступ контролируется в три уровня: RBAC (роли), ABAC (условия), POSIX ACL (файлы и каталоги).
- Четыре этапа обработки: ingest, store, prep and train, model and serve.
- Без управления данными и качеством озеро превращается в data swamp; планируйте структуру и governance заранее.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-data-lake-storage/
- Introduction to Azure Data Lake Storage Gen2 (упомянуто в уроке 8); Azure Databricks, Microsoft Fabric, Azure Synapse Analytics, Azure Event Hubs, Azure Stream Analytics (упомянуты в уроках модуля)
