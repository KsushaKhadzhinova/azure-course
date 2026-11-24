# Azure Data Lake Storage Gen2

## Что это и зачем

Azure Data Lake Storage Gen2 (ADLS Gen2) - это набор возможностей для аналитики больших данных, построенный поверх Azure Blob Storage. Важно понимать, что ADLS Gen2 не является отдельным сервисом или отдельным типом учетной записи: это набор функций, которые включаются в обычной storage account настройкой **hierarchical namespace** (иерархического пространства имен) (docs/d1-azure-storage-blobs-data-lake-storage-introduction.md).

Зачем это нужно. Data lake - это единое централизованное хранилище, в котором можно держать и структурированные, и неструктурированные данные в исходном (raw или native) формате, обычно в виде файлов или blob-объектов. По источнику ADLS Gen2 предоставляет масштабируемое, безопасное облачное хранилище для такого data lake. Документация подчеркивает три свойства: file system semantics, file-level security и масштаб (сервис рассчитан на несколько петабайт данных при пропускной способности в сотни гигабит в секунду) (docs/d1-azure-storage-blobs-data-lake-storage-introduction.md). Ограничений на размер аккаунта, размер файла или объем данных в документации не указано; размер отдельного файла может составлять от нескольких килобайт до сотен терабайт (там же).

Из материалов курса (pages/04-intro-azure-data-lake-storage.md) следует, что модуль "Introduction to Azure Data Lake Storage Gen2" учит описывать ключевые возможности и преимущества ADLS Gen2, включать его в storage account, сравнивать с Blob Storage, понимать место сервиса в этапах аналитической обработки и типовые аналитические нагрузки.

## Архитектура и ключевые компоненты

Ниже - слои, из которых состоит решение, по данным документации.

1. **Storage account.** Учетная запись хранения, в которой размещаются данные. Для ADLS Gen2 подходят два типа: Standard general-purpose v2 и Premium block blob. Выбор делается на вкладке Basics при создании аккаунта, а сама опция hierarchical namespace включается на вкладке Advanced (docs/d1-azure-storage-blobs-create-data-lake-storage-account.md).

2. **Hierarchical namespace.** Ключевая функция, которая организует объекты и файлы аккаунта в иерархию директорий и вложенных поддиректорий, как на обычном компьютере. Переименование и удаление директории становятся одной атомарной операцией над метаданными директории, без перебора всех объектов с общим префиксом (docs/d1-azure-storage-blobs-data-lake-storage-introduction.md; docs/d1-azure-storage-blobs-data-lake-storage-namespace.md).

3. **Blob Storage как основа.** Данные хранятся как blob-объекты, а управляет ими сервис Azure Blob Storage. Поэтому доступны диагностическое логирование, access tiers и lifecycle management policies. Большинство функций Blob Storage поддерживается, но часть возможностей может быть в статусе preview или не поддерживаться вовсе (docs/d1-azure-storage-blobs-data-lake-storage-introduction.md).

4. **Доступ по протоколам.** ADLS Gen2 рассчитан прежде всего на Hadoop и фреймворки, которые используют HDFS как слой доступа к данным. Дистрибутивы Hadoop включают ABFS driver (Azure Blob File System), который позволяет приложениям работать с данными Blob Storage напрямую. REST API доступны через endpoint dfs.core.windows.net. Примеры фреймворков - Apache Spark и Presto (docs/d1-azure-storage-blobs-data-lake-storage-introduction.md).

5. **Модель управления доступом.** Поддерживаются Shared Key, SAS, Azure RBAC, Azure ABAC и ACL (подробнее в разделе "Безопасность и стоимость") (docs/d1-azure-storage-blobs-data-lake-storage-access-control-model.md).

6. **Сеть и шифрование.** Firewall rules, virtual network rules, private endpoints, шифрование at rest (docs/d2-azure-storage-common-storage-network-security.md; docs/d2-azure-storage-common-storage-private-endpoints.md; docs/d1-azure-storage-common-storage-service-encryption.md).

