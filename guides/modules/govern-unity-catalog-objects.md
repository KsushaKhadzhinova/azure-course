# Управление объектами Unity Catalog

**Источник:** https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/

## Цель модуля

Документировать таблицы и столбцы (комментарии и теги), применять управление доступом на основе атрибутов (ABAC) через governed tags и политики, настраивать хранение данных (retention, VACUUM, predictive optimization) и удаление по запросам, отслеживать lineage и аудит, а также спроектировать безопасный сценарий OpenSharing (ранее Delta Sharing).

## Ключевые понятия

- **Комментарии (comments)** - описания каталогов, схем, таблиц, представлений и столбцов; для изменения комментария выполняется ALTER.
- **Теги (tags)** - пары ключ-значение для классификации и поиска; в отличие от комментариев позволяют структурированную классификацию.
- **Governed tags** - теги с заранее определёнными ключами и допустимыми значениями на уровне аккаунта; отмечаются значком замка.
- **ABAC (attribute-based access control)** - политики, которые применяются по атрибутам (тегам), а не к каждой таблице отдельно.
- **Row filter / column mask (фильтр строк, маска столбца)** - функции-UDF, которые скрывают строки или маскируют значения для указанных групп.
- **delta.logRetentionDuration / delta.deletedFileRetentionDuration** - сроки хранения журнала транзакций (по умолчанию 30 дней) и удалённых файлов (по умолчанию 7 дней).
- **VACUUM** - удаление файлов, на которые больше не ссылается таблица и которые старше порога хранения.
- **Predictive optimization** - автоматический VACUUM, OPTIMIZE и ANALYZE для управляемых таблиц.
- **Data lineage (происхождение данных)** - автоматически собираемые связи между таблицами, колонками, заданиями и дашбордами.
- **Audit log (`system.access.audit`)** - журнал действий на уровне аккаунта.
- **OpenSharing (ранее Delta Sharing)** - обмен данными без копирования; протоколы Databricks-to-Databricks и Databricks-to-Open.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/1-introduction

Governance включает видимость данных, подотчётность, централизованное управление политиками, lineage, аудит и безопасный обмен. Unity Catalog - основа для всех этих возможностей.

### 2. Создание и сохранение определений таблиц и столбцов
Источник: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/2-preserve-table-column-definitions

- Комментарии добавляются в `CREATE TABLE` (`COMMENT` у столбца) или через `COMMENT ON TABLE ... IS '...'` и `ALTER COLUMN ... COMMENT`. Поддерживается Markdown.
- AI-генерация комментариев в Catalog Explorer (AI generate): проверяйте предложения перед сохранением; не используйте их для классификации PII. Сохранение выполняет ALTER, который может нарушить работу конвейеров.
- Права на комментарии: владение таблицей, либо MODIFY и SELECT плюс USE CATALOG и USE SCHEMA. Для представлений и материализованных представлений - владение. Просмотр комментариев - с привилегией BROWSE.
- Теги: `ALTER TABLE ... SET TAGS ('domain' = 'sales')`, `ALTER COLUMN ... SET TAGS`, удаление - `UNSET TAGS`.
- Governed tags: администраторы задают допустимые ключи и значения на уровне аккаунта.
- Ограничения тегов: до 50 тегов на объект; до 1 000 тегов столбцов на таблицу; ключи и значения до 256 символов; ключи чувствительны к регистру; в ключах запрещены символы `. , - = / :`; пробелы по краям недопустимы.
- Обнаружение: Catalog Explorer (вкладки Columns, Sample Data, Details, History, Insights за 30 дней); SQL: `SHOW CATALOGS`, `SHOW SCHEMAS IN`, `SHOW TABLES IN`, `DESCRIBE TABLE EXTENDED`, `SHOW TBLPROPERTIES`; поиск по тегам; ERD по внешним ключам.

Пример из урока:

```
ALTER TABLE sales.customers.profiles
ALTER COLUMN email
SET TAGS ('pii' = 'email', 'sensitivity' = 'high');
```

### 3. Настройка ABAC с помощью тегов и политик
Источник: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/3-configure-attribute-based-access-control-tags-policies

