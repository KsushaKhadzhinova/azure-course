# Настройка Azure Blob Storage

**Источник:** https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/

## Цель модуля

Научиться настраивать Azure Blob Storage для хранения больших объемов неструктурированных данных: создавать учетные записи и контейнеры, назначать уровни доступа (access tiers), настраивать правила жизненного цикла (lifecycle management) и object replication для отказоустойчивости. Модуль привязан к экзамену AZ-104 (Microsoft Azure Administrator). Учебный сценарий: медиакомпания с видеотекой, к которой обращаются тысячи раз в день.

## Ключевые понятия

- **Blob Storage** — объектное хранилище Azure для неструктурированных данных (текст, бинарные файлы, видео, установщики).
- **Storage account** — учетная запись хранения; содержит контейнеры.
- **Container** — контейнер, группирующий blobs. Blob не может существовать вне контейнера.
- **Blob** — объект данных. Типы: block blob (по умолчанию), append blob, page blob. Тип после создания нельзя изменить.
- **Access tiers** — уровни доступа Hot, Cool, Cold и Archive с разным соотношением стоимости хранения и доступа.
- **Lifecycle management policy** — правила, которые переводят данные в более холодный уровень или удаляют их по возрасту.
- **Object replication** — асинхронное копирование blobs между контейнерами, в том числе между регионами.
- **Public access level** — уровень публичного доступа контейнера: Private, Blob или Container.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/1-introduction

Введение в Blob Storage как сервис для неструктурированных данных. Перечислены цели модуля и рекомендуемые предварительные знания (облачные концепции, Azure fundamentals, Azure portal или CLI).

### 2. Implement Azure Blob Storage
https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/2-implement

Blob Storage использует три ресурса: storage account, контейнеры и blobs. Настраиваются параметры контейнеров, типы blobs и варианты загрузки, access tiers, lifecycle rules и object replication. Типичные сценарии: загрузка из браузера, распределенный доступ, потоковое видео и аудио, архивирование и восстановление, аналитика приложениями.

### 3. Create blob containers
https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/3-create-blob-containers

Контейнер группирует blobs; учетная запись может содержать неограниченное число контейнеров. Настраиваются имя и уровень публичного доступа. Уровни Blob и Container действуют только при включенной на уровне учетной записи настройке Allow Blob anonymous access; Microsoft рекомендует держать анонимный доступ выключенным, кроме сценариев публичного контента.

### 4. Assign blob access tiers
https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/4-create-blob-access-tiers

Hot — частые чтение и запись, высокая стоимость хранения и низкая стоимость доступа. Cool — редко используемые данные, минимум 30 дней. Cold — минимум 90 дней. Archive — оффлайн-уровень с задержкой извлечения в часы, минимум 180 дней. Данные из Archive возвращаются через Copy Blob (рекомендуется) или Set Blob Tier, с приоритетом Standard (до 15 часов) или High (в пределах 1 часа для объектов до 10 ГБ). Сравнительная таблица: доступность 99.9% для Hot и 99% для остальных уровней; задержка в миллисекундах для Hot, Cool и Cold и в часах для Archive.

### 5. Add blob lifecycle management rules
https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/5-add-blob-lifecycle-management-rules

Правила lifecycle management доступны для GPv2 и Premium block blob аккаунтов (для новых развертываний рекомендуется GPv2; legacy-аккаунты тоже поддерживаются). Правила переводят blobs в более холодный уровень (Hot→Cool, Hot→Cold, Hot→Archive, Cool→Cold, Cool→Archive, Cold→Archive), удаляют текущие или предыдущие версии и snapshots, а также могут возвращать blob из Cool в Hot при доступе. Фильтры: вся учетная запись, выбранные контейнеры или подмножество blobs по префиксу имени или blob index tags. Правило состоит из блока If (More than, days ago) и Then (move to cool / cold / archive storage или delete the blob).

### 6. Determine blob object replication
https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/6-determine-blob-object-replication