7. **Избыточность.** Выбирается на уровне аккаунта (LRS, ZRS, GRS, GZRS и варианты с read access) (docs/d1-azure-storage-common-storage-redundancy.md).

**Типы учетных записей и их отличие.** Документация по storage account overview описывает типы аккаунтов, рекомендуемые для большинства сценариев; legacy Blob Storage аккаунты с блоками и append blobs, по этому же источнику, рекомендуется обновлять до GPv2, чтобы использовать access tiers и lifecycle management (docs/d0-azure-storage-common-storage-account-overview.md). Для аналитики документация отдельно рекомендует premium block blob (см. "Практика" и раздел "Безопасность и стоимость").

**Место в аналитическом процессе.** Data lake хранит сырые данные, из которых аналитические движки строят результаты. Документация показывает ADLS Gen2 как хранилище для этапов ingest, process и analyze; список поддерживаемых сервисов приведен ниже (deep/d1-azure-storage-blobs-data-lake-storage-supported-azure-services.md).

## Основные понятия (glossary)

| Термин (English) | Определение |
|---|---|
| Azure Data Lake Storage Gen2 | Набор возможностей аналитики больших данных поверх Blob Storage, включаемый через hierarchical namespace. |
| Hierarchical namespace | Иерархия директорий и поддиректорий в аккаунте; дает атомарные операции над директориями и file system semantics. |
| Storage account | Учетная запись Azure Storage, в которой размещаются контейнеры и данные. |
| Blob | Объект данных в Blob Storage. В документации файлы, загруженные в аккаунт, называются blob. |
| Container (file system) | Контейнер, который в контексте ADLS Gen2 выступает как файловая система; термины считаются синонимами. |
| ABFS driver (Azure Blob File System) | Драйвер для Hadoop и совместимых фреймворков, обеспечивающий прямой доступ к данным Blob Storage. |
| dfs.core.windows.net | Endpoint REST API для ADLS Gen2. |
| Azure RBAC | Назначение ролей (role assignments) субъектам на "грубом" уровне: доступ ко всем данным аккаунта или контейнера. |
| Azure ABAC | Условия (role assignment conditions) к ролям RBAC, например доступ к объектам с определенным тегом. |
| ACL (Access Control List) | Список записей доступа к директории или файлу; позволяет "тонкий" доступ, например запись в конкретную директорию. |
| ACL entry | Запись внутри ACL, связывающая субъект безопасности с уровнем доступа. |
| Security principal | Пользователь, группа, service principal или managed identity из Microsoft Entra ID. |
| Shared Key | Ключевая авторизация аккаунта; вызывающий получает полный доступ ко всем операциям и ACL не применяются. |
| SAS (shared access signature) | Токен ограниченного доступа; user delegation SAS может использовать ACL. |
| Access tiers (hot, cool, cold, archive, smart, turbo) | Уровни хранения blob-данных с разной стоимостью хранения и доступа. |
| LRS / ZRS / GRS / GZRS | Варианты избыточности: локальная, зональная, геореплицированная, геозональная. |
| RA-GRS / RA-GZRS | Варианты геореплики с доступом на чтение из вторичного региона. |
| Private endpoint | Сетевой интерфейс с IP-адресом из virtual network, обеспечивающий доступ к хранилищу по Private Link. |
| Service endpoint | Прямое подключение подсети к Azure Storage через Virtual Network service endpoint. |
| Encryption scope | Ключ шифрования, привязанный к контейнеру или отдельному blob. |
| Customer-managed keys | Ключи шифрования клиента, хранимые в Azure Key Vault или Key Vault HSM. |

## Как работает / типовые сценарии

**Как работает включение и использование.** Hierarchical namespace включается при создании аккаунта или при обновлении существующего аккаунта. Важное ограничение: после включения нельзя вернуться к плоскому пространству имен (docs/d1-azure-storage-blobs-data-lake-storage-namespace.md). Перед включением документация советует оценить влияние на рабочие нагрузки, приложения, стоимость, интеграции и функции, а также выполнить TCO-анализ. Там же сказано, что для backup, хранения изображений и подобных сценариев, где организация объектов хранится отдельно (например, в базе данных), выгоды могут не проявиться.

