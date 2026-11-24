# Стратегия моделирования и партиционирования данных в Azure Cosmos DB

**Источник:** https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/<юнит>`)

## Цель модуля

Научиться моделировать и партиционировать данные для NoSQL-базы (Azure Cosmos DB) на примере перевода реляционной модели интернет-магазина в NoSQL: денормализация, поддержка ссылочной целостности через change feed, объединение сущностей в одном контейнере и денормализация агрегатов.

## Ключевые понятия

- **Denormalization (денормализация)** — добавление в документ данных из связанных сущностей (например, названия категории и тегов), чтобы получить все нужное одним запросом; в NoSQL нет join между контейнерами.
- **Embedding (встраивание)** — хранение связанных данных внутри документа; подходит для связи «один ко многим» с небольшим числом элементов (one-to-few).
- **Partition key (ключ партиционирования)** — выбирается по операциям приложения; например, `categoryId` для запросов товаров по категории даёт запрос в одной партиции.
- **Change feed (лента изменений)** — API, встроенный в каждый контейнер; потоково передает вставки и обновления, на которые можно реагировать кодом. Используется для поддержания ссылочной целостности.
- **Referential integrity (ссылочная целостность)** — согласованность связанных данных между контейнерами, которую в NoSQL поддерживает приложение (например, через change feed).
- **Combining entities (объединение сущностей)** — хранение разных сущностей в одном контейнере при общем partition key и похожих шаблонах доступа; различаются через свойство-дискриминатор `type`.
- **Denormalized aggregates (денормализованные агрегаты)** — хранение предвычисленного значения (например, `salesOrderCount`) в документе для быстрых запросов.
- **Transactional batch (пакетная транзакция)** — набор операций в одной логической партиции, выполняемых атомарно; доступен в .NET и Java SDK. Транзакции в Azure Cosmos DB работают в пределах одной логической партиции; альтернатива — хранимые процедуры.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/1-introduction
Сценарий: стартап розничной торговли переводит модель онлайн-заказов из реляционной в NoSQL. Модуль охватывает денормализацию, ссылочную целостность через change feed, объединение сущностей и денормализацию агрегатов (с transactional batch).

### 2. Denormalize data in your model
Источник: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/2-denormalize-data-your-model
Связь товаров и тегов решено встроить в товар (one-to-few). Партиционирование товаров выполняется по `categoryId`, так как товары выводятся по категории. Чтобы вывести страницу товара одним запросом, в документ добавляются название категории и названия тегов, так как joins между контейнерами недоступны.

### 3. Manage referential integrity by using change feed
Источник: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/3-manage-referential-integrity-by-using-change-feed
Из-за денормализации нужно поддерживать согласованность master-данных (productCategory и productTag) с контейнером product. Change feed слушает изменения в контейнерах и передает их в код, который обновляет связанные документы: один change feed для productCategory и второй для productTag.

### 4. Combine multiple entities in the same container
Источник: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/4-combine-multiple-entities-same-container
Детали заказа встроены в заказ как массив, контейнер `salesOrder` партиционируется по `customerId`. Поскольку контейнеры customer и salesOrder имеют общий ключ и похожий доступ, данные объединяются в один контейнер: у клиента добавляется `customerId`, а свойство `type` (customer или salesOrder) различает документы. Каждый клиент — отдельная логическая партиция с его заказами.

### 5. Denormalize aggregates in the same container
Источник: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/5-denormalize-aggregates-same-container
Для запроса «топ-10 клиентов по числу заказов» в документ клиента добавляется свойство `salesOrderCount`. При создании заказа увеличение счетчика и вставка заказа выполняются в одной транзакции внутри одной логической партиции — через хранимые процедуры или transactional batch.

### 6. Finalize the data model
Источник: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/6-finalize-data-model
Девять реляционных таблиц превращены в четыре контейнера. Поскольку productCategory и productTag имеют общий partition key, их можно объединить в контейнер `productMeta`. Один change feed обрабатывает все сущности, маршрутизируя изменения по свойству `type`. В итоге получается три контейнера: customer (с заказами), product (с тегами) и productMeta.

### 7. Exercise advanced modeling patterns
Источник: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/7-exercise-advanced-modeling-patterns
Практика (около 25 минут): продвинутые шаблоны моделирования. Нужна подписка Azure с правами администратора; создаются группа ресурсов, локальное окружение и включаются resource providers.

### 8. Knowledge check
Источник: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/8-knowledge-check
Проверка знаний (в исходнике текст отсутствует).

### 9. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/9-summary
Подытожены денормализация, ссылочная целостность через change feed, объединение сущностей и денормализация агрегатов с transactional batch. Такая модель эффективна по compute и масштабируется при росте данных и пропускной способности.

## Важные команды / код / настройки

В исходниках нет блоков кода. Ключевые настройки из текста:

- Партиционирование товаров: `categoryId` (контейнер `product`).
- Партиционирование заказов: `customerId` (контейнер `salesOrder`, затем объединен с customer).
- Свойство-дискриминатор: `type` со значениями `customer` и `salesOrder` (и далее для reference-данных).
- Денормализованный счетчик: `salesOrderCount` в документе клиента.
- Объединенные контейнеры: `productMeta` для productCategory и productTag.

## Что запомнить

- В NoSQL нет join между контейнерами, поэтому данные денормализуют, чтобы получить их одним запросом.
- Ключ партиционирования выбирается по операциям приложения (например, `categoryId` для товаров по категории).
- Change feed поддерживает ссылочную целостность, реагируя на изменения в контейнерах.
- Сущности с общим ключом партиционирования и похожим доступом можно хранить в одном контейнере с дискриминатором `type`.
- Транзакции в Azure Cosmos DB работают только внутри одной логической партиции; для этого служат transactional batch и хранимые процедуры.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/
- Документация: Understand the differences between NoSQL and relational databases (упоминается в уроке 9).
- Документация: Data modeling in Azure Cosmos DB (упоминается в уроке 9).
- Документация: Model and partition data on Azure Cosmos DB by using a real-world example (упоминается в уроке 9).
- Документация: Change feed in Azure Cosmos DB; Transactional batch operations in Azure Cosmos DB that use the .NET SDK (упоминаются в уроке 9).
- Связанный модуль: Process Azure Cosmos DB for NoSQL change feed (`process-azure-cosmos-db-nosql-change-feed`).
