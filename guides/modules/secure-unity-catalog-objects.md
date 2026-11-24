# Безопасность объектов Unity Catalog в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/

## Цель модуля

Спроектировать и реализовать безопасность в Azure Databricks с помощью Unity Catalog: понять жизненный цикл запроса, выдавать привилегии, ограничивать строки и маскировать столбцы, получать секреты из Azure Key Vault и аутентифицировать доступ к данным через service principal и managed identity.

## Ключевые понятия

- **Unity Catalog** - централизованное управление данными, вычислительными ресурсами и доступом; control plane для безопасности и аудита.
- **Metastore** - верхний контейнер объектов Unity Catalog; привязан к региону Azure и к одному рабочему пространству одновременно.
- **Привилегии (privileges)** - права на объекты, например SELECT, MODIFY, USE CATALOG, USE SCHEMA, CREATE TABLE, MANAGE, ALL PRIVILEGES; наследуются от каталога и схемы, если разрешено.
- **Principal (принципал)** - пользователь, группа или service principal, которому выдаются привилегии. Рекомендуются группы аккаунта, синхронизированные из Microsoft Entra ID.
- **Row filter и column mask** - функции SQL, которые фильтруют строки и маскируют значения столбцов в зависимости от группы пользователя.
- **Dynamic view (динамическое представление)** - представление с CASE и WHERE, которое применяет те же правила без изменения исходной таблицы.
- **ABAC (Attribute-Based Access Control)** - политики на основе тегов, применяемые автоматически ко всем подходящим таблицам.
- **Azure Key Vault-backed secret scope** - область секретов Databricks, доступная только для чтения и ссылающаяся на Azure Key Vault.
- **Storage credential и external location** - учетные данные хранилища (service principal или managed identity через access connector) и путь во внешнем хранилище, которому выдаются права.
- **Managed identity и access connector** - удостоверение Azure без управления секретами; позволяет работать с хранилищами за сетевыми ограничениями.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/1-introduction

Unity Catalog дает централизованное управление безопасностью: права на каталоги, схемы и таблицы; ограничение строк и столбцов; аутентификация через service principal или managed identity; секреты из Azure Key Vault без их раскрытия в ноутбуках и заданиях.

### 2. Жизненный цикл запроса
URL: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/2-understand-query-lifecycle

Шаги запроса к таблице Unity Catalog: 1) принципал отправляет запрос в кластер или SQL warehouse; 2) вычислительный ресурс передает запрос в Unity Catalog, который проверяет права и пишет запрос в журнал аудита (при отказе запрос блокируется); 3) для каждого объекта Unity Catalog использует облачные учетные данные, настроенные администратором (для управляемых таблиц - хранилище metastore, для внешних - внешняя локация); 4) выдается временный токен с ограниченной областью и защищенный URL; 5) вычислительный ресурс читает данные из ADLS Gen2 напрямую; 6) хранилище возвращает данные; 7) на вычислительном ресурсе применяются фильтры строк и столбцов; 8) результат возвращается пользователю. В Azure для доступа к ADLS рекомендуется managed identity с access connector: service principal не работает с хранилищем за сетевыми правилами. При ограничениях файрвола нужно разрешить доступ, иначе запрос будет отклонен даже с действительным токеном. Для Hive metastore (`hive_metastore`) модель устаревшая: проверка через ACL таблиц, доступ через сервисные аккаунты, точки монтирования и политики хранения, аудит менее интегрирован.

### 3. Стратегии управления доступом
URL: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/3-implement-access-control-strategies

Четыре механизма: привилегии и владение (каталоги, схемы, таблицы), ABAC (по тегам), фильтры строк и столбцов на таблице, привязки рабочих пространств (workspace bindings). Для чтения таблицы нужны USE CATALOG, USE SCHEMA и SELECT (явный подход). При наследовании от схемы SELECT на схему дает доступ ко всем текущим и будущим таблицам схемы. При наследовании от каталога нужны USE CATALOG, USE SCHEMA и SELECT; SELECT сам по себе не дает USE SCHEMA. Для создания таблицы нужны USE CATALOG, USE SCHEMA и CREATE TABLE. Metastore привязан к региону, рабочее пространство - к одному metastore. Выдача прав: SQL (GRANT/REVOKE) или Catalog Explorer (вкладка Permissions). Проверка: SHOW GRANTS. Владельцы объектов имеют все привилегии неявно. ALL PRIVILEGES не включает MANAGE, READ METADATA, EXTERNAL USE SCHEMA и EXTERNAL USE LOCATION. Принципалы: пользователи, service principal (в обратных кавычках), группы; `account users` - встроенная группа всех пользователей и service principal аккаунта; рабочие локальные группы не могут получать доступ к Unity Catalog.

### 4. Тонкое управление доступом
URL: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/4-understand-fine-grained-access-control