**Почему важен namespace.** Объектные хранилища без иерархии имитируют каталоги через слэши в именах объектов, поэтому операции переименования и удаления каталогов требуют обработки множества blob. Инструменты Hive и Spark часто пишут результат во временное место и затем переименовывают его по завершении задания; без иерархии это переименование может занимать больше времени, чем сама аналитика (docs/d1-azure-storage-blobs-data-lake-storage-namespace.md).

**Типовые сценарии из документации:**
- Загрузка данных через Azure Data Factory в контейнер ADLS Gen2 (Data Factory поддерживается с общей доступностью GA, см. список сервисов).
- Аналитика в Azure Databricks, Azure Synapse Analytics, HDInsight, Azure Machine Learning, Power BI, Azure Data Explorer.
- Потоковая обработка: Azure Stream Analytics читает данные из Event Hubs, фильтрует их и пишет в ADLS Gen2. Пример no-code сценария описан в docs/d2-azure-stream-analytics-filter-ingest-data-lake-storage-gen2.md.
- Захват событий: Azure Event Hubs может записывать (capture) события в Blob Storage или ADLS Gen2 (deep/d1-azure-storage-blobs-data-lake-storage-supported-azure-services.md).

**Поддерживаемые сервисы** (по таблице из документации; уровень поддержки - generally available, если не указано иное):

| Сервис | Entra ID | Shared Key |
|---|---|---|
| Azure Data Factory | Да | Да |
| Azure Databricks | Да | Да |
| Azure Event Hubs | Нет | Да |
| Azure Event Grid | Да | Да |
| Azure Logic Apps | Нет | Да |
| Azure Machine Learning | Да | Да |
| Azure Stream Analytics | Да | Да |
| HDInsight | Да | Да |
| Power BI | Да | Да |
| Azure Synapse Analytics | Да | Да |
| Azure Data Explorer | Да | Да |
| Azure AI Search | Да | Да |
| Azure SQL Managed Instance (preview) | Нет | Да |

Источник: deep/d1-azure-storage-blobs-data-lake-storage-supported-azure-services.md. Список документация называет развивающимся.

**Лучшие практики структуры данных** (deep/d1-azure-storage-blobs-data-lake-storage-best-practices.md): рекомендуется использовать Parquet для аналитики (колоночный формат, позволяет пропускать нерелевантные данные и эффективнее сжимать); при проектировании структуры директорий полезно ставить дату в конец пути, а не в начало: тогда ACL проще назначать отдельным регионам и тематикам, а количество директорий не растет экспоненциально. Этот пример в документации дан для IoT-структуры.

## Практика (steps, commands, code only from sources)

**1. Создание аккаунта с hierarchical namespace** (docs/d1-azure-storage-blobs-create-data-lake-storage-account.md):
- Откройте страницу Create a storage account.
- На вкладке Basics выберите Standard (general-purpose v2) или Premium (premium block blob).
- На вкладке Advanced включите настройку Enable hierarchical namespace.
- Для существующего аккаунта используйте сценарий Upgrade Azure Blob Storage with Azure Data Lake Storage capabilities (ссылка из того же документа; сам сценарий в загруженных материалах не разобран).

**2. Работа с контейнерами и директориями через Azure CLI** (docs/d1-azure-storage-blobs-data-lake-storage-directory-file-acl-cli.md). Требуется Azure CLI версии 2.6.0 или новее; примеры используют Microsoft Entra authorization (`--auth-mode login`).

```
az login
az account set --subscription <subscription-id>
az storage fs create -n my-file-system --account-name mystorageaccount --auth-mode login
az storage fs show -n my-file-system --account-name mystorageaccount --auth-mode login
az storage fs file list -f my-file-system --account-name mystorageaccount --auth-mode login
az storage fs directory create -n my-directory -f my-file-system --account-name mystorageaccount --auth-mode login
az storage fs directory move -n my-directory -f my-file-system --new-directory "my-file-system/my-new-directory" --account-name mystorageaccount --auth-mode login
az storage fs directory delete -n my-directory -f my-file-system --account-name mystorageaccount --auth-mode login
```

