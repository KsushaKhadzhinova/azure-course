# Расширенная безопасность вычислительных ресурсов Azure

**Источник:** https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/

## Цель модуля

Научиться планировать и внедрять расширенные меры безопасности для вычислительных ресурсов Azure: защищённый удалённый доступ к VM (Azure Bastion, JIT), изоляцию и мониторинг AKS, аутентификацию в AKS через workload identity и Microsoft Entra ID, безопасность контейнеров (ACI, ACA, ACR), шифрование дисков (ADE, encryption at host, confidential disk encryption) и рекомендации по безопасности Azure API Management.

## Ключевые понятия

- **Azure Bastion** - управляемый PaaS-сервис, который даёт RDP/SSH-доступ к VM через портал или нативный клиент без публичного IP на VM.
- **Just-in-time (JIT) VM access** - доступ к VM ограничен по времени, что уменьшает поверхность атаки.
- **AKS (Azure Kubernetes Service)** - управляемый Kubernetes; control plane создаётся и обслуживается Azure бесплатно, оплачиваются только узлы.
- **Изоляция в AKS** - логическая (namespace, RBAC, network policies) и физическая (отдельные кластеры) изоляция команд и нагрузок.
- **Microsoft Entra ID в AKS** - централизованное управление идентичностями; группы Entra привязываются к ролям Kubernetes через bindings.
- **Workload identity** - аутентификация подов в ресурсы Azure через OIDC-федерацию и service account без хранения секретов.
- **Microsoft Defender for Containers** - защита контейнеров по пяти доменам: управление состоянием безопасности, уязвимости, threat protection во время выполнения, защита цепочки поставок ПО, развёртывание и мониторинг.
- **Azure Container Registry (ACR) RBAC** - набор встроенных ролей (Owner, Contributor, Reader, AcrPush, AcrPull, AcrDelete, AcrImageSigner) для доступа к реестру.
- **Azure Disk Encryption (ADE)** - шифрование дисков VM средствами BitLocker (Windows) и dm-crypt (Linux).
- **Encryption at host** - шифрование данных VM на стороне хоста.
- **Confidential disk encryption** - шифрование с аппаратной защитой для чувствительных нагрузок.
- **Envelope encryption (DEK/KEK)** - иерархия ключей: Data Encryption Key шифрует данные, Key Encryption Key (в Key Vault) шифрует DEK.
- **Azure Key Vault** - централизованное хранилище ключей, сертификатов и секретов.
- **Azure API Management security baseline** - рекомендации Microsoft Cloud Security Benchmark для API Management (сеть, идентичность, привилегии, данные, логирование, резервное копирование).

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/1-introduction

Модуль задаёт цель: спроектировать, внедрить и поддерживать меры безопасности для compute-ресурсов Azure. Перечислены учебные цели: Bastion и JIT, изоляция AKS, аутентификация AKS через workload identity и Entra ID, мониторинг ACI и ACA, доступ к ACR, шифрование дисков и рекомендации для API Management.

### 2. Удалённый доступ, Azure Bastion и JIT
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/2-remote-access-public-endpoints-include-azure-bastion

- Bastion подключается к VM по приватному IP, поэтому VM не нужен публичный IP, агент или особое клиентское ПО; RDP/SSH идёт по TLS на порту 443 (поддерживается TLS 1.2 и выше).
- Выделенные SKU (Basic, Standard, Premium) разворачиваются в VNet с подсетью `AzureBastionSubnet` минимум /26. Developer SKU - бесплатный облегчённый вариант для dev/test в выбранных регионах, без подсети AzureBastionSubnet, без пиринга VNet, с одним подключением к VM одновременно.
- Различия SKU: Standard и Premium дают native client, custom inbound port, shareable link, upload/download файлов, подключение по IP. Premium добавляет запись сессий (session recording) и private-only deployment (без публичного IP).
- Масштабирование: Basic - 2 фиксированных инстанса (40 RDP или 80 SSH сессий); Standard и Premium - от 2 до 50 инстансов (до 1000 RDP или 2000 SSH сессий при максимуме). Один инстанс поддерживает примерно 20 RDP и 40 SSH одновременных подключений.
- Записи сессий Premium хранятся в blob-контейнере аккаунта хранения (через SAS URL).

### 3. Обзор Azure Kubernetes Service
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/3-azure-kubernetes-service-overview

- AKS - управляемый Kubernetes; Azure ведёт control plane, здоровье и обслуживание.
- Azure Linux 2.0 больше не поддерживается с 30 ноября 2025; нужно перейти на Azure Linux 3. Образы узлов будут удалены, начиная с 31 марта 2026.
- Возможности: интеграция с Kubernetes RBAC и Microsoft Entra ID, workload identity, Container Insights, KEDA, cluster autoscaler, HPA, AKS Automatic, Azure Policy, разные варианты сети (Kubenet, Azure CNI), Istio-based service mesh add-on.
- Для хранения: Azure Disks (один под), Azure Files (несколько подов), Azure NetApp Files.

