# Безопасность и управление объектами Unity Catalog в Azure Databricks

**Источник** https://learn.microsoft.com/en-us/training/paths/azure-databricks-data-engineer-secure-govern-unity-catalog

## О курсе

Безопасность и governance данных в Azure Databricks с помощью Unity Catalog: контроль доступа, разрешения, учетные данные.

- **Уровень:** средний (Intermediate)
- **Роль:** Data Engineer
- **Продукты и сервисы:** Azure Databricks, Unity Catalog, Microsoft Entra ID
- **Предварительные требования:** Понимание рабочих областей Azure Databricks и Unity Catalog; знакомство с SQL и шаблонами доступа к данным; знание Microsoft Entra ID и основ безопасности Azure.

## Чему научитесь

- Защита объектов Unity Catalog и гранулярные разрешения.
- Управление учетными данными и практики governance данных.

## Модули

1. **Безопасность объектов Unity Catalog в Azure Databricks**. Спроектировать и реализовать безопасность в Azure Databricks с помощью Unity Catalog: понять жизненный цикл запроса, выдавать привилегии, ограничивать строки и маскировать столбцы, получать секреты из Azure Key Vault и аутентифицировать доступ к данным через service principal и managed identity. [guide](../modules/secure-unity-catalog-objects.md)
2. **Управление объектами Unity Catalog**. Документировать таблицы и столбцы (комментарии и теги), применять управление доступом на основе атрибутов (ABAC) через governed tags и политики, настраивать хранение данных (retention, VACUUM, predictive optimization) и удаление по запросам, отслеживать lineage и аудит, а также спроектировать безопасный сценарий OpenSharing (ранее Delta Sharing). [guide](../modules/govern-unity-catalog-objects.md)

## Ключевые технологии и понятия

- Unity Catalog
- Metastore
- Привилегии (privileges)
- Principal (принципал)
- Row filter и column mask
- Dynamic view (динамическое представление)
- ABAC (Attribute-Based Access Control)
- Azure Key Vault-backed secret scope
- Storage credential и external location
- Managed identity и access connector
- Комментарии (comments)
- Теги (tags)
- Governed tags
- ABAC (attribute-based access control)

## Для каких ролей полезно

- Data Engineer (DE, инженер данных)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/azure-databricks-data-engineer-secure-govern-unity-catalog
- Модуль «Безопасность объектов Unity Catalog в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/secure-unity-catalog-objects/
- Модуль «Управление объектами Unity Catalog»: https://learn.microsoft.com/en-us/training/modules/govern-unity-catalog-objects/