Команды взяты из источника; значения `mystorageaccount` и `<subscription-id>` - плейсхолдеры. Команда `directory move` демонстрирует ту самую атомарную операцию над директорией, о которой говорилось выше.

**3. Назначение ACL в портале** (docs/d1-azure-storage-blobs-data-lake-storage-acl-azure-portal.md): откройте storage account, в разделе Data storage выберите Containers, перейдите к контейнеру, директории или blob, щелкните правой кнопкой и выберите Manage ACL; на вкладке Access permissions управляйте доступом. Для этого нужна роль Storage Blob Data Owner в области контейнера, аккаунта, группы ресурсов или подписки либо владение объектом.

**4. Потоковая загрузка через Stream Analytics no-code editor** (docs/d2-azure-stream-analytics-filter-ingest-data-lake-storage-gen2.md): предварительные условия - Event Hubs должен быть публично доступен (не за firewall и не в VNet), данные в JSON, CSV или Avro. Для запуска рекомендуется начать с трех Streaming Units (SU). Задание запускается в течение двух минут; файлы появляются в выбранном контейнере.

**5. Просмотр содержимого в Azure Storage Explorer.** Для просмотра содержимого контейнера в Storage Explorer принципал должен войти через Microsoft Entra ID и иметь как минимум доступ чтения (R--) к корневой папке контейнера (docs/d1-azure-storage-blobs-data-lake-storage-access-control-model.md).

## Безопасность и стоимость

**Модель авторизации.** Из документации access control model (docs/d1-azure-storage-blobs-data-lake-storage-access-control-model.md):

- Shared Key, account SAS и service SAS дают доступ без идентичности в Microsoft Entra ID; Azure RBAC, ABAC и ACL при этом не действуют. Shared Key дает вызывающему "super-user" доступ, включая смену владельца и ACL.
- User delegation SAS защищен учетными данными Entra, поэтому к нему применимы ACL: Azure Storage выполняет проверку POSIX ACL по object ID при наличии параметра suoid.
- Azure RBAC - грубый уровень (например, чтение всех данных аккаунта). Роли: Storage Blob Data Owner (полный доступ, включая смену владельца и ACL), Storage Blob Data Contributor (чтение, запись, удаление, без смены владельца), Storage Blob Data Reader (чтение и список). Роли Owner, Contributor, Reader и Storage Account Contributor данных не открывают, но, кроме Reader, могут получить ключи доступа к хранилищу.
- ABAC уточняет назначения RBAC условиями. Явно запретить доступ условиями нельзя.
- ACL - тонкий уровень, на директории и файлы. Каждая запись связывает субъекта с уровнем доступа.

**Порядок оценки.** Сначала проверяется, есть ли role assignment для принципала. Если есть, проверяются условия ABAC; если все условия совпадают или условий нет, доступ предоставляется. Иначе проверяются ACL. Важное следствие из документации: ACL нельзя использовать, чтобы ограничить доступ, уже предоставленный role assignment, потому что при достаточном праве роли ACL игнорируются.

**Рекомендации по ACL и группам** (docs/d1-azure-storage-blobs-data-lake-storage-access-control-model.md):
- Всегда назначайте в ACL группы Microsoft Entra, а не отдельных пользователей или service principals, чтобы не переназначать ACL на всей иерархии при изменении состава.
- Microsoft Entra рекомендует держать членство принципала менее чем в 200 группах; превышение может вызвать непредвиденные проблемы с производительностью Data Lake Storage Gen2.
- Лимиты: 4000 role assignments на подписку; 32 записи ACL на файл или директорию (фактически 28), отдельно для access и default ACL.

**Пример из документации** для групп: директория /LogData, группа LogsWriter с rwx, группа LogsReader с r-x, service principal Data Factory в LogsWriter, service principal Databricks в LogsReader.