### 4. Изоляция сети и мультитенантность в AKS
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/4-best-practices-cluster-isolation-azure-kubernetes-service

- Namespace - логическая граница изоляции; рекомендуется логическая изоляция в одном кластере, а физическая - только когда нужна изоляция враждебных мультитенантных нагрузок.
- Планирование: resource quotas, pod disruption budgets, taints и tolerations, node selectors, affinity/anti-affinity.
- Сеть: network policies управляют трафиком подов.
- Аутентификация: RBAC, Microsoft Entra integration, workload identities, секреты в Azure Key Vault.
- Контейнеры: Pod Security Standards и Pod Security Admission, Azure Policy add-on, сканирование образов через Defender for Containers, AppArmor или Seccomp.

### 5. Безопасность и мониторинг AKS (Microsoft Defender for Containers)
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/5-microsoft-defender-containers

- Defender for Containers охватывает пять доменов: управление безопасностью (posture), уязвимости, threat protection во время выполнения, безопасность цепочки поставок ПО, развёртывание и мониторинг.
- Agentless: discovery Kubernetes, оценка уязвимостей образов и узлов, runtime container scanning (GA для AKS), инвентаризация и risk hunting в security explorer.
- Sensor-based: Azure Policy for Kubernetes контролирует запросы к API server; binary drift detection выявляет неавторизованные процессы в контейнерах.
- Vulnerability assessment работает с ACR, ECR, GAR, GCR и внешними реестрами; основан на Microsoft Defender Vulnerability Management.
- Gated deployment (GA) блокирует или аудирует развёртывание образов, нарушающих правила, через admission control.
- Алерты рантайма имеют префикс `K8S.NODE_`; оповещения действуют только для событий после включения Defender.

### 6. Аутентификация и авторизация в AKS
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/6-best-practices-authentication-authorization

- Microsoft Entra integration: роли (Roles/ClusterRoles) связываются с пользователями и группами Entra; изменения статуса пользователя или группы применяются автоматически.
- Kubernetes RBAC: минимально необходимые права на уровне кластера или namespace.
- Azure RBAC нужен на двух уровнях: доступ к ресурсу AKS в подписке (масштабирование, обновление, получение kubeconfig) и доступ к Kubernetes API (Kubernetes RBAC или интеграция Azure RBAC).
- Workload identity: OIDC-федерация, без секретов в подах и образах; токен service account проецируется в под, Azure Identity SDK обменивает его на токен Microsoft Entra. Преимущества: нет секретов, автоматическая ротация, не нужны DaemonSet и перехват IMDS (в отличие от pod-managed identity, который устарел).

### 7. Мониторинг ресурсов Azure Container Instances
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/7-monitor-container-resources-azure-container-instances

- Метрики Azure Monitor для ACI (только для Linux-контейнеров в режиме предварительной версии): CPU Usage (в милликорах), Memory Usage (в байтах), Network bytes received/transmitted per second. По умолчанию агрегируются как средние.
- Метрики доступны на уровне группы контейнеров и отдельных контейнеров; для разбивки по контейнерам используется dimension `containerName`.

### 8. Безопасность контейнеров (урок озаглавлен как Azure Container Apps)
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/8-security-considerations-azure-container-instances

Урок содержит общие рекомендации по безопасности контейнеров:
- Использовать приватный реестр (например, Azure Container Registry) и только утверждённые образы и реестры.
- Сканировать образы до публикации и в реестре; ACR интегрирован с Defender for Cloud.
- Хранить секреты в Azure Key Vault, а не в коде.
- Принцип наименьших привилегий во время выполнения, без privileged-контейнеров; allowlist файлов и исполняемых файлов; сегментация сети.
- Мониторинг через Container insights (заменил устаревшее Azure Container Monitoring Solution, которое прекращено 31 августа 2024) и аудит административного доступа через resource logs.

### 9. Управление доступом к Azure Container Registry
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/9-azure-container-registry-roles-permissions

- Встроенные роли: Owner и Contributor (полный набор, включая создание/удаление реестра и изменение политик); Reader (доступ к ARM и pull); AcrPush (push и pull); AcrPull (только pull); AcrDelete (удаление данных образов); AcrImageSigner (подпись образов).
- CI/CD: для автоматизации сборки и push рекомендуется роль AcrPush, а не Contributor.
- Узлы с контейнерами получают роль AcrPull, без Reader.
- Аутентификация: Microsoft Entra identities (рекомендуется для production), токены с областью действия на репозитории, административная учётная запись (только для тестов, в production отключить).

