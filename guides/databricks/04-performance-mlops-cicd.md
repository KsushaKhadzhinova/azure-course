# Производительность, MLOps и CI/CD в Azure Databricks

Конспект для подготовки. Охватывает настройку производительности Spark и Databricks, мониторинг и устранение неполадок, CI/CD и DevOps, MLflow и машинное обучение, а также Databricks SQL и BI. Материал собран из документации Microsoft Learn (сохраненные Markdown-копии в папках `docs2`, `docs`) и из конспектов модулей Learn, которые уже есть в проекте (`guides/modules`). Утверждения привязаны к источникам; там, где источники не дают ответа, это отмечено в разделе «Пробелы в источниках».

Соглашения: термины Spark и Databricks оставлены на английском (partitioning, shuffle, skew, spill, Photon, Git folder, Declarative Automation Bundles и т. д.). Блоки кода приведены только там, где они есть в источниках.

---

## 1. Производительность Spark и Databricks

### 1.1. Сначала диагностика, потом тюнинг

Главное правило: сначала понять, где тратится время, и только потом менять настройки. Spark UI показывает, какие jobs выполнялись, сколько длилась каждая stage, сколько данных переместилось по сети и где упали задачи. Рекомендуемый порядок из гайда Spark UI:

1. Открыть **Jobs Timeline** и найти основные проблемы.
2. Посмотреть самую долгую stage (longest stage).
3. Проверить наличие skew или spill.
4. Определить, является ли самая долгая stage I/O-bound.
5. Искать другие причины медленной stage.

Если на таймлайне видны упавшие jobs, длинные разрывы между jobs или много мелких jobs, дальнейшие шаги пропускаются, и нужно перейти к странице, посвященной этому паттерну.

### 1.2. Партиционирование и liquid clustering

Источник: гайд «When to partition tables on Azure Databricks».

- Большинство таблиц объемом менее 100 ТБ не нуждаются в явном партиционировании. Delta Lake для неразделенных таблиц автоматически использует **ingestion time clustering**, что дает производительность, близкую к партиционированию по датам, без ручной настройки.
- Пороги из документа:
  - менее 1 ТБ - **не партиционировать**;
  - от 1 ТБ до 100 ТБ - использовать **liquid clustering** вместо партиционирования, так как партиционирование чаще вредит производительности, чем помогает;
  - 100 ТБ и больше - партиционирование может помочь, но Databricks рекомендует сначала liquid clustering и проверить результат.
- Для партиций важно, чтобы каждая содержала не менее 1 ГБ данных. Таблицы с меньшим числом крупных партиций обычно работают быстрее, чем таблицы с множеством мелких.
- Колонки партиционирования должны быть top-level. Нельзя партиционировать по complex types (StructType, MapType, ArrayType, VariantType) и по полям структуры (`struct_col.field`). Liquid clustering распознает поле структуры как ключ кластеризации.
- Неэффективная стратегия партиционирования может ухудшить производительность и потребовать полной перезаписи данных, что дорого для больших таблиц.
- Для конвертации партиционированной Delta-таблицы в liquid clustering документ использует конструкцию `ALTER TABLE ... REPLACE PARTITIONED BY WITH CLUSTER BY` (в тексте без полного примера).
- Если таблица часто изменяется через `UPDATE` или `MERGE`, чтобы сохранить ingestion time clustering, Databricks рекомендует liquid clustering по колонке, соответствующей порядку вставки (event timestamp или дата создания).

Ключевой вывод для собеседования: в современных рекомендациях Databricks партиционирование перестает быть первым выбором; по умолчанию используется liquid clustering.

### 1.3. Shuffle

Shuffle - перемещение данных между executors при join, aggregation, repartition и других операциях, требующих группировки по ключу. В Spark UI это колонки Shuffle Read и Shuffle Write, а в DAG - узлы Exchange. В query profile shuffle описан как дорогая операция, поскольку перемещает данные между executors.

Способы снижения shuffle (модуль «Monitor, troubleshoot, optimize workloads»):

- ранняя фильтрация и выбор только нужных колонок до join и aggregation;
- broadcast join для малых таблиц;
- отказ от лишних `repartition()`;
- bucketing или партиционирование, если таблицы часто join-ятся по одному ключу.

Число партиций shuffle задается параметром `spark.sql.shuffle.partitions`. Значение по умолчанию в справочнике Spark config - `auto`. В модуле рекомендуется явно выставлять то же значение:

```
spark.conf.set("spark.sql.shuffle.partitions", "auto")
```

### 1.4. Перекос данных (skew)

Skew - неравномерное распределение данных: часть задач получает значительно больше работы, и stage ждет самые медленные задачи.

Как обнаружить: в **Summary Metrics** стадии сравнить **Max duration** с 75-м перцентилем. Если Max больше 75-го перцентиля на 50 % и более, вероятен перекос. Типичные причины: неравномерные значения ключа, null-значения, попавшие в одну партицию, временное партиционирование.

Как исправить:

- **Adaptive Query Execution (AQE)** - в модуле указано, что он включен по умолчанию;
- **salting** ключей (соль: добавление случайного суффикса к ключу для распределения горячих значений);
- **broadcast** малых таблиц;
- для SQL-хранилища insight `DATA_SKEW` рекомендует «review the data distribution, then use key salting or pre-aggregation to balance the workload» (проверить распределение, затем применить salting или предварительную агрегацию).

Связь со spill: spill часто сопутствует перекосу, поэтому сначала устраняется перекос.

### 1.5. Spill и кеширование

**Spill** - сброс промежуточных данных на диск, когда памяти не хватает. В Spark UI смотрят метрики Shuffle Spill (Memory) и Shuffle Spill (Disk). Любой ненулевой spill - признак давления на память.

Что делать (из модуля):

- увеличить память (более крупные worker-узлы);
- увеличить число партиций shuffle (`spark.sql.shuffle.partitions = auto`);
- ранний выбор колонок и фильтрация;
- если есть перекос - сначала исправить его.

**Кеширование** бывает двух видов:

- **Disk cache** (раньше назывался Delta cache) автоматически кеширует Parquet-данные на локальных дисках worker-узлов. Признак недокеширования - повторные чтения (высокий Input в стадиях). Признак переизбытка - давление на память.
- **Spark cache** (`.cache()`, `.persist()`) не освобождается сам. Его нужно явно снимать через `.unpersist()`.

Проверка состояния кеша и AQE в ноутбуке:

```
spark.conf.get("spark.databricks.io.cache.enabled")
spark.conf.get("spark.databricks.optimizer.adaptive.enabled")
```

```
df.unpersist()
```

### 1.6. Adaptive Query Execution и broadcast join

AQE во время выполнения пересматривает план. По материалам модуля:

- AQE конвертирует sort-merge join в broadcast join, если одна из таблиц меньше порога `spark.databricks.adaptive.autoBroadcastJoinThreshold`, который по умолчанию равен **30 МБ**;
- AQE помогает при перекосе (см. 1.4).

Практический вывод: broadcast join экономит shuffle, но применим только к малым таблицам. Если размер стороны join превышает порог, Spark выполнит обычный shuffle join.

### 1.7. Размер файлов, OPTIMIZE, Predictive Optimization и auto compaction

Проблема small files: много мелких файлов увеличивает время сканирования. Инструменты:

- **Liquid clustering** и `OPTIMIZE`. Гайд по размеру файлов: «In Databricks Runtime 13.3 LTS and above, Databricks recommends using clustering for table layout». Для таблиц больше 1 ТБ рекомендуется регулярно запускать `OPTIMIZE`. Если включен liquid clustering, `OPTIMIZE` автоматически кластеризует данные.
- **Predictive optimization** - для Unity Catalog managed tables автоматически запускает `OPTIMIZE` и `VACUUM`. Работает асинхронно на serverless compute. Databricks рекомендует его как основной способ обслуживания.
- **Auto compaction** (`autoOptimize.autoCompact` на уровне таблицы или `spark.databricks.delta.autoCompact.enabled` на уровне сессии) объединяет мелкие файлы синхронно на кластере, выполняющем запись. Predictive optimization и auto compaction независимы и могут использоваться вместе.
- **Optimized writes** и auto compaction всегда включены для операций `MERGE`, `UPDATE` и `DELETE`; отключить нельзя.
- Для Unity Catalog managed tables ручные рекомендации по размеру файлов не применяются: Databricks настраивает их автоматически.

Команда для ручного пересжатия Iceberg-таблицы после смены ключей кластеризации (из справочника по Iceberg):

```
OPTIMIZE main.default.iceberg_table FULL;
```

Заметки из справочника по OPTIMIZE: `OPTIMIZE table_name` сжимает мелкие файлы и инкрементально кластеризует данные; `OPTIMIZE table_name FULL` переписывает файлы, не соответствующие текущим ключам кластеризации; для `OPTIMIZE` с liquid clustering нельзя указывать `ZORDER BY`.

Предупреждение: Z-order работает только внутри партиций, поэтому для партиционированных таблиц его эффект ограничен.

### 1.8. Photon

Photon - нативный векторный движок Azure Databricks на C++. Catalyst по-прежнему строит план, а исполнение обрабатывает Photon пакетами (batches) колонок. Ключевые эффекты из документации:

- ускорение joins и shuffles (hash joins вместо sort-merge joins);
- нативный Parquet writer, ускоряющий запись Delta, Iceberg и Parquet, включая `MERGE INTO`, `UPDATE`, `DELETE`, `CTAS`;
- filter pushdown и row-group skipping;
- неподдерживаемые операции автоматически откатываются на обычный Spark runtime.

Ограничения эффекта: запросы, которые выполняются менее двух секунд, практически не выигрывают, так как время уходит на планирование и scheduling.

Включение: Photon включен по умолчанию на serverless compute, SQL warehouses и serverless Lakeflow pipelines. Для классических all-purpose и jobs compute Photon включен по умолчанию, но его можно переключить в чекбоксе «Use Photon Acceleration» в разделе Performance. При создании через Clusters API или Jobs API нужно явно указать `runtime_engine` со значением `PHOTON`; в Pipelines API - `photon` со значением `true`. Photon-инстансы расходуют DBU с другой скоростью, чем обычные инстансы.

Insight `COVERAGE_PHOTON` сообщает, что операцию не может ускорить Photon, и рекомендует проверить ограничения Photon.

### 1.9. Размер кластера, autoscaling и serverless

- **Autoscaling**: задаются минимум и максимум worker-узлов; Databricks выбирает нужное число. Autoscaling не работает для spark-submit jobs. Для Structured Streaming масштабирование вниз ограничено; документ рекомендует Spark Declarative Pipelines с enhanced autoscaling.
- **Auto-termination**: период бездействия от 10 до 10 000 минут. Кластер считается неактивным, когда завершены все команды (Spark-задания, Structured Streaming, JDBC, web terminal). DStream не отслеживается: для таких нагрузок нужно отключить auto-termination или перейти на Structured Streaming.
- **Serverless compute** для notebooks, jobs и Lakeflow pipelines не требует провизии кластеров: Databricks сам выделяет ресурсы. Требования: включен Unity Catalog и регион, поддерживающий serverless. Serverless ускоряет старт и масштабирование, сокращает простой и снижает потребность в управлении инфраструктурой.
- **Serverless SQL warehouse** - рекомендуемый тип для SQL: старт обычно 2-6 секунд, быстрый апскейл, Intelligent Workload Management и Predictive IO. Pro warehouse не поддерживает IWM, а classic поддерживает только Photon.

Insight `COMPUTE_SIZE` для serverless: если job или pipeline достиг лимита размера compute object, автоскейлер не добавляет executors; нужно выбрать больший размер.

Метрика Server load distribution: если драйвер сильно загружен, нужен более крупный тип инстанса драйвера.

### 1.10. Контроль стоимости

Инструменты из модуля и документации:

- **Budgets** в консоли аккаунта: Usage > Budgets > Add budget. Можно задать до четырех ежемесячных порогов с фильтрами по рабочей области или тегу. Создавать бюджеты на уровне аккаунта может только account admin; workspace admins работают через Governance Hub.
- **Системные таблицы**: `system.billing.usage` (DBU) вместе с `system.compute.clusters`. Теги ресурсов попадают в записи использования после перезапуска compute.
- **Auto-termination** и **autoscaling** - главные рычаги против простоя.
- Для serverless в `system.billing.usage` фильтр: `product_features.is_serverless = true`; `identity_metadata.run_as` указывает запустившего. Агрегировать через `SUM()`, так как возможны корректирующие записи.
- SQL-алерты можно построить по system tables для расходов на serverless billing.

---

## 2. Мониторинг и устранение неполадок

### 2.1. Метрики кластера и Spark UI

