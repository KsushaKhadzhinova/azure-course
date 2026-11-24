# Защита ресурсов Azure с помощью RBAC

**Источник:** https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/<юнит>`)

## Цель модуля

Научиться управлять доступом к ресурсам Azure с помощью Azure RBAC: проверять доступ для себя и других, назначать роли на нужном уровне (scope) и просматривать activity log изменений RBAC.

## Ключевые понятия

- **Azure RBAC** — система авторизации на базе Azure Resource Manager; определяет, кто может что делать и где.
- **Security principal (кто)** — пользователь, группа, приложение, service principal или managed identity.
- **Role definition (что)** — набор разрешений (Actions, NotActions, DataActions, NotDataActions); например Owner, Contributor, Reader, User Access Administrator.
- **Scope (где)** — уровень действия роли: management group, subscription, resource group или отдельный ресурс.
- **Role assignment (назначение роли)** — связка «кто + что + где»; чтобы предоставить доступ, создают назначение, чтобы отозвать — удаляют.
- **Наследование** — назначение на родительском scope распространяется на дочерние; наследование не добавляет разрешений роли.
- **Аддитивная модель** — назначения суммируются; NotActions не является запретом (запрет дает только deny assignment).
- **Microsoft Entra roles** — управление каталогом (пользователи, группы, приложения); отделено от доступа к ресурсам Azure.
- **PIM (Privileged Identity Management)** — eligible и time-bound назначения, требующие активации.
- **Activity Log** — журнал операций подписки; хранит события 90 дней.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/1-introduction
Сценарий компании First Up Consultants, которая перенесла нагрузки в Azure. Цели модуля: проверять доступ, назначать доступ, просматривать activity log изменений Azure RBAC.

### 2. What is Azure RBAC?
Источник: https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/2-rbac-overview
Подписка связана с одним клиентом Microsoft Entra; членство в каталоге само по себе не дает доступа к ресурсам. Отключение локальной учетной записи не гарантирует мгновенного прекращения доступа в облаке: токены и сессии могут действовать некоторое время. Роли: Owner (полный доступ, включая делегирование), Contributor (управление ресурсами без выдачи доступа), Reader (просмотр), User Access Administrator (управление доступом). Глобальный администратор Microsoft Entra не получает доступ к ресурсам Azure автоматически. Для полного администрирования подписки и делегирования назначают Owner на уровне подписки; для узких задач — подходящую роль (например, Role Based Access Control Administrator) на минимально достаточном scope. Contributor не может выдавать доступ: исключены, в частности, Microsoft.Authorization/*/Write и */Delete. Развертывания рекомендуется описывать в Bicep или ARM; для управления набором ресурсов — deployment stacks, для хранения и версий шаблонов — template specs.

### 3. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/3-knowledge-check-rbac-overview
Проверка знаний (в исходнике текст отсутствует).

### 4. Exercise - List access using Azure RBAC and the Azure portal
Источник: https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/4-list-access
Практика (около 8 минут): посмотреть свои разрешения через меню профиля (My permissions) и назначения на группе ресурсов через Access control (IAM) → Role assignments. Назначения, унаследованные от родительского scope, помечаются как (Inherited). Для просмотра назначений нужно право `Microsoft.Authorization/roleAssignments/read` (например, роль Reader на нужном scope). Вкладка Roles показывает встроенные и пользовательские роли.

### 5. Exercise - Grant access using Azure RBAC and the Azure portal
Источник: https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/5-grant-access
Практика (около 8 минут): назначить роль Virtual Machine Contributor пользователю на уровне группы ресурсов по принципу наименьших привилегий. Роль не дает управления виртуальной сетью и учетной записью хранения, которые использует VM. Для назначения нужны `Microsoft.Authorization/roleAssignments/write` и `.../delete` (например, через Role Based Access Control Administrator). В портале: Access control (IAM) → Add → Add role assignment → Role → Members → (при наличии) Assignment type → Review + assign. Проверка — через Check access. Изменения могут применяться до 10 минут; при необходимости выйти и войти снова. Удаление касается только созданного назначения; унаследованные назначения управляются на том scope, где созданы.

### 6. Exercise - View activity logs for Azure RBAC changes
Источник: https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/6-view-activity-logs
Практика (около 4 минут): отчет за прошлый календарный месяц по операциям назначения и удаления ролей (`Microsoft.Authorization/roleAssignments/write` и `/delete`) и по записи и удалению пользовательских определений ролей (`roleDefinitions/write` и `/delete`). Для чтения журнала подписки нужна роль, например Monitoring Reader на уровне подписки. Записи содержат статус, отметку времени, вызывающего и scope; неуспешные операции не являются завершенными изменениями. Журнал появляется с задержкой 3–20 минут. Экспорт в CSV содержит совпавшие записи, а не только успешные изменения; для отчета о завершенных изменениях фильтруйте статус `Succeeded`. Activity log хранится 90 дней; для более длительного хранения настраивается diagnostic setting (Log Analytics или Storage). Журнал не показывает текущие назначения — для инвентаризации используйте Download role assignments. Журнал активности не покрывает PIM полностью; аудит PIM и Microsoft Entra audit logs (хранятся 30 дней с P1/P2) настраивается отдельно.

### 7. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/7-knowledge-check-rbac
Проверка знаний (в исходнике текст отсутствует).

### 8. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/8-summary
Чтобы выдать доступ, назначают пользователю роль на определенном scope; так предоставляется ровно тот объем доступа, который нужен для работы. Azure RBAC содержит более 200 встроенных ролей; при необходимости создаются пользовательские роли. Azure отслеживает изменения RBAC, что позволяет восстановить историю. Список справочных материалов содержит документацию по ролям, PIM, журналам активности и процедурам отзыва доступа.

## Важные команды / код / настройки

В исходниках приведены только шаги портала и названия операций; блоков кода нет.

Операции Activity Log для отчета:

- Create role assignment — `Microsoft.Authorization/roleAssignments/write`
- Delete role assignment — `Microsoft.Authorization/roleAssignments/delete`
- Create or update custom role definition — `Microsoft.Authorization/roleDefinitions/write`
- Delete custom role definition — `Microsoft.Authorization/roleDefinitions/delete`

Путь в портале для назначения роли: Resource groups → группа ресурсов → Access control (IAM) → Role assignments → Add → Add role assignment → Role (Job function roles) → Virtual Machine Contributor → Members → Select members → Review + assign.

Разрешения, упомянутые в модуле:

- `Microsoft.Authorization/roleAssignments/read` — просмотр назначений.
- `Microsoft.Authorization/roleAssignments/write` и `/delete` — создание и удаление назначений.
- Monitoring Reader на уровне подписки — чтение activity log.

Ограничения и сроки:

- Activity log хранится 90 дней; события появляются с задержкой около 3–20 минут.
- Изменения назначений RBAC могут применяться до 10 минут.
- Назначения PIM нельзя удалить в первые 5 минут после создания.
- Microsoft Entra audit logs хранятся 30 дней с лицензией P1 или P2.

## Что запомнить

- Назначение роли = кто + что + где; доступ выдается назначением, отзывается удалением назначения.
- Наследование идет от родительского scope к дочернему; оно не добавляет разрешений роли.
- Azure RBAC — модель allow: назначения суммируются; NotActions не запрещает, запрет дает только deny assignment.
- Для минимальных привилегий назначайте роль на минимально нужном scope (например, Virtual Machine Contributor на группе ресурсов).
- Activity log хранит 90 дней; для долгого хранения настройте diagnostic setting; для текущего состава назначений используйте Download role assignments.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/
- Документация: What is Azure role-based access control (Azure RBAC)?; Azure and Microsoft Entra role models; Understand Azure role definitions; Azure built-in role catalog (упоминаются в уроке 8).
- Документация: Check access and activate an eligible role; Remove Azure role assignments in the portal; Troubleshoot Azure RBAC (упоминаются в уроке 8).
- Документация: View activity logs for Azure RBAC changes; Azure Activity Log retention and export (упоминаются в уроке 8).
- Документация: Azure resource role assignment in PIM; View audit report for Azure resource roles in PIM (упоминаются в уроке 8).
- Документация: User access revocation procedure; Deployment stacks; Template specs (упоминаются в уроке 8).
- Связанный модуль: Configure storage security (`configure-storage-security`).
