# Внедрение безопасности Azure Storage

**Источник** https://learn.microsoft.com/en-us/training/paths/implement-azure-storage-security

## О курсе

Стратегия глубокой защиты (defense in depth) для Azure Storage: доступ, сеть и обнаружение угроз.

- **Уровень:** средний (Intermediate)
- **Роль:** Security Engineer
- **Продукты и сервисы:** Azure Storage, Azure Blob Storage, Azure Files, Microsoft Defender for Cloud
- **Предварительные требования:** Знакомство с учетными записями Azure Storage (Blob Storage и Azure Files); понимание Azure RBAC и managed identities; базовое знакомство с Microsoft Defender for Cloud.

## Чему научитесь

- Типы сервисов хранения в Azure.
- Контроль доступа на уровне учетной записи, managed identities Microsoft Entra ID и stored access policies.
- Сетевые ограничения: правила firewall и private endpoints.
- Microsoft Defender for Storage для обнаружения угроз Blob Storage.

## Модули

1. **Описание сервисов хранения Azure**. Научиться сравнивать сервисы Azure Storage, понимать типы учетных записей хранения, уровни доступа Blob, варианты избыточности и способы переноса данных в Azure и внутри него (AzCopy, Azure Storage Explorer, Azure File Sync, Azure Migrate, Azure Data Box). [guide](../modules/describe-azure-storage-services.md)
2. **Реализация безопасности учётной записи хранения Azure**. Настроить базовые параметры безопасности учётной записи хранения (secure transfer, минимальная версия TLS, запрет анонимного доступа, запрет репликации между арендаторами), выбрать модель авторизации (managed identity и RBAC предпочтительны), управлять жизненным циклом SAS-токенов через stored access policies и отключить Shared Key авторизацию с контролем через Azure Policy. [guide](../modules/implement-storage-account-security.md)
3. **Настройка сетевой безопасности Azure Storage**. Научиться ограничивать сетевой доступ к учётным записям хранения Azure: создавать правила брандмауэра (deny-all по умолчанию), правила виртуальной сети и IP-правила, правила экземпляров ресурсов и исключения для доверенных служб, а также внедрять приватные конечные точки (private endpoints). [guide](../modules/configure-network-security-azure-storage.md)
4. **Внедрение Microsoft Defender for Storage**. Научиться включать Microsoft Defender for Storage на уровне подписки и ресурса, настраивать сканирование вредоносных файлов с лимитами стоимости, обнаружение угроз для чувствительных данных, маршрутизацию оповещений и проверять покрытие защитой. [guide](../modules/implement-defender-storage.md)

## Ключевые технологии и понятия

- Storage account (учетная запись хранения)
- Azure Blobs
- Azure Files
- Azure Queues
- Azure Disks
- Azure Tables
- Access tiers (уровни доступа)
- LRS (Locally redundant storage)
- ZRS (Zone-redundant storage)
- GRS / GZRS
- RA-GRS / RA-GZRS
- RPO (Recovery Point Objective)
- AzCopy
- Azure Storage Explorer

## Для каких ролей полезно

- Security Engineer (инженер по безопасности)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/implement-azure-storage-security
- Модуль «Описание сервисов хранения Azure»: https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/
- Модуль «Реализация безопасности учётной записи хранения Azure»: https://learn.microsoft.com/en-us/training/modules/implement-storage-account-security/
- Модуль «Настройка сетевой безопасности Azure Storage»: https://learn.microsoft.com/en-us/training/modules/configure-network-security-azure-storage/
- Модуль «Внедрение Microsoft Defender for Storage»: https://learn.microsoft.com/en-us/training/modules/implement-defender-storage/
