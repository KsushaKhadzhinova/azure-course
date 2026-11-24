# Мониторинг, устранение неполадок и оптимизация нагрузок в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/

## Цель модуля

Отслеживать потребление ресурсов кластеров и SQL-хранилищ, контролировать стоимость (бюджеты и системные таблицы), диагностировать и восстанавливать Lakeflow Jobs и Spark-задания, устранять проблемы производительности (кеш, перекос данных, spill, shuffle) и настроить централизованное логирование в Azure Log Analytics.

## Ключевые понятия

- **Cluster metrics (метрики кластера)** - аппаратные (CPU, память, сеть), Spark (активные задачи, shuffle) и GPU-метрики.
- **Auto-termination** - автоматическое завершение простаивающего кластера (от 10 до 10 000 минут).
- **Autoscaling** - динамическое изменение числа рабочих узлов.
- **Budgets и system.billing.usage** - бюджеты в консоли аккаунта и системная таблица для анализа DBU.
- **Состояния запуска job** - Failed, Succeeded with failures, Skipped, Timed Out, Canceled; Disabled - для отдельных задач.
- **Repair run** - повторный запуск только неуспешных задач и зависимых от них.
- **Spark UI, DAG, query profile** - инструменты диагностики Spark-заданий и SQL-запросов.
- **Data skew (перекос данных)**, **spill (сброс на диск)**, **shuffle (перемещение данных)**, **disk cache** - основные причины снижения производительности.
- **Log streaming (потоковая передача логов)** - передача диагностических логов в Azure Log Analytics через diagnostic settings.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/1-introduction

Нагрузки в Azure Databricks требуют постоянного контроля ресурсов, состояния job и производительности. Инструменты: метрики кластера, Spark UI, системные таблицы для биллинга и логи в Log Analytics. Типичные проблемы: перекос данных, spill, избыточный shuffle, проблемы с кешем.

### 2. Мониторинг и управление потреблением кластеров
Источник: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/2-monitor-manage-cluster-consumption

- Метрики: Compute > выбрать ресурс > вкладка Metrics. Hardware (CPU, память, сеть), Spark (активные, завершённые и упавшие задачи, shuffle read/write), GPU (Runtime ML 13.3 и новее). Данные за последние 30 дней; выбор узла через All nodes; тип метрик через Hardware.
- Serverless для notebook и job использует query insights вместо UI метрик.
- Мониторинг SQL-хранилища: вкладка Monitoring; пиковое число запросов, работающие кластеры, история запросов.
- Auto-termination: период неактивности 10-10 000 минут; кластер неактивен, когда завершены все команды (включая Spark-задания, Structured Streaming, JDBC и web terminal). DStream не отслеживается - для таких нагрузок отключите auto-termination или перейдите на Structured Streaming.
- Autoscaling: задаются минимум и максимум рабочих узлов.
- Бюджеты: в консоли аккаунта Usage > Budgets > Add budget; до четырёх ежемесячных порогов; фильтры по рабочей области или тегу. Создавать бюджеты на уровне аккаунта может только администратор аккаунта; администраторы рабочих областей - через Governance Hub.
- Системная таблица `system.billing.usage` (вместе с `system.compute.clusters`) для анализа DBU; теги ресурсов попадают в записи использования (после перезапуска compute).
- Serverless: фильтр `product_features.is_serverless = true`; `identity_metadata.run_as` указывает запускающего; агрегировать через SUM(), так как возможны корректирующие записи.

### 3. Устранение неполадок и восстановление Lakeflow Jobs
Источник: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/3-troubleshoot-repair-lakeflow-jobs

