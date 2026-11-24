# AZ-104: внедрение и управление хранилищем в Azure

**Источник** https://learn.microsoft.com/en-us/training/paths/az-104-manage-storage

## О курсе

Управление учетными записями хранения, данными Azure Storage, Azure Files и Azure Blob Storage.

- **Уровень:** начальный (Beginner)
- **Роль:** Administrator
- **Продукты и сервисы:** Azure Storage, Azure Blob Storage, Azure Files, Azure Storage Accounts, Azure Storage Explorer, Azure Virtual Machines
- **Предварительные требования:** Microsoft Azure Fundamentals: describe cloud concepts; Azure Fundamentals: describe Azure architecture and services; Azure Fundamentals: describe Azure management and governance; AZ-104: Prerequisites for Azure administrators (перечислено в источнике).

## Чему научитесь

- Настройка учетных записей хранения, включая репликацию и конечные точки.
- Настройка Azure Blob Storage, включая уровни хранения (tiers) и object replication.
- Настройка функций безопасности хранилища, например shared access signatures.
- Настройка Azure Files и Azure File Sync.

## Модули

1. **Настройка учетных записей хранения Azure (Storage accounts)**. Научиться настраивать учетные записи хранения (storage accounts) и выбирать подходящий тип хранилища: понимать возможности и сценарии использования Azure Storage, создавать storage account, выбирать стратегию репликации и настраивать безопасный сетевой доступ к конечным точкам (endpoints). Модуль готовит к экзамену AZ-104. [guide](../modules/configure-storage-accounts.md)
2. **Настройка Azure Blob Storage**. Научиться настраивать Azure Blob Storage для хранения больших объемов неструктурированных данных: создавать учетные записи и контейнеры, назначать уровни доступа (access tiers), настраивать правила жизненного цикла (lifecycle management) и object replication для отказоустойчивости. Модуль привязан к экзамену AZ-104 (Microsoft Azure Administrator). [guide](../modules/configure-blob-storage.md)
3. **Настройка безопасности Azure Storage**. Настроить shared access signature (SAS) с нужными URI и параметрами, настроить шифрование Azure Storage, внедрить customer-managed keys (CMK) и предложить меры по улучшению безопасности хранилища. Модуль относится к подготовке к экзамену AZ-104. [guide](../modules/configure-storage-security.md)
4. **Настройка Azure Files и Azure File Sync**. Научиться выбирать хранилище для файловых шар, сравнивать Azure Files с Blob Storage, настраивать файловые шары, снапшоты и soft delete, работать с Azure Storage Explorer и понимать, как Azure File Sync кэширует шары на локальных Windows Server. Модуль готовит к экзамену AZ-104. [guide](../modules/configure-azure-files-file-sync.md)

## Ключевые технологии и понятия

- Azure Storage
- Storage account (учетная запись хранения)
- Standard и Premium
- General-purpose v2 (GPv2)
- Hierarchical namespace (HNS)
- Replication (репликация)
- Endpoint (конечная точка)
- Custom domain (пользовательский домен)
- Service endpoint
- Private endpoint
- Storage Service Encryption (SSE)
- Blob Storage
- Storage account
- Container

## Для каких ролей полезно

- Administrator (администратор)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/az-104-manage-storage
- Модуль «Настройка учетных записей хранения Azure (Storage accounts)»: https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/
- Модуль «Настройка Azure Blob Storage»: https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/
- Модуль «Настройка безопасности Azure Storage»: https://learn.microsoft.com/en-us/training/modules/configure-storage-security/
- Модуль «Настройка Azure Files и Azure File Sync»: https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/