- Метрики находятся в Compute > выбрать ресурс > вкладка Metrics: Hardware (CPU, память, сеть), Spark (активные, завершенные и упавшие задачи, shuffle read/write), GPU (Runtime ML 13.3 и новее). Доступны данные за 30 дней.
- Serverless для notebook и job использует query insights вместо UI метрик.
- Spark UI открывается на странице кластера кнопкой Spark UI.
- Jobs Timeline: упавшие задачи (красный статус), длинные задачи, разрывы выполнения более минуты в середине конвейера (признак перегрузки драйвера или сбоя).
- В стадии: одна задача - нехватка параллелизма; неравномерная длительность задач - перекос. Колонки Input, Output, Shuffle Read, Shuffle Write.
- Перезапуск кластера: Compute > кластер > Restart либо CLI `databricks clusters restart CLUSTER_ID`. Перед перезапуском проверить Event log. Перезапуск прерывает jobs и notebook.

```
databricks clusters restart CLUSTER_ID
```

### 2.2. Query profile и performance insights

Для SQL запросов в Query History: запрос > See query profile.

- Левая панель: Details (сводные метрики), Top operators (самые дорогие операторы), Query text.
- Правая часть: DAG с метриками Time spent, Memory peak, Rows; можно переключать метрику, искать операторы, открыть детали кликом.
- Типовые операторы: Scan, Join, Union, Shuffle (дорогая операция), Hash / Sort, Filter.
- Для SQL запросов профиль можно открыть в Spark UI через меню «Open in Spark UI». Скрытые операции включаются через Enable verbose mode.

Performance insights - подсказки, которые Databricks выводит для запроса. Ключевые коды:

| Insight | Смысл | Рекомендация |
|---|---|---|
| `COVERAGE_FILTER_KEYS_CLUSTERING` | ключи кластеризации не используются в фильтрах | добавить фильтры по ключам кластеризации |
| `COVERAGE_PHOTON` | Photon не может ускорить операцию | проверить ограничения Photon |
| `EXPLODING_JOIN` | join дает намного больше строк, чем читает | уточнить условие join |
| `SELECTIVE_JOIN` | join дает намного меньше строк, чем читает | фильтровать до join |
| `REDUNDANT_JOIN` | внешний join не меняет число строк | удалить join или задать PK/unique |
| `WIDE_PROJECTION` | запрос читает все колонки | выбирать только нужные колонки |
| `CONCURRENT_WRITE` | конкурентные записи конфликтуют | пересмотреть расписание, изучить Delta history |
| `COVERAGE_STATS_DELTA` | нет или неполная статистика Delta для skipping | собрать статистику Delta |
| `COVERAGE_STATS_OPTIMIZER` | нет статистики оптимизатора | собрать статистику |
| `DATA_FILE_SIZE` | скан читает много мелких файлов | включить Predictive Optimization, выполнить OPTIMIZE, перейти на liquid clustering |
| `DATA_SKEW` | неравномерное распределение данных | salting или предагрегация |
| `MANUAL_DATA_LAYOUT` | таблица оптимизирована вручную | перейти на managed table, включить Predictive Optimization и automatic clustering |
| `COMPUTE_SIZE` | serverless достиг лимита размера compute | взять compute большего размера |

### 2.3. Логи и Azure Log Analytics

- Диагностические логи отправляются через diagnostic settings (Send to Log Analytics). Также возможны архивация в storage account и отправка в Event Hub.
- Требуется план Azure Databricks **Premium**. Логи обычно поступают в течение 15 минут; срок доставки не гарантирован.
- Таблицы: DatabricksClusters, DatabricksJobs, DatabricksNotebook, DatabricksSQL, DatabricksUnityCatalog, DatabricksWorkspace, DatabricksSecrets. Стандартные колонки: TimeGenerated, OperationName, Identity, SourceIPAddress, RequestParams, Response.
- Для аудита внутри Databricks рекомендуется системная таблица `system.access.audit`; Log Analytics нужен для кросс-сервисного мониторинга и KQL-алертов.

Примеры KQL из модуля:

```
DatabricksJobs
| where TimeGenerated > ago(24h)
| project TimeGenerated, OperationName, Identity, SourceIPAddress
| order by TimeGenerated desc
| take 100
```

```
DatabricksUnityCatalog
| where TimeGenerated > ago(24h)
| where ActionName in~ ("createTable", "deleteTable", "updateTables")
| project TimeGenerated, Identity, ActionName, RequestParams
| order by TimeGenerated desc
```

Алерты в Azure Monitor создаются из запроса (New alert rule из запроса) с условием и Action group. Примеры из модуля: более пяти сбоев job за час; операции с таблицами вне рабочего времени; всплеск создания кластеров.

### 2.4. Databricks SQL alerts

SQL alerts выполняют запрос по расписанию и уведомляют, когда результат удовлетворяет условию; доступна история проверок. Сценарии: бизнес-метрики (в том числе metric views), качество данных (вместе с data quality monitors), расходы (system tables для serverless billing), здоровье warehouse и запросов, аудит. Устаревшие алерты описаны отдельно как legacy alerts.

### 2.5. Устранение неполадок Lakeflow Jobs и repair run

- Статус запуска определяется по leaf-задачам (без последующих зависимостей): Failed, Succeeded with failures, Skipped (превышен лимит параллельных запусков), Timed Out, Canceled. Disabled-задачи пропускаются.
- Поиск причины: Jobs & Pipelines > задание > Runs (матричный вид) > Task run details с логами.
- Repair run доступен для заданий с двумя и более задачами: перезапускает неуспешные задачи и зависимые от них. Если задачи делили job-кластер, создается новый экземпляр кластера.
- **Важно**: задача перезапускается с начала. Если она уже записала часть данных, возможна дупликация. Поэтому нужны идемпотентные операции: overwrite или merge вместо append.
- Для continuous jobs в exponential backoff действие Restart run отменяет текущий запуск, сбрасывает период ожидания и сразу запускает новый.

---

## 3. CI/CD и DevOps для Databricks

### 3.1. Git folders

Git folder - интеграция Git-репозитория (Azure DevOps, GitHub, GitLab, Bitbucket) в рабочую область. Правила из модуля:

