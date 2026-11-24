# Безопасность Azure SQL Database и Azure SQL Managed Instance

**Источник:** https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/

## Цель модуля

Спланировать и внедрить меры безопасности для Azure SQL Database и Azure SQL Managed Instance: сетевой доступ (firewall), аутентификация через Microsoft Entra ID, аудит, классификация данных в Microsoft Purview, динамическое маскирование, шифрование at rest (TDE) и критерии выбора Always Encrypted.

## Ключевые понятия

- **Server-level IP firewall rule (правило брандмауэра уровня сервера)** - разрешает доступ ко всем базам сервера; хранится в master; до 256 правил.
- **Database-level IP firewall rule (правило уровня базы)** - разрешает доступ к одной базе; создаётся только T-SQL; переносится вместе с базой.
- **Virtual network rule (правило виртуальной сети)** - разрешает трафик из выбранных подсетей через service endpoints.
- **Microsoft Entra authentication** - вход по identity Entra; централизованное управление пользователями и политиками.
- **Contained database user (автономный пользователь)** - пользователь, созданный в базе `FROM EXTERNAL PROVIDER`, без логина в master.
- **Database auditing (аудит баз данных)** - журнал событий в хранилище, Log Analytics или Event Hubs.
- **Microsoft Purview** - сервис управления данными: Data Map, Data Catalog, Data Estate Insights, Data Sharing, Data Policy.
- **Классификация (classification) и метки чувствительности (sensitivity labels)** - классы данных (более 200 системных) и метки безопасности; это разные понятия.
- **Dynamic Data Masking (DDM)** - маскирование результата запроса без изменения данных; пользователи с правом UNMASK видят исходные значения.
- **TDE (Transparent Data Encryption)** - шифрование файлов, резервных копий и журнала на уровне страниц (AES 256); DEK защищается TDE protector.
- **Always Encrypted** - клиентское шифрование столбцов; ключи не раскрываются движку БД; поддерживает детерминированное и рандомизированное шифрование.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/1-introduction

Администратор БД защищает конфиденциальные данные от несанкционированного доступа, утечек и несоответствия требованиям. Цели модуля: внедрить меры защиты, включить аутентификацию Entra, аудит, классификацию через Purview, DDM, TDE и выбрать случаи для Always Encrypted.

### 2. Безопасность Azure SQL Database и SQL Managed Instance
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/2-azure-sql-database

Стратегия многоуровневой защиты (defense in depth), от периметра к данным:
- **Сеть**: IP firewall rules и virtual network rules (service endpoints; для NSG используйте SQL service tags).
- **Доступ**: SQL-аутентификация (серверный администратор с логином и паролем) и Microsoft Entra-аутентификация (MFA, Conditional Access). Managed Instance дополнительно поддерживает Windows-аутентификацию для принципалов Entra через Kerberos. Авторизация - через роли БД; рекомендуется создавать пользовательские роли с минимальными правами, не назначать права напрямую пользователям, ограничивать `db_owner`; для контекста выполнения - `EXECUTE AS`. Row-Level Security - доступ к строкам по признакам пользователя.
- **Угрозы**: аудит (в Azure Monitor logs, Event Hubs, хранилище клиента) и Advanced Threat Protection (через Microsoft Defender for Cloud, платно на сервер): SQL-инъекции, брутфорс, аномалии доступа.
- **Шифрование**: TLS для данных в движении (сервер всегда требует шифрования; в строке подключения рекомендуются `Encrypt=True` и `TrustServerCertificate=False`); TDE для данных at rest (BYOK через Azure Key Vault); Always Encrypted для данных in use; Dynamic data masking для результатов запросов.
- **Управление безопасностью**: vulnerability assessment (часть Microsoft Defender for SQL); data discovery and classification (в превью).

### 3. Включение аутентификации Microsoft Entra для базы данных
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/3-authorize-database-access

