# Начало работы с Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/try-azure-cosmos-db-sql-api/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/try-azure-cosmos-db-sql-api/<юнит>`)

## Цель модуля

Освоить базовую иерархию ресурсов аккаунта Azure Cosmos DB for NoSQL и научиться создавать аккаунт, базу данных, контейнер и элементы (items).

## Ключевые понятия

- **Account (аккаунт)** — единица распределения данных, высокой доступности и безопасности; задает регионы и глобально уникальное DNS-имя для API-запросов.
- **Database (база данных)** — логическая единица управления контейнерами.
- **Container (контейнер)** — основная единица масштабирования; данные автоматически разбиваются на партиции по ключу партиционирования (partition key). Пропускная способность обычно задается на уровне контейнера, возможен также serverless-режим.
- **Item (элемент)** — JSON-документ внутри контейнера; схема не фиксирована (schema-agnostic). Операции записи над JSON-документами атомарны.
- **Stored procedures, triggers, UDF** — JavaScript-объекты, которые могут храниться в контейнере.
- **Partition key (ключ партиционирования)** — свойство документа, по значению которого распределяются элементы.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/try-azure-cosmos-db-sql-api/1-introduction
Первый шаг — создать аккаунт. Модуль показывает иерархию ресурсов NoSQL-аккаунта и способ создания аккаунта с ресурсами.

### 2. Explore resources
Источник: https://learn.microsoft.com/en-us/training/modules/try-azure-cosmos-db-sql-api/2-explore-resources
Иерархия: аккаунт, одна или несколько баз данных, один или несколько контейнеров, множество элементов. Контейнер — основная единица масштабирования; в нем можно задать indexing policy и default time-to-live. Элементы — JSON-документы; контейнеры могут хранить также JavaScript-процедуры, триггеры и UDF.

### 3. Review basic operations
Источник: https://learn.microsoft.com/en-us/training/modules/try-azure-cosmos-db-sql-api/3-review-basic-operations
Описаны базовые операции в портале Azure: создание аккаунта (сначала выбирается API, после создания его нельзя изменить; обязательные параметры — вкладка Basics: глобально уникальное имя, регион, режим емкости provisioned throughput или serverless), создание базы данных (нужно только уникальное имя в аккаунте), создание контейнера (родительская база, уникальное имя, путь к partition key, опционально provisioned throughput) и создание элементов как JSON-документов.

### 4. Exercise: Create an Azure Cosmos DB for NoSQL account
Источник: https://learn.microsoft.com/en-us/training/modules/try-azure-cosmos-db-sql-api/4-exercise-create-account
Практика (около 15 минут): создание аккаунта. Нужна подписка Azure с правами администратора; создаются группа ресурсов, локальное окружение и включаются resource providers.

### 5. Knowledge check
Источник: https://learn.microsoft.com/en-us/training/modules/try-azure-cosmos-db-sql-api/5-knowledge-check
Проверка знаний (в исходнике текст отсутствует).

### 6. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/try-azure-cosmos-db-sql-api/6-summary
Вы выполнили базовые операции: создали аккаунт NoSQL API, базу данных и контейнер, а также элементы через Data Explorer.

## Важные команды / код / настройки

Пример элемента (JSON-документа) из модуля:

```json
{
  "id": "0012D555-C7DE",
  "type": "customer",
  "fullName": "Franklin Ye",
  "title": null,
  "emailAddress": "fye@cosmic.works",
  "creationDate": "2014-02-05",
  "addresses": [
    {
      "addressLine": "1796 Westbury Drive",
      "cityStateZip": "Melton, VIC 3337 AU"
    },
    {
      "addressLine": "9505 Hargate Court",
      "cityStateZip": "Bellflower, CA 90706 US"
    }
  ],
  "password": {
    "hash": "GQF7qjEgMk=",
    "salt": "12C0F5A5"
  },
  "salesOrderCount": 2
}
```

Настройки при создании в портале: API (нельзя изменить после создания), глобально уникальное имя аккаунта, регион, режим емкости (provisioned throughput или serverless); для контейнера — родительская база, имя, путь к partition key, пропускная способность (если не serverless).

## Что запомнить

- Иерархия: аккаунт → база данных → контейнер → элементы.
- API выбирается при создании аккаунта и не может быть изменен позже.
- Контейнер — основная единица масштабирования; данные партиционируются по ключу партиционирования.
- Элемент — JSON-документ; схема не фиксирована.
- Базы данных и контейнеры создаются в Data Explorer портала, элементы создаются там же.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/try-azure-cosmos-db-sql-api/
- Документация: Quickstart: Create an Azure Cosmos account, database, container, and items from the Azure portal (упоминается в уроке 6).
- Связанные модули: Use consistency models (`use-consistency-models-azure-cosmos-db-sql-api`), Customize indexes (`customize-indexes-azure-cosmos-db-sql-api`).