- Статус запуска определяется по leaf-задачам (без последующих зависимостей): Failed, Succeeded with failures (листовые задачи успешны, но часть задач упала), Skipped (превышен лимит параллельных запусков), Timed Out, Canceled.
- Disabled-задачи пропускаются; в repair-запуске состояние запуска определяет, что перезапускается; отключённую задачу можно принудительно включить, указав её явно.
- Поиск причины: Jobs & Pipelines > задание > вкладка Runs (матричное представление, наведение на красную ячейку - время, статус, ошибка); открыть Task run details с логами. Кнопка Diagnose Error (помощь Genie Code).
- Частые причины: ошибки конфигурации (Edit task), нехватка ресурсов (изменить cluster, квоты), превышение Maximum concurrent runs, внешние зависимости (после устранения - repair).
- Repair run: доступен для заданий с двумя и более задачами; перезапускает неуспешные задачи и зависимые; можно переопределить параметры. Если задачи делили job-кластер, создаётся новый экземпляр (например, `my_job_cluster_v1`).
- Важно: задача перезапускается с начала; если она уже записала часть данных, возможна дупликация. Используйте идемпотентные операции (overwrite или merge вместо append).
- Остановка: кнопка stop у активного запуска; Cancel runs или Cancel all queued runs. Для continuous jobs в exponential backoff - Restart run (отменяет текущий запуск, сбрасывает период ожидания и сразу запускает новый).
- Проактивно: уведомления, просмотр истории, системные таблицы схемы `system.lakeflow` (если администратор её включил).

### 4. Устранение неполадок Spark-заданий и notebook
Источник: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/4-troubleshoot-repair-spark-jobs-notebooks

- Причины сбоев: ошибки кода и схемы; нехватка CPU, памяти и диска (OOM, медленный shuffle); среды (сбой запуска кластера, квоты, eviction spot-VM, сеть).
- Spark UI (кластер > вкладка Spark UI): Jobs Timeline - упавшие задачи (красный статус), длинные задачи, разрывы выполнения (более минуты в середине конвейера - признак перегрузки драйвера или сбоя).
- Стадия: одна задача в стадии - нехватка параллелизма; неравномерная длительность задач - перекос данных. Колонки Input, Output, Shuffle Read, Shuffle Write.
- Ресурсы: память - spill, решения: увеличить размер воркеров, уменьшить число партиций, оптимизировать трансформации; CPU - Photon или больше воркеров; сеть - фильтрация раньше, broadcast join для малых таблиц, перепартиционирование. Server load distribution в Metrics: если драйвер сильно загружен, нужен больший тип инстанса.
- Перезапуск кластера: Compute > кластер > Restart; через CLI `databricks clusters restart CLUSTER_ID`. Перед этим проверьте Event log. Перезапуск прерывает задания и notebook.
- После исправления проверьте следующий запуск: время выполнения и ошибки в Spark UI.

### 5. Диагностика кеша, перекоса, spill и shuffle
Источник: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/5-resolve-cache-skew-spill-shuffle

- Инструменты: DAG (план выполнения), Spark UI (стадии и задачи), query profile для SQL-хранилищ (Query History > запрос > See query profile).
- **Кеш**: disk cache (бывший Delta cache) автоматически кеширует Parquet на воркерах; under-caching - повторные чтения (высокий Input), over-caching - давление на память. Spark cache (`.cache()`, `.persist()`) требует явного `.unpersist()`.
- **Перекос (skew)**: в Summary Metrics стадии сравните Max duration с 75-м перцентилем; если Max больше 75-го на 50 % и более - вероятен перекос. Причины: неравномерные ключи, null-значения в одной партиции, временное партиционирование. Решения: Adaptive Query Execution (включён по умолчанию), salting ключей, broadcast малых таблиц.
- **Spill**: метрики Shuffle Spill (Memory) и Shuffle Spill (Disk); любой ненулевой spill - давление памяти. Решения: увеличить число партиций (`spark.sql.shuffle.partitions` = `auto`), больше памяти, раннее выбирание колонок и фильтрация. Spill часто сопутствует перекосу - сначала устраняйте перекос.
- **Shuffle**: Shuffle Read/Write в Spark UI; exchange-узлы в DAG. Снижение: ранняя фильтрация, broadcast join (AQE конвертирует sort-merge в broadcast, если таблица меньше `spark.databricks.adaptive.autoBroadcastJoinThreshold` = 30 МБ по умолчанию), избегать лишних `repartition()`, bucketing или партиционирование для частых join по одному ключу.

### 6. Потоковая передача логов в Azure Log Analytics
Источник: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/6-implement-log-streaming-azure-analytics

