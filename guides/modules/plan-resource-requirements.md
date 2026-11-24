# Планирование ресурсов для Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/plan-resource-requirements/

## Цель модуля

Научиться оценивать требования приложения к пропускной способности (throughput) и хранению данных, а также правильно настраивать аккаунт и ресурсы Azure Cosmos DB для NoSQL под новое решение.

## Ключевые понятия

- **Request Units (RU)** - условная валюта, которая абстрагирует CPU, память и IO. Расходуется на чтение, запись (включая индексацию) и запросы, как фоновые, так и пользовательские операции.
- **RU/s** - пропускная способность, которая выделяется в единицах RU в секунду.
- **Container (контейнер)** - единица масштабируемости по throughput и хранению; данные распределяются по партициям и регионам.
- **Database (база данных)** - единица управления набором контейнеров; throughput можно выделить на уровне базы, но это подходит только при похожей нагрузке всех контейнеров.
- **Serverless** - оплата только за фактически выполненные запросы; рекомендуется для старта новых приложений и редких запросов.
- **Standard provisioned throughput** - фиксированный выделенный RU/s с SLA.
- **Autoscale provisioned throughput** - автоматически масштабируемый RU/s.
- **Dynamic Autoscale** - масштабирует только те партиции и регионы, где идут запросы, поэтому платится только потребленный throughput.
- **Capacity calculator (калькулятор емкости)** - онлайн-инструмент для оценки storage, throughput и стоимости по данным существующей нагрузки.
- **TTL (Time-to-live)** - время жизни документа в секундах от последнего изменения; по истечении документ автоматически удаляется.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/plan-resource-requirements/1-introduction

Создание аккаунта требует множества настроек. Значения по умолчанию подходят многим сценариям, но важно понимать опции, чтобы настроить аккаунт оптимально. Цель модуля - научиться готовить и настраивать аккаунт и ресурсы под новое решение и оценивать требования приложения.

### 2. Understand throughput
https://learn.microsoft.com/en-us/training/modules/plan-resource-requirements/2-understand-throughput

Иерархия: аккаунт -> база данных (единица управления) -> контейнеры (единица масштабирования). Throughput, выделенный на уровне контейнера, зарезервирован только для него и подкреплен SLA. Для новых аккаунтов рекомендуется начинать с serverless. Выделение throughput на уровне базы допустимо только при сходной нагрузке контейнеров.

### 3. Evaluate throughput requirements
https://learn.microsoft.com/en-us/training/modules/plan-resource-requirements/3-evaluate-throughput-requirements

Каждый запрос тратит фиксированное число RU. Минимумы provisioned throughput: 400 RU/s (standard) и 1000 RU/s с масштабированием до 100 RU/s (autoscale). Оценку делают по top-5 запросам и числу операций чтения и записи в секунду. Расчет RU/s лучше измерять на масштабе, а не на одной партиции; для точных данных используйте proof of concept и свойство request charge в SDK.

### 4. Evaluate data storage requirements
https://learn.microsoft.com/en-us/training/modules/plan-resource-requirements/4-evaluate-data-storage-requirements

Планирование включает два компонента: throughput и storage. Данные хранятся на SSD и оплачиваются за ГБ в месяц. Для миграции существующих транзакционных нагрузок используется Azure Cosmos DB Capacity Calculator. Он запрашивает общий объем данных, потребность в near real-time аналитике, размер документов, число point reads и запросов в секунду.

### 5. Time-to-live (TTL)
https://learn.microsoft.com/en-us/training/modules/plan-resource-requirements/5-time-to-live

TTL задается в секундах от последнего изменения. Устанавливается на уровне контейнера и может переопределяться для отдельного элемента. Удаление выполняется фоновой задачей, которая использует RU и запускается, когда система не загружена. Максимальное значение TTL - 2147483647.

### 6. Plan for data retention with time-to-live (TTL)
https://learn.microsoft.com/en-us/training/modules/plan-resource-requirements/6-plan-for-data-retention-with-time-to-live

Storage оплачивается по факту использования, предварительно резервировать его не нужно. В сценариях с интенсивной записью TTL помогает экономить на хранении: данные, уже переданные в хранилища или агрегированные, можно сразу удалить из локального SSD. Для переноса данных упоминаются change feed, Microsoft Fabric и Azure Blob Storage. Срок хранения в Cosmos DB стоит продумать заранее.

### 7. Knowledge check
https://learn.microsoft.com/en-us/training/modules/plan-resource-requirements/7-knowledge-check

Проверка знаний (около 5 минут). Текст в источнике не приведен.

### 8. Summary
https://learn.microsoft.com/en-us/training/modules/plan-resource-requirements/8-summary

Модуль связывает требования приложения с понятиями Azure Cosmos DB: throughput и storage. После модуля можно оценивать требования приложения и настраивать аккаунт Azure Cosmos DB for NoSQL.

## Важные команды / код / настройки

Оценка RU/s из источника (пример):

| Тип операции | Запросов в секунду | RU на запрос | RU/s нужно |
|---|---|---|---|
| Write Single Document | 10 000 | 10 | 100 000 |
| Top Query #1 | 700 | 100 | 70 000 |
| Top Query #2 | 200 | 100 | 20 000 |
| Top Query #3 | 100 | 100 | 10 000 |
| Итого | | | 200 000 RU/s |

Ориентиры из источника: чтение 1-КБ документа - 1 RU; запись 1-КБ документа с отключенной индексацией - 6 RU.

Настройка TTL на контейнере через свойство JSON-объекта контейнера `DefaultTimeToLive`:

| DefaultTimeToLive | Поведение |
|---|---|
| не задано | Элементы не удаляются автоматически |
| -1 | Элементы по умолчанию не истекают |
| n | Удаление через n секунд после последнего изменения |

TTL элемента задается свойством `ttl`. Оно работает только если `DefaultTimeToLive` задан у контейнера и переопределяет его значение.

| Container.DefaultTimeToLive | Item.ttl | Истечение |
|---|---|---|
| 1000 | не задан | через 1000 с |
| 1000 | -1 | никогда |
| 1000 | 2000 | через 2000 с |
| не задан | не задан | никогда |
| не задан | 2000 | TTL отключен на уровне контейнера, элемент не истекает |

## Что запомнить

- Throughput в Cosmos DB измеряется в RU/s, и каждый запрос имеет фиксированную стоимость в RU.
- Минимум provisioned throughput: 400 RU/s (standard) и 1000 RU/s с масштабированием до 100 RU/s (autoscale).
- Для новых приложений с редкими запросами рекомендуется serverless.
- Оценку RU/s делайте по top-запросам и измеряйте на масштабе через proof of concept и request charge в SDK.
- TTL на уровне контейнера удаляет устаревшие данные, а значение на элементе его переопределяет.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/plan-resource-requirements/
- В источнике упоминаются (без ссылок в тексте): Estimate RU/s using the Azure Cosmos DB capacity planner, Request Units in Azure Cosmos DB, Introduction to provisioned throughput in Azure Cosmos DB.
