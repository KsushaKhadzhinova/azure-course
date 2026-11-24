# Развертывание и поддержка пайплайнов данных и нагрузок в Azure Databricks

**Источник** https://learn.microsoft.com/en-us/training/paths/azure-databricks-data-engineer-deploy-maintain-data-pipelines-workloads

## О курсе

Полный жизненный цикл пайплайнов данных в Azure Databricks: проектирование, оркестрация, мониторинг и оптимизация.

- **Уровень:** средний (Intermediate)
- **Роль:** Data Engineer
- **Продукты и сервисы:** Azure Databricks
- **Предварительные требования:** Хорошее понимание рабочих областей Azure Databricks; знакомство с концепциями инженерии данных и SQL; опыт Python и ноутбуков; основы системы контроля версий Git.

## Чему научитесь

- Проектирование и внедрение пайплайнов данных с помощью ноутбуков и Lakeflow pipelines.
- Создание и оркестрация Lakeflow Jobs с триггерами, расписаниями и обработкой ошибок.
- Интеграция с практиками разработки через Git folders.
- Мониторинг и оптимизация нагрузок данных.

## Модули

1. **Проектирование и реализация конвейеров данных в Azure Databricks**. Спроектировать конвейер данных по архитектуре medallion (bronze, silver, gold), выбрать между notebook и Lakeflow pipelines, настроить логику задач в Lakeflow Jobs (зависимости, условия, For each, параметры) и заложить обработку ошибок (expectations, повторы, таймауты, уведомления, исключения в коде). [guide](../modules/design-implement-data-pipelines.md)
2. **Реализация Lakeflow Jobs в Azure Databricks**. Создать и настроить Lakeflow Job (задачи, compute, зависимости, параметры, права, run identity с доступом к Unity Catalog), настроить триггеры (table update, file arrival, continuous) и расписания (simple и cron), выстроить оповещения и автоматические перезапуски с повторами и таймаутами. [guide](../modules/implement-lakeflow-jobs.md)
3. **Реализация процессов жизненного цикла разработки в Azure Databricks**. Организовать разработку конвейеров данных в Azure Databricks: контроль версий через Git folders, ветвление и pull request, стратегию тестирования (пирамида тестов) и развертывание через Declarative Automation Bundles (DABs) с Databricks CLI. [guide](../modules/implement-development-lifecycle-processes-in-azure-databricks.md)
4. **Мониторинг, устранение неполадок и оптимизация нагрузок в Azure Databricks**. Отслеживать потребление ресурсов кластеров и SQL-хранилищ, контролировать стоимость (бюджеты и системные таблицы), диагностировать и восстанавливать Lakeflow Jobs и Spark-задания, устранять проблемы производительности (кеш, перекос данных, spill, shuffle) и настроить централизованное логирование в Azure Log Analytics. [guide](../modules/monitor-troubleshoot-optimize-workloads-azure-databricks.md)

## Ключевые технологии и понятия

- Medallion architecture (bronze, silver, gold)
- Notebook
- Lakeflow pipelines (Lakeflow Declarative Pipeline)
- Streaming table
- Materialized view
- Lakeflow Jobs / DAG
- Dependency condition
- If/else condition task
- Run if dependencies
- For each task
- Expectations (ожидания качества данных)
- Retry policy, timeouts, notifications
- Ingest
- Clean and validate

## Для каких ролей полезно

- Data Engineer (DE, инженер данных)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/azure-databricks-data-engineer-deploy-maintain-data-pipelines-workloads
- Модуль «Проектирование и реализация конвейеров данных в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/design-implement-data-pipelines/
- Модуль «Реализация Lakeflow Jobs в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/implement-lakeflow-jobs/
- Модуль «Реализация процессов жизненного цикла разработки в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/implement-development-lifecycle-processes-in-azure-databricks/
- Модуль «Мониторинг, устранение неполадок и оптимизация нагрузок в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/