Object replication асинхронно копирует содержимое, метаданные и версии blobs согласно политике. Требования: включенное blob versioning на исходном и целевом аккаунтах. Snapshots не реплицируются. Поддерживаются уровни Hot, Cool и Cold, причем у источника и приемника они могут различаться. Политика содержит правила с исходным и целевым контейнером. Сценарии: снижение задержки чтения за счет ближайшего региона, распределение вычислений и данных, экономия за счет переноса реплицированных данных в Archive через lifecycle policies.

### 7. Manage blobs
https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/7-upload-blobs

Три типа blobs: block blob (файлы, изображения, видео; по умолчанию), append blob (оптимизирован для добавления данных, например для логов) и page blob (до 8 ТБ; используется Azure Virtual Machines для дисков ОС и данных). Для небольшого количества файлов подходит портал; для больших объемов — Azure Storage Explorer, AzCopy (командная строка для Windows и Linux) и Azure Data Box Disk для переноса больших наборов данных с локальной среды.

### 8. Determine Blob Storage pricing
https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/8-determine-storage-pricing

Стоимость зависит от объема хранимых данных, количества и типа операций и передачи данных, а также от выбранного уровня избыточности. Оценка выполняется в Azure Pricing Calculator. Учитываются: стоимость хранения (ниже на более холодных уровнях), плата за чтение для Cool, Cold и Archive, плата за транзакции, георепликация, исходящий трафик. Смена уровня аккаунта: переход Cool→Hot оплачивается как чтение всех данных; переход Hot→Cool (только GPv2) — как запись всех данных в Cool.

### 9. Exercise: Provide storage for the public website
https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/9-simulation-blobs

Сценарий: сайт с изображениями, видео и документами для пользователей по всему миру. Задачи: создать учетную запись с высокой доступностью, включить анонимный публичный доступ, создать контейнер для документов, включить soft delete и blob versioning. Оценочное время 30 минут; нужна подписка Azure.

### 10. Module assessment
https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/10-knowledge-check

В исходнике есть только описание сценария (видеотека, вопросы о поддерживаемых access tiers и object replication для отказоустойчивости). Варианты ответов и правильные ответы в источнике не приведены.

### 11. Summary and resources
https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/11-summary-resources

Итоги: Blob Storage — объектное хранилище для неструктурированных данных; уровни Hot, Cool, Cold и Archive подбираются по шаблону использования; lifecycle policies автоматически переводят данные между уровнями и задают сроки истечения; object replication копирует blobs между регионами для избыточности и снижения задержки.

## Важные команды / код / настройки

В источнике нет команд и кода. Настройки, которые упоминаются:

- **Имя контейнера:** от 3 до 63 символов; только строчные буквы, цифры и дефис; начинается с буквы или цифры; уникально в пределах учетной записи.
- **Public access level:** Private (по умолчанию), Blob (анонимное чтение только blobs), Container (анонимное чтение и список всего контейнера).
- **Allow Blob anonymous access:** настройка учетной записи; без нее Blob и Container не действуют.
- **Lifecycle rule:** условие More than (days ago); действия move to cool storage, move to cold storage, move to archive storage, delete the blob.
- **Минимальный срок хранения:** Cool — 30 дней, Cold — 90 дней, Archive — 180 дней.
- **Упражнение:** включить anonymous public access, создать контейнер, включить soft delete и blob versioning.

## Что запомнить

- Blob обязан находиться в контейнере; контейнеры и blobs организуют данные внутри storage account.
- Hot подходит для активной работы, Cool, Cold и Archive — для редко читаемых данных с минимальными сроками хранения.
- Archive требует времени на извлечение (часы), для срочного восстановления используется приоритет High.
- Lifecycle management автоматизирует переходы между уровнями и удаление по возрасту (GPv2 и Premium block blob).
- Object replication требует включенного blob versioning на обоих аккаунтах и не копирует snapshots.

## Связанные материалы

- Azure Blob Storage documentation (официальная документация Microsoft).
- Azure Blob Storage Concepts — storage accounts, containers, blobs.
- Azure Blob Storage Security — аутентификация, авторизация, шифрование.
- Azure Blob Storage Performance and Scalability.
- Azure Blob Storage Lifecycle Management.
- Модуль Manage the Azure Blob storage lifecycle (упомянут в уроке 5).
- Экзамен AZ-104: Microsoft Azure Administrator.
