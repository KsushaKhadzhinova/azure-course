# Основные концепции данных

**Источник:** https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/

## Цель модуля

Освоить базовые понятия работы с данными: форматы данных (структурированные, полуструктурированные и неструктурированные), способы хранения в файлах и базах данных, а также характеристики транзакционной (OLTP) и аналитической (OLAP) обработки. Модуль закладывает основу для изучения сервисов Azure для работы с данными и является подготовкой к сертификации Azure Data Fundamentals.

## Ключевые понятия

- **Структурированные данные** — данные с фиксированной схемой, обычно в виде таблиц.
- **Полуструктурированные данные** — данные с частично определенной структурой, например JSON.
- **Неструктурированные данные** — документы, изображения, аудио, видео и бинарные файлы; также векторные данные (embeddings).
- **BLOB (Binary Large Object)** — файл в бинарном виде, например изображение или видео.
- **Реляционная БД** — таблицы с первичными и внешними ключами, нормализация, язык SQL.
- **Нереляционные БД (NoSQL)** — key-value, document, column family и graph.
- **OLTP** — транзакционная обработка, операции CRUD с соблюдением ACID.
- **OLAP и semantic model** — агрегированные данные для аналитики с мерами и измерениями.
- **Data lake, data warehouse, data lakehouse** — файловое хранилище, реляционное хранилище и гибрид.
- **Medallion architecture** — слои Bronze, Silver и Gold в lakehouse.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/1-introduction

Введение: данные служат ценным активом для бизнеса, поэтому нужны способы их хранения, сбора и анализа. Модуль описывает варианты представления и хранения данных и типичные рабочие нагрузки.

### 2. Identify data formats
https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/2-data-formats

Данные делятся на структурированные (фиксированная схема, таблицы), полуструктурированные (JSON, допускающий различия между экземплярами сущности) и неструктурированные (документы, изображения, аудио, видео, векторы embeddings). Хранилища делятся на файловые и базы данных.

### 3. Explore file storage
https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/3-file-storage

Форматы файлов: текст с разделителями (CSV, TSV, fixed-width), JSON, XML (устаревающий, но используемый), BLOB для бинарных данных и оптимизированные форматы Parquet (колоночный, Apache), Avro (строковый, Apache) и Delta Lake (Parquet с журналом транзакций).

### 4. Explore databases
https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/4-databases

Реляционные БД хранят данные в таблицах с первичными ключами, нормализованы и управляются SQL. Нереляционные БД (NoSQL) бывают четырех типов: key-value (ключ и значение в любом формате), document (значение — JSON-документ), column family (столбцы объединены в семейства) и graph (узлы и связи).

### 5. Explore transactional data processing
https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/5-transactional-data-processing

Транзакционные системы (OLTP) обрабатывают большой поток небольших операций CRUD. Свойства ACID: атомарность, согласованность, изолированность и долговечность. Пример: перевод $40 между счетами A и B должен выполниться как единое неделимое действие. Такие системы обслуживают line-of-business приложения.

### 6. Explore analytical data processing
https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/6-analytical-processing

Аналитическая обработка работает с историческими данными в режиме чтения. Типичная архитектура: ETL или ELT в data lake, таблицы в lakehouse или data warehouse, агрегированная semantic model (OLAP, ранее кубы) с мерами и измерениями, отчеты и дашборды. Описаны роли специалистов: data scientists, аналитики и бизнес-пользователи. Также кратко описаны Microsoft Fabric, Azure Databricks и Microsoft Purview, а также medallion architecture с уровнями Bronze, Silver и Gold.

### 7. Module assessment
https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/7-knowledge-check

Проверочный тест (около 3 минут). Вопросы и ответы в источнике не приведены.

### 8. Summary
https://learn.microsoft.com/en-us/training/modules/explore-core-data-concepts/8-summary

Итоги: распознавание форматов данных, варианты хранения в файлах и базах, характеристики транзакционной и аналитической обработки.

## Важные команды / код / настройки

В источнике есть примеры данных, но нет команд или настроек. Примеры структур:

- **JSON-документы клиентов** (урок 2): объекты с полями `firstName`, `lastName`, `address`, массив `contact` с разными типами контактов (home, email).
- **CSV** (урок 3): строка заголовка `FirstName,LastName,Email` и строки с данными.
- **XML** (урок 3): элементы `<Customers>`, `<Customer>`, `<ContactDetails>`, `<Contact>`.

Пример ACID из урока 5: перевод $40 со счета A (баланс $100) на счет B (баланс $50).

## Что запомнить

- Структурированные данные имеют фиксированную схему, полуструктурированные допускают вариации, неструктурированные не имеют заданной структуры.
- Parquet и Avro оптимизированы для хранения и обработки; Delta Lake добавляет к Parquet ACID-транзакции и версионирование.
- Реляционные БД используют ключи и SQL, NoSQL — четыре модели: key-value, document, column family и graph.
- OLTP обрабатывает много коротких транзакций с ACID-гарантиями; OLAP агрегирует исторические данные для анализа.
- Medallion architecture (Bronze, Silver, Gold) задает качественные границы в lakehouse.

## Связанные материалы

- Сертификация Azure Data Fundamentals (упоминается в уроке 8).
- Microsoft Fabric, Azure Databricks и Microsoft Purview (упоминаются в уроке 6).
