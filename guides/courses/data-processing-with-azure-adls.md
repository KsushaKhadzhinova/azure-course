# Обработка больших данных с Azure Data Lake Storage Gen2

**Источник** https://learn.microsoft.com/en-us/training/paths/data-processing-with-azure-adls

## О курсе

Использование Azure Data Lake Storage Gen2 для аналитической обработки больших данных: настройка, загрузка данных и безопасность.

- **Уровень:** начальный (Beginner)
- **Роль:** Data Engineer
- **Продукты и сервисы:** Azure, Azure Portal, Azure Storage, Azure Virtual Machines
- **Предварительные требования:** В источнике не указаны.

## Чему научитесь

- Роль Azure Data Lake Storage в типовых архитектурах аналитики.
- Создание учетной записи Azure Data Lake Storage Gen2 и загрузка данных.
- Многоуровневые функции безопасности Azure Storage.

## Модули

1. **Введение в Azure Data Lake Storage**. Понять назначение озера данных (data lake), возможности Azure Data Lake Storage Gen2 (безопасность, производительность, избыточность), отличия от Blob Storage, этапы обработки больших данных и типовые аналитические сценарии. [guide](../modules/introduction-to-azure-data-lake-storage.md)
2. **Загрузка данных в Azure Data Lake Storage**. Создать хранилище Data Lake Storage Gen2 (учётная запись Azure Storage с включённым иерархическим пространством имён) и загрузить в него данные вручную с помощью Azure Storage Explorer. [guide](../modules/upload-data-to-azure-data-lake-storage.md)
3. **Защита учетной записи Azure Storage**. Научиться защищать данные в учетной записи Azure Storage: понимать встроенное шифрование, выбирать способ авторизации (Microsoft Entra ID, ключи учетной записи, SAS), ограничивать сетевой доступ, включать защиту от угроз (Microsoft Defender for Storage), аудировать доступ и использовать механизмы безопасности Azure Data Lake Storage Gen2. [guide](../modules/secure-azure-storage-account.md)

## Ключевые технологии и понятия

- Data lake (озеро данных)
- Azure Data Lake Storage Gen2
- Hierarchical namespace (иерархическое пространство имён)
- Azure RBAC и ABAC
- POSIX ACL
- Избыточность
- Data swamp (болото данных)
- Этапы обработки больших данных
- Открытость
- Безопасность
- Производительность
- Планирование
- Ingest
- Store

## Для каких ролей полезно

- Data Engineer (DE, инженер данных)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/data-processing-with-azure-adls
- Модуль «Введение в Azure Data Lake Storage»: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-data-lake-storage/
- Модуль «Загрузка данных в Azure Data Lake Storage»: https://learn.microsoft.com/en-us/training/modules/upload-data-to-azure-data-lake-storage/
- Модуль «Защита учетной записи Azure Storage»: https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/
