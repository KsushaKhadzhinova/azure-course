# Выбор и настройка вычислительных ресурсов в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/

## Цель модуля

Научиться выбирать тип вычислительного ресурса (serverless, classic, SQL warehouse, job compute, instance pools) для нагрузки, настраивать производительность (узлы, автомасштабирование, завершение работы), функции (Photon, версия Runtime), устанавливать библиотеки и управлять доступом к compute.

## Ключевые понятия

- **Serverless compute** - полностью управляемые вычисления Azure Databricks; запускаются за 2-6 секунд; не поддерживают Scala и R в notebooks, RDD API, JAR-библиотеки и часть Spark-настроек.
- **Classic compute** - вычисления, которые создаются и настраиваются пользователем в вашей подписке; запуск 3-7 минут.
- **Access mode (режим доступа)** - Standard (несколько пользователей, изоляция через Lakeguard) и Dedicated (один пользователь или группа; нужны для RDD, R, ML и GPU).
- **Multi-node / single-node cluster** - кластер с driver и workers или только с driver.
- **Performance mode serverless** - Performance-optimized (по умолчанию, старт за секунды) и Standard (дешевле до 70% DBU, старт 4-6 минут).
- **SQL warehouse** - вычисления для SQL: serverless, pro и classic.
- **Instance pool (пул экземпляров)** - набор простаивающих VM для быстрого запуска кластеров; оплачиваются простаивающие VM.
- **Job compute** - кластеры для автоматических задач; завершаются после выполнения.
- **Spot instances (Azure Spot VMs)** - дешевые VM, которые Azure может отобрать с уведомлением за 30 секунд.
- **Flexible node types** - резервные типы VM при нехватке мощности (ошибка CLOUD_PROVIDER_RESOURCE_STOCKOUT).
- **Photon** - движок выполнения запросов, ускоряющий SQL и DataFrame; несовместим с GPU.
- **Databricks Runtime (LTS)** - версия среды с Spark; LTS - для стабильных производственных задач.
- **Compute-scoped libraries (библиотеки уровня кластера)** - устанавливаются на кластер и переустанавливаются при каждом запуске.
- **Allowlist** - список одобренных администратором библиотек и init-скриптов для standard access mode.
- **Permission levels (уровни прав)** - No permissions, CAN ATTACH TO, CAN RESTART, CAN MANAGE.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/1-introduction

Выбор типа и конфигурации compute влияет на стоимость, производительность и безопасность. В разработке нужны быстрые циклы, в production - стабильность и экономия. Модуль учит выбирать compute, настраивать производительность, функции, библиотеки и доступ.

### 2. Choose an appropriate compute type
https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/2-choose-appropriate-compute-type

Описаны serverless compute (ограничения: Scala и R в notebooks, RDD, JAR; режимы Performance-optimized и Standard), classic compute (Standard и Dedicated access modes; multi-node и single-node), SQL warehouses (serverless, pro, classic), instance pools и job compute. Таблица сравнения и рекомендации: начинать с serverless и переходить на classic при конкретном ограничении.

### 3. Configure compute performance
https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/3-configure-compute-performance

Производительность зависит от ядер executor, памяти executor и локального хранилища для shuffle. Типы узлов: memory-optimized (E-series), compute-optimized (F-series), storage-optimized (L-series), GPU (NC- и ND-series). Flexible node types, автомасштабирование (optimized autoscaling; проверка каждые 40 секунд для job compute и 150 секунд для all-purpose), завершение по неактивности (рекомендуется 45 минут для интерактивной работы), spot-инстансы для workers, но не для driver, decommissioning, instance pools и диагностика через Spark UI.

### 4. Configure compute features
https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/4-configure-compute-feature-settings

Photon - ускоряет SQL и DataFrame (по умолчанию с Databricks Runtime 9.1 LTS и выше), не поддерживается на GPU-кластерах. Для производственных задач выбирайте LTS-версии Runtime, для разработки - новейшую. Для ML используйте Databricks Runtime ML; для GPU Photon нужно отключить.

### 5. Install libraries for compute
https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/5-install-libraries-for-compute

Библиотеки уровня кластера доступны всем notebooks и заданиям и переустанавливаются при запуске; для установки нужно право CAN MANAGE. Источники: PyPI, Maven, CRAN, workspace files, Unity Catalog volumes и облачное хранилище. Рекомендуется указывать точную версию (например, `pymssql==2.3.9`). Для standard access mode Maven-координаты, JAR и init-скрипты требуют allowlist у metastore admin. Для Runtime 15.0+ поддерживается requirements.txt. Init-скрипты - крайний случай; для Runtime 13.3 LTS и выше их хранят в volumes.