- Требования: клиент Microsoft Entra с пользователями и группами; существующий ресурс Azure SQL.
- Администратор Entra задаётся для логического сервера (portal: SQL server > Microsoft Entra ID > Set admin > Save; для Managed Instance аналогично, но выбирать можно только поддерживаемые идентичности). Удаление администратора отключает Entra-аутентификацию на сервере. Имя администратора не должно совпадать с существующим пользователем master.
- Managed Instance: назначить managed identity роль **Directory Readers** (может сделать Privileged Role Administrator или выше).
- Создание принципалов: `CREATE USER [имя] FROM EXTERNAL PROVIDER` (contained user) или `CREATE USER [имя] FROM LOGIN [имя]` (на основе логина, для Entra-логинов - публичный превью в Azure SQL Database).
- Внешние пользователи из другого тенанта импортируются в тенант подписки и затем используются как contained users.
- Рекомендуется выдавать права ролям, а не пользователям; наследуются права группы Entra и логина.
- Ошибка 33134 чаще всего связана с Conditional Access; разрешите приложение Microsoft Graph (`00000003-0000-0000-c000-000000000000`). Если вход выполнен как service principal - команда должна выполняться от пользователя.
- Для MFA: включить MFA и применить Conditional Access.

Пример:

```
CREATE USER [alice@fabrikam.com] FROM EXTERNAL PROVIDER;
```

### 4. Включение и мониторинг аудита базы данных
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/4-database-audit

- Аудит записывает события в журнал: хранилище Azure (append blobs, формат .xel, открывается в SSMS), Log Analytics или Event Hubs.
- Возможности: сохранение следа по выбранным категориям, готовые отчёты и дашборд, анализ подозрительной активности.
- При высокой нагрузке аудит может пропускать некоторые события ради производительности.
- Ограничения: аудит на приостановленном Synapse SQL pool не поддерживается; UAMI не поддерживается для Synapse; для Synapse - только группы действий по умолчанию.
- Для хранилища за VNet или firewall нужен general-purpose v2; при аутентификации через ключи хранилища ключи должны быть доступны; при Entra-only - управляемые идентичности.
- Неуспешные входы через Microsoft Entra не попадают в журнал SQL - их смотрят в центре администрирования Entra.
- Immutable storage для журнала настраивается в Azure Storage (включите Allow additional appends).
- Аудит на read-only replicas включается автоматически.
- Пороговые alerts threat detection настраиваются после аудита.

### 5. Сценарии использования портала управления данными Microsoft Purview
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/5-microsoft-purview-governance-portal-use-cases

- Purview - унифицированный сервис управления данными (on-premises, мультиоблако, SaaS). Требуется учётная запись Purview в портале Azure.
- **Data Map** - автоматическое обнаружение, сканирование и классификация; основа для каталога; API совместим с Apache Atlas 2.2.
- **Data Catalog** - поиск по фильтрам (глоссарий, классификации, метки), управление глоссарием, визуализация lineage.
- **Data Estate Insights** - обзор пробелов в управлении для руководителей данных.
- **Data Sharing** - безопасный обмен данными внутри организации и с партнёрами; отзыв доступа.
- **Data Policy** - централизованное управление доступом на основе ролей (например, Read, Modify), в том числе с плоскостью данных вне источника.

### 6. Классификация чувствительных данных в Microsoft Purview
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/6-implement-data-classification-sensitive-information

