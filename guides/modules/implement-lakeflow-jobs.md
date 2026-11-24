# Реализация Lakeflow Jobs в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/

## Цель модуля

Создать и настроить Lakeflow Job (задачи, compute, зависимости, параметры, права, run identity с доступом к Unity Catalog), настроить триггеры (table update, file arrival, continuous) и расписания (simple и cron), выстроить оповещения и автоматические перезапуски с повторами и таймаутами.

## Ключевые понятия

- **Lakeflow Job** - оркестратор задач, организованных в DAG; у каждого задания есть имя, задачи и compute.
- **Run identity** - principal, права которого проверяет Unity Catalog при выполнении задания (по умолчанию владелец job; для production можно service principal).
- **Права на job** - CAN VIEW, CAN RUN, CAN MANAGE RUN, CAN MANAGE.
- **Trigger (триггер)** - условие запуска на основе событий: Table update, File arrival, Continuous.
- **Schedule (расписание)** - Simple (интервал) или Advanced (cron-выражение с часовым поясом).
- **Maximum concurrent runs и очередь** - ограничение параллельных запусков и поведение новых запусков: Queue, Cancel, Skip.
- **Notifications (уведомления)** - события Start, Success, Failure, Duration warning, Streaming backlog; назначения: email, Slack, Microsoft Teams, PagerDuty, HTTP webhook.
- **Retries (повторы)** - число и интервал повторов задачи; таймауты; экспоненциальный backoff для continuous jobs.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/1-introduction

Автоматизация - основа production-конвейеров: задания должны выполняться без вмешательства человека, реагировать на изменения данных и восстанавливаться после сбоев. Lakeflow Jobs даёт оркестрацию, триггеры, расписания, оповещения и политики повторов.

### 2. Создание и настройка Lakeflow Job
Источник: https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/2-create-lakeflow-job

- Создание: Jobs & Pipelines > Create > Job; у каждой задачи есть имя и тип (Notebook, Python script, Python wheel, SQL, Pipeline, dbt, JAR, Spark Submit, Run Job).
- Источник кода: Workspace, Git provider (единая ссылка на commit/ветку для всех задач job) или DBFS/ADLS (для Python-скриптов, по URI `abfss://...`).
- Compute: serverless (по умолчанию для поддерживаемых типов), classic jobs compute (версия Spark, типы инстансов, автомасштабирование), SQL warehouse. Просмотр и изменение: Job details > Compute (Configure или Swap).
- Зависимости задаются полем Depends on и условием Run if (All succeeded, At least one succeeded, None failed, All done, At least one failed, All failed).
- Параметры job доступны всем задачам; в notebook - через `dbutils.widgets.get("имя")`, в Python-скриптах - как аргументы командной строки; динамические значения вида `{{job.trigger.time.iso_date}}`.
- Теги помогают фильтровать задания и передаются в job-кластеры для учёта затрат.
- Права на job: CAN VIEW, CAN RUN, CAN MANAGE RUN, CAN MANAGE; настраиваются во вкладке Permissions. Задание выполняется с правами владельца job или service principal, а не инициатора запуска.
- Для доступа к Unity Catalog run identity нужны привилегии: SELECT (чтение таблицы), MODIFY (запись), CREATE TABLE и USE SCHEMA (создание таблиц в схеме), READ VOLUME или WRITE VOLUME (тома). Без них задание падает с ошибкой авторизации.

### 3. Настройка триггеров задания
Источник: https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/3-configure-job-triggers

