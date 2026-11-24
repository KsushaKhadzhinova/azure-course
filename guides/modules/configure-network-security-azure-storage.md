# Настройка сетевой безопасности Azure Storage

**Источник:** https://learn.microsoft.com/en-us/training/modules/configure-network-security-azure-storage/

## Цель модуля

Научиться ограничивать сетевой доступ к учётным записям хранения Azure: создавать правила брандмауэра (deny-all по умолчанию), правила виртуальной сети и IP-правила, правила экземпляров ресурсов и исключения для доверенных служб, а также внедрять приватные конечные точки (private endpoints).

## Ключевые понятия

- **Storage firewall** - брандмауэр учётной записи хранения; при настройке сетевых правил меняет поведение с allow-all на deny-all.
- **Virtual network rules (правила виртуальной сети)** - разрешают трафик из подсетей с включённой service endpoint.
- **IP network rules (IP-правила)** - разрешают трафик из диапазонов публичных IP-адресов в нотации CIDR; частные адреса RFC 1918 не поддерживаются.
- **Resource instance rules (правила экземпляров ресурсов)** - разрешают доступ конкретному ресурсу Azure (например, Azure AI Foundry или Azure Machine Learning) по его ресурсному ID и managed identity.
- **Trusted service exceptions (исключения для доверенных служб)** - разрешают доступ всем службам из списка доверенных служб Microsoft (например, Azure Backup, Azure Monitor).
- **Service endpoint (Microsoft.Storage / Microsoft.Storage.Global)** - маршрутизация трафика к хранилищу через бэкбон Azure; `Microsoft.Storage.Global` разрешает доступ к учётным записям в любом регионе.
- **Private endpoint** - сетевой интерфейс в VNet с приватным IP-адресом, связанный с конкретной службой хранения (blob, file, queue, table, dfs); позволяет полностью отключить публичный доступ.
- **Private DNS zone (например, `privatelink.blob.core.windows.net`)** - DNS-зона, которая возвращает приватный IP вместо публичного.
- **Авторизация** - отдельная проверка после сети: shared keys, shared access signatures или Microsoft Entra ID с RBAC.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/configure-network-security-azure-storage/1-introduction

Сценарий: конвейер обработки документов Contoso с Azure Functions, локальными сканерами и Azure AI Foundry. Цель - разрешить доступ только легитимным источникам, остальной трафик блокировать по умолчанию, а затем перейти на приватные конечные точки.

### 2. Сетевые средства контроля Azure Storage
Источник: https://learn.microsoft.com/en-us/training/modules/configure-network-security-azure-storage/2-describe-storage-network-security

- По умолчанию учётные записи принимают подключения из любой сети; после настройки сетевых правил включается deny-all.
- Сетевые правила действуют только на публичную конечную точку; трафик через private endpoint их обходит.
- Четыре типа правил: виртуальные сети, IP-сети, экземпляры ресурсов, исключения для доверенных служб.
- Сначала проверяется сеть; если источник не разрешён, запрос отклоняется до проверки авторизации. Затем проверяются учётные данные и права.

### 3. Правила виртуальной сети и IP-правила
Источник: https://learn.microsoft.com/en-us/training/modules/configure-network-security-azure-storage/3-configure-vnet-ip-rules

- Правила виртуальной сети требуют включить service endpoint на подсети. Доступны два типа: `Microsoft.Storage` (только учётные записи того же региона) и `Microsoft.Storage.Global` (любой регион). На подсеть можно включить только один тип.
- Для GRS и RA-GRS при региональном отказе нужен `Microsoft.Storage.Global`; в зеркальном регионе нужно заранее создать сеть и правила.
- Учётная запись поддерживает до 400 правил виртуальной сети и до 400 IP-правил.
- Включение service endpoint меняет исходный адрес трафика на частное пространство подсети: прежние IP-правила для публичного адреса перестают работать, поэтому нужно добавить правило подсети.
- IP-правила принимают только публичные адреса; /31 и /32 не поддерживаются (одиночный адрес указывается без суффикса). IP-правила не влияют на трафик из того же региона Azure.

