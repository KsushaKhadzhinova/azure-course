# Мониторинг и устранение неполадок в решении Azure Cosmos DB для NoSQL

**Источник** https://learn.microsoft.com/en-us/training/paths/monitor-troubleshoot-azure-cosmos-db-sql-api-solution

## О курсе

Административные задачи Azure Cosmos DB: мониторинг, метрики производительности, резервное копирование и безопасность.

- **Уровень:** средний (Intermediate)
- **Роль:** Developer
- **Продукты и сервисы:** Azure Cosmos DB, Azure Monitor
- **Предварительные требования:** Опыт создания облачных приложений на Microsoft C# или аналогичном языке программирования.

## Чему научитесь

- Azure Monitor для создания и анализа данных мониторинга Azure Cosmos DB.
- Коды ответов REST, которые возвращает Azure Cosmos DB.
- Две модели резервного копирования Azure Cosmos DB.
- Модели безопасности Azure Cosmos DB.

## Модули

1. **Измерение производительности Azure Cosmos DB (SQL API) с Azure Monitor**. Научиться использовать Azure Monitor для наблюдения за Azure Cosmos DB: измерять пропускную способность (Total Request Units), обнаруживать события ограничения скорости (429), анализировать логи через диагностические настройки и запросы KQL. [guide](../modules/measure-performance-azure-cosmos-db-sql-api.md)
2. **Мониторинг ответов и событий Azure Cosmos DB (SQL API)**. Научиться отслеживать состояние запросов к Azure Cosmos DB for NoSQL по HTTP-кодам ответов: распознавать частые коды, диагностировать транзитные ошибки (503 и сетевые таймауты) и ограничение скорости (429), настраивать алерты Azure Monitor и аудировать безопасность аккаунта. [guide](../modules/monitor-responses-events-azure-cosmos-db-sql-api.md)
3. **Резервное копирование и восстановление Azure Cosmos DB (SQL API)**. Научиться понимать варианты резервного копирования и восстановления Azure Cosmos DB, оценивать периодическое резервное копирование (periodic backup), настраивать непрерывное резервное копирование (continuous backup) и выполнять восстановление на момент времени (point-in-time recovery). [guide](../modules/implement-backup-restore-for-azure-cosmos-db-sql-api.md)
4. **Безопасность Azure Cosmos DB (SQL API)**. Настроить сетевой контроль доступа, рассмотреть варианты шифрования данных, использовать RBAC (роли Azure и встроенные роли данных), подключаться с Microsoft Entra ID и понять Always Encrypted. [guide](../modules/implement-security-azure-cosmos-db-sql-api.md)

## Ключевые технологии и понятия

- Azure Monitor
- Metrics (метрики)
- Diagnostic logs (диагностические логи)
- Diagnostic setting (диагностическая настройка)
- Total Request Units
- 429 (Request rate too large)
- Hot partition (горячая партиция)
- Log Analytics / KQL (Kusto Query Language)
- AzureDiagnostics vs resource-specific tables
- Метрики
- Диагностические логи
- Портал Azure Cosmos DB
- NoSQL SDK и REST API
- Большая частота запросов

## Для каких ролей полезно

- Developer (разработчик)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/monitor-troubleshoot-azure-cosmos-db-sql-api-solution
- Модуль «Измерение производительности Azure Cosmos DB (SQL API) с Azure Monitor»: https://learn.microsoft.com/en-us/training/modules/measure-performance-azure-cosmos-db-sql-api/
- Модуль «Мониторинг ответов и событий Azure Cosmos DB (SQL API)»: https://learn.microsoft.com/en-us/training/modules/monitor-responses-events-azure-cosmos-db-sql-api/
- Модуль «Резервное копирование и восстановление Azure Cosmos DB (SQL API)»: https://learn.microsoft.com/en-us/training/modules/implement-backup-restore-for-azure-cosmos-db-sql-api/
- Модуль «Безопасность Azure Cosmos DB (SQL API)»: https://learn.microsoft.com/en-us/training/modules/implement-security-azure-cosmos-db-sql-api/
