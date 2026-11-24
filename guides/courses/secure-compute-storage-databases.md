# Защита вычислений, хранилищ и баз данных

**Источник** https://learn.microsoft.com/en-us/training/paths/secure-compute-storage-databases

## О курсе

Защита вычислительных ресурсов, учетных записей хранения и баз данных Azure: шифрование, контроль доступа и практики безопасности.

- **Уровень:** средний (Intermediate)
- **Роль:** Administrator, Security Engineer
- **Продукты и сервисы:** Azure, Azure App Service, Azure Blob Storage, Azure Files, Azure Key Vault, Azure SQL Database, Azure SQL Managed Instance, Azure Storage, Azure Table Storage, Microsoft Graph
- **Предварительные требования:** В источнике не указаны.

## Чему научитесь

- Защита вычислительных ресурсов Azure (например, контейнеры и удаленный доступ).
- Защита учетных записей хранения и данных в них.
- Защита баз данных Azure SQL Database и Azure SQL Managed Instance.

## Модули

1. **Расширенная безопасность вычислительных ресурсов Azure**. Научиться планировать и внедрять расширенные меры безопасности для вычислительных ресурсов Azure: защищённый удалённый доступ к VM (Azure Bastion, JIT), изоляцию и мониторинг AKS, аутентификацию в AKS через workload identity и Microsoft Entra ID, безопасность контейнеров (ACI, ACA, ACR), шифрование дисков (ADE, encryption at host, confidential disk encryption) и рекомендации по безопасности Azure API Management. [guide](../modules/advanced-security-compute.md)
2. **Безопасность Azure Storage**. Научиться планировать и внедрять меры безопасности для ресурсов Azure Storage по принципам Zero Trust: аутентификация и авторизация через Microsoft Entra ID, управление ключами доступа учетной записи, выбор метода доступа к Azure Files, Blobs, Tables и Queues, защита данных (soft delete, резервные копии, версионирование, immutable storage, point-in-time restore), шифрование с BYOK через Azure Key Vault и двойное шифрование на уровне инфраструктуры. [guide](../modules/security-storage.md)
3. **Безопасность Azure SQL Database и Azure SQL Managed Instance**. Спланировать и внедрить меры безопасности для Azure SQL Database и Azure SQL Managed Instance: сетевой доступ (firewall), аутентификация через Microsoft Entra ID, аудит, классификация данных в Microsoft Purview, динамическое маскирование, шифрование at rest (TDE) и критерии выбора Always Encrypted. [guide](../modules/security-azure-sql-database-azure-sql-managed-instance.md)

## Ключевые технологии и понятия

- Azure Bastion
- Just-in-time (JIT) VM access
- AKS (Azure Kubernetes Service)
- Изоляция в AKS
- Microsoft Entra ID в AKS
- Workload identity
- Microsoft Defender for Containers
- Azure Container Registry (ACR) RBAC
- Azure Disk Encryption (ADE)
- Encryption at host
- Confidential disk encryption
- Envelope encryption (DEK/KEK)
- Azure Key Vault
- Azure API Management security baseline

## Для каких ролей полезно

- Administrator (администратор)
- Security Engineer (инженер по безопасности)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/secure-compute-storage-databases
- Модуль «Расширенная безопасность вычислительных ресурсов Azure»: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/
- Модуль «Безопасность Azure Storage»: https://learn.microsoft.com/en-us/training/modules/security-storage/
- Модуль «Безопасность Azure SQL Database и Azure SQL Managed Instance»: https://learn.microsoft.com/en-us/training/modules/security-azure-sql-database-azure-sql-managed-instance/