**Сеть** (docs/d2-azure-storage-common-storage-network-security.md):
- Firewall rules ограничивают публичный endpoint. По умолчанию аккаунт принимает подключения из любой сети; при настройке сетевых правил разрешен только явно разрешенный трафик.
- Четыре типа правил: virtual network rules (до 400 на аккаунт), IP network rules (до 400 на аккаунт), resource instance rules, trusted service exceptions.
- Трафик к подсети блокируется по умолчанию; запросы получают ошибку 403, пока не добавлено правило и не включен service endpoint Microsoft.Storage (или Microsoft.Storage.Global для любого региона). Для одной подсети можно включить только один из этих типов.
- Если для подсети включен service endpoint, трафик из нее использует приватный адрес, и IP-правила для нее уже не действуют.

**Private endpoints** (docs/d2-azure-storage-common-storage-private-endpoints.md). Приватный endpoint получает IP из диапазона virtual network и подключает клиентов по Private Link через магистраль Microsoft, без выхода в интернет. Создание приватного endpoint отправляет запрос на согласие владельцу аккаунта. Частный доступ можно сделать единственным, настроив firewall на отказ через публичный endpoint. Приватные endpoints не поддерживаются для general-purpose v1 аккаунтов.

**Шифрование** (docs/d1-azure-storage-common-storage-service-encryption.md):
- Серверное шифрование (SSE) включено для всех аккаунтов и не отключается. Используется 256-битный AES (AES-GCM), FIPS 140-2 совместимо. Дополнительной платы нет.
- По умолчанию данные шифруются ключами Microsoft; можно указать customer-managed keys в Azure Key Vault или Key Vault Managed HSM, либо customer-provided keys в запросе к Blob Storage.
- Encryption scopes позволяют задать ключ на уровне контейнера или blob, например для разделения данных разных клиентов в одном аккаунте.
- Infrastructure encryption - второй слой шифрования на уровне инфраструктуры с отдельным ключом Microsoft.
- Client-side encryption v1 не рекомендуется из-за уязвимости в реализации CBC; нужно переходить на v2.

**Рекомендации по безопасности Blob Storage** (docs/d1-azure-storage-blobs-security-recommendations.md): включить Microsoft Defender for Storage; включить soft delete для blob и контейнеров; установить Azure Resource Manager lock на аккаунт (он защищает сам аккаунт, но не данные внутри); хранить критичные данные в immutable blobs (WORM, legal hold и time-based retention); требовать secure transfer (HTTPS); ограничивать SAS только HTTPS.

**Избыточность и доступность** (docs/d1-azure-storage-common-storage-redundancy.md). Документ отмечает, что ZRS рекомендуется в основном регионе для рабочих нагрузок Azure Data Lake Storage.

| Параметр | LRS | ZRS | GRS / RA-GRS | GZRS / RA-GZRS |
|---|---|---|---|---|
| Долговечность за год | не менее 11 девяток | не менее 12 девяток | не менее 16 девяток | не менее 16 девяток |
| Чтение во вторичном регионе | Нет | Нет | Только RA-GRS | Только RA-GZRS |

- LRS: одна физическая площадка; защищает от сбоев дисков, серверов и стоек, но не от пожара или наводнения в ЦОД. Самый дешевый вариант.
- ZRS: три или более зон доступности в основном регионе, синхронная запись; при недоступности зоны операции продолжаются, но возможно перенастроение DNS, поэтому нужны retry-политики с exponential back-off.
- GRS/GZRS: асинхронная репликация во вторичный регион. Без RA данные во вторичном регионе недоступны до failover. RPO для Block Blobs при Geo priority replication - не более 15 минут.
- Архивный tier для Blob Storage не поддерживается для ZRS, GZRS и RA-GZRS аккаунтов.