Два способа: Row and Column Security (маски столбцов и фильтры строк на таблице) и Dynamic Views. Для одной таблицы рекомендуется Row and Column Security: меньше объектов, централизованная логика, гибкие комбинации. Dynamic views нужны, когда таблицы должны быть закрыты интерфейсом, когда данные собираются из нескольких таблиц или при миграции с существующих представлений. ABAC применяет политики по тегам ко многим таблицам без настройки каждой. Частые ошибки: дублирование таблиц для каждой аудитории, множество похожих представлений, сложная бизнес-логика внутри маскирующих функций, чрезмерное маскирование; функции безопасности тоже надо защищать от изменения.

### 5. Фильтрация строк и маскирование столбцов
URL: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/5-implement-row-filtering-column-masking

Функция маски и фильтра использует `is_account_group_member()`. Маска применяется через `ALTER TABLE ... ALTER COLUMN ... SET MASK`; фильтр строк - через `ALTER TABLE ... SET ROW FILTER ... ON (...)`. Пример: маска телефона, видимого только группе `metastore_admins`; фильтр по `c_nationkey = 21` для всех, кроме группы `admin`. Динамическое представление использует CASE в SELECT и WHERE; права выдаются на представление через GRANT SELECT ON VIEW. Row and Column Security встроена в таблицу и действует везде, где используется таблица; динамические представления дают гибкость, но сохраняют базовую таблицу открытой.

### 6. Доступ к секретам Azure Key Vault
URL: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/6-access-azure-key-vault

Секрет-область (secret scope) может быть Databricks-backed (зашифрованная база Databricks, управление через CLI или API) или Azure Key Vault-backed (только чтение, секреты в Key Vault). Для Key Vault-backed области нужна модель доступа Vault access policy, а не Azure RBAC; в источнике указано, что версии API Key Vault 2026-02-01 и новее по умолчанию создают хранилища с RBAC, и тогда создание области завершится ошибкой. Область создается по адресу `https://<databricks-instance>#secrets/createScope` (S в createScope заглавная). Нужны DNS Name и Resource ID хранилища. Databricks выдает службе Get и List на Key Vault; у учетной записи должна быть роль Key Vault Contributor, Contributor или Owner. Разрешения на область распространяются на все секреты Key Vault; для разграничения создавайте отдельные хранилища. Получение секрета: `dbutils.secrets.get(scope=..., key=...)` (значения маскируются в выводе как [REDACTED]), `dbutils.secrets.list(...)`, SQL-функции `secret()` и `try_secret()`. Секреты в конфигурации Spark (`{{secrets/scope/key}}`, публичный превью) и переменные окружения доступны всем, кто может подключаться к кластеру или запускать ноутбук. После обновления секрета в Key Vault нужно перезапустить кластер. Права: READ, WRITE (только для Databricks-backed), MANAGE; управление через `databricks secrets put-acl`, `list-acls`, `get-acl`, `delete-acl`. Ограничить MANAGE только создателем может план Premium.

### 7. Аутентификация доступа к данным через service principal
URL: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/7-authenticate-data-access-service-principals

Service principal - удостоверение приложения с Application (client) ID, Directory (tenant) ID и client secret. Учетные данные хранятся в storage credential Unity Catalog; инженер данных обычно работает с уже созданными credential через external locations. При необходимости в ноутбуке настраиваются параметры Spark для OAuth (ClientCredsTokenProvider), с секретом из `dbutils.secrets.get`. Чтение через `abfss://` URL. Рекомендации: не хранить секреты в коде, учитывать срок действия и ротацию секретов, соблюдать принцип наименьших привилегий. Managed identity предпочтительнее для storage credential: не нужна ротация секретов и поддерживается доступ к хранилищам с сетевыми правилами.

### 8. Аутентификация доступа к ресурсам через managed identity
URL: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/8-authenticate-resource-access-managed-identities

Access connector для Azure Databricks - ресурс Azure, связывающий managed identity (системную или пользовательскую) с аккаунтом Databricks. Системная identity удаляется вместе с access connector; пользовательская сохраняется независимо. Использование: managed storage metastore и внешние хранилища. Создание: access connector в том же регионе, что и хранилище; роль Storage Blob Data Contributor на аккаунт хранения (или Storage Blob Delegator на аккаунт и Storage Blob Data Contributor на контейнер для ограниченного доступа). Для файловых событий - Storage Queue Data Contributor, а для автоматической настройки - Storage Account Contributor и EventGrid EventSubscription Contributor. Storage credential создается в Catalog Explorer (Create a credential, тип Azure Managed Identity, ID access connector). Для создания нужна привилегия CREATE STORAGE CREDENTIAL (по умолчанию у account admins и metastore admins). External location сочетает storage credential с путем `abfss://`; можно пометить credential как только для чтения и привязать к рабочим пространствам (workspace binding). Для сетевых ограничений нужна сетевая связность (private endpoint или service endpoint).

### 9. Упражнение: защита объектов Unity Catalog
URL: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/9-exercise-secure-unity-catalog-objects

Лабораторная работа: выдать права группе Databricks, применить фильтр строк по региону, замаскировать email (PII) функцией маски, создать секрет-область на базе Azure Key Vault и получать секреты в ноутбуке. Нужна подписка Azure с правами администратора.