- каждый участник работает в собственной Git folder, связанной с общим репозиторием;
- перед новой работой выполняйте pull; при pull notebook сбрасывает состояние (выводы ячеек, комментарии, историю версий);
- ветки создаются от `main` с понятными именами (`feature/feature-name`, `bugfix/issue-description`, `users/username/description`);
- выводы notebook не попадают в коммит для форматов `.py`, `.scala`, `.sql`, `.r`; для версионирования выводов используйте IPYNB;
- если нет прав на `main`, создайте feature-ветку и pull request через интерфейс провайдера;
- ограничения: рабочие ветки до 1 ГБ, рекомендуется не более 20 000 ассетов; для больших репозиториев - sparse checkout.

Git folder для production можно обновлять вручную или из GitHub Actions при merge. Команда CLI из примера GitHub Actions:

```
databricks repos update /Workspace/<git-folder-path> --branch git-folder-cicd-example
```

Ограничение этого подхода: в Git folder под контролем версий находятся только файлы кода (notebooks, черновики дашбордов), а конфигурации jobs и pipelines - нет.

### 3.2. Declarative Automation Bundles (DABs)

Declarative Automation Bundles (ранее Databricks Asset Bundles) - рекомендуемый подход к CI/CD на Databricks: описание ресурсов (jobs, pipelines, dashboards, serving endpoints, MLflow experiments и models) в YAML-файлах вместе с исходным кодом и тестами. Bundle разворачивается в целевое окружение и запускается через Databricks CLI (версия v0.218.0 и выше по документации).

Минимальный `databricks.yml` из модуля:

```yaml
bundle:
  name: my-data-pipeline

include:
  - resources/*.yml

workspace:
  host: https://adb-1234567890123456.7.azuredatabricks.net

resources:
  jobs:
    daily-ingestion-job:
      name: daily-ingestion-job
      tasks:
        - task_key: ingest-data
          notebook_task:
            notebook_path: ./notebooks/ingest.py

targets:
  dev:
    default: true
  prod:
    workspace:
      host: https://adb-9876543210987654.3.azuredatabricks.net
```

Переменные и подстановка через `${var.name}`:

```yaml
variables:
  cluster_id:
    description: The cluster to use for job execution
    default: 1234-567890-abcde123
  environment:
    description: The deployment environment name
    default: development

resources:
  jobs:
    my-job:
      name: ${var.environment}-data-pipeline
      tasks:
        - task_key: process-data
          existing_cluster_id: ${var.cluster_id}
          notebook_task:
            notebook_path: ./notebooks/process.py
```

Зависимости задач и job-кластер:

```yaml
resources:
  jobs:
    etl-pipeline:
      name: etl-pipeline
      tasks:
        - task_key: extract-task
          notebook_task:
            notebook_path: ./notebooks/extract.py
        - task_key: transform-task
          depends_on:
            - task_key: extract-task
          notebook_task:
            notebook_path: ./notebooks/transform.py
            base_parameters:
              source_table: ${var.source_table}
```

```yaml
resources:
  jobs:
    my-job:
      job_clusters:
        - job_cluster_key: shared-cluster
          new_cluster:
            spark_version: 16.4.x-scala2.12
            node_type_id: Standard_DS3_v2
            num_workers: 2
      tasks:
        - task_key: my-task
          job_cluster_key: shared-cluster
          notebook_task:
            notebook_path: ./notebooks/analysis.py
```

Команды CLI из модуля:

```
databricks bundle validate
databricks bundle plan
databricks bundle plan -t production
databricks bundle deploy
databricks bundle deploy -t dev
databricks bundle deploy -t production --auto-approve
databricks bundle summary
databricks bundle open data_ingestion_job
databricks auth login --host https://adb-1234567890123456.7.azuredatabricks.net
databricks bundle deploy --force-lock
```

Порядок: `validate` → `plan` → `deploy`. CLI хранит состояние в рабочей области: создает новые ресурсы, обновляет существующие и удаляет те, что исчезли из конфигурации. Одновременные развертывания одного bundle в один target конфликтуют. `--force-lock` применять только тогда, когда никакое другое развертывание не выполняется. `--fail-on-active-runs` прерывает развертывание при активных запусках. Для CI/CD используется `--auto-approve`.

### 3.3. Окружения: targets, mode и presets

- **Targets** - окружения (dev, prod, staging) с разными настройками. Переменные переопределяются в target; значения можно передать через `--var="name=value"` или переменные окружения с префиксом `BUNDLE_VAR_`.
- **mode: development** - имена ресурсов получают префикс `[dev username]`, расписания приостанавливаются, параллельные запуски разрешены.
- **mode: production** - CLI проверяет соответствие локальной Git-ветки указанной в конфигурации `git`, рекомендуются service principals.
- **presets** - тонкая настройка поведения: `name_prefix`, `trigger_pause_status`, `tags`.

```yaml
targets:
  dev:
    default: true
    mode: development
```

```yaml
targets:
  prod:
    mode: production
    workspace:
      host: https://adb-prod.7.azuredatabricks.net
```

```yaml
targets:
  staging:
    presets:
      name_prefix: staging_
      trigger_pause_status: PAUSED
      tags:
        environment: staging
```

Пути в конфигурации относительны файла, в котором они объявлены.

### 3.4. Тестирование

Пирамида тестов из модуля: много быстрых **unit**-тестов (миллисекунды, одна функция), меньше **integration**-тестов (секунды, несколько компонентов), еще меньше **end-to-end** (минуты, весь конвейер) и **UAT** (приемка бизнес-пользователями в staging).

- Integration-тесты - только на тестовых ресурсах (отдельная схема или каталог), никогда на продуктивных таблицах.
- End-to-end тесты очищают данные после проверки; их лучше запускать вне пика нагрузки или в deployment-пайплайне.
- Структура проекта: `src/`, `tests/unit`, `tests/integration`, `tests/e2e`, `notebooks/run_tests.py`, `requirements.txt`.
- Тесты можно запускать из Databricks job перед развертыванием.

Пример функции и pytest-тестов (из модуля):

```python
def filter_country_region(df, country_region="USA"):
    return df[df.iso_code == country_region]
```

```python
import pytest
import pandas as pd
from transforms import filter_country_region

@pytest.fixture
def sample_data():
    """Create test data that mimics production structure."""
    return pd.DataFrame({
        'iso_code': ['USA', 'USA', 'CAN', 'GBR'],
        'value': [100, 200, 150, 175]
    })

def test_filter_country_region_default(sample_data):
    result = filter_country_region(sample_data)
    assert len(result) == 2
    assert all(result.iso_code == 'USA')

def test_filter_country_region_specific(sample_data):
    result = filter_country_region(sample_data, country_region='CAN')
    assert len(result) == 1
    assert result.iloc[0]['value'] == 150
```

