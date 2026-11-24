# Реляционные данные и предложения Azure

**Источник:** https://learn.microsoft.com/en-us/training/modules/explore-relational-data-offerings/

## Цель модуля

Понять характеристики реляционных баз данных: как моделировать сущности в таблицах, зачем нужна нормализация, какие группы операторов SQL существуют и какие объекты базы данных (представления, хранимые процедуры, индексы) используются для организации и ускорения работы с данными.

## Ключевые понятия

- **Таблица (table)** — модель коллекции сущностей; строка — один экземпляр сущности, столбец — атрибут определенного типа данных.
- **NULL** — отсутствие значения в столбце; столбцы с `NOT NULL` обязательны.
- **Первичный ключ (primary key)** — уникальный идентификатор строки.
- **Внешний ключ (foreign key)** — ссылка на первичный ключ связанной таблицы; RDBMS обеспечивает ссылочную целостность.
- **Составной ключ (composite key)** — ключ из нескольких столбцов, например OrderNo и ItemNo.
- **Нормализация** — проектирование схемы, которое минимизирует дублирование данных и обеспечивает целостность.
- **SQL и диалекты** — стандартный язык работы с реляционными БД; Transact-SQL (T-SQL), PL/pgSQL и PL/SQL — диалекты разных систем.
- **DDL, DCL, DML** — группы операторов SQL: определение данных, управление доступом и манипулирование данными.
- **Представление (view), хранимая процедура (stored procedure), индекс (index)** — объекты базы данных.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/explore-relational-data-offerings/1-introduction

Введение: реляционная модель стандартизировала представление и запросы данных, что позволило приложениям работать с общей структурой. Реляционные БД применяются для учета запасов, e-commerce и хранения критичных данных клиентов.

### 2. Understand relational data
https://learn.microsoft.com/en-us/training/modules/explore-relational-data-offerings/2-understand-relational-data

Сущности моделируются таблицами, строки соответствуют экземплярам, столбцы имеют типы данных (текст, decimal, integer, date/time). Типы зависят от СУБД, но стандартные ANSI-типы поддерживаются большинством систем. Столбец может допускать NULL.

### 3. Understand normalization
https://learn.microsoft.com/en-us/training/modules/explore-relational-data-offerings/3-normalization

Практическое определение нормализации: каждая сущность в отдельной таблице, каждый атрибут в отдельном столбце, уникальный первичный ключ и внешние ключи для связей. Пример: таблица продаж с дублирующимися данными клиентов и товаров разбивается на таблицы клиентов, товаров, заказов и строк заказа. Изменение адреса клиента теперь требует правки одной строки.

### 4. Explore SQL
https://learn.microsoft.com/en-us/training/modules/explore-relational-data-offerings/4-query-with-sql

SQL — язык запросов реляционных СУБД (SQL Server, Azure SQL Database, Azure SQL Managed Instance, MySQL, PostgreSQL, Oracle и др.). Группы операторов: DDL (CREATE, ALTER, DROP, RENAME), DCL (GRANT, DENY, REVOKE), DML (SELECT, INSERT, UPDATE, DELETE). Примеры запросов в модуле написаны на T-SQL. Предупреждения: DROP удаляет объект безвозвратно; UPDATE и DELETE без WHERE затрагивают все строки.

### 5. Describe database objects
https://learn.microsoft.com/en-us/training/modules/explore-relational-data-offerings/5-database-objects

Представление — виртуальная таблица на основе SELECT, которую можно фильтровать как таблицу. Хранимая процедура — набор SQL-операторов с параметрами, вызываемый по команде. Индекс ускоряет поиск по столбцу, но занимает место и замедляет вставку, обновление и удаление; для маленьких таблиц оптимизатор может его не использовать.

### 6. Module assessment
https://learn.microsoft.com/en-us/training/modules/explore-relational-data-offerings/6-knowledge-check

Проверочный тест (около 3 минут). Вопросы и ответы в источнике не приведены.

### 7. Summary
https://learn.microsoft.com/en-us/training/modules/explore-relational-data-offerings/7-summary

Итоги: реляционные БД хранят данные в связанных таблицах; SQL используется для запросов и изменения данных; представления, хранимые процедуры и индексы расширяют базу. Рекомендуемый следующий шаг — сертификация Azure Data Fundamentals.

## Важные команды / код / настройки

**Создание таблицы (DDL):**

```
CREATE TABLE Product
(
    ID INT PRIMARY KEY,
    Name VARCHAR(20) NOT NULL,
    Price DECIMAL NULL
);
```

**Права доступа (DCL):**

```
GRANT SELECT, INSERT, UPDATE
ON Product
TO user1;
```

**Выборка и изменение данных (DML):**

```
SELECT *
FROM Customer
WHERE City = 'Seattle';

SELECT FirstName, LastName, Address, City
FROM Customer
WHERE City = 'Seattle'
ORDER BY LastName;

SELECT o.OrderNo, o.OrderDate, c.Address, c.City
FROM [Order] AS o
JOIN Customer AS c
ON o.Customer = c.ID;

UPDATE Customer
SET Address = '123 High St.'
WHERE ID = 1;

DELETE FROM Product
WHERE ID = 162;

INSERT INTO Product(ID, Name, Price)
VALUES (99, 'Drill', 4.99);
```

**Представление:**

```
CREATE VIEW Deliveries
AS
SELECT o.OrderNo, o.OrderDate,
       c.FirstName, c.LastName, c.Address, c.City
FROM [Order] AS o JOIN Customer AS c
ON o.Customer = c.ID;
```

**Хранимая процедура:**

```
CREATE PROCEDURE RenameProduct
    @ProductID INT,
    @NewName VARCHAR(20)
AS
UPDATE Product
SET Name = @NewName
WHERE ID = @ProductID;

EXEC RenameProduct 201, 'Spanner';
```

**Индекс:** `CREATE INDEX idx_ProductName ON Product(Name);`

**Предупреждения из источника:** команда DROP удаляет объект вместе со строками без возможности восстановления без резервной копии; без WHERE команды UPDATE и DELETE затрагивают всю таблицу.

## Что запомнить

- Строка таблицы — экземпляр сущности, столбец — атрибут; каждый атрибут имеет тип данных.
- Нормализация убирает дублирование данных: сущности разносятся по таблицам и связываются через первичные и внешние ключи.
- DDL определяет структуру, DCL управляет правами, DML работает со строками (SELECT, INSERT, UPDATE, DELETE).
- Всегда используйте WHERE в UPDATE и DELETE, иначе изменения затронут все строки.
- Индексы ускоряют чтение, но увеличивают стоимость записи и занимают место, поэтому их число нужно сбалансировать.

## Связанные материалы

- Query and modify data with Transact-SQL (учебный путь Microsoft Learn; упоминается в уроке 4).
- Azure Data Fundamentals (сертификация, упоминается в уроке 7).
- Microsoft Copilot in Azure для Azure SQL Database, генерирующий T-SQL (упоминается в уроке 4).