- **Table update**: запуск при обновлении отслеживаемых таблиц (Delta и Iceberg managed, external Delta, materialized views, streaming tables, зависимые view). Варианты: Any table is updated или All tables are updated. Дополнительно: Minimum time between triggers и Wait after last change (например, 60 секунд для группировки обновлений). Для ускорения включите file events на external location.
- Параметры table update: `{{job.trigger.table_update.updated_tables}}`, `{{job.trigger.table_update.<catalog.schema.table>.commit_timestamp.iso_datetime}}`, `{{job.trigger.table_update.<catalog.schema.table>.version}}`.
- **File arrival**: запуск при появлении новых файлов в external location или volume (например, `/Volumes/mycatalog/myschema/myvolume/incoming/`); проверка примерно раз в минуту; рекурсивно проверяет подкаталоги. Перезапись файла с тем же именем не запускает задание. Без file events: до 50 таких заданий на рабочую область и до 10 000 файлов в отслеживаемом месте.
- **Continuous**: новый запуск сразу после завершения или сбоя предыдущего. На serverless поддерживаются только ограниченные триггеры Structured Streaming (например, `Trigger.AvailableNow`); `Trigger.ProcessingTime` и `Trigger.Continuous` требуют classic jobs compute. Для low-latency на serverless используйте Lakeflow pipelines в continuous mode.
- Управление: Pause и Resume в разделе Schedules & Triggers; уведомления о сбое оценки триггера (например, после изменения прав).

### 4. Расписание задания
Источник: https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/4-schedule-job

- **Simple**: интервал (минуты, часы, дни, недели); первый запуск время выбирает планировщик. Минимальный интервал - 10 секунд.
- **Advanced**: cron-выражение, период, время начала и часовой пояс; Show Cron Syntax для редактирования.
- Часовой пояс: при DST почасовые задания могут пропустить запуск или сдвинуться; для абсолютных интервалов и согласования регионов используйте UTC.
- Maximum concurrent runs: по умолчанию допускаются параллельные запуски; для заданий, которые не должны пересекаться, установите 1.
- Поведение при превышении лимита: Queue the run (ждать свободного слота; рекомендуется для большинства конвейеров), Cancel the run, Skip the run. Поставленные в очередь запуски не потребляют ресурсы.
- Для production: закладывайте буфер между зависимыми конвейерами, не полагайтесь на точность до секунды, следите за историей запусков.

### 5. Настройка оповещений job
Источник: https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/5-configure-job-alerts

- События: Start, Success, Failure, Duration warning, Streaming backlog (порог превышен в течение 10 минут).
- Состояние Succeeded with failures считается успешным; для видимости частичных сбоев настройте task-level уведомления.
- Назначения: email и системные назначения (Slack, Microsoft Teams, PagerDuty, HTTP webhook). Системные назначения создаёт администратор рабочей области: Admin Settings > Notifications. Не более трёх системных назначений на событие для каждого job или задачи. Используйте разные учётные данные для разных назначений.
- Настройка job-уведомлений: Job details > Job notifications > Edit notifications > Add notification.
- Уведомления job не отправляются при повторах отдельных задач; для этого нужны task-level уведомления.
- Mute notifications until the last retry - не слать уведомления на каждую попытку. Mute для skipped и canceled runs - только для job-level; task-level фильтры задаются отдельно.
- Webhook получает JSON с полями `event_type`, `workspace_id`, `run.run_id`, `job.job_id`, `job.name`.
- При оркестрации через Azure Data Factory: Monitor > Alerts & metrics в портале Data Factory (статус запусков, количество activity runs, загрузка Integration Runtime).

### 6. Автоматические перезапуски
Источник: https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/6-configure-job-automatic-restarts

- По умолчанию для большинства заданий повторы отключены; serverless jobs по умолчанию оптимизируют повторы. Continuous jobs используют экспоненциальный backoff и перезапускают всё задание. Для неидемпотентных операций повторы и авто-оптимизацию нужно отключать.
- Task-level: Tasks > задача > Retries > + Add; задаются число попыток и интервал (в миллисекундах от начала неудачного запуска до следующего).
- Таймаут применяется к каждой попытке; таймаут считается неудачной попыткой и запускает повтор, если попытки остались.
- Continuous: Add trigger > Continuous > Task retry mode (On failure - по умолчанию для новых заданий; Never - повтор только на уровне job). Зависимости и task-level повторы в классическом смысле не поддерживаются.
- Таймауты: Metric thresholds > Run duration > Warning (уведомление) и Timeout (остановка). Статус задачи - "Timed Out".
- Рекомендации: 1-3 повтора, интервалы 30 секунд - 5 минут для транзиентных сбоев; не используйте неограниченные повторы; отслеживайте частоту повторов; проектируйте идемпотентные операции; документируйте выбранные параметры.