- Отличия: стандартные теги - любой с APPLY TAG; governed tags - заранее заданные ключи и значения, назначать может только пользователь с правом ASSIGN; визуальный признак - замок.
- Создание governed tag: Catalog > Govern > Governed Tags > Create governed tag. Значения хранятся в открытом виде, поэтому не используйте в них чувствительные данные.
- Теги на каталогах и схемах наследуются объектами для оценки ABAC; теги на отдельных столбцах не наследуются.
- **Row filter**: UDF возвращает TRUE для строк, которые можно видеть. Пример политики `CREATE POLICY ... ON CATALOG ... ROW FILTER ... TO analysts FOR TABLES MATCH COLUMNS has_tag_value('pii','address') AS addr USING COLUMNS (addr)`.
- **Column mask**: UDF возвращает маскированное значение; политика `COLUMN MASK ... TO account users EXCEPT compliance_team`.
- Рекомендации по UDF: простая логика, детерминированность, без внешних вызовов, только столбцы таблицы, SQL вместо Python, тестирование на объёмах.
- Политики выполняются по идентичности вызывающего пользователя (session user), а не владельца представления.
- Квоты: 100 политик на каталог, 100 на схему, 50 на таблицу, 10 000 на metastore, 20 принципалов на политику (TO и EXCEPT вместе). На таблицу - одна row filter, на столбец - одна маска.
- Для доступа к таблицам с ABAC нужен Databricks Runtime 16.4 или новее либо serverless compute; старые рантаймы падают, если пользователь не указан в EXCEPT.

Пример из урока:

```
CREATE OR REPLACE FUNCTION sales.governance.mask_ssn(ssn STRING)
RETURNS STRING
DETERMINISTIC
RETURN '***-**-****';
```

### 4. Применение политик хранения данных
Источник: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/4-apply-data-retention-policies

- `delta.logRetentionDuration` (по умолчанию 30 дней) - история журнала; `delta.deletedFileRetentionDuration` (по умолчанию 7 дней) - когда VACUUM может удалить файлы. Для более длинного time travel нужно менять оба свойства; рост срока увеличивает затраты на хранение.
- `VACUUM` удаляет неиспользуемые файлы старше порога; после этого time travel к старым версиям невозможен. Для таблиц с deletion vectors нужен `REORG TABLE ... APPLY (PURGE)` перед VACUUM.
- Право на удаление данных: `DELETE FROM bronze.users WHERE user_id = 12345`; пакетно через MERGE с контрольной таблицей запросов (`WHEN MATCHED THEN DELETE`).
- Распространение по слоям: материализованные представления отражают удаления после обновления; streaming tables требуют `skipChangeCommits`; затем VACUUM.
- Predictive optimization: `ALTER SCHEMA ... ENABLE PREDICTIVE OPTIMIZATION` выполняет VACUUM, OPTIMIZE и ANALYZE; мониторинг через `system.storage.predictive_optimization_operations_history`. По умолчанию включено для аккаунтов, созданных после 11 ноября 2024; требуется план Premium; только для управляемых таблиц Unity Catalog.
- Интеграция с lifecycle policies Azure Storage: перенос в cool или archive; осторожно с архивными файлами (запросы к Archive падают без восстановления), свойство `delta.timeUntilArchived` (Public Preview, Runtime 13.3 LTS и новее, только Azure Archive; политика не должна архивировать `_delta_log`), представления, отсекающие архив, и предикаты в OPTIMIZE/VACUUM.

Примеры:

```
ALTER TABLE sales.customers.transactions
SET TBLPROPERTIES (
    'delta.logRetentionDuration' = 'interval 30 days',
    'delta.deletedFileRetentionDuration' = 'interval 30 days'
);

VACUUM sales.customers.transactions RETAIN 168 HOURS;

ALTER SCHEMA sales.customers ENABLE PREDICTIVE OPTIMIZATION;
```

### 5. Настройка и управление lineage
Источник: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/5-manage-data-lineage-tracking

- Lineage собирается автоматически для запросов из DataFrame и Databricks SQL на compute с доступом к Unity Catalog (standard или dedicated access mode, serverless, SQL warehouse с Unity Catalog, задания на таком compute). Column-level lineage - только когда источник и приёмник указаны по имени, а не по пути; используйте `catalog.schema.table`.
- Lineage общий для всех рабочих областей, подключённых к metastore.
- Хранение: Catalog Explorer и API - без ограничения срока для событий после 1 сентября 2024; системные таблицы `system.access.table_lineage` и `system.access.column_lineage` - скользящее окно один год.
- Просмотр: Catalog > таблица > Lineage > See Lineage Graph; кнопка + раскрывает связи; панель Lineage details; колонки в графе; Jobs и Dashboards во вкладке Lineage.
- Владелец объекта может меняться: Owner > edit, сохранить. Смена владельца - владелец, MANAGE, владелец родительского контейнера или metastore admin. Просмотр lineage требует BROWSE на родительском каталоге; недоступные узлы маскируются.
- История Delta: вкладка History или `DESCRIBE HISTORY`.
- Программно: `system.access.table_lineage` (подсчёт обращений за 7 дней).
- Genie Code: `/getTableLineages`, `/getTableInsights`.
- Ограничения: lineage не сохраняется при переименовании; колонки по пути не отслеживаются; global temporary views и `system.information_schema` не отслеживаются; некоторые UDF скрывают сопоставление колонок.

