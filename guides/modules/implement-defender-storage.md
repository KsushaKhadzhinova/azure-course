# Внедрение Microsoft Defender for Storage

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-defender-storage/

## Цель модуля

Научиться включать Microsoft Defender for Storage на уровне подписки и ресурса, настраивать сканирование вредоносных файлов с лимитами стоимости, обнаружение угроз для чувствительных данных, маршрутизацию оповещений и проверять покрытие защитой.

## Ключевые понятия

- **Microsoft Defender for Storage** - сервис обнаружения угроз для Azure Storage (Blob, Files, Data Lake Storage Gen2); работает без агентов на уровне сервиса хранения.
- **Activity monitoring (мониторинг активности)** - анализ операций data plane и control plane, выявление подозрительного доступа, в том числе по SAS-токенам; использует Microsoft Threat Intelligence. Включен всегда.
- **Malware scanning (сканирование на вредоносное ПО)** - проверка содержимого файлов через Microsoft Defender Antivirus; платная функция с тарификацией за ГБ.
- **Sensitive data threat detection (обнаружение угроз для чувствительных данных)** - обогащает оповещения метками классификации из Microsoft Purview.
- **Classic plan и new plan** - классический план (оплата за транзакции, только hash reputation) и новый план (оплата за аккаунт, полное сканирование как дополнение).
- **SAS token (токен подписанного доступа)** - доступ без идентичности пользователя или сервисного принципала; именно такие сценарии отслеживает activity monitoring.
- **Scan result tag (тег результата сканирования)** - blob index tag, который записывается в blob после сканирования.
- **Monthly cap (месячный лимит)** - ограничение объема сканирования в ГБ на аккаунт в месяц.
- **Scanning filters (фильтры сканирования)** - исключения по контейнеру, префиксу пути, суффиксу имени или размеру (до 24 критериев на аккаунт).
- **Storage Center** - представление в портале Azure с состоянием защиты аккаунтов (Protected, Partly protected, Not protected); в источнике указано, что стало доступно в целом в апреле 2026 года.
- **Suppression rules (правила подавления)** - скрывают ожидаемое поведение, чтобы оно не создавало оповещений.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/implement-defender-storage/1-introduction

Сценарий: компания Contoso принимает файлы от партнеров для AI-обработки. Вредоносный файл с валидным SAS-токеном прошел сетевые правила и политики доступа. Defender for Storage добавляет слой, который проверяет содержимое и анализирует доступ независимо от способа его выдачи. Цели модуля: три направления обнаружения, включение защиты через политику, настройка сканирования с лимитами, чувствительные данные, маршрутизация оповещений.

### 2. Explore Microsoft Defender for Storage capabilities
https://learn.microsoft.com/en-us/training/modules/implement-defender-storage/2-explore-defender-storage-capabilities

Три взаимодополняющих направления: мониторинг активности (логи data и control plane, в том числе SAS-токены и гео-аномалии), сканирование вредоносного ПО (содержимое загружаемых файлов), обнаружение угроз для чувствительных данных (действия над классифицированными ресурсами). Новый план использует покупку за аккаунт и полное сканирование, классический - за транзакции и только hash reputation. Агентов не требуется.

### 3. Enable and deploy Defender for Storage
https://learn.microsoft.com/en-us/training/modules/implement-defender-storage/3-enable-deploy-defender-storage

Два уровня включения: подписка (защищает все аккаунты, включая новые) и ресурс (отдельные аккаунты; новые аккаунты не защищаются автоматически). Рекомендуемый способ - Azure Policy с встроенным определением "Configure Microsoft Defender for Storage to be enabled" (эффект deployIfNotExists), назначаемое на уровне группы управления. Ресурсный уровень переопределяет настройки подписки. Покрытие проверяется в Storage Center.

### 4. Configure malware scanning and sensitive data detection
https://learn.microsoft.com/en-us/training/modules/implement-defender-storage/4-configure-malware-scanning-sensitive-data

Два режима: on-upload (при создании, перезаписи или переименовании blob, а также при фиксации через PutBlockList или FlushWithClose) и on-demand (ретроспективное сканирование без месячного лимита). Результаты записываются в теги. Ограничения: blob больше 50 ГБ, blob в архивном уровне и blob с ключами, предоставленными клиентом, не сканируются. Лимит по умолчанию 10 000 ГБ в месяц; оповещения при 75% и 100%. Настраиваются фильтры сканирования. Sensitive data detection работает с Microsoft Purview без новых типов оповещений.