### 6. Configure compute access
https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/6-configure-compute-access-perms

Четыре уровня прав: No permissions, CAN ATTACH TO (подключение и Spark UI), CAN RESTART (управление жизненным циклом), CAN MANAGE (полный контроль, включая права других). Driver logs по умолчанию видны только CAN MANAGE, так как могут содержать секреты. Режим No isolation shared является устаревшим. Dedicated group access mode: назначение кластера группе (Unity Catalog, Runtime 15.4+), объекты принадлежат группе. Также упоминаются entitlement "Allow cluster creation" и аудит через system.access.audit.

### 7. Exercise - Select and Configure Compute in Azure Databricks
https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/7-exercise-select-configure-compute

Практическое задание (около 45 минут): создание all-purpose кластера, установка библиотек на уровне кластера и notebook, генерация и анализ синтетических записей пациентов через библиотеку faker и PySpark. Нужна подписка Azure с правами администратора.

### 8. Module assessment
https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/8-knowledge-check

Проверка знаний (около 5 минут). Текст вопросов в источнике не приведен.

### 9. Summary
https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/9-summary

Serverless дает быстрый старт с минимальными затратами; classic - полный контроль; SQL warehouses - аналитика; job clusters - автоматизация без простоя. Производительность настраивается через узлы, автомасштабирование и завершение; Photon ускоряет SQL. Права по принципу наименьших привилегий, библиотеки из репозиториев и volumes с allowlist.

## Важные команды / код / настройки

**Установка библиотеки PyPI с версией:** `pymssql==2.3.9`.

**Maven-координаты:** формат `groupId:artifactId:version`, например `com.microsoft.sqlserver:mssql-jdbc:13.2.1.jre11`. Allowlist: `groupId:artifactId:version`, `groupId:artifactId` или `groupId`.

**Пути к файлам библиотек и скриптов (примеры из источника):**
- Workspace files (лимит 500 МБ): `/Workspace/Users/you@example.com/libraries/mypackage-1.0.0-py3-none-any.whl`
- Unity Catalog volume (нужно право READ VOLUME): `/Volumes/main/engineering/libraries/mypackage-1.0.0-py3-none-any.whl`
- Init-скрипт в volume (Runtime 13.3 LTS и выше): `/Volumes/main/engineering/scripts/setup.sh`

Allowlist использует префиксное сопоставление; завершающий слеш предотвращает случайное совпадение каталогов (например, `/Volumes/prod-libraries/`).

**Параметры производительности и жизненного цикла:**
- Serverless Performance-optimized (по умолчанию) и Standard (до 70% меньше DBU, старт 4-6 минут).
- Автомасштабирование: минимум и максимум workers; оптимизированное масштабирование; проверка каждые 40 секунд (job compute) и 150 секунд (all-purpose).
- Автозавершение: например, 45 минут неактивности для интерактивной работы.
- Instance pool: минимум простаивающих экземпляров, максимум, автозавершение простоя (пример: минимум 3, завершение через 30 минут).
- Spot-инстансы: для workers; driver - on-demand.

**Флаг Spark для логов драйвера:** `spark.databricks.acl.needAdminPermissionToViewLogs` (по умолчанию доступ к логам драйвера только у CAN MANAGE).

**Отключение flexible node types для кластера:** установить `alternate_node_type_ids` в пустой список через Clusters API.

**Путь к папке группы:** `/Workspace/Groups/<groupName>` с правом CAN MANAGE для группы.

**Журнал доступа:** таблица `system.access.audit`.

**Photon и GPU:** Photon по умолчанию с Databricks Runtime 9.1 LTS и выше; для GPU-кластеров Photon нужно отключить.

## Что запомнить

- Начинайте с serverless; переходите на classic только при ограничении serverless (RDD, R, JAR, Scala в notebooks, нестандартная сеть).
- Dedicated access mode нужен для RDD, R, ML и GPU; Standard - для совместного использования.
- Driver на on-demand, workers могут быть spot: отозванный driver приводит к падению всего кластера.
- Библиотеки уровня кластера переустанавливаются при запуске; для standard access mode нужен allowlist; версии закрепляйте явно.
- Driver logs могут содержать секреты, поэтому по умолчанию доступ к ним только у CAN MANAGE; секреты храните в Databricks secret scopes.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/select-and-configure-compute/
- В источнике есть схемы выбора типа compute, установки библиотек и уровней доступа (без текстового описания). Упомянуты также документация по allowlist библиотек и Spark UI; ссылки в тексте не приведены.