Запуск в notebook:

```python
%pip install pytest

import pytest
retcode = pytest.main([".", "-v", "-p", "no:cacheprovider"])
assert retcode == 0, "Tests failed. Check the output above."
```

Функции должны возвращать значения одного типа (DataFrame, даже пустой).

Для unit-тестов в проекте допускается `pytest`; для Databricks notebook тесты можно вызвать через `pytest.main` (как выше).

### 3.5. GitHub Actions и Azure DevOps

Общий поток CI/CD на Databricks, по документации: Version (Git) → Code (Lakeflow Pipelines Editor, Databricks VS Code extension) → Build (artifact mapping, pylint с плагином Databricks Labs) → Deploy (DABs через Azure DevOps, GitHub Actions или Jenkins) → Test (pytest) → Run (`databricks bundle run`) → Monitor.

Рекомендуемые механизмы аутентификации для CI/CD: service principals и workload identity federation (OAuth token federation), что позволяет не хранить Databricks secrets. В примере GitHub Actions для федерации добавляется `id-token: write` в `permissions` и `DATABRICKS_AUTH_TYPE: github-oidc`.

Пример GitHub Actions для dev-окружения (из документации; публикуется при pull request в `main`):

```yaml
# This workflow validates, deploys, and runs the specified bundle
# within a pre-production target named "dev".
name: 'Dev deployment'

# Ensure that only a single job or workflow using the same concurrency group
# runs at a time.
concurrency: 1

# Trigger this workflow whenever a pull request is opened against the repo's
# main branch or an existing pull request's head branch is updated.
on:
  pull_request:
    types:
      - opened
      - synchronize
    branches:
      - main

jobs:
  # Used by the "pipeline_update" job to deploy the bundle.
  # Bundle validation is automatically performed as part of this deployment.
  # If validation fails, this workflow fails.
  deploy:
    name: 'Deploy bundle'
    runs-on: ubuntu-latest

    steps:
      # Check out this repo, so that this workflow can access it.
      - uses: actions/checkout@v3

      # Download the Databricks CLI.
      # See https://github.com/databricks/setup-cli
      - uses: databricks/setup-cli@main

      # Deploy the bundle to the "dev" target as defined
      # in the bundle's settings file.
      - run: databricks bundle deploy
        working-directory: .
        env:
          DATABRICKS_TOKEN: ${{ secrets.SP_TOKEN }}
          DATABRICKS_BUNDLE_TARGET: dev

  # Validate, deploy, and then run the bundle.
  pipeline_update:
    name: 'Run pipeline update'
    runs-on: ubuntu-latest

    # Run the "deploy" job first.
    needs:
      - deploy

    steps:
      # Check out this repo, so that this workflow can access it.
      - uses: actions/checkout@v3

      # Use the downloaded Databricks CLI.
      - uses: databricks/setup-cli@main

      # Run the Databricks workflow named "sample_job" as defined in the
      # bundle that was just deployed.
      - run: databricks bundle run sample_job --refresh-all
        working-directory: .
```

Для продакшена в документации есть отдельный workflow с целевым окружением `prod` и триггером на pull request в `main`; пример с `DATABRICKS_TOKEN` заменяется на OIDC-федерацию, как указано выше. Документация также показывает сборку JAR перед развертыванием bundle (отдельный пример) и пиннинг версии `databricks/setup-cli@v1.23.0`.

Azure DevOps: документация ссылается на страницу «Continuous integration and delivery on Azure Databricks using Azure DevOps», но ее содержимое в проекте не сохранено (см. «Пробелы»).

Jenkins: в проекте есть отдельная страница `d2-azure-databricks-dev-tools-ci-cd-jenkins.md`, но ее код в этом конспекте не разбирался.

---

## 4. MLflow и машинное обучение на Databricks

### 4.1. MLflow Tracking

MLflow - открытая платформа жизненного цикла ML: Tracking, Projects, Models и Model Registry. Tracking фиксирует параметры, метрики, версии библиотек и артефакты запуска (run); эксперимент (experiment) - набор запусков для сравнения.

- Эксперимент создается автоматически при старте первого запуска; по умолчанию имя совпадает с именем notebook; его можно задать переменной окружения `MLFLOW_EXPERIMENT_NAME`.
- Логирование параметров и метрик внутри `mlflow.start_run()`.
- По умолчанию MLflow пишет в workspace-tracking server Databricks.
- Autologging и logging API: в документации показаны оба варианта.

Пример из модуля:

```python
with mlflow.start_run():
    mlflow.log_param("input1", input1)
    mlflow.log_param("input2", input2)
    # Perform operations here like model training.
    mlflow.log_metric("rmse", rmse)
```

Логирование модели с регистрацией из модуля:

```python
with mlflow.start_run():
    # code to train model goes here

    # log the model itself (and the environment it needs to be used)
    unique_model_name = "my_model-" + str(time.time())
    mlflow.spark.log_model(spark_model=model,
                           artifact_path=unique_model_name
                           conda_env=mlflow.spark.get_default_conda_env(),
                           registered_model_name="my_model")
```

Примечание: строка `artifact_path=unique_model_name` в источнике не имеет запятой перед `conda_env` - это ошибка в исходной копии модуля; при использовании код нужно исправить.

### 4.2. Model Registry и Unity Catalog

Модели регистрируются в Unity Catalog с трехуровневым именем `<catalog>.<schema>.<model>`. Пример из документации (scikit-learn, MLflow с Unity Catalog):

```python
import os
os.environ['MLFLOW_USE_DATABRICKS_SDK_MODEL_ARTIFACTS_REPO_FOR_UC'] = 'True'
```

```python
%pip install --upgrade "mlflow-skinny[databricks]"
dbutils.library.restartPython()
```

```python
import mlflow
mlflow.set_registry_uri("databricks-uc")
```

```python
import mlflow
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

with mlflow.start_run():
    # Train a sklearn model on the iris dataset
    X, y = datasets.load_iris(return_X_y=True, as_frame=True)
    clf = RandomForestClassifier(max_depth=7)
    clf.fit(X, y)
    # Take the first row of the training dataset as the model input example.
    input_example = X.iloc[[0]]
    # Log the model and register it as a new version in UC.
    mlflow.sklearn.log_model(
        sk_model=clf,
        name="model",
        # The signature is automatically inferred from the input example and its predicted output.
        input_example=input_example,
        # Use three-level name to register model in Unity Catalog.
        registered_model_name="prod.ml_team.iris_model",
    )
```