**Access tiers и стоимость** (docs/d1-azure-storage-blobs-access-tiers-overview.md):
- Hot - для активно используемых данных; самая высокая цена хранения, самая низкая цена доступа.
- Cool - минимум 30 дней хранения; ниже цена хранения, выше цена доступа.
- Cold - минимум 90 дней; еще ниже хранение и выше доступ, но быстрое извлечение сохраняется.
- Archive - офлайн-уровень с задержкой порядка часов; минимум 180 дней. Самое низкое хранение, самый высокий порог извлечения.
- Smart tier автоматически переносит данные между hot, cool и cold по шаблону использования.
- Turbo tier (Preview) - SSD-производительность для низкой задержки и высокой пропускной способности, например для AI, ML и интерактивной аналитики, внутри general-purpose аккаунта.
- Ранний перенос или удаление до истечения минимального срока тарифицируется пропорционально (пример из документации: удаление в cool через 21 день - плата за 9 оставшихся дней). Если soft delete включен, удаленный blob не подпадает под штраф до истечения retention.
- Tier можно задать только для block blobs; изменение tier для append и page blobs не поддерживается.
- Лимиты емкости задаются на уровне аккаунта, а не tier.

**Premium tier.** Документация рекомендует при низких и стабильных задержках или высоком числе IOPS использовать premium block blob аккаунт с ADLS Gen2 (так называемый premium tier for Azure Data Lake Storage). Данные лежат на SSD; стоимость хранения выше, стоимость транзакций ниже, поэтому при большом количестве операций такой вариант может быть экономичен (deep/d1-azure-storage-blobs-data-lake-storage-best-practices.md).

**Стоимость по данным namespace-документации.** Цены для аккаунтов с плоским и иерархическим пространством имен документ предлагает сравнить на странице Azure Data Lake Storage pricing, которая в загруженных материалах не открыта. Конкретных ценовых значений в этом разделе нет. Документация также указывает, что вычисления часто составляют более 85% совокупной стоимости, поэтому снижение задержки за счет namespace может уменьшить TCO, даже если хранение дорожает.

**Потенциальные ограничения.** Shared Key и SAS без user delegation не привязаны к идентичности, поэтому ACL к ним не применяются (Shared Key дает полный доступ). Документация по RBAC также отмечает, что роли Owner, Contributor и Storage Account Contributor могут получить доступ к ключам хранилища.

## Частые вопросы для собеседования

**1. Чем ADLS Gen2 отличается от Blob Storage?**
ADLS Gen2 - это не отдельный сервис, а набор возможностей поверх Blob Storage, включаемый hierarchical namespace. Он добавляет иерархию директорий с атомарными операциями, file system semantics, POSIX-подобные ACL и ABFS-драйвер для Hadoop-совместимых фреймворков, оставаясь при этом на цене уровня Blob Storage (docs/d1-azure-storage-blobs-data-lake-storage-introduction.md).

**2. Почему hierarchical namespace важен для аналитики?**
Переименование и удаление директории выполняются как одна операция над метаданными родительской директории, а не как обработка всех blob с префиксом. Это критично для Spark и Hive, которые переименовывают временные выходные директории по завершении задания (docs/d1-azure-storage-blobs-data-lake-storage-namespace.md).

**3. Можно ли отключить hierarchical namespace после включения?**
Нет. После включения аккаунт нельзя вернуть к плоскому пространству имен (docs/d1-azure-storage-blobs-data-lake-storage-namespace.md).

**4. Как RBAC и ACL взаимодействуют?**
Сначала проверяются role assignments и их условия ABAC; если доступ предоставлен, ACL игнорируются. Если назначения не дают нужного доступа, проверяются ACL. Поэтому ACL нельзя использовать, чтобы закрыть доступ, уже выданный через RBAC. ACL применяются к Entra-идентичностям и user delegation SAS, но не к Shared Key (docs/d1-azure-storage-blobs-data-lake-storage-access-control-model.md).

**5. Почему в ACL рекомендуется использовать группы Microsoft Entra?**
Группы позволяют добавлять и удалять пользователей без переназначения ACL на всей иерархии директорий. Лимиты: менее 200 групп на принципала и 32 записи ACL на объект (с учетом практического ограничения 28) (docs/d1-azure-storage-blobs-data-lake-storage-access-control-model.md).