- Логи поступают обычно в течение 15 минут через diagnostic settings (Send to Log Analytics); также возможны архивирование в storage account или отправка в Event Hub. Доставка без гарантии срока.
- Требуется план Azure Databricks Premium.
- Для аудита внутри Databricks рекомендуется системная таблица `system.access.audit`; Log Analytics - для кросс-сервисного мониторинга и KQL-алертов.
- Таблицы: DatabricksClusters, DatabricksJobs, DatabricksNotebook, DatabricksSQL, DatabricksUnityCatalog, DatabricksWorkspace, DatabricksSecrets. Стандартные колонки: TimeGenerated, OperationName, Identity, SourceIPAddress, RequestParams, Response.
- Запросы KQL: выборка последних событий job; поиск сбоев по `Response contains "error" or "failed"` с группировкой по часу; события кластеров; события создания, удаления и обновления таблиц (`ActionName in~ (...)`).
- Алерты: New alert rule из запроса, условие, Action group. Примеры: более пяти сбоев job за час; операции с таблицами вне рабочего времени; всплеск создания кластеров.
- Сценарии: диагностика сбоев (DatabricksJobs, затем DatabricksClusters и DatabricksNotebook), производительность (события масштабирования), безопасность (DatabricksUnityCatalog и DatabricksSecrets с SourceIPAddress), учёт затрат.

### 7. Упражнение: мониторинг, устранение неполадок и оптимизация
Источник: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/7-exercise-monitor-troubleshoot-optimize-workloads-azure-databricks

Упражнение (около 45 минут): синтетическая нагрузка с намеренным перекосом данных и избыточным shuffle; диагностика в Spark UI и исправление через broadcast join, Adaptive Query Execution и уменьшение shuffle. Требуется подписка Azure с правами администратора.

### 8. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/8-knowledge-check

В исходных материалах вопросы не приведены.

### 9. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/9-summary

Модуль охватил мониторинг кластеров (метрики, auto-termination, бюджеты), восстановление Lakeflow Jobs (матричный вид, repair run), диагностику Spark (Spark UI, метрики) и оптимизацию (кеш, перекос, spill, shuffle), а также централизацию логов в Log Analytics.

## Важные команды / код / настройки

Перезапуск кластера (CLI):

```
databricks clusters restart CLUSTER_ID
```

Проверка disk cache и Adaptive Query Execution:

```
spark.conf.get("spark.databricks.io.cache.enabled")
spark.conf.get("spark.databricks.optimizer.adaptive.enabled")
```

Освобождение Spark cache:

```
df.unpersist()
```

Настройка числа партиций shuffle:

```
spark.conf.set("spark.sql.shuffle.partitions", "auto")
```

Запросы к системным таблицам:

```
SELECT
  usage_date,
  sum(usage_quantity) as DBUs_Consumed
FROM system.billing.usage
WHERE billing_origin_product = "ALL_PURPOSE"
GROUP BY usage_date
ORDER BY usage_date ASC
```

```
WITH latest_clusters AS (
  SELECT cluster_id, owned_by
  FROM system.compute.clusters
  QUALIFY row_number() OVER (PARTITION BY cluster_id ORDER BY change_time DESC) = 1
)
SELECT
  c.owned_by,
  sum(u.usage_quantity) as total_dbus
FROM system.billing.usage u
JOIN latest_clusters c
  ON u.usage_metadata.cluster_id = c.cluster_id
WHERE u.usage_metadata.cluster_id IS NOT NULL
GROUP BY c.owned_by
ORDER BY total_dbus DESC
```

Запросы KQL в Log Analytics:

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

Настройки из уроков: auto-termination 10-10 000 минут; бюджеты - до четырёх порогов; порог перекоса - Max duration более чем на 50 % выше 75-го перцентиля; broadcast-порог AQE - 30 МБ по умолчанию (`spark.databricks.adaptive.autoBroadcastJoinThreshold`); логи Log Analytics - Premium-план, задержка до 15 минут.

## Что запомнить

- Для стоимости используйте бюджеты и `system.billing.usage`; auto-termination и autoscaling снижают простой.
- Статус job определяется листовыми задачами; repair run перезапускает только неуспешные ветви, но задача стартует заново, поэтому нужны идемпотентные записи.
- Перекос - главная причина spill; сначала ищите его через Summary Metrics стадии (Max против 75-го перцентиля).
- Снижайте shuffle: фильтрация раньше, broadcast join для малых таблиц, без лишних `repartition()`.
- Для централизованного мониторинга и KQL-алертов используйте diagnostic settings в Log Analytics (план Premium).

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/
- Упомянутые инструменты: Spark UI, query profile, Azure Log Analytics, system.billing.usage, system.access.audit (уроки 2-6)