В источнике есть также вариант с `artifact_path="model"` (для MLflow 2.x). Регистрация уже залогированной модели через `mlflow.register_model`:

```python
mlflow.register_model(
  "runs:/<run_id>/model", "prod.ml_team.iris_model"
)
```

Aliases (псевдонимы) - основной механизм. Stages в Unity Catalog не поддерживаются; вместо них рекомендуется трехуровневое имя (окружение) и aliases (состояние деплоя).

```python
# create "Champion" alias for version 1 of model "prod.ml_team.iris_model"
client.set_registered_model_alias("prod.ml_team.iris_model", "Champion", 1)

# reassign the "Champion" alias to version 2
client.set_registered_model_alias("prod.ml_team.iris_model", "Champion", 2)

# get a model version by alias
client.get_model_version_by_alias("prod.ml_team.iris_model", "Champion")

# delete the alias
client.delete_registered_model_alias("prod.ml_team.iris_model", "Champion")
```

Загрузка версии по alias для batch inference:

```python
model_version_uri = "models:/prod.ml_team.iris_model@Champion"
```

Model serving endpoint может ссылаться на версию по alias; деплой-workflow получает версию по alias и обновляет endpoint.

Права: для регистрации нужна привилегия `CREATE MODEL` на схеме (`GRANT CREATE MODEL ON SCHEMA <schema-name> TO <principal>`). Для продвижения из staging в prod пользователь должен иметь чтение staging-модели и запись в prod-модель.

### 4.3. Model Serving

Mosaic AI Model Serving (в документации - Model Serving) предоставляет REST API для real-time и batch inference: модель, залогированная в формате MLflow, превращается в endpoint, который автоматически масштабируется. Сервис использует serverless compute. Есть унифицированный REST API и MLflow Deployment API, а также доступ к моделям из SQL через AI Functions и ai-query для batch-сценариев.

Пути инференса из модуля: онлайн (real-time HTTP endpoint), потоковый (по Delta-таблице признаков), пакетный (job на Spark).

Конкретные команды создания endpoint в проанализированных страницах не приведены (см. «Пробелы»).

### 4.4. Feature Store

Databricks Feature Store создает Unity Catalog-управляемые признаки. Два способа описания:

- **Feature Views (рекомендуются)** - декларативные признаки как объекты Unity Catalog; Databricks сам создает и ведет пайплайны признаков, включая time-windowed агрегации и streaming. Можно экспериментировать с признаками в notebook до регистрации.
- **Feature tables** - Delta-таблица в Unity Catalog с primary key; пайплайн заполнения ведет команда. Нужны для Delta Sharing или сторонних online store.

Оба способа публикуются в Online Feature Store и поддерживают lineage и governance. Поиск и совместное использование признаков - через каталог.

### 4.5. MLOps workflow

Рекомендации документации:

- отдельные окружения для development, staging и production с явными переходами;
- код в Git (Git folders); данные - в Delta-таблицах в lakehouse с контролем доступа; эксперименты - в MLflow; версии моделей - в Models in Unity Catalog;
- **деплоить код, а не модели**: в большинстве случаев продвигаются код из ветки development в staging и release, так что весь код проходит одинаковый review и integration tests, а продуктивная модель обучается на продуктивном коде.

Этапы: development (данные, EDA, код, обучение, валидация, commit); staging (merge в staging-ветку, integration tests в CI, создание release branch); production (обучение, валидация, деплой). Продвижение модели между версиями делается сменой alias: challenger становится champion после прохождения проверок валидации.

---

## 5. Databricks SQL и BI

### 5.1. SQL warehouses

- SQL warehouse - вычислительный ресурс для запросов. Databricks рекомендует serverless SQL warehouses, когда они доступны.
- Типы: **Serverless** (Photon, Predictive IO, Intelligent Workload Management; старт около 2-6 с, быстрый апскейл), **Pro** (Photon, Predictive IO; вычисления в вашей подписке; нужен для сетевых ограничений, когда serverless недоступен в регионе), **Classic** (Photon).
- Lakehouse Real-Time (Beta) - serverless-тип для субсекундных запросов с высокой конкуренцией.
- Автозапуск: при запросе к остановленному warehouse, по расписанию job, при подключении JDBC/ODBC и при открытии dashboard с привязанным warehouse.
- Starter Warehouse создается автоматически; его можно изменить или удалить.
- Для запуска вручную нужна привилегия не ниже CAN MONITOR.
- SQL warehouse не поддерживает credential passthrough; управление доступом - через Unity Catalog.

### 5.2. Мониторинг SQL-хранилища и алерты

- Вкладка Monitoring: пиковое число запросов, работающие кластеры, история запросов.
- Query history и query profile (см. 2.2) для анализа конкретного запроса.
- SQL alerts (см. 2.4).

### 5.3. Dashboards (AI/BI)

AI/BI dashboards: датасеты из таблиц, представлений или пользовательских запросов; визуализации; фильтры (глобальные, на уровне страницы, виджета), cross-filtering и drill-through; custom calculations и LOD-выражения; настройки темы и локали. Публикация с общими или индивидуальными правами (data permissions), расписания обновления, email- и Slack-подписки, встраивание через iframe, Genie Agents для обработки естественным языком.

### 5.4. Power BI

Источник: «Connect Power BI Desktop to Azure Databricks».

- Способы подключения: **Partner Connect** (плитка Power BI в Partner Connect integrations; в Power BI выбирается подключение с учетными данными) и **ручное подключение**: Server Hostname и HTTP Path склада SQL warehouse, режим Import или DirectQuery.
- Рекомендация: **для DirectQuery используйте Databricks SQL warehouse**.
- Аутентификация: personal access token, Microsoft Entra ID (Sign in), M2M OAuth через service principal (Power BI Desktop 2.143.878.0 и выше). Документация рекомендует токены сервисных принципалов вместо токенов пользователей.
- Нативные SQL-запросы через коннектор доступны с версии Power BI 2.112.603.0 и выше.
- Ограничения: в сочетании с DirectQuery не поддерживается `Databricks.Query`; OpenSharing-коннектор загружает данные в локальную память и ограничен Row Limit.
- Коннектор поддерживает web proxy, но не поддерживает автоматические `.pac`-настройки.