- Этапы: регистрация источника (Register), сканирование и загрузка (Scan and Ingest), классификация (Classify).
- Роли: Data Source Admin плюс одна из ролей Purview (например, Data Reader или Data Share Contributor).
- Регистрация сопоставляет источник с коллекцией в Data Map; выберите integration runtime и учётные данные.
- Сканирование может запускаться сразу или по расписанию; можно задать scan rule set (системные наборы правил назначаются каждому типу источника автоматически).
- Классификации: более 200 системных (например, Person's Name, Credit Card Number) и пользовательские (по регулярному выражению или словарю).
- Метки чувствительности (sensitivity labels) - это не классификации: они относятся к безопасности и конфиденциальности (например, Highly Confidential, Public) и требуют лицензии Microsoft 365 в том же тенанте. Labeling в Data Map - в превью.
- Автометки: правила, которые присваивают метку на основе классификаций при сканировании. Метки в SSMS (локальные) не отображаются в Purview и наоборот; для БД рекомендуется Purview.

### 7. Планирование и внедрение динамического маскирования
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/7-dynamic-data-mask

- DDM скрывает данные в результатах запроса, не меняя их в базе; пример: сотрудник колл-центра видит часть e-mail клиента.
- Политика задаётся в портале (SQL Database > Security > Dynamic Data Masking); исключения (SQL users excluded from masking); администраторы всегда видят исходные данные.
- Функции маскирования: default (полная маска по типу данных), email (`aXXX@XXXX.com`), random (случайное число в диапазоне), custom string (`partial(prefix,[padding],suffix)`), datetime (маскирование года, месяца, дня и т.д. - для SQL Server 2022).
- Для Azure SQL Database в списке функций также: credit card (XXXX-XXXX-XXXX-1234), random number, custom text.
- Рекомендательный движок DDM отмечает потенциально чувствительные поля, которые можно замаскировать в портале (Add Mask).
- Права: встроенные роли SQL Security Manager, SQL DB Contributor, SQL Server Contributor; действия `Microsoft.Sql/servers/databases/dataMaskingPolicies/*`.
- Права UNMASK выдаются на уровне базы, схемы, таблицы или столбца (`GRANT UNMASK`), отзываются через `REVOKE UNMASK`.

Пример определения маскированной таблицы:

```
CREATE TABLE Data.Membership (
    MemberID INT IDENTITY(1, 1) NOT NULL PRIMARY KEY CLUSTERED,
    FirstName VARCHAR(100) MASKED WITH (FUNCTION = 'partial(1, "xxxxx", 1)') NULL,
    LastName VARCHAR(100) NOT NULL,
    Phone VARCHAR(12) MASKED WITH (FUNCTION = 'default()') NULL,
    Email VARCHAR(100) MASKED WITH (FUNCTION = 'email()') NOT NULL,
    DiscountCode SMALLINT MASKED WITH (FUNCTION = 'random(1, 100)') NULL,
    BirthDay DATETIME MASKED WITH (FUNCTION = 'default()') NULL
);
```

Примеры выдачи UNMASK:

```
GRANT UNMASK ON Data.Membership(FirstName) TO ServiceAttendant;
GRANT UNMASK ON Data.Membership TO ServiceLead;
GRANT UNMASK ON SCHEMA::Data TO ServiceManager;
GRANT UNMASK TO ServiceHead;
```

### 8. Реализация Transparent Data Encryption
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/8-transparent-data-encryption

- TDE шифрует базу, резервные копии и журнал транзакций в реальном времени (страница за страницей), без изменений приложения; алгоритм AES 256.
- DEK (Database Encryption Key) защищается TDE protector: service-managed certificate (по умолчанию) либо асимметричный ключ в Azure Key Vault (customer-managed, BYOK).
- Для Azure SQL Database и Synapse протектор задаётся на уровне логического сервера и наследуется базами; для Managed Instance - на уровне инстанса (BYOK в превью).
- Новые базы шифруются по умолчанию; старые (до мая 2017 для SQL Database, до февраля 2019 для MI) - нет, их надо включить вручную. Статус: `sys.dm_database_encryption_keys`, столбец `encryption_state_desc`.
- Системные базы (master и др.) TDE не шифрует; tempdb шифруется всегда.
- Если доступ сервера к Key Vault отозван, база становится недоступной.
- Перенос: TDE наследуется при geo-restore, point-in-time restore, восстановлении удалённой базы, active geo-replication, копировании базы.
- Экспорт в BACPAC не шифруется; после импорта включите TDE.
- В Managed Instance ручной COPY-ONLY бэкап базы под service-managed TDE не поддерживается.
- Управление: портал (роли Azure Owner, Contributor или SQL Security Manager); для MI - T-SQL.

### 9. Рекомендации по использованию Always Encrypted
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/9-always-encrypted

- Always Encrypted шифрует столбцы (например, номера карт, идентификаторы) на клиенте; ключи не раскрываются движку БД - защита от администраторов и облачных операторов.
- Два типа ключей: column master key (хранится в Azure Key Vault, Windows certificate store или HSM) и column encryption key (зашифрован column master key).
- Детерминированное шифрование: одинаковое значение - одинаковый шифротекст; поддерживает точечный поиск, `IN`, `GROUP BY`, `DISTINCT`, equality joins; риск угадывания по шаблонам при малом наборе значений (например, True/False, регионы). Используйте для полей поиска, например, госидентификатора.
- Рандомизированное шифрование: надёжнее, но без поиска, группировки и индексирования; для данных вроде конфиденциальных комментариев.
- Выполнение: клиентский драйвер шифрует параметры и расшифровывает результаты; пользователю нужны доступ к ключу мастера в хранилище ключей и включённый Always Encrypted в строке подключения; без этого возвращается шифротекст.
- Ограничения: без вычислений над зашифрованными столбцами (кроме поддерживаемых сравнений); литералы и переменные T-SQL вместо параметров не поддерживаются; нельзя смешивать plaintext и encrypted в одной операции; не поддерживаются FOR XML и FOR JSON; ряд типов и свойств столбцов несовместим (IDENTITY, computed columns, маскированные через DDM столбцы, default constraints и др.).
- Secure enclaves расширяют возможности (поиск по шаблону, сравнения, сортировка) для рандомизированного шифрования.
- Права БД: ALTER ANY COLUMN MASTER KEY, ALTER ANY COLUMN ENCRYPTION KEY, VIEW ANY COLUMN MASTER KEY DEFINITION, VIEW ANY COLUMN ENCRYPTION KEY DEFINITION. В SQL Database последние два права не выдаются роли public по умолчанию - их нужно выдать явно.

### 10. Настройка брандмауэра Azure SQL Database
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/10-implement-an-azure-sql-database-firewall

- По умолчанию сервер блокирует публичный endpoint; брандмауэр не применяется к Azure SQL Managed Instance.
- **Server-level rules**: до 256 правил; хранятся в master; доступ ко всем базам. Создаются через портал, PowerShell, CLI, REST или T-SQL.
- **Database-level rules**: до 256 правил на базу; создаются и управляются только T-SQL (`sp_set_database_firewall_rule`); доступны только после первого server-level rule.
- Рекомендация: database-level там, где нужна изоляция и переносимость; server-level для администраторов и многих баз с одинаковыми требованиями.
- Порядок проверки для подключения из интернета: сначала database-level, затем server-level; если ни одно правило не совпало - отказ.
- Разрешение Azure-сервисов: правило 0.0.0.0-0.0.0.0 (AllowAllWindowsAzureIps); включает все подключения из Azure, в том числе чужих подписок - ограничивайте логины и права. Применимо только к Azure SQL Database.
- Права на управление server-level: SQL Server Contributor, SQL Security Manager или владелец ресурса; для database-level по T-SQL нужно минимум CONTROL DATABASE.
- Аудит изменений брандмауэра: через Database Auditing. Кэш server-level правил обновляется `DBCC FLUSHAUTHCACHE`.
- Диагностика: открыть порт 1433 локально; NAT может менять IP (смотрите Current Client IP Address в портале); изменения применяются с задержкой до пяти минут; брандмауэр только разрешает попытку - логин и пароль проверяются отдельно; для динамических IP - диапазон провайдера или статический адрес.

Примеры:

```
EXECUTE sp_set_firewall_rule @name = N'ContosoFirewallRule', @start_ip_address = '192.168.1.1', @end_ip_address = '192.168.1.10';

EXECUTE sp_delete_firewall_rule @name = N'ContosoFirewallRule';
```

```
az sql server firewall-rule create --resource-group myResourceGroup --server mysqldbserver -n ContosoIPRange --start-ip-address 192.168.1.0 --end-ip-address 192.168.1.255
```

### 11. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/11-knowledge-check

В исходных материалах вопросы не приведены.

### 12. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/12-summary

Модуль охватил аутентификацию Microsoft Entra, аудит, классификацию в Purview, динамическое маскирование, TDE и критерии выбора Always Encrypted.

## Важные команды / код / настройки

Правила брандмауэра (T-SQL, server-level):

```
SELECT * FROM sys.firewall_rules ORDER BY name;

EXECUTE sp_set_firewall_rule @name = N'ContosoFirewallRule', @start_ip_address = '192.168.1.1', @end_ip_address = '192.168.1.10';

EXECUTE sp_delete_firewall_rule @name = N'ContosoFirewallRule';
```

Правило брандмауэра (PowerShell, Az.Sql):

```
New-AzSqlServerFirewallRule -ResourceGroupName "myResourceGroup" `-ServerName $servername `-FirewallRuleName "ContosoIPRange" -StartIpAddress "192.168.1.0" -EndIpAddress "192.168.1.255"
```

Правило брандмауэра (Azure CLI):

```
az sql server firewall-rule create --resource-group myResourceGroup --server $servername -n ContosoIPRange --start-ip-address 192.168.1.0 --end-ip-address 192.168.1.255
```

Создание пользователя Entra:

```
CREATE USER [<Microsoft_Entra_principal_name>] FROM EXTERNAL PROVIDER;
CREATE USER [appName] FROM LOGIN [appName];
```

Маскирование и UNMASK:

```
ALTER COLUMN Gender ADD MASKED WITH (FUNCTION = 'default()');
ALTER COLUMN Email ADD MASKED WITH (FUNCTION = 'email()');
ALTER COLUMN [Phone Number] ADD MASKED WITH (FUNCTION = 'partial(1,"XXXXXXX",0)');
GRANT UNMASK ON SCHEMA::Data TO ServiceManager;
REVOKE UNMASK FROM ServiceHead;
```

Проверка шифрования TDE:

```
SELECT encryption_state_desc FROM sys.dm_database_encryption_keys;
```

Строка подключения (рекомендация из урока 2):

```
Encrypt=True;TrustServerCertificate=False
```

Настройки: до 256 server-level и до 256 database-level правил брандмауэра; Azure-правило `0.0.0.0-0.0.0.0`; задержка применения до пяти минут; параметры DDM, TDE и Purview см. выше.

## Что запомнить

- Брандмауэр - первый уровень защиты: database-level правила предпочтительны для изоляции, server-level - для администраторов и однотипных баз.
- Entra-аутентификация централизует управление доступом; назначайте права ролям, а не отдельным пользователям, и добавьте MFA через Conditional Access.
- Аудит пишется в хранилище, Log Analytics или Event Hubs; неуспешные входы Entra смотрите в центре администрирования Entra.
- Маскирование (DDM) меняет только результат запроса, данные в базе не меняются; шифрование at rest - TDE (по умолчанию для новых баз); Always Encrypted защищает от администраторов, но накладывает ограничения на запросы.
- Классификация (Purview) и метки чувствительности - разные вещи: классификация описывает тип данных, метка - уровень конфиденциальности.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/
- Azure SQL Database firewall, Microsoft Entra authentication, Microsoft Purview governance portal, Always Encrypted, Transparent Data Encryption (ссылки и темы из уроков модуля)