### 7. Упражнение: реализация Lakeflow Jobs в Azure Databricks
Источник: https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/7-exercise-implement-lake-flow-jobs

Упражнение (около 45 минут): конвейер обработки записей о вызовах (CDR) компании TelConnect через слои bronze, silver и gold. Нужно запустить параметризованный notebook и настроить Lakeflow Job: зависимости задач, параметр job, расписание и триггер по событию, уведомления об ошибках и политику повторов. Требуется подписка Azure с правами администратора.

### 8. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/8-knowledge-check

В исходных материалах вопросы не приведены.

### 9. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/9-summary

Модуль охватил создание job с DAG, выбор compute, зависимости, триггеры (table update, file arrival, continuous), расписания (simple и cron), оповещения и автоматические перезапуски (task-level повторы и экспоненциальный backoff для continuous jobs).

## Важные команды / код / настройки

Выдача привилегий run identity (SQL):

```
GRANT SELECT, MODIFY ON TABLE catalog.schema.table TO `service-principal-id`;
GRANT USE SCHEMA ON SCHEMA catalog.schema TO `service-principal-id`;
```

Динамические значения и параметры:

```
{{job.parameters.target_catalog}}
{{job.trigger.time.iso_date}}
{{job.trigger.table_update.updated_tables}}
{{job.trigger.table_update.<catalog.schema.table>.version}}
```

Чтение параметра в notebook:

```
target_catalog = dbutils.widgets.get("target_catalog")
spark.sql(f"USE CATALOG {target_catalog}")
```

Пути для file arrival trigger:

```
/Volumes/mycatalog/myschema/myvolume/
/Volumes/mycatalog/myschema/myvolume/incoming/
```

Формат cron (шесть или семь полей):

```
Секунды Минуты Часы День_месяца Месяц День_недели [Год]
```

Примеры cron из урока:

| Выражение | Расписание |
|---|---|
| `0 0 12 * * ?` | каждый день в 12:00 |
| `0 15 10 ? * MON-FRI` | по будням в 10:15 |
| `0 0 8 1 * ?` | 1-го числа каждого месяца в 8:00 |
| `0 30 6 ? * 6L` | последняя пятница месяца в 6:30 |
| `0 0 */2 * * ?` | каждые 2 часа |

Пример полезной нагрузки webhook:

```
{
  "event_type": "jobs.on_failure",
  "workspace_id": "your_workspace_id",
  "run": {
    "run_id": "run_id"
  },
  "job": {
    "job_id": "job_id",
    "name": "job_name"
  }
}
```

Настройки из уроков: минимальный интервал simple-расписания - 10 секунд; не более трёх системных назначений на событие; интервал повтора указывается в миллисекундах; Metric thresholds: Warning и Timeout.

## Что запомнить

- Run identity должна иметь нужные привилегии Unity Catalog, иначе задание падает с ошибкой авторизации даже при корректной конфигурации.
- Table update и file arrival триггеры запускают job по событиям; continuous - сразу после завершения предыдущего запуска.
- Для непересекающихся запусков задайте Maximum concurrent runs = 1 и режим Queue the run.
- Используйте Mute notifications until the last retry, чтобы не получать уведомления на каждой попытке.
- Повторы - 1-3 попытки с разумным интервалом; таймаут применяется к каждой попытке; проектируйте задачи идемпотентными.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/
- Design and implement data pipelines (упомянут в уроке 2 как модуль о If/else и For each): https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/