---

## 6. Шпаргалка: симптомы и исправления

| Симптом | Вероятная причина | Что сделать |
|---|---|---|
| Одна задача в стадии работает намного дольше остальных (Max > 75-го перцентиля на 50 %+) | перекос данных | AQE; salting ключа; broadcast малой таблицы; предагрегация |
| Shuffle Spill (Memory или Disk) ненулевой | нехватка памяти, часто из-за перекоса | сначала убрать перекос; `spark.sql.shuffle.partitions = auto`; крупнее worker; раньше фильтровать и выбирать колонки |
| Стадия из одной задачи | нехватка параллелизма | увеличить число партиций; проверить источник данных |
| Высокий Input при повторных чтениях одних данных | недокеширование | проверить disk cache (`spark.databricks.io.cache.enabled`) |
| Высокое давление на память от кеша | переизбыток кеша | `.unpersist()`; ограничить кеширование |
| Скан читает много мелких файлов (`DATA_FILE_SIZE`) | small files | Predictive Optimization; `OPTIMIZE`; liquid clustering |
| Скан читает все колонки (`WIDE_PROJECTION`) | лишние колонки | `SELECT` только нужных колонок |
| Join читает много и выдает мало (`SELECTIVE_JOIN`) | поздняя фильтрация | фильтровать до join |
| Join выдает намного больше строк (`EXPLODING_JOIN`) | неверное условие join | уточнить условие, уменьшить входы |
| Большой shuffle при join с малой таблицей | нет broadcast | AQE / broadcast (порог 30 МБ по умолчанию) |
| Драйвер перегружен (server load) | мелкий драйвер | более крупный тип инстанса драйвера |
| Разрыв в Jobs Timeline больше минуты | перегрузка драйвера или сбой | проверить Event log и метрики драйвера |
| Таблица менее 1 ТБ партиционирована | избыточное партиционирование | убрать партиционирование |
| Таблица 1-100 ТБ партиционирована | партиционирование вредит | перейти на liquid clustering |
| Photon не ускоряет операцию (`COVERAGE_PHOTON`) | неподдерживаемая операция | проверить ограничения Photon |
| Короткие запросы (менее 2 с) не ускоряются | накладные расходы планирования | ожидаемо; оценивать длинные запросы |
| Serverless достиг лимита (`COMPUTE_SIZE`) | малый размер compute | взять compute большего размера |
| Неожиданный рост расходов | простой, нет бюджетов | auto-termination; autoscaling; бюджеты; `system.billing.usage` |
| Конфликты конкурентных записей (`CONCURRENT_WRITE`) | пересекающиеся записи | изменить расписание; Delta history |
| Job упал на одной задаче | сбой задачи | repair run; идемпотентные записи (overwrite или merge) |
| Ошибка аутентификации CLI | не настроен доступ | `databricks auth login --host ...` |
| Зависла блокировка bundle | прерванное развертывание | `--force-lock`, только если другого развертывания нет |
| Продакшен-деплой без review | нет CI | pull request, bundle validate и plan, `--auto-approve` только в CI |

---

## 7. Вопросы для собеседования

**1. Когда не нужно партиционировать таблицу в Databricks?**
Если данных меньше 1 ТБ. От 1 ТБ до 100 ТБ рекомендуется liquid clustering, а не партиционирование. Партиционирование также может ухудшить производительность, если партиции меньше 1 ГБ.

**2. Чем liquid clustering отличается от партиционирования?**
Liquid clustering не использует фиксированные границы партиций и не страдает от проблемы small files, характерной для статического партиционирования. Он работает с колонками высокой и низкой кардинальности и распознает поля структуры (struct fields) как ключи, чего нельзя сделать с PARTITIONED BY. Для таких таблиц в OPTIMIZE нельзя указывать ZORDER BY.

**3. Как обнаружить перекос данных (skew) в Spark UI?**
В Summary Metrics стадии сравнить Max duration с 75-м перцентилем. Если максимум больше 75-го перцентиля на 50 % и более, вероятен перекос. Далее применяют AQE, salting или broadcast малой таблицы.

**4. Что означает ненулевой Shuffle Spill и что с ним делать?**
Spill означает, что промежуточные данные не поместились в память и были записаны на диск. Это признак давления на память. Сначала устраняют перекос, затем увеличивают число партиций shuffle (`auto`), память или раньше фильтруют данные.

**5. Что делает AQE и каков порог broadcast по умолчанию?**
AQE пересматривает план во время выполнения: в том числе конвертирует sort-merge join в broadcast join, если одна сторона меньше порога `spark.databricks.adaptive.autoBroadcastJoinThreshold`, по умолчанию 30 МБ. Также помогает при перекосе.

**6. В каких случаях Photon не даст заметного эффекта?**
Для коротких запросов (менее двух секунд), где время уходит на планирование и scheduling, а также для операций, которые Photon не поддерживает (тогда он откатывается на обычный runtime; insight COVERAGE_PHOTON). Stateful streaming Photon не поддерживает.

**7. Что такое repair run и почему нужны идемпотентные записи?**
Repair run перезапускает только неуспешные задачи и зависимые от них. Задача стартует заново с начала, поэтому если она уже успела записать часть данных, возможна дупликация. Поэтому записи делают идемпотентными: overwrite или merge вместо append.

**8. Что такое Declarative Automation Bundles и зачем разделять targets development и production?**
DABs - инфраструктура как код: jobs, pipelines и другие ресурсы описываются в YAML и разворачиваются через Databricks CLI (`validate`, `plan`, `deploy`). Target задает окружение. Режим development добавляет префикс к именам, приостанавливает расписания и разрешает параллельные запуски; режим production проверяет соответствие Git-ветки и рекомендует service principals.

**9. Почему в MLOps рекомендуется продвигать код, а не модели?**
Так весь код проходит одинаковый review и integration tests, а продуктивная модель обучается на продуктивном коде. Модели создаются заново в каждом окружении из проверенного кода.

**10. Как продвигать модель в продакшен в Unity Catalog и чем Import отличается от DirectQuery в Power BI?**
В Unity Catalog stages не поддерживаются; версии получают aliases (например, Champion), а деплой-workflow или batch-джобы ссылаются на модель через `models:/<name>@Champion`. В Power BI режим Import загружает данные в модель, DirectQuery запрашивает SQL warehouse при каждом обращении; для DirectQuery Databricks рекомендует SQL warehouse.