Пример:

```
SELECT
  source_table_full_name,
  COUNT(DISTINCT event_id) AS query_count
FROM system.access.table_lineage
WHERE event_date > CURRENT_DATE() - INTERVAL 7 DAYS
  AND source_table_full_name IS NOT NULL
GROUP BY source_table_full_name
ORDER BY query_count DESC
LIMIT 10;
```

### 6. Настройка аудита
Источник: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/6-configure-audit-logging

- Таблица `system.access.audit` (Public Preview) фиксирует события Unity Catalog на уровне аккаунта по всем рабочим областям. Включение системных таблиц - администратор аккаунта.
- Основные колонки: event_time, event_date, user_identity, workspace_id (0 для событий аккаунта), service_name (например, unityCatalog, notebook, clusters), action_name (например, getTable, createTable), request_params, response, source_ip_address.
- Хранение аудита - до одного года.
- Сервисы рабочей области: notebooks, clusters, jobs, databricksql, accounts. Сервисы аккаунта: Unity Catalog, управление аккаунтом, billable usage; OpenSharing логируется под unityCatalog.
- Примеры запросов: кто обращался к таблице за 7 дней (`request_params.full_name_arg`, `action_name IN ('getTable', 'createTable', 'deleteTable')`); изменения прав (`updatePermissions`); неуспешные обращения (`response.status_code != 200`).
- Verbose audit logs: Admin Settings > Advanced > Verbose Audit Logs; логируют текст команд (runCommand в notebook и jobs, commandSubmit в databrickssql). Осторожно: текст может содержать чувствительные данные.
- Доставка во внешние системы через diagnostic settings: Log Analytics (KQL), Storage Account (архив), Event Hubs (потоковая передача); требуется план Premium. Но diagnostic settings не включают события аккаунта и Unity Catalog/OpenSharing - для них используйте системную таблицу.

Пример:

```
SELECT
  event_time,
  user_identity.email AS changed_by,
  request_params.securable_type,
  request_params.securable_full_name,
  request_params.changes
FROM system.access.audit
WHERE
  service_name = 'unityCatalog'
  AND action_name = 'updatePermissions'
ORDER BY event_time DESC;
```

### 7. Проектирование безопасной стратегии OpenSharing
Источник: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/7-secure-open-sharing-strategy

- **Databricks-to-Databricks**: предпочтительный вариант для получателей с Unity Catalog; аутентификация платформой; идентификатор получателя (облако, регион, UUID metastore); поддерживаются таблицы, представления, тома, файлы notebook и модели ИИ; есть общий доступ к истории.
- **Open sharing (Databricks-to-Open)**: для других платформ; bearer-токены или OIDC-федерация; только табличные данные; нужно управлять токенами.
- Ограничения: срок токена задаётся на уровне metastore (Allow OpenSharing with parties outside your organization); токен живёт не более одного года; OIDC выдаёт короткоживущие токены Databricks OAuth в обмен на JWT провайдера.
- IP access list: до 100 IP или CIDR на получателя; запросы с других адресов отклоняются и логируются; `DESCRIBE RECIPIENT`.
- Привилегии: CREATE SHARE, CREATE RECIPIENT, USE SHARE, USE RECIPIENT, SET SHARE PERMISSION - назначайте группам, а не отдельным людям.
- Создание: `CREATE SHARE`; `ALTER SHARE ... ADD TABLE` (с алиасом `AS`, с историей `WITH HISTORY`), `ADD SCHEMA` (включает будущие таблицы), `ADD VOLUME`, `ADD VIEW`; получатель Databricks - `CREATE RECIPIENT ... USING ID '...'`; открытый получатель - `CREATE RECIPIENT`, затем `DESCRIBE RECIPIENT` для ссылки активации (отдаётся один раз).
- Выдача доступа: `GRANT SELECT ON SHARE ... TO RECIPIENT ...`; просмотр `SHOW GRANT ON SHARE`, `SHOW GRANTS TO RECIPIENT`; отзыв `REVOKE`, удаление `DROP RECIPIENT`.
- Тонкий контроль: свойства получателя (`ALTER RECIPIENT ... SET PROPERTIES`), функция `CURRENT_RECIPIENT('country_region')` в динамических представлениях, фильтрация партиций `PARTITION (region = CURRENT_RECIPIENT().region)`.
- Аудит: события `createShare`, `createRecipient`, `updateShare`, `updateSharePermissions`, а также `deltaSharingQueriedTable` и `generateTemporaryTableCredential` (доступ получателей). OpenSharing-события не поступают через diagnostic settings.
- Ротация токенов: при ротации выбирается срок действия старого токена (0 - немедленно); у получателя не более двух токенов.
- Регулярные проверки: ежемесячный аудит получателей, содержимого шар, сроков токенов и неуспешных попыток доступа.