### 5. Configure alert routing and validate Defender coverage
https://learn.microsoft.com/en-us/training/modules/implement-defender-storage/5-configure-alert-routing-validate-coverage

Маршруты оповещений: email-уведомления из Defender for Cloud (Environment settings, Email notifications), Microsoft Sentinel через коннектор Defender for Cloud (для новых развертываний рекомендуется tenant-based коннектор, в статусе preview), правила подавления (Alerts, Suppression rules; правило должно быть узким). Проверка: Storage Center, тестовый файл и тег результата сканирования, образцы оповещений (Sample alerts).

### 6. Knowledge check
https://learn.microsoft.com/en-us/training/modules/implement-defender-storage/6-knowledge-check

Проверка знаний (около 3 минут). Текст вопросов в источнике не приведен.

### 7. Summary
https://learn.microsoft.com/en-us/training/modules/implement-defender-storage/7-summary

Итог сценария: три направления защиты (мониторинг активности, сканирование, чувствительные данные), развертывание через Azure Policy с переопределениями для отдельных аккаунтов, маршрутизация в email и Sentinel, правила подавления и проверка Storage Center. Защита - непрерывный процесс: проверяйте отчеты Azure Policy и Storage Center, следите за лимитами сканирования.

## Важные команды / код / настройки

В источнике команд CLI нет (упомянуты PowerShell, Azure CLI и REST API без примеров). Ниже параметры из текста:

**Уровни включения:**
- Subscription: все аккаунты подписки, новые аккаунты защищаются автоматически.
- Resource: отдельные аккаунты; при наличии обеих настроек приоритет у ресурсного уровня.

**Azure Policy:** встроенное определение "Configure Microsoft Defender for Storage to be enabled"; эффект `deployIfNotExists`; назначение на уровне группы управления; параметры: мониторинг активности (всегда включен), сканирование на вредоносное ПО (настраивается), обнаружение угроз для чувствительных данных (настраивается), месячный лимит сканирования.

**Сканирование:**
- Лимит по умолчанию: 10 000 ГБ в месяц на аккаунт (только для on-upload).
- Оповещение при достижении 75% лимита и при 100% (после этого сканирование останавливается до конца месяца).
- Blob больше 50 ГБ получают результат `Not scanned`.
- Не сканируются blob в архивном уровне и blob с ключами, предоставленными клиентом.
- Фильтры: до 24 критериев на аккаунт (контейнер или префикс пути, суффикс имени, размер).

**Теги результата сканирования:**
- `Malware scanning scan result` - значения: `No threats found`, `Malicious`, `Error`, `Not scanned`.
- `Malware scanning scan time (UTC)`.

**Пример лимитов из сценария источника (не являются рекомендацией):** внешние партнеры 25 000 ГБ; внутренние выходы 10 000 ГБ (по умолчанию); ML-данные 5 000 ГБ; временные артефакты сборки - сканирование отключено.

**Маршрутизация:** Defender for Cloud > Environment settings > Email notifications; Microsoft Sentinel > Data connectors > Microsoft Defender for Cloud (tenant-based, Preview; subscription-based - Legacy); Defender for Cloud > Alerts > Suppression rules; Defender for Cloud > Alerts > Sample alerts.

## Что запомнить

- Мониторинг активности включен всегда и видит злоупотребление SAS-токенами, даже если сетевые правила разрешили доступ.
- Для непрерывного покрытия назначайте Azure Policy на уровне группы управления: новые подписки защищаются автоматически.
- Сканирование на вредоносное ПО - платная функция с месячным лимитом (по умолчанию 10 000 ГБ) и ограничениями: blob больше 50 ГБ, архивный уровень и клиентские ключи не сканируются.
- Проверяйте тег `Malware scanning scan result` перед обработкой загруженного файла.
- Правила подавления должны быть узкими, иначе они скроют реальные угрозы.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/implement-defender-storage/
- В источнике упоминаются (без ссылок в тексте): Microsoft Defender Antivirus; Microsoft Purview sensitive data discovery; Microsoft Sentinel; Microsoft Threat Intelligence; Microsoft Entra ID; Azure Monitor; Azure Firewall. Также упоминается, что модуль входит в learning path из трех модулей (account hardening, network and access controls, Defender for Storage).
