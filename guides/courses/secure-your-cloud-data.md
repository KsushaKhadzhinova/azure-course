# Защита облачных данных

**Источник** https://learn.microsoft.com/en-us/training/paths/secure-your-cloud-data

## О курсе

Встроенные сервисы безопасности Azure для надежного хранения данных приложения и контроля доступа.

- **Уровень:** начальный (Beginner), средний (Intermediate)
- **Роль:** Developer, Administrator
- **Продукты и сервисы:** Azure, Azure Key Vault, Azure Storage, Azure Cosmos DB, Azure Synapse Analytics, Azure SQL Database
- **Предварительные требования:** В источнике не указаны.

## Чему научитесь

- Многоуровневая защита данных в Azure Storage.
- Управление доступом к ресурсам Azure с помощью Azure RBAC.

## Модули

1. **Защита учетной записи Azure Storage**. Научиться защищать данные в учетной записи Azure Storage: понимать встроенное шифрование, выбирать способ авторизации (Microsoft Entra ID, ключи учетной записи, SAS), ограничивать сетевой доступ, включать защиту от угроз (Microsoft Defender for Storage), аудировать доступ и использовать механизмы безопасности Azure Data Lake Storage Gen2. [guide](../modules/secure-azure-storage-account.md)
2. **Защита ресурсов Azure с помощью RBAC**. Научиться управлять доступом к ресурсам Azure с помощью Azure RBAC: проверять доступ для себя и других, назначать роли на нужном уровне (scope) и просматривать activity log изменений RBAC. [guide](../modules/secure-azure-resources-with-rbac.md)

## Ключевые технологии и понятия

- Storage Service Encryption (SSE)
- Encryption in transit
- CORS (Cross-Origin Resource Sharing)
- Microsoft Entra ID и RBAC
- Managed identity
- Storage account keys
- Shared access signature (SAS)
- Private endpoint
- Microsoft Defender for Storage
- ACL (POSIX-like)
- Azure RBAC
- Security principal (кто)
- Role definition (что)
- Scope (где)

## Для каких ролей полезно

- Developer (разработчик)
- Administrator (администратор)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/secure-your-cloud-data
- Модуль «Защита учетной записи Azure Storage»: https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/
- Модуль «Защита ресурсов Azure с помощью RBAC»: https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/
