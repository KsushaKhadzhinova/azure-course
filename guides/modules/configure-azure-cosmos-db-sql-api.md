# Настройка пропускной способности Azure Cosmos DB для SQL API

**Источник:** https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/

## Цель модуля

Сравнить модели предоставления пропускной способности в Azure Cosmos DB (serverless, standard/manual provisioned, autoscale) и научиться выполнять миграцию между standard и autoscale throughput в соответствии с характером нагрузки.

## Ключевые понятия

- **Request Units (RU/s)** - единица измерения стоимости и пропускной способности операций в Cosmos DB.
- **Serverless** - потребительская модель: оплата за запросы, без предварительного выделения RU/s; подходит для разработки, тестов и непредсказуемого трафика.
- **Provisioned throughput** - заранее выделенное количество RU/s на контейнер; подходит для предсказуемой нагрузки с минимальным разбросом производительности.
- **Standard (manual) throughput** - фиксированное значение RU/s, которое задаёт команда.
- **Autoscale throughput** - задаётся только максимум RU/s; система масштабирует пропускную способность в реальном времени; минимальная оплата - 10 % от максимума при нулевой нагрузке.
- **Rate limiting** - при превышении RU/s сервис возвращает ответ с рекомендацией подождать и повторить запрос.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/1-introduction

Модуль описывает, что разные приложения имеют разный профиль нагрузки (предсказуемый или со всплесками), и Cosmos DB предлагает разные способы размещения нагрузки. Цели: сравнить варианты сервиса и пропускной способности и выполнить миграцию между standard и autoscale.

### 2. Serverless
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/2-serverless

Serverless - модель потребления, в которой каждый запрос расходует RU, без предварительного выделения. Сценарии: новое приложение с трудно прогнозируемой нагрузкой, прототипы, интеграция с Azure Functions, знакомство с Cosmos DB, приложения с низкой нагрузкой.

### 3. Сравнение serverless и provisioned throughput
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/3-compare-serverless-provisioned-throughput

- Provisioned подходит для предсказуемого трафика; serverless - для резких скачков и низкого соотношения среднего и пикового трафика.
- Provisioned распространяется на неограниченное число регионов; serverless работает только в одном регионе (можно использовать Availability Zones).
- Provisioned допускает неограниченный объём данных в контейнере; serverless - до 1 ТБ в контейнере.
- Аккаунт serverless можно мигрировать на autoscale, и наоборот.

### 4. Autoscale throughput
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/4-autoscale-throughput

Autoscale задаёт диапазон RU/s, и контейнер масштабируется автоматически и мгновенно по фактическому использованию. Подходит для переменного и непредсказуемого трафика и снижает неиспользуемую мощность.

### 5. Сравнение autoscale и standard throughput
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/5-compare-autoscale-standard-throughput

- Standard подходит для стабильной нагрузки; рекомендуется, когда полный объём RU/s используется более чем в 66 % часов в месяц.
- Autoscale подходит для непредсказуемой нагрузки; рекомендуется, если максимум используется менее чем в 66 % часов в месяц.
- Standard: статичный RU/s; запросы сверх лимита ограничиваются (rate limiting). Autoscale: растёт до максимума RU/s, и только затем начинается ограничение запросов.
- Autoscale: задаётся только максимум; минимальная оплата - 10 % от максимума.

### 6. Миграция между standard и autoscale throughput
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/6-migrate-standard-autoscale-throughput

Существующие контейнеры мигрируются в autoscale и обратно через портал Azure, Azure CLI или Azure PowerShell. Во время миграции система автоматически назначает контейнеру значение RU/s, которое затем можно изменить.

### 7. Практика: настройка throughput в портале Azure
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/7-exercise-configure-throughput-for-azure-portal

Упражнение (около 15 минут) выполняется в лабораторной среде: создать группу ресурсов, подготовить локальное окружение, включить провайдеры ресурсов Azure. Подробные шаги в исходных материалах не приведены (указано лишь «запустите упражнение и следуйте инструкциям»).

### 8. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/8-knowledge-check

В исходных материалах вопросы не приведены.

### 9. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/9-summary

Serverless, autoscale и standard provisioning покрывают разные профили нагрузки; сравнение моделей и миграция между autoscale и standard - ключевые навыки модуля.

## Важные команды / код / настройки

В уроках модуля команды и код не приведены. Настройки и пороги из уроков:
- Serverless: до 1 ТБ данных в контейнере; один регион.
- Autoscale: минимальная оплата 10 % от максимума RU/s.
- Выбор standard: полный объём RU/s используется более чем в 66 % часов в месяц; выбор autoscale: менее чем в 66 %.
- Миграция: портал Azure, Azure CLI, Azure PowerShell.

## Что запомнить

- Serverless подходит для разработки, тестов и непредсказуемых всплесков нагрузки, но ограничен одним регионом и 1 ТБ на контейнер.
- Provisioned throughput подходит для предсказуемой нагрузки и поддерживает глобальное распределение данных.
- Standard (manual) выгоден при стабильном использовании более 66 % часов в месяц; иначе выгоднее autoscale.
- Autoscale задаёт только максимум RU/s, минимальная оплата - 10 % от максимума.
- Контейнер можно мигрировать между standard и autoscale через портал, CLI или PowerShell, а serverless - в autoscale и обратно.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/configure-azure-cosmos-db-sql-api/
- Create Azure Cosmos containers with autoscale throughput; Introduction to provisioned throughput in Azure Cosmos DB; Azure Cosmos DB serverless; How to choose between standard (manual) and autoscale provisioned throughput; How to choose between provisioned throughput and serverless (ссылки из урока 9)