---

## 8. Пробелы в источниках

- **Azure DevOps**: нет сохраненной страницы с YAML-пайплайном для Azure DevOps. Упоминается только ссылка на «Continuous integration and delivery on Azure Databricks using Azure DevOps» и «Authenticate with Azure DevOps».
- **Jenkins**: страница есть в docs2, но код в конспект не включен.
- **Liquid clustering**: нет полного примера `CREATE TABLE ... CLUSTER BY` и страницы «Use liquid clustering for tables» в сохраненных источниках; есть только `ALTER TABLE ... REPLACE PARTITIONED BY WITH CLUSTER BY` в тексте и `OPTIMIZE ... FULL` в справочнике.
- **AQE и настройки shuffle**: отдельной страницы про AQE в источниках нет. Сведения о включенном по умолчанию AQE и пороге 30 МБ взяты из конспекта модуля; официальный параметр `spark.sql.adaptive.enabled` в проверенных страницах не найден.
- **Размер файлов**: страница Control data file size обрезана; полные значения target file size не проверены.
- **Feature Store**: в источниках нет примеров кода создания feature views или feature tables.
- **Model Serving**: нет примеров создания endpoint (REST, MLflow Deployment API), только обзорные описания.
- **Мониторинг**: страниц Jobs timeline и Summary Metrics из Spark UI в источниках нет; описание взято из конспекта модуля.
- **Стоимость**: нет цен и тарифов; только механизмы контроля.
- **Power BI**: нет сравнения производительности Import и DirectQuery; описаны только подключение и ограничения.
- **Вопросы для самопроверки**: в конспектах модулей тексты контрольных вопросов не приведены (в источнике отмечено «вопросы не приведены»).
- **Ссылка Git webhooks** для автодеплоя приложений описана в таблице, но без подробностей.

---

## Источники

Документация Microsoft Learn (Markdown-копии в проекте):

- `docs2/d2-azure-databricks-optimizations-spark-ui-guide.md` - Diagnose cost and performance issues using the Spark UI. https://learn.microsoft.com/en-us/azure/databricks/optimizations/spark-ui-guide
- `docs2/d2-azure-databricks-tables-partitions.md` - When to partition tables on Azure Databricks. https://learn.microsoft.com/en-us/azure/databricks/tables/partitions
- `docs/d2-azure-databricks-optimizations-auto-optimize.md` - Control data file size (auto compaction, optimized writes, OPTIMIZE).
- `docs2/d0-azure-databricks-delta.md` - Delta Lake: liquid clustering, data skipping, control data file size.
- `docs2/d2-azure-databricks-compute-photon.md` - What is Photon?
- `docs2/d2-azure-databricks-compute-serverless.md` - Connect to serverless compute.
- `docs2/d2-azure-databricks-compute-configure.md` - Compute configuration, autoscaling.
- `docs2/d2-azure-databricks-compute-sql-warehouse.md` - Connect to a SQL warehouse.
- `docs2/d2-azure-databricks-compute-sql-warehouse-warehouse-types.md` - SQL warehouse types.
- `docs2/d2-azure-databricks-sql-user-queries-query-profile.md` - Query profile.
- `docs2/d2-azure-databricks-sql-user-queries-performance-insights.md` - Query performance insights.
- `docs2/d2-azure-databricks-sql-user-alerts.md` - Databricks SQL alerts.
- `docs2/d2-azure-databricks-spark-conf.md` - Spark configuration (spark.sql.shuffle.partitions).
- `docs2/d2-azure-databricks-sql-language-manual.md` - SQL language reference (CLUSTER BY clause).
- `docs2/d2-azure-databricks-error-messages-error-classes.md` - OPTIMIZE error classes (liquid clustering, ZORDER).
- `docs2/d2-azure-databricks-dev-tools-bundles.md` - What are Declarative Automation Bundles? https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles
- `docs2/d2-azure-databricks-dev-tools-bundles-reference.md` - Bundle configuration reference.
- `docs2/d2-azure-databricks-dev-tools-ci-cd.md` - CI/CD on Azure Databricks. https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd
- `docs2/d2-azure-databricks-dev-tools-ci-cd-github.md` - GitHub Actions (примеры workflow).
- `docs2/d2-azure-databricks-dev-tools-ci-cd-flows.md` - CI/CD workflows on Databricks.
- `docs2/d2-azure-databricks-dev-tools-ci-cd-jenkins.md` - CI/CD with Jenkins (не разбиралось).
- `docs2/d2-azure-databricks-repos.md` - Git folders.
- `docs2/d2-azure-databricks-mlflow-tracking.md` - Track model development using MLflow.
- `docs2/d2-azure-databricks-machine-learning-manage-model-lifecycle.md` - Manage model lifecycle in Unity Catalog (aliases, registration).
- `docs2/d2-azure-databricks-machine-learning-model-serving.md` - Deploy models using Model Serving.
- `docs2/d2-azure-databricks-machine-learning-feature-store.md` - Databricks Feature Store.
- `docs2/d2-azure-databricks-machine-learning-mlops-mlops-workflow.md` - MLOps workflows on Azure Databricks.
- `docs2/d2-azure-databricks-partners-bi-power-bi-desktop.md` - Connect Power BI Desktop to Azure Databricks.
- `docs2/d2-azure-databricks-dashboards.md` - Dashboards.
- `docs2/d2-azure-databricks-mlflow.md` - MLflow overview.

Конспекты модулей Learn в проекте (`guides/modules`):

- `guides/modules/monitor-troubleshoot-optimize-workloads-azure-databricks.md` - Мониторинг, устранение неполадок и оптимизация. https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/
- `guides/modules/implement-development-lifecycle-processes-in-azure-databricks.md` - Процессы жизненного цикла разработки. https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/
- `guides/modules/mlflow-azure-databricks.md` - MLflow в Azure Databricks. https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/
- `guides/modules/machine-learning-production-azure-databricks.md` - Машинное обучение в продакшене. https://learn.microsoft.com/en-us/training/modules/machine-learning-production-azure-databricks/

Курсы в проекте (`guides/courses`):

- `guides/courses/azure-databricks-data-engineer-deploy-maintain-data-pipelines-workloads.md` - Deploy and maintain data pipelines and workloads (контекст).
- `guides/courses/build-operate-machine-learning-solutions-azure-databricks.md` - Build and operate ML solutions (контекст).