### 10. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/10-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 11. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/11-summary

Безопасность Unity Catalog работает на нескольких уровнях: проверка прав и выдача временных токенов, наследуемые и явные привилегии, фильтры строк и маски столбцов. Azure Key Vault дает секреты без раскрытия в коде; service principal и managed identity - способы аутентификации к хранилищу, причем managed identity не требует управления секретами. Тонкое управление доступом: Row and Column Security для централизованного контроля, Dynamic Views для гибкости.

## Важные команды / код / настройки

Выдача и отзыв привилегий (SQL):

```sql
GRANT SELECT ON TABLE sales TO `analysts`;
GRANT USE SCHEMA ON SCHEMA finance TO `analysts`;
GRANT USE CATALOG ON CATALOG corpdata TO `analysts`;
GRANT CREATE TABLE ON SCHEMA finance TO `analysts`;
REVOKE SELECT ON TABLE sales FROM `analysts`;
```

Проверка прав:

```sql
SHOW GRANTS ON TABLE sales.reporting.monthly_revenue;
SHOW GRANTS `finance-team` ON TABLE sales.reporting.monthly_revenue;
```

Маска столбца:

```sql
CREATE OR REPLACE FUNCTION phone_mask(c_phone STRING)
  RETURN CASE WHEN is_account_group_member('metastore_admins')
    THEN c_phone
    ELSE 'REDACTED PHONE NUMBER'
  END;

ALTER TABLE customers
  ALTER COLUMN c_phone
  SET MASK phone_mask;
```

Фильтр строк:

```sql
CREATE OR REPLACE FUNCTION nation_filter(c_nationkey INT)
  RETURN IF(is_account_group_member('admin'), true, c_nationkey = 21);

ALTER TABLE customers
SET ROW FILTER nation_filter ON (c_nationkey);
```

Динамическое представление:

```sql
CREATE OR REPLACE VIEW vw_customers AS
SELECT
  c_custkey,
  c_name,
  c_address,
  c_nationkey,
  CASE
    WHEN is_account_group_member('admins') THEN c_phone
    ELSE 'REDACTED PHONE NUMBER'
  END as c_phone,
  c_acctbal,
  c_mktsegment,
  c_comment
FROM customers_new
WHERE
  CASE WHEN
    is_account_group_member('admins') THEN TRUE
    ELSE c_nationkey = 21
  END;

GRANT SELECT ON VIEW vw_customers TO `account users`;
```

Получение секретов:

```python
username = dbutils.secrets.get(scope="jdbc", key="username")
password = dbutils.secrets.get(scope="jdbc", key="password")
dbutils.secrets.list("jdbc")
```

```sql
SELECT secret('jdbc', 'username') AS db_username;
```

Ссылка на секрет в конфигурации Spark и переменной окружения:

```
spark.storage.key {{secrets/storage/account-key}}
STORAGE_KEY={{secrets/storage/account-key}}
```

Права на область секретов (Databricks CLI):

```bash
databricks secrets put-acl jdbc data-engineers READ
databricks secrets list-acls jdbc
databricks secrets get-acl jdbc data-engineers
databricks secrets delete-acl jdbc data-engineers
```

Аутентификация Spark через service principal (фрагмент из источника):

```python
service_credential = dbutils.secrets.get(scope="storage-secrets", key="sp-client-secret")
spark.conf.set("fs.azure.account.auth.type.<storage-account>.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.<storage-account>.dfs.core.windows.net",
               "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
```

Внешняя таблица в external location:

```sql
CREATE EXTERNAL TABLE sales_data
USING DELTA
LOCATION 'abfss://data@mystorageaccount.dfs.core.windows.net/sales/';
```

Адрес создания секрет-области: `https://<databricks-instance>#secrets/createScope`.

Роли для managed identity (из источника): Storage Blob Data Contributor; для ограниченного доступа - Storage Blob Delegator на аккаунт и Storage Blob Data Contributor на контейнер; для файловых событий - Storage Queue Data Contributor, а также Storage Account Contributor и EventGrid EventSubscription Contributor.

## Что запомнить

- Для доступа к таблице нужны права на каталог, схему и таблицу (явная модель) или наследование от схемы или каталога.
- Unity Catalog проверяет права, пишет аудит и выдает временный токен; для хранилищ за сетевыми правилами используйте managed identity.
- Секреты из Azure Key Vault читаются через `dbutils.secrets.get`; значения маскируются в выводе, но доступны всем, кто может запускать код.
- Key Vault-backed область требует модель доступа Vault access policy; после смены секрета перезапустите кластер.
- Managed identity предпочтительнее service principal для storage credential: нет ротации секретов и поддерживаются защищенные сетевые хранилища.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/
- Модуль "Govern Unity Catalog objects" (упомянут в источнике, URL не приведен); Connect to an Azure Data Lake Storage Gen2 (ADLS Gen2) external location (упомянута в источнике, URL не приведен)
