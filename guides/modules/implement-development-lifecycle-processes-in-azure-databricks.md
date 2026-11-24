# Реализация процессов жизненного цикла разработки в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/<юнит>`)

## Цель модуля

Организовать разработку конвейеров данных в Azure Databricks: контроль версий через Git folders, ветвление и pull request, стратегию тестирования (пирамида тестов) и развертывание через Declarative Automation Bundles (DABs) с Databricks CLI.

## Ключевые понятия

- **Git folders** — интеграция Git в рабочую область Azure Databricks: клонирование, ветки, коммиты, pull и push через визуальный клиент и API.
- **Declarative Automation Bundles (DABs)** — подход «инфраструктура как код»: ресурсы (jobs, pipelines) описываются в YAML; ранее назывались Databricks Asset Bundles.
- **Testing pyramid (пирамида тестирования)** — много быстрых unit-тестов внизу, меньше integration-тестов, еще меньше end-to-end и UAT наверху.
- **Unit tests** — проверка отдельных функций изолированно (в модуле — pytest с fixture на синтетических данных).
- **Integration tests** — проверка совместной работы компонентов, часто на тестовых таблицах Databricks; никогда не на продуктивных таблицах.
- **End-to-end tests** — проверка полного конвейера от входных данных до итоговой таблицы.
- **UAT (user acceptance testing)** — приемка бизнес-пользователями в staging-среде.
- **databricks.yml** — главный конфигурационный файл бандла в корне проекта; включает bundle, include, resources, targets и variables.
- **Targets (цели развертывания)** — окружения (dev, prod и др.) с разными настройками; режимы `development` и `production`.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/1-introduction
Надежные решения требуют процессов: совместной работы, контроля качества и согласованных развертываний. Git folders дают версионирование в рабочей области, DABs — инфраструктуру как код, пирамида тестирования — раннее обнаружение ошибок.

### 2. Apply Git version control best practices
Источник: https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/2-apply-version-control-git
Git folder подключается к удаленному репозиторию (Azure DevOps, GitHub, GitLab, Bitbucket). Каждый участник должен работать в собственной Git folder, подключенной к общему репозиторию. Перед новой работой выполняйте pull; при pull изменений notebook состояние notebook сбрасывается (выводы ячеек, комментарии и история версий). Используйте `.gitignore` (для уже отслеживаемых файлов нужно явное удаление из индекса). Удаляйте устаревшие ветки. Ограничения: рабочие ветки до 1 ГБ, рекомендуется не более 20 000 ассетов; для больших репозиториев — sparse checkout.

### 3. Manage branching and pull requests
Источник: https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/3-manage-branching-pull-requests-conflicts
Ветку создают через диалог Git, базируя ее на main. Примеры имен: `feature/feature-name`, `bugfix/issue-description`, `users/username/description`. Переключение ветки может удалить ассеты, которых нет в целевой ветке. Коммит и push — через Commit & Push; если нет прав на main, создайте feature-ветку и pull request через интерфейс провайдера. Outputs notebook не попадают в коммит в форматах `.py`, `.scala`, `.sql`, `.r`; для версионирования выводов используйте IPYNB. Конфликты: Keep current / Take incoming, ручное разрешение по маркерам, Mark As Resolved, Continue Merge / Continue Rebase, Abort.

### 4. Implement testing strategy
Источник: https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/4-implement-testing-strategy
Пирамида тестирования: unit (миллисекунды, одна функция), integration (секунды, несколько компонентов), end-to-end (минуты, полный конвейер), UAT (бизнес-сценарии). Unit-тесты пишутся на pytest; файлы названы `test_*.py` или `*_test.py`; fixture создает синтетические данные. Запуск в блокноте: `%pip install pytest` и `pytest.main`. Функции должны возвращать значения одного типа (DataFrame, даже пустой). Integration-тесты работают с реальными тестовыми ресурсами (отдельная тестовая схема или каталог), никогда не с продуктивными таблицами. End-to-end-тесты запускают полный конвейер и проверяют итоги, затем очищают данные; их лучше запускать вне пика нагрузки или в пайплайне развертывания. UAT — определить критерии приемки заранее, создать staging, подготовить сценарии и порядок обратной связи. Структура проекта: `src/`, `tests/unit`, `tests/integration`, `tests/e2e`, `notebooks/run_tests.py`, `requirements.txt`. Тесты можно запускать из Databricks job перед развертыванием.

