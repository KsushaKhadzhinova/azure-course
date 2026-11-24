# Загрузка данных в Azure Data Lake Storage

**Источник:** https://learn.microsoft.com/en-us/training/modules/upload-data-to-azure-data-lake-storage/

## Цель модуля

Создать хранилище Data Lake Storage Gen2 (учётная запись Azure Storage с включённым иерархическим пространством имён) и загрузить в него данные вручную с помощью Azure Storage Explorer.

## Ключевые понятия

- **Azure Data Lake Storage Gen2** - набор возможностей поверх Azure Blob Storage, включаемых параметром hierarchical namespace при создании учётной записи; отдельного типа аккаунта нет.
- **Hierarchical namespace (иерархическое пространство имён)** - структура каталогов, которая поддерживает совместимость со Spark, RBAC и POSIX-подобные ACL.
- **Standard general-purpose v2** - основной тип учётной записи для Data Lake Storage Gen2.
- **Premium block blob** - вариант для нагрузок с жёсткими требованиями к задержкам и производительности.
- **Resource group (группа ресурсов)** - контейнер для связанных ресурсов; упрощает очистку после работы.
- **File system (файловая система)** - в Data Lake Storage Gen2 это контейнер Blob Storage.
- **Azure Storage Explorer** - бесплатное приложение для Windows, macOS и Linux для работы с данными Azure Storage, включая Data Lake Storage Gen2; подходит для разовых загрузок.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/upload-data-to-azure-data-lake-storage/1-introduction

Data Lake Storage Gen2 - это возможности, построенные на Blob Storage, которые включаются выбором hierarchical namespace. Они дают поддержку аналитических фреймворков (например, Apache Spark), иерархическую структуру каталогов, модель безопасности на базе RBAC и POSIX ACL, масштабируемость по цене Blob Storage. Модуль показывает два способа загрузки: ad-hoc через Storage Explorer и интеграцию загрузки в приложения. Цели: создать хранилище Gen2 и загрузить данные через Storage Explorer.

### 2. Создание учётной записи хранения для Data Lake Storage (упражнение)
Источник: https://learn.microsoft.com/en-us/training/modules/upload-data-to-azure-data-lake-storage/2-create-azure-data-lake

Порядок действий в портале Azure:
1. Создать группу ресурсов, например `mslearn-datalake-test`, в выбранном регионе.
2. Создать ресурс Storage account, выбрать группу ресурсов и уникальное имя (3-24 символа, только цифры и строчные латинские буквы; можно начать с префикса `dlakedata`). Регион в примере - Central US.
3. На вкладке Advanced включить **Enable hierarchical namespace**.
4. Проверить и создать учётную запись.

Для существующего аккаунта Blob Storage возможен апгрейд до Data Lake Storage Gen2, но он необратим.

### 3. Загрузка данных с помощью Azure Storage Explorer (упражнение)
Источник: https://learn.microsoft.com/en-us/training/modules/upload-data-to-azure-data-lake-storage/3-upload-data-using-explorer

- Storage Explorer версии 1.42.0 и новее требует .NET 10 runtime той же архитектуры, что и установка Storage Explorer.
- Вход: View > Account Management (или кнопка Manage Accounts), Add an account, выбор подписки, Apply.
- Создание файловой системы: в учётной записи выбрать Blob Containers, создать контейнер `salesdata`.
- В контейнере создать папки `sample` и затем `data` внутри неё.
- Создать локальный файл `sales.txt` с примером данных о зарплатах (строки с датой, компанией, сотрудником и суммой; первые строки начинаются с `#`).
- Загрузка: открыть папку `data`, Upload > Upload Files, выбрать `sales.txt`, убедиться, что назначение - `sample/data`, нажать Upload.
- Скачивание: правой кнопкой по файлу > Download, выбрать место сохранения.

### 4. Заключение
Источник: https://learn.microsoft.com/en-us/training/modules/upload-data-to-azure-data-lake-storage/6-summary

Azure SDK помогают автоматизировать регулярную загрузку файлов из локальных систем в Data Lake Storage Gen2, а затем аналитика (Azure Databricks, Microsoft Fabric, Azure Synapse Analytics) работает с данными. Storage Explorer удобен для ручной работы с данными, в том числе с file shares, queues и tables. По завершении нужно удалить группу ресурсов `mslearn-datalake-test`, чтобы не платить за ресурсы.

## Важные команды / код / настройки

Код и CLI-команды в уроках не приведены. Настройки из уроков:
- Тип учётной записи: Standard general-purpose v2 (или Premium block blob).
- Вкладка Advanced > Data Lake Storage > **Enable hierarchical namespace** = включено.
- Имя учётной записи: 3-24 символа, только цифры и строчные буквы, уникальное в Azure.
- Контейнер для примера: `salesdata`; путь загрузки: `sample/data`.
- Минимальная версия Storage Explorer для нового .NET: 1.42.0 требует .NET 10 runtime.

Пример содержимого `sales.txt` из урока:

```
#salaries Details
#Company Information
#Fields : Date company employee Salaries
01-01-2019  c1   e1 1000
01-01-2019  c2   e2 2000
01-01-2019  c1   e3 4000
01-01-2019  c2   e4 2000
01-01-2019  c1   e5 5000
01-01-2019  c3   e6 7000
```

## Что запомнить

- Data Lake Storage Gen2 - это не отдельный сервис, а включаемая возможность Storage-аккаунта с иерархическим пространством имён.
- Иерархическое пространство имён включается при создании аккаунта; апгрейд существующего аккаунта необратим.
- Файловая система Data Lake Storage Gen2 - это контейнер Blob Storage.
- Storage Explorer подходит для разовых загрузок и скачиваний; для регулярной загрузки используйте SDK или автоматизацию.
- После практики удалите группу ресурсов, чтобы не платить за ресурсы.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/upload-data-to-azure-data-lake-storage/
- Storage Explorer; Azure Databricks, Microsoft Fabric и Azure Synapse Analytics (упомянуты в уроке 6 как потребители данных)
