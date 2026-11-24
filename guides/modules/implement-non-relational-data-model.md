# Реализация нереляционной модели данных в Azure Cosmos DB

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/

## Цель модуля

Научиться переносить реляционную модель в нереляционную (NoSQL) модель Azure Cosmos DB for NoSQL: проектировать документы по шаблонам доступа, выбирать между встраиванием (embedding) и ссылками (referencing), подбирать партиционный ключ без горячих партиций и моделировать небольшие справочники. Сквозной пример модуля: перенос интернет-магазина из реляционной БД.

## Ключевые понятия

- **Горизонтальное масштабирование (scale-out)** — рост за счет добавления физических партиций; у реляционных БД рост обычно вертикальный.
- **Partition key (партиционный ключ)** — обязательное свойство документа, по которому Azure Cosmos DB распределяет данные.
- **Логическая партиция** — все документы с одним значением ключа; ограничение 20 ГБ на логическую партицию.
- **Физическая партиция** — единица хранения и пропускной способности; до 50 ГБ и 10 000 RU/s.
- **Hot partition** — перегруженная партиция по хранению или по запросам.
- **Cross-partition query** — запрос без фильтра по партиционному ключу, который обходит все партиции.
- **Embedding и referencing** — хранение связанных данных в одном документе или в отдельных документах.
- **Entity discriminator** — константное свойство (например, `type`), которое позволяет собрать малые справочники в одну партицию.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/1-introduction

Введение: Azure Cosmos DB — нереляционная и горизонтально масштабируемая БД; чтобы использовать масштабирование, нужно понимать моделирование и партиционирование. Сценарий: стартап розничной торговли проектирует базу онлайн-заказов по существующей ER-модели из девяти сущностей.

### 2. What's the difference between NoSQL and relational databases?
https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/2-whats-difference-between-nosql-relational-databases

Реляционные БД растут за счет более мощных машин, NoSQL — за счет добавления узлов. Данные маршрутизируются по партиционному ключу. В NoSQL нет внешних ключей и ограничений между данными. Нормализация появилась, когда память была дорогой; сегодня данные часто хранят в денормализованном виде, как их использует приложение. NoSQL подходит и для реляционных нагрузок, но техники моделирования другие.

### 3. Identify access patterns for your app
https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/3-identify-access-patterns-for-your-app

Цель модели: выполнять операции минимальным числом запросов. В Azure Cosmos DB for NoSQL документы называются items, а контейнеры — collections. Для сущностей клиента (Customer, CustomerAddress, CustomerPassword) описаны операции создания, обновления и чтения; все данные нужны сразу, поэтому они объединяются в один документ.

### 4. When to embed or reference data
https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/4-when-to-embed-reference-data

Встраивать данные, если они читаются и обновляются вместе, связаны отношением 1:1 или 1:few (ограниченное 1:N). Выносить в отдельные документы, если данные читаются или обновляются независимо, если документ большой и часто меняется частично, если связь 1:N неограниченная или N:M. Обновление в Azure Cosmos DB заменяет весь элемент целиком.

### 5. Exercise: Measure performance for customer entities
https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/5-exercise-measure-performance-for-customer-entities

Практика (около 25 минут): измерить производительность для сущностей клиентов. Нужна подписка Azure с правами администратора; шаги: создать группу ресурсов, подготовить локальную среду, включить провайдеры ресурсов.

### 6. Choose a partition key
https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/6-choose-partition-key

Логические партиции создаются по значениям ключа, физические — из них. Лимиты: физическая партиция 50 ГБ и 10 000 RU/s, логическая 20 ГБ. Горячие партиции бывают по хранению (неравномерный объем данных) и по пропускной способности (выделенные RU/s делятся между физическими партициями поровну). Для записи нужен ключ с высокой кардинальностью; для чтения — запросы с фильтром равенства по ключу или IN. Для клиентов выбран ключ `id`, так как операция чтения по ID самая частая.

### 7. Model small lookup entities
https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/7-model-small-lookup-entities

Сущности ProductCategory и ProductTag — малые справочники, связанные отношением 1:N. Чтобы запрос списка всех категорий оставался одно-партиционным, добавляется свойство `type` с константным значением (`category` для категорий и `tag` для тегов), которое служит партиционным ключом. Запрос принимает вид `SELECT * FROM c WHERE c.type = "category"`.

### 8. Knowledge check
https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/8-knowledge-check

Проверочный тест (около 5 минут). Вопросы и ответы в источнике не приведены.

### 9. Summary
https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/9-summary

Итоги: различия NoSQL и реляционных БД, шаблоны доступа, embedding против referencing, выбор партиционного ключа и моделирование справочников. Customer-сущности объединены в один документ, а категории и теги собраны в малые контейнеры с discriminator-ключом. Дополнительно: модуль Optimize your database by using advanced modeling patterns for Azure Cosmos DB.

## Важные команды / код / настройки

В источнике нет кода. Упомянутые значения и настройки:

- **Лимит физической партиции:** 50 ГБ хранения и 10 000 RU/s.
- **Лимит логической партиции:** 20 ГБ. Обход лимита: ключ с высокой кардинальностью или иерархические партиционные ключи (в источнике — отдельный учебный путь).
- **Партиционный ключ в примере:** `/username` (контейнер из иллюстрации урока 6).
- **Партиционный ключ для клиентов:** `id`.
- **Партиционный ключ для справочников:** `type` с константными значениями `category` и `tag`.
- **Запросы для малых справочников:** `SELECT * FROM c` (до модели) и `SELECT * FROM c WHERE c.type = "category"` (после модели).
- **Распределение пропускной способности:** выделенные RU/s делятся между физическими партициями равномерно (пример: 30 000 RU/s на три партиции дают по 10 000 RU/s).

## Что запомнить

- В NoSQL-модели проектируйте документы под операции приложения: данные, которые читаются вместе, храните вместе.
- Встраивайте 1:1 и ограниченные 1:N; выносите неограниченные связи, часто меняющиеся части и N:M.
- Партиционный ключ должен равномерно распределять и данные, и запросы; проверяйте его под нагрузкой.
- Запросы с фильтром по партиционному ключу выполняются в одной партиции, остальные становятся cross-partition и дорожают с ростом контейнера.
- Для малых справочников константный discriminator-ключ позволяет держать список в одной партиции.

## Связанные материалы

- Understanding the differences between NoSQL and relational databases.
- Data modeling in Azure Cosmos DB.
- How to model and partition data on Azure Cosmos DB using a real-world example.
- Partitioning and horizontal scaling in Azure Cosmos DB.
- Partitioning strategy and provisioned throughput costs.
- Модуль Optimize your database by using advanced modeling patterns for Azure Cosmos DB (упоминается в уроках 1 и 9).