### 4. Правила экземпляров ресурсов и доверенные службы
Источник: https://learn.microsoft.com/en-us/training/modules/configure-network-security-azure-storage/4-configure-resource-instance-rules

- Правило экземпляра ресурса задаётся типом ресурса и ресурсным ID; ресурс аутентифицируется через managed identity. Сетевой доступ даёт правило, а операции определяют роли RBAC (например, Storage Blob Data Reader или Storage Blob Data Contributor).
- Примеры типов: `Microsoft.MachineLearningServices/workspaces` (Azure Machine Learning) и `Microsoft.CognitiveServices/accounts` (Azure AI Foundry).
- Исключение для доверенных служб включает весь список служб Microsoft (Azure Backup, Azure Event Grid, Azure Monitor, Azure Synapse Analytics и др.) одной настройкой, без указания отдельных ресурсов.
- Правила экземпляров ресурсов и исключения можно комбинировать в одной учётной записи.

### 5. Приватные конечные точки для учётных записей хранения
Источник: https://learn.microsoft.com/en-us/training/modules/configure-network-security-azure-storage/5-implement-private-endpoints

- Приватная конечная точка получает приватный IP из адресного пространства VNet; для каждой службы (blob, file, queue, table, dfs) создаётся отдельная конечная точка.
- Отличия от service endpoint: у учётной записи остаётся публичный IP (для service endpoint); у private endpoint приватный IP, и публичный доступ можно отключить полностью.
- DNS: в портале Azure private DNS-зона (например, `privatelink.blob.core.windows.net`) создаётся автоматически и связывается с VNet. При использовании Azure CLI, PowerShell или Bicep DNS-зону и записи нужно создать вручную.
- После настройки можно отключить публичный сетевой доступ; клиенты извне VNet (кроме подключённых через ExpressRoute или VPN) перестают работать.
- Private endpoint нужен, если запрещён публичный доступ, для доступа по ExpressRoute private peering или VPN, для архитектуры hub-and-spoke и для стратегии defense in depth.

### 6. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/configure-network-security-azure-storage/6-knowledge-check

В исходных материалах вопросы не приведены.

### 7. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/configure-network-security-azure-storage/7-summary

Сетевая защита строится послойно: deny-all брандмауэр, правила VNet, IP-правила, правила экземпляров ресурсов, исключения для доверенных служб и приватные конечные точки. Сеть - лишь первый уровень; без правильной авторизации (SAS, shared keys, Entra ID + RBAC) защита неполна. Следующий модуль - Microsoft Defender for Storage.

## Важные команды / код / настройки

Код и команды в уроках не приведены. Настройки из уроков:
- Тип правила экземпляра ресурса Azure Machine Learning: `Microsoft.MachineLearningServices/workspaces`; Azure AI Foundry: `Microsoft.CognitiveServices/accounts`.
- Service endpoint: `Microsoft.Storage` (тот же регион) или `Microsoft.Storage.Global` (любой регион, нужен для GRS/RA-GRS).
- Имя private DNS-зоны для blob: `privatelink.blob.core.windows.net`.
- Роли для managed identity: `Storage Blob Data Reader` (чтение), `Storage Blob Data Contributor` (чтение, запись, удаление).
- Лимиты: до 400 правил виртуальной сети и до 400 IP-правил на учётную запись.

## Что запомнить

- Включение сетевых правил переводит брандмауэр в режим deny-all; разрешайте только нужные источники.
- Правила VNet требуют service endpoint; для GRS/RA-GRS используйте `Microsoft.Storage.Global`.
- IP-правила работают только с публичными адресами и не влияют на трафик из того же региона.
- Resource instance rules дают доступ конкретному ресурсу по managed identity, а RBAC определяет, что он может делать.
- Private endpoints убирают публичную конечную точку; DNS-зону `privatelink` при автоматизации нужно настроить вручную.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/configure-network-security-azure-storage/
- Следующий модуль в курсе: Implement Microsoft Defender for Storage (упомянут в уроке 7)