Примеры:

```
CREATE SHARE IF NOT EXISTS partner_analytics
COMMENT 'Sales analytics data for partner integration';

ALTER SHARE partner_analytics ADD TABLE catalog.schema.transactions
WITH HISTORY;

GRANT SELECT ON SHARE partner_analytics TO RECIPIENT contoso_analytics;
```

```
CREATE VIEW catalog.schema.regional_sales AS
SELECT * FROM catalog.schema.all_sales
WHERE region = CURRENT_RECIPIENT('country_region');
```

### 8. Упражнение: управление объектами Unity Catalog
Источник: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/8-exercise-govern-unity-catalog-objects

Упражнение (около 45 минут): платформа данных подключённых автомобилей на Azure Databricks. Нужно пометить таблицы и столбцы для классификации PII, настроить retention и выполнить VACUUM, включить predictive optimization, а затем с помощью системных таблиц проследить lineage и проанализировать аудит. Требуется подписка Azure с правами администратора.

### 9. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/9-knowledge-check

В исходных материалах вопросы не приведены.

### 10. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/10-summary

Governance строится на комментариях и тегах, ABAC-политиках на основе governed tags, управлении хранением (retention, VACUUM, predictive optimization), lineage, аудите (`system.access.audit`) и безопасном OpenSharing.

## Важные команды / код / настройки

Комментарии и теги:

```
COMMENT ON TABLE sales.customers.profiles
IS 'Contains customer profile information including contact details and preferences';

ALTER TABLE sales.customers.profiles
SET TAGS ('domain' = 'sales', 'data_classification' = 'internal');
```

ABAC: политика-фильтр строк:

```
CREATE POLICY hide_eu_customers
ON CATALOG sales
ROW FILTER sales.governance.filter_non_eu
TO `analysts`
FOR TABLES
MATCH COLUMNS
    has_tag_value('pii', 'address') AS addr
USING COLUMNS (addr);
```

Политика маскирования столбца:

```
CREATE POLICY mask_sensitive_ssn
ON SCHEMA sales.customers
COLUMN MASK sales.governance.mask_ssn
TO `account users`
EXCEPT `compliance_team`
FOR TABLES
MATCH COLUMNS
    has_tag_value('pii', 'ssn') AS ssn_col
ON COLUMN ssn_col;
```

Retention и VACUUM:

```
ALTER TABLE sales.customers.transactions
SET TBLPROPERTIES (
    'delta.logRetentionDuration' = 'interval 30 days',
    'delta.deletedFileRetentionDuration' = 'interval 30 days'
);

VACUUM sales.customers.transactions RETAIN 168 HOURS;
```

Удаление по запросу (MERGE с контрольной таблицей):

```
MERGE INTO bronze.users AS target
USING (
    SELECT user_id
    FROM compliance.deletion_requests
    WHERE status = 'pending'
) AS source
ON target.user_id = source.user_id
WHEN MATCHED THEN DELETE;
```

Streaming-таблица с пропуском изменений удаления:

```
spark.readStream.option('skipChangeCommits', 'true').table("bronze.users")
```

Аудит и OpenSharing:

```
SELECT
  event_time,
  user_identity.email AS performed_by,
  action_name,
  request_params
FROM system.access.audit
WHERE service_name = 'unityCatalog'
  AND action_name IN ('createShare', 'createRecipient', 'updateShare', 'updateSharePermissions')
ORDER BY event_time DESC;
```

Настройки и лимиты: по умолчанию `delta.logRetentionDuration` 30 дней, `delta.deletedFileRetentionDuration` 7 дней; квоты ABAC - 100 политик на каталог и схему, 50 на таблицу, 10 000 на metastore, 20 принципалов на политику; Runtime 16.4+ для ABAC; до 50 тегов на объект; до 100 IP на получателя OpenSharing; срок токена до одного года; хранение аудита до одного года; системные таблицы lineage - скользящий год.

## Что запомнить

- Комментарии и теги - основа находимости; governed tags дают контролируемые значения и лежат в основе ABAC.
- ABAC-политики применяются по тегам и масштабируются автоматически для новых таблиц; одна row filter и одна маска на объект.
- VACUUM необратимо удаляет старые версии; для удаления по запросу сочетайте DELETE или MERGE с VACUUM и помните о слоях bronze, silver и gold.
- Lineage собирается автоматически на compute с Unity Catalog; column-level lineage работает только при ссылке по имени.
- Для OpenSharing предпочитайте Databricks-to-Databricks, ограничивайте IP и срок токенов, а аудит читайте через `system.access.audit`.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/
- Enable system tables (упомянуто в уроке 6); Diagnostic log reference (упомянуто в уроке 6)
