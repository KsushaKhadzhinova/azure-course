# Identity и доступ в Azure: Azure RBAC

## Что это и зачем

Azure role-based access control (Azure RBAC) - система авторизации, которая управляет тем, кто имеет доступ к ресурсам Azure, какие действия он может выполнять и к каким областям (scope) имеет доступ. Azure RBAC построена на Azure Resource Manager и обеспечивает fine-grained управление доступом к ресурсам (источник: pages/03-azure-rbac-overview.md, https://learn.microsoft.com/en-us/azure/role-based-access-control/overview).

Типовые примеры из материалов:
- один пользователь управляет виртуальными машинами в подписке, другой - виртуальными сетями;
- группа DBA управляет SQL-базами данных в подписке;
- пользователь управляет всеми ресурсами в resource group;
- приложение получает доступ ко всем ресурсам в resource group (источник: pages/03-azure-rbac-overview.md).

Принцип предоставления доступа - least privilege: выдавать только тот доступ, который нужен для работы, и не назначать широкие роли на широких областях "для удобства" (источник: deep/d2-azure-role-based-access-control-best-practices.md).

Использование Azure RBAC бесплатно и входит в подписку Azure (источник: pages/03-azure-rbac-overview.md).

## Архитектура и ключевые компоненты

### Модель назначения роли

Доступ задается через role assignment, который состоит из трех элементов (источник: pages/03-azure-rbac-overview.md):

1. **Security principal** - объект, представляющий user, group, service principal или managed identity, который запрашивает доступ.
2. **Role definition** - коллекция разрешений (роль), например Owner, Contributor или Storage Blob Data Reader.
3. **Scope** - набор ресурсов, на который распространяется доступ.

Доступ предоставляется созданием role assignment и отзывается удалением role assignment (источник: pages/03-azure-rbac-overview.md).

### Role definition: структура

Role definition содержит (источник: deep/d1-azure-role-based-access-control-role-definitions.md):
- `Actions` - control plane действия, которые роль разрешает;
- `NotActions` - control plane действия, исключенные из `Actions`;
- `DataActions` - data plane действия над данными внутри объекта;
- `NotDataActions` - data plane действия, исключенные из `DataActions`;
- `AssignableScopes` - области, где роль доступна для назначения;
- `Condition` и `ConditionVersion` (для built-in ролей; версия по умолчанию 2.0, единственная поддерживаемая).

Формат действия: `{Company}.{ProviderName}/{resourceType}/{action}`. Подстрока `{action}` может быть `*` (все действия), `read` (GET), `write` (PUT или PATCH), `action` (POST, например restart виртуальной машины) или `delete` (DELETE) (источник: deep/d1-azure-role-based-access-control-role-definitions.md).

Пример из источника: роль Contributor имеет `Actions: ["*"]` и набор `NotActions`, например `Microsoft.Authorization/*/Write` и `Microsoft.Authorization/*/Delete`. Поэтому Contributor управляет всеми ресурсами, но не может назначать роли в Azure RBAC (описание роли: "does not allow you to assign roles in Azure RBAC") (источник: deep/d1-azure-role-based-access-control-role-definitions.md).

### Control plane и data plane

Azure имеет data actions, которые дают доступ к данным внутри объекта. Например, если у пользователя роль read data access к storage account, он может читать blobs или messages внутри этого account (источник: pages/03-azure-rbac-overview.md). В примере из deep/d1-azure-role-based-access-control-role-definitions.md Alice с ролью Owner на уровне подписки и Bob с ролью Storage Blob Data Contributor на уровне storage account имеют разные наборы действий: Bob может читать, записывать и удалять контейнеры и blobs в указанном account, но только в рамках `Actions` и `DataActions` своей роли.

### Scope

Scope задает, к каким ресурсам применяется доступ. Доступны четыре уровня: management group, subscription, resource group и resource. Области образуют иерархию parent-child; роли, назначенные на более высоком уровне, наследуются нижними уровнями (источник: deep/d1-azure-role-based-access-control-scope-overview.md).

Формат scope (источник: deep/d1-azure-role-based-access-control-scope-overview.md):

```
/subscriptions
    /{subscriptionId}
        /resourcegroups
            /{resourceGroupName}
                /providers
                    /{providerName}
                        /{resourceType}
                            /{resourceSubType1}
                                /{resourceSubType2}
                                    /{resourceName}
```

Management group имеет формат `/providers/Microsoft.Management/managementGroups/{managementGroupName}` и является самым широким уровнем (источник: deep/d1-azure-role-based-access-control-scope-overview.md).

### Порядок оценки доступа

Источник описывает следующие шаги (pages/03-azure-rbac-overview.md):
1. Пользователь или service principal получает токен для Azure Resource Manager; токен содержит членство в группах, включая транзитивное.
2. Пользователь делает REST-вызов в Azure Resource Manager с токеном.
3. Resource Manager получает все role assignments и deny assignments, относящиеся к ресурсу.
4. Если применим deny assignment, доступ блокируется.
5. Определяются role assignments для пользователя и его групп.
6. Проверяется, входит ли действие в роли на этом scope. Для wildcard `*` эффективные права вычисляются как `Actions - NotActions` (для данных - `DataActions - NotDataActions`).
7. Если подходящего действия нет, доступ запрещен; иначе вычисляются conditions.
8. Доступ разрешается, только если conditions выполнены (если они есть).

Модель аддитивная: эффективные права - сумма всех role assignments. Например, Contributor на подписке и Reader на resource group дают фактически Contributor на подписке, и назначение Reader ничего не меняет (источник: pages/03-azure-rbac-overview.md).

Членство в группах транзитивно: если пользователь состоит в группе, которая входит в другую группу с role assignment, пользователь получает права из этого назначения (источник: pages/03-azure-rbac-overview.md).

### Deny assignments

Deny assignment блокирует действия для user, group, service principal или managed identity даже при наличии role assignment, который их разрешает. Deny assignment может исключать principals и не наследоваться дочерними scope (параметр `DoNotApplyToChildScopes`, по умолчанию false) (источник: deep/d2-azure-role-based-access-control-deny-assignments.md). В generally available сценариях deny assignments создаются и управляются Azure, например при указании deny settings в deployment stack. Создание customer-managed deny assignments в источнике описано как private preview (источник: deep/d2-azure-role-based-access-control-deny-assignments.md).

### Хранение данных RBAC

Role definitions, role assignments и deny assignments хранятся глобально. Удаление role assignment также удаляется глобально, и principals теряют доступ (источник: pages/03-azure-rbac-overview.md).

### Microsoft Entra ID (идентичность)

Microsoft Entra - семейство продуктов identity и network access, которое помогает реализовать стратегию Zero Trust. Ядро - Microsoft Entra ID: облачный сервис управления identity и доступом, который обеспечивает аутентификацию, enforcement политик и защиту пользователей, устройств, приложений и ресурсов. Каждая подписка Microsoft 365 или Azure уже использует Microsoft Entra ID как tenant (источник: docs/d1-azure-active-directory-fundamentals-active-directory-whatis.md, https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-whatis).

Группы, созданные в Microsoft Entra ID, используются как security principals для назначения ролей: когда роль назначена группе, все ее участники получают эту роль (источник: deep/d1-azure-role-based-access-control-role-assignments-steps.md).

### Security principals: пользователи, группы, service principals, managed identities

Источник role-assignments-steps перечисляет четыре типа (deep/d1-azure-role-based-access-control-role-assignments-steps.md):
- **User** - отдельный пользователь с профилем в Microsoft Entra ID; роли можно назначать и пользователям из других tenants (через Microsoft Entra B2B).
- **Group** - набор пользователей в Microsoft Entra ID.
- **Service principal** - учетная запись приложения или сервиса для доступа к конкретным ресурсам Azure.
- **Managed identity** - identity в Microsoft Entra ID, которым управляет Azure.

Service principal - локальное представление application object в конкретном tenant. Single-tenant приложение имеет один service principal в домашнем tenant; multi-tenant приложение требует service principal в каждом tenant, который дает согласие (источник: docs/d2-azure-active-directory-architecture-service-accounts-principal.md, https://learn.microsoft.com/en-us/azure/active-directory/architecture/service-accounts-principal). ApplicationID (ClientID) един для всех экземпляров приложения, ObjectID уникален для объекта в конкретном tenant (тот же источник).

### Managed identities

Managed identity - identity, назначаемая compute-ресурсу Azure (Virtual Machine, Virtual Machine Scale Set, Service Fabric Cluster, Azure Kubernetes cluster) или приложению на платформе, поддерживаемой Azure. После назначения identity может получить доступ к зависимым ресурсам, таким как storage account, SQL database или Cosmos DB. Managed identity заменяет secrets вроде access keys и паролей (источник: deep/d2-azure-active-directory-managed-identities-azure-resources-overview.md, https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview).

Два типа (там же):
- **System-assigned** - включается непосредственно на ресурсе; создается service principal особого типа, который живет вместе с ресурсом и удаляется при удалении ресурса. Только этот ресурс может запрашивать токены для identity. Имя service principal совпадает с именем ресурса.
- **User-assigned** - создается как отдельный ресурс Azure и может назначаться нескольким ресурсам. Service principal управляется отдельно от ресурсов, которые его используют.

Использование managed identities не стоит дополнительно (источник: там же).

### Data plane доступ к Storage через Microsoft Entra ID

Azure Storage поддерживает авторизацию запросов к данным blob через Microsoft Entra ID. Azure RBAC выдает разрешения security principal (user, group или application service principal). Microsoft Entra ID аутентифицирует principal и возвращает OAuth 2.0 token, которым авторизуется запрос к Blob service. Такая авторизация поддерживается для general-purpose и Blob storage accounts, созданных через Azure Resource Manager deployment model (источник: deep/d2-azure-storage-blobs-authorize-access-azure-active-directory.md, https://learn.microsoft.com/en-us/azure/storage/blobs/authorize-access-azure-active-directory).

Встроенные роли для blob данных (источник: docs/d2-azure-role-based-access-control-built-in-roles.md, https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles):
- **Storage Blob Data Reader** - чтение и просмотр контейнеров и blobs;
- **Storage Blob Data Contributor** - чтение, запись и удаление контейнеров и blobs;
- **Storage Blob Data Owner** - полный доступ к контейнерам и данным blob, включая назначение POSIX access control.

Azure Data Lake Storage (ADLS) сочетает Azure RBAC с POSIX-like ACL. Role assignments на уровне storage account и контейнера наследуются вниз до контейнера. ACL задаются на уровне directory и file; default ACL применяются к новым дочерним элементам, а для существующих нужно обновлять ACL рекурсивно (источник: docs/d0-azure-storage-blobs-data-lake-storage-access-control.md, https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control). ACL применяются только к principals того же tenant (там же).

## Основные понятия (glossary)

| Термин (English) | Определение |
|---|---|
| Azure RBAC | Система авторизации на базе Azure Resource Manager, которая управляет доступом к ресурсам через роли (pages/03-azure-rbac-overview.md). |
| Security principal | Объект (user, group, service principal или managed identity), которому назначается роль (deep/d1-azure-role-based-access-control-role-assignments-steps.md). |
| Role definition (role) | Коллекция разрешений: список Actions, NotActions, DataActions, NotDataActions (deep/d1-azure-role-based-access-control-role-definitions.md). |
| Role assignment | Привязка role definition к security principal на определенном scope; создание дает доступ, удаление отзывает (pages/03-azure-rbac-overview.md). |
| Scope | Набор ресурсов, к которым применяется доступ: management group, subscription, resource group или resource (deep/d1-azure-role-based-access-control-scope-overview.md). |
| Built-in role | Готовая роль, которую предоставляет Azure, например Virtual Machine Contributor (pages/03-azure-rbac-overview.md). |
| Custom role | Роль, которую создает пользователь, если встроенные роли не подходят (pages/03-azure-rbac-overview.md). |
| Actions / NotActions | Control plane действия, которые роль разрешает / исключает (deep/d1-azure-role-based-access-control-role-definitions.md). |
| DataActions / NotDataActions | Data plane действия над данными внутри объекта (там же). |
| Control plane / data plane | Управление ресурсом (Resource Manager) и доступ к его данным (pages/03-azure-rbac-overview.md). |
| Deny assignment | Назначение, которое блокирует действия даже при наличии role assignment (deep/d2-azure-role-based-access-control-deny-assignments.md). |
| Least privilege | Принцип выдачи минимально необходимых прав (deep/d2-azure-role-based-access-control-best-practices.md). |
| Privileged administrator role | Роль, дающая право управлять доступом, например Owner (deep/d1-azure-role-based-access-control-role-assignments-steps.md). |
| Job function role | Роль, которая управляет конкретными ресурсами, например Virtual Machine Contributor (там же). |
| Microsoft Entra ID | Облачный сервис identity и access management, источник пользователей, групп и service principals (docs/d1-azure-active-directory-fundamentals-active-directory-whatis.md). |
| Service principal | Локальное представление application object в tenant; identity приложения (docs/d2-azure-active-directory-architecture-service-accounts-principal.md). |
| Managed identity | Identity, которой управляет Azure и которую можно назначить ресурсу; заменяет секреты в коде (deep/d2-azure-active-directory-managed-identities-azure-resources-overview.md). |
| System-assigned managed identity | Identity, включенная на ресурсе и удаляемая вместе с ним (там же). |
| User-assigned managed identity | Самостоятельный ресурс-identity, назначаемый нескольким ресурсам (там же). |
| Tenant | Экземпляр Microsoft Entra ID; каждая подписка Azure использует один tenant (docs/d1-azure-active-directory-fundamentals-active-directory-whatis.md). |
| OAuth 2.0 token | Токен, которым Microsoft Entra ID авторизует запрос к данным Storage (deep/d2-azure-storage-blobs-authorize-access-azure-active-directory.md). |
| POSIX ACL | Список прав на уровне directory и file в ADLS, дополняющий Azure RBAC (docs/d0-azure-storage-blobs-data-lake-storage-access-control.md). |

## Как работает / типовые сценарии

**Сценарий 1. Назначение минимальной роли на уровне ресурса.** Если principal должен читать blobs, но не записывать, выбирается Storage Blob Data Reader, а не Storage Blob Data Contributor и тем более не Storage Blob Data Owner (deep/d1-azure-role-based-access-control-role-assignments-steps.md). Scope можно сузить до конкретного контейнера, например `.../storageAccounts/{name}/blobServices/default/containers/{container}` (deep/d2-azure-role-based-access-control-role-assignments-cli.md).

**Сценарий 2. Наследование и аддитивность.** Роль на subscription наследуется всеми resource group и ресурсами внутри. Назначения складываются, поэтому более узкое назначение не ограничивает более широкое (pages/03-azure-rbac-overview.md).

**Сценарий 3. Группы вместо пользователей.** Рекомендуется назначать роли группам, а не отдельным пользователям, чтобы упростить управление и не расходовать лимит назначений (deep/d2-azure-role-based-access-control-best-practices.md).

**Сценарий 4. Приложение с managed identity.** Managed identity назначается ресурсу (например, Function App), затем ей выдается роль на нужном scope. Пример из источника: GitHub Actions workflow получает роль Website Contributor на Function App через managed identity (deep/d2-azure-azure-functions-functions-how-to-github-actions.md). Для доступа к blob-данным роль Storage Blob Data Reader назначается identity на scope над blob пакета (deep/d2-azure-azure-functions-deployment-zip-push.md).

**Сценарий 5. Диагностика отказа.** Доступ проверяется по шагам из раздела "Порядок оценки доступа" выше. Первое, что проверяется, - deny assignments и наличие роли с нужным действием на нужном scope (pages/03-azure-rbac-overview.md).

**Сценарий 6. Лимиты.** При превышении лимита назначений рекомендуется заменить назначения пользователям назначениями группам (deep/d2-azure-role-based-access-control-troubleshoot-limits.md).

## Практика (steps, commands, code only from sources)

**Шаг 1. Выбрать роль.** Начать со списка built-in ролей, найти категорию сервиса (например, storage) и выбрать самую узкую роль. Если подходящей нет, создать custom role (deep/d1-azure-role-based-access-control-role-assignments-steps.md).

**Шаг 2. Определить scope.** Для resource scope можно открыть ресурс в портале и посмотреть Resource ID либо назначить роль временно и вывести назначение через CLI или PowerShell, где scope указан как свойство (deep/d1-azure-role-based-access-control-scope-overview.md).

**Шаг 3. Назначить роль через Azure CLI.** Источник (deep/d2-azure-role-based-access-control-role-assignments-cli.md, https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-cli):

Формат на уровне resource group:

```
az role assignment create --assignee "{assignee}" \
--role "{roleNameOrId}" \
--scope "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}"
```

Формат на уровне management group:

```
az role assignment create --assignee "{assignee}" \
--role "{roleNameOrId}" \
--scope "/providers/Microsoft.Management/managementGroups/{managementGroupName}"
```

Пример назначения Storage Blob Data Contributor service principal на уровне storage account:

```
az role assignment create --assignee "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb" \
--role "Storage Blob Data Contributor" \
--scope "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/Example-Storage-rg/providers/Microsoft.Storage/storageAccounts/storage12345"
```

Пример назначения на уровне контейнера:

```
az role assignment create --assignee "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb" \
--role "Storage Blob Data Contributor" \
--scope "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/Example-Storage-rg/providers/Microsoft.Storage/storageAccounts/storage12345/blobServices/default/containers/blob-container-01"
```

**Шаг 4. Назначить роль managed identity.** Из материала по GitHub Actions (deep/d2-azure-azure-functions-functions-how-to-github-actions.md, https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-github-actions):

```
IDENTITY_PRINCIPAL=$(az identity show --name myGitHubDeployIdentity --resource-group <RESOURCE_GROUP> --query 'principalId' -o tsv)
az role assignment create --assignee $IDENTITY_PRINCIPAL --role "Website Contributor" --scope $FUNCTION_APP_ID
```

Замените `<APP_NAME>` и `<RESOURCE_GROUP>` на имена приложения и resource group (там же).

**Шаг 5. Проверить лимит назначений.** Количество назначений в подписке можно получить через портал (вкладка Access control (IAM)) или PowerShell (источник: deep/d2-azure-role-based-access-control-troubleshoot-limits.md):

```
$scope = "/subscriptions/<subscriptionId>"
$ras = Get-AzRoleAssignment -Scope $scope | Where-Object {$_.scope.StartsWith($scope)}
$ras.Count
```

**Шаг 6. Назначать по ID роли в скриптах.** Имя роли может измениться, а ID остается прежним, поэтому в автоматизации рекомендуется использовать role ID (deep/d2-azure-role-based-access-control-best-practices.md).

## Безопасность и стоимость

**Стоимость.** Azure RBAC бесплатна и входит в подписку Azure (pages/03-azure-rbac-overview.md). Managed identities не имеют дополнительной стоимости (deep/d2-azure-active-directory-managed-identities-azure-resources-overview.md).

**Лимиты.**
- Azure RBAC: до 5000 role assignments на подписку; лимит включает назначения на уровнях subscription, resource group и resource, но не management group. Eligible и запланированные в будущем назначения в лимит не входят. Лимит фиксированный и не увеличивается (deep/d2-azure-role-based-access-control-troubleshoot-limits.md).
- Azure RBAC: до 500 role assignments на management group (там же).
- В документе по ADLS указан лимит "4000 Azure role assignments in a subscription" (docs/d0-azure-storage-blobs-data-lake-storage-access-control.md). Это расходится с 5000 из troubleshoot-документа; для проверки актуального значения стоит опираться на официальную страницу Troubleshoot Azure RBAC limits.
- ACL: 32 ACL entries (effectively 28) на файл и на директорию; access и default ACL имеют собственные лимиты по 32 записи (docs/d0-azure-storage-blobs-data-lake-storage-access-control.md).

**Рекомендации по безопасности** (источник: deep/d2-azure-role-based-access-control-best-practices.md):
- Выдавать только необходимый доступ; не назначать широкие роли на широких scope.
- Не более трех subscription owners (рекомендация, отслеживаемая в Microsoft Defender for Cloud).
- Удалять лишние privileged role assignments; если нужна привилегированная роль, использовать узкий scope.
- Для ролей, которые могут назначать роли, добавлять condition.
- Использовать Microsoft Entra Privileged Identity Management (PIM) для just-in-time доступа с ограничением по времени.
- При создании custom roles явно указывать `Actions` и `DataActions`, а не wildcard `*`.
- Использовать managed identities вместо секретов: "Managed identity replaces secrets such as access keys or passwords" (deep/d2-azure-active-directory-managed-identities-azure-resources-overview.md).
- Для SAS рекомендуется user delegation SAS, защищенный учетными данными Microsoft Entra (deep/d2-azure-storage-blobs-authorize-access-azure-active-directory.md).

**Важно про удаление.** Удаление role assignment удаляется глобально, и principal теряет доступ (pages/03-azure-rbac-overview.md).

**Ограничения материалов.** Подробности о ценах Microsoft Entra ID (тарифные планы) и детальный список всех built-in ролей в загруженных материалах отсутствуют; в документе использованы только встречающиеся в источниках роли.

## Частые вопросы для собеседования

**1. Из чего состоит role assignment в Azure RBAC?**
Из трех элементов: security principal (user, group, service principal или managed identity), role definition (набор разрешений) и scope (management group, subscription, resource group или resource) (pages/03-azure-rbac-overview.md).

**2. Как работает наследование scope и складываются ли роли?**
Scope образует иерархию parent-child, и роли, назначенные на более высоком уровне, наследуются нижними уровнями. Модель аддитивная: эффективные права равны сумме назначений. Например, Contributor на подписке и Reader на resource group дают эффективно Contributor на подписке (pages/03-azure-rbac-overview.md, deep/d1-azure-role-based-access-control-scope-overview.md).

**3. Чем отличается role assignment от deny assignment?**
Role assignment выдает доступ и может создаваться напрямую. Deny assignment блокирует действия, может исключать principals и не наследоваться дочерними scope; в generally available сценариях создается Azure, например через deployment stacks (deep/d2-azure-role-based-access-control-deny-assignments.md).

**4. Как вычисляются эффективные права при wildcard в роли?**
Если Actions содержат `*`, эффективные права вычисляются как `Actions - NotActions`, а для данных как `DataActions - NotDataActions`. Так работает Contributor: `*` минус действия по управлению доступом (pages/03-azure-rbac-overview.md, deep/d1-azure-role-based-access-control-role-definitions.md).

**5. В чем разница между системной и пользовательской managed identity?**
System-assigned создается на ресурсе, живет вместе с ним, удаляется при удалении ресурса и может использоваться только этим ресурсом. User-assigned - отдельный ресурс, назначаемый нескольким ресурсам, с управлением жизненным циклом отдельно от них (deep/d2-azure-active-directory-managed-identities-azure-resources-overview.md).

**6. Почему рекомендуется назначать роли группам, а не пользователям?**
Группы упрощают управление и уменьшают количество role assignments, которое ограничено на подписку (deep/d2-azure-role-based-access-control-best-practices.md, deep/d2-azure-role-based-access-control-troubleshoot-limits.md).

**7. Какую роль выбрать, чтобы дать только чтение blobs?**
Storage Blob Data Reader: она позволяет читать и перечислять контейнеры и blobs. Storage Blob Data Contributor добавляет запись и удаление, а Storage Blob Data Owner дает полный доступ, включая POSIX ACL (deep/d1-azure-role-based-access-control-role-assignments-steps.md, docs/d2-azure-role-based-access-control-built-in-roles.md).

**8. Что такое service principal и чем он отличается от application?**
Application и service principal - два представления приложения в Microsoft Entra ID. ApplicationID (ClientID) един для всех экземпляров, а service principal создается в каждом tenant, где приложение используется, и задает права приложения в этом tenant (docs/d2-azure-active-directory-architecture-service-accounts-principal.md).

## Источники

Использованные файлы (относительно C:\...\azure-course):
- pages/03-azure-rbac-overview.md - https://learn.microsoft.com/en-us/azure/role-based-access-control/overview
- deep/d1-azure-role-based-access-control-role-definitions.md - https://learn.microsoft.com/en-us/azure/role-based-access-control/role-definitions
- deep/d1-azure-role-based-access-control-scope-overview.md - https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview
- deep/d1-azure-role-based-access-control-role-assignments-steps.md - https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps
- deep/d2-azure-role-based-access-control-best-practices.md - https://learn.microsoft.com/en-us/azure/role-based-access-control/best-practices
- deep/d2-azure-role-based-access-control-deny-assignments.md - https://learn.microsoft.com/en-us/azure/role-based-access-control/deny-assignments
- deep/d2-azure-role-based-access-control-troubleshoot-limits.md - https://learn.microsoft.com/en-us/azure/role-based-access-control/troubleshoot-limits
- deep/d2-azure-role-based-access-control-role-assignments-cli.md - https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-cli
- docs/d2-azure-role-based-access-control-built-in-roles.md - https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles
- deep/d2-azure-active-directory-managed-identities-azure-resources-overview.md - https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview
- docs/d2-azure-active-directory-architecture-service-accounts-principal.md - https://learn.microsoft.com/en-us/azure/active-directory/architecture/service-accounts-principal
- docs/d1-azure-active-directory-fundamentals-active-directory-whatis.md - https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-whatis
- deep/d2-azure-storage-blobs-authorize-access-azure-active-directory.md - https://learn.microsoft.com/en-us/azure/storage/blobs/authorize-access-azure-active-directory
- docs/d0-azure-storage-blobs-data-lake-storage-access-control.md - https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control
- deep/d2-azure-azure-functions-functions-how-to-github-actions.md - https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-github-actions
- deep/d2-azure-azure-functions-deployment-zip-push.md - упоминание роли Storage Blob Data Reader для доступа к blob пакета (URL см. заголовок файла)

Пропущено: deep/d1-azure-synapse-analytics-quickstart-create-workspace.md и другие материалы по сервисам (Synapse, Data Factory, Stream Analytics) - упоминают назначение ролей и managed identity, но не являются основным источником по RBAC; deep/*media*.md и *.png - изображения без текста.