**6. Какую избыточность выбрать для data lake?**
Документация рекомендует ZRS в основном регионе для рабочих нагрузок ADLS и георепликацию в secondary region для защиты от регионального сбоя, а для чтения во время сбоя - RA-GRS или RA-GZRS. Варианты LRS, ZRS, GRS, GZRS различаются по долговечности (11, 12 и 16 девяток) и поведению при сбоях (docs/d1-azure-storage-common-storage-redundancy.md).

**7. Как ограничить сетевой доступ к аккаунту ADLS Gen2?**
Настроить firewall rules (virtual network rules, IP rules, resource instance rules, trusted service exceptions), при этом по умолчанию трафик из подсетей блокируется до добавления правила; либо использовать private endpoint по Private Link и запретить доступ через публичный endpoint (docs/d2-azure-storage-common-storage-network-security.md; docs/d2-azure-storage-common-storage-private-endpoints.md).

**8. Как шифруются данные в Azure Storage?**
Все данные шифруются на стороне сервиса 256-битным AES; это нельзя отключить и нет доплаты. По умолчанию используются ключи Microsoft. Можно перейти на customer-managed keys в Azure Key Vault, включить infrastructure encryption для двойного шифрования или задать encryption scopes для контейнера или blob (docs/d1-azure-storage-common-storage-service-encryption.md).

## Источники

Файлы относительно базовой папки azure-course:

- pages/04-intro-azure-data-lake-storage.md - https://learn.microsoft.com/en-us/training/modules/intro-to-azure-data-lake-storage
- docs/d1-azure-storage-blobs-data-lake-storage-introduction.md - https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction
- docs/d1-azure-storage-blobs-data-lake-storage-namespace.md - https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-namespace
- docs/d1-azure-storage-common-storage-redundancy.md - https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy
- docs/d1-azure-storage-blobs-access-tiers-overview.md - https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview
- docs/d2-azure-storage-common-storage-network-security.md - https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security
- docs/d2-azure-storage-common-storage-private-endpoints.md - https://learn.microsoft.com/en-us/azure/storage/common/storage-private-endpoints
- docs/d1-azure-storage-blobs-create-data-lake-storage-account.md - https://learn.microsoft.com/en-us/azure/storage/blobs/create-data-lake-storage-account
- docs/d1-azure-storage-common-storage-service-encryption.md - https://learn.microsoft.com/en-us/azure/storage/common/storage-service-encryption
- docs/d1-azure-storage-blobs-data-lake-storage-access-control-model.md - https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control-model
- docs/d1-azure-storage-blobs-data-lake-storage-directory-file-acl-cli.md - https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-directory-file-acl-cli
- docs/d1-azure-storage-blobs-data-lake-storage-acl-azure-portal.md - https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-acl-azure-portal
- docs/d1-azure-storage-blobs-security-recommendations.md - https://learn.microsoft.com/en-us/azure/storage/blobs/security-recommendations
- docs/d2-azure-stream-analytics-filter-ingest-data-lake-storage-gen2.md - https://learn.microsoft.com/en-us/azure/stream-analytics/filter-ingest-data-lake-storage-gen2
- docs/d0-azure-storage-common-storage-account-overview.md - https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview
- deep/d1-azure-storage-blobs-data-lake-storage-supported-azure-services.md - https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-supported-azure-services
- deep/d1-azure-storage-blobs-data-lake-storage-best-practices.md - https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-best-practices

Пропущено: учебные модули modules/ и deep/ по Azure Storage (configure-storage-security, configure-network-security-azure-storage и другие) не открывались, так как основные темы закрыты официальной документацией. Страница https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control-model из документации была загружена как docs/d1-azure-storage-blobs-data-lake-storage-access-control-model.md; страница по цене ADLS Gen2 и сценарий обновления существующего аккаунта в материалах не загружены и не использованы.