### 10. Шифрование дисков и данных at rest
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/10-azure-data-encryption

- Encryption at rest защищает данные на диске; многие регуляции (HIPAA, PCI, FedRAMP) требуют его.
- Envelope encryption: DEK (симметричный AES256) шифрует блоки данных, KEK (в Key Vault) шифрует DEK. Отключение KEK позволяет криптографически стереть данные.
- Для IaaS VM используется Azure Disk Encryption (Windows и Linux). Управляемые диски, снимки и образы шифруются Storage Service Encryption с ключом сервиса.
- Хранилища Azure по умолчанию используют server-side шифрование с ключами сервиса; Blob и Azure Files поддерживают RSA 2048 customer-managed keys в Key Vault; Blob, Table и Queue поддерживают client-side шифрование.
- Azure SQL Database: Transparent Data Encryption (TDE) включён по умолчанию на новых базах, поддерживает customer-managed keys; Always Encrypted - клиентское шифрование колонок.

### 11. Рекомендации по безопасности Azure API Management
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/11-azure-security-baseline-api-management

- Security baseline основан на Microsoft Cloud Security Benchmark; соответствие отслеживается в Microsoft Defender for Cloud через Azure Policy.
- Сеть: развернуть API Management в VNet (внешний или внутренний режим); при невозможности - Private Endpoint (он не сочетается с уже настроенным VNet); отключить публичный сетевой доступ; для защиты API использовать Application Gateway с WAF.
- Идентичность: Microsoft Entra ID как основной метод аутентификации для Developer Portal и OAuth 2.0 для API; отключить локальные учётные записи; managed identity для доступа к Key Vault.
- Привилегии: Azure RBAC для управления сущностями API Management; Customer Lockbox для одобрения доступа поддержки Microsoft.
- Данные: хранить секреты (named values) и сертификаты в Key Vault; TLS для данных в передаче.
- Логирование: включить resource logs (GatewayLogs, WebSocketConnectionLogs); резервное копирование через встроенную функцию backup/restore в аккаунт хранения клиента.

### 12. Оценка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/12-knowledge-check

В исходных материалах вопросы не приведены (только заголовок и инструкция выбрать лучший ответ).

### 13. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/13-summary

Сводка ключевых тезисов по всем разделам: Bastion и JIT, AKS (workload identity вместо pod-managed identity, network policies, Pod Security Standards, Azure Linux 3), Defender for Containers, Container insights, gated deployment, ACR RBAC, ADE/encryption at host/confidential disk encryption, Key Vault и конверт-шифрование, безопасность API Management.

## Важные команды / код / настройки

Команды из урока по метрикам Azure Container Instances:

```
CONTAINER_GROUP=$(az container show --resource-group <resource-group> --name <container-group> --query id --output tsv)
az monitor metrics list --resource $CONTAINER_GROUP --metric CPUUsage --output table
az monitor metrics list --resource $CONTAINER_GROUP --metric MemoryUsage --output table
az monitor metrics list --resource $CONTAINER_GROUP --metric MemoryUsage --dimension containerName --output table
```

Ключевые настройки из уроков (в виде текста, без кода):
- Подсеть Bastion: `AzureBastionSubnet`, минимум /26 (для dedicated SKU).
- Роль для CI/CD в ACR: `AcrPush`; для узлов, которые только тянут образы: `AcrPull`.
- Сеть API Management: внешний или внутренний режим VNet; в сочетании с Application Gateway (WAF) для внутреннего режима.

## Что запомнить

- Azure Bastion позволяет подключаться к VM по RDP/SSH без публичного IP на VM; Premium добавляет запись сессий и private-only deployment.
- В AKS предпочитайте workload identity (OIDC-федерация) вместо секретов и устаревшего pod-managed identity.
- Для изоляции команд в AKS сначала используйте логическую изоляцию (namespace, RBAC, network policies), а физическую - только для враждебных мультитенантных нагрузок.
- В ACR назначайте минимальные роли: AcrPush для CI/CD, AcrPull для узлов; административную учётную запись отключайте в production.
- Шифрование at rest строится на иерархии ключей DEK/KEK, KEK хранится в Azure Key Vault; ADE шифрует диски VM, encryption at host и confidential disk encryption добавляют защиту на уровне хоста и аппаратуры.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/advanced-security-compute/
- Microsoft Cloud Security Benchmark (упомянут в уроке 11)
- Azure Bastion, Azure Kubernetes Service, Azure Container Registry, Azure Key Vault, Microsoft Defender for Containers (упомянуты в уроках модуля)