### 5. Configure and package Declarative Automation Bundles
Источник: https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/5-configure-package-databricks-asset-bundles
Файл `databricks.yml` находится в корне проекта: в нем bundle (имя), include (например, `resources/*.yml`), workspace, resources и targets. Переменные задаются в `variables` и подставляются через `${var.name}`; значения можно переопределить в target, через `--var="name=value"` или переменные окружения с префиксом `BUNDLE_VAR_`. Jobs содержат задачи (tasks), например `notebook_task` и `spark_python_task`; зависимости задаются через `depends_on`; параметры — через `base_parameters`; compute задается через `existing_cluster_id` или `job_clusters` с `new_cluster`. Пути в конфигурации — относительно файла, где они объявлены. В режиме `development` имена ресурсов получают префикс `[dev username]`, расписания приостанавливаются, параллельные запуски разрешены. В режиме `production` CLI проверяет соответствие локальной Git-ветки указанной в `git` и рекомендует service principals. Через `presets` тонко настраиваются поведение (например, `name_prefix`, `trigger_pause_status`, `tags`).

### 6. Deploy bundle with Databricks CLI
Источник: https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/6-deploy-bundle-databricks-cli
Последовательность: `databricks bundle validate` (проверка), `databricks bundle plan` (предпросмотр), `databricks bundle deploy` (развертывание; `-t` выбирает target). CLI хранит состояние в рабочей области: создает новые ресурсы, обновляет существующие и удаляет те, что исчезли из конфигурации. У каждого развертывания уникальная идентичность (имя бандла, target и пользователь); одновременные развертывания одного бандла в один target конфликтуют. Для CI/CD добавляется `--auto-approve`. `databricks bundle summary` выводит ссылки на ресурсы; `databricks bundle open <ресурс>` открывает ресурс в браузере. Устранение неполадок: `databricks auth login --host ...` при ошибках аутентификации; `--force-lock` при зависшей блокировке (только если никакое другое развертывание не выполняется); `--fail-on-active-runs` — прервать развертывание при активных запусках; обновить CLI при предупреждениях о свойствах.

### 7. Exercise - Implement development lifecycle processes in Azure Databricks
Источник: https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/7-exercise-implement-development-lifecycle-processes-in-azure-databricks
Практика (около 45 минут): тестирование конвейера трансформации через pytest, затем упаковка и развертывание конвейера как DAB через Databricks CLI. Нужна подписка Azure с правами администратора.

### 8. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/8-knowledge-check
Проверка знаний (в исходнике текст отсутствует).

### 9. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/9-summary
Git folders, ветвление с pull request, стратегия тестирования и DABs с развертыванием через CLI вместе обеспечивают совместную работу, качество и воспроизводимые развертывания по окружениям.

## Важные команды / код / настройки

Минимальный `databricks.yml`:

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

Переменные и подстановка:

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

Переопределение переменных по target:

```yaml
targets:
  dev:
    default: true
    variables:
      cluster_id: 1234-567890-abcde123
      environment: development
  prod:
    variables:
      cluster_id: 9876-543210-zyxwv987
      environment: production
```

Задачи с зависимостями и job-кластер:

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

Режимы целей:

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

Тест pytest для функции фильтрации:

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

Запуск тестов в блокноте:

```python
%pip install pytest

import pytest
retcode = pytest.main([".", "-v", "-p", "no:cacheprovider"])
assert retcode == 0, "Tests failed. Check the output above."
```

Команды CLI:

```bash
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

Флаги: `--var="cluster_id=5678-901234-fghij567"`, `--fail-on-active-runs`.

## Что запомнить

- Каждый участник работает в собственной Git folder; перед работой делайте pull, помня про сброс состояния notebook.
- Ветки от main с понятными именами; pull request проводится в интерфейсе Git-провайдера.
- Пирамида тестов: много unit, меньше integration, мало end-to-end и UAT; integration-тесты никогда не запускайте на продуктивных таблицах.
- DABs описывают jobs и pipelines в `databricks.yml` и YAML-файлах; target задает окружение, а переменные — параметры.
- Порядок развертывания: `validate` → `plan` → `deploy`; для CI/CD — `--auto-approve`; `--force-lock` — только если другое развертывание не запущено.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/
- Документация: Bundle configuration in Python; Collaborate on bundles in the workspace (упоминаются в уроках 5–6).
- Связанный модуль: Machine learning in Azure Databricks (`machine-learning-azure-databricks`).
- Связанный модуль: MLflow в Azure Databricks (`mlflow-azure-databricks`).
