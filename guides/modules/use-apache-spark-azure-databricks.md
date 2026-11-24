# Использование Apache Spark в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/

## Цель модуля

Понять архитектуру Apache Spark, создать и настроить кластер Spark в Azure Databricks, использовать Spark в ноутбуках для обработки и анализа файлов данных (чтение, трансформация, SQL-запросы, запись) и визуализировать результаты.

## Ключевые понятия

- **Apache Spark** - открытый распределенный движок обработки данных, который хранит по возможности данные в памяти (RAM) и масштабируется от ноутбука до кластеров с сотнями машин.
- **Spark Core** - основа: планирование задач, управление памятью, восстановление после сбоев.
- **Spark SQL** - работа со структурированными данными через SQL и DataFrame API.
- **Spark Structured Streaming** - обработка данных почти в реальном времени тем же DataFrame API, что и пакетная обработка.
- **MLlib** - библиотека машинного обучения; **GraphX** - вычисления на графах.
- **Driver (драйвер)** - процесс, который превращает команды в план задач.
- **Executor (исполнитель)** - рабочий процесс на машине кластера, который выполняет задачи; задачи назначает cluster manager.
- **Lazy evaluation (ленивые вычисления)** - трансформации записываются в план (DAG), а выполняются только при действии (action).
- **DAG (направленный ациклический граф)** - граф операций, который оптимизатор Spark упрощает перед выполнением.
- **Databricks Runtime** - набор версий Spark, Python, Scala и других компонентов, устанавливаемый в кластере.
- **Access mode (режим доступа)** - Standard (несколько пользователей, изоляция кода) или Dedicated (один пользователь или группа; нужен для RDD API, GPU и R).
- **Cluster architecture** - Multi-node (драйвер и воркеры) или Single-node (только драйвер).
- **Serverless compute** - вычислительный ресурс без настройки кластера, с мгновенным запуском и автомасштабированием.
- **Control plane / compute plane** - служебная часть Databricks (управляется Microsoft) и часть, где выполняются нагрузки.
- **Unity Catalog volume** - путь к файлам вида `/Volumes/<catalog>/<schema>/<volume>/<path>`; рекомендуемый способ доступа к файлам.
- **DataFrame** - неизменяемая распределенная таблица Spark; трансформации создают новый DataFrame.
- **Temporary view (временное представление)** - имя для DataFrame в каталоге Spark, которое удаляется по окончании сессии.
- **Managed table / external table** - управляемая таблица хранит данные в хранилище каталога (удаляется вместе с данными); внешняя таблица ссылается на данные во внешнем месте.
- **Genie Code (ранее Databricks Assistant)** - AI-помощник в ноутбуках для написания, объяснения и исправления кода.

## Содержание по урокам

### 1. Введение
Источник: https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/01-introduction

Данные создаются огромными объемами (соцсети, покупки, финансовые операции, датчики). Традиционный MapReduce часто был медленным, потому что интенсивно работал с диском. Apache Spark - открытая распределенная система, которая обрабатывает большие данные на множестве машин, держа по возможности данные в памяти, что делает ее быстрой и масштабируемой.

### 2. Знакомство со Spark
Источник: https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/02-understand-spark

- Spark - движок обработки данных, объединяющий пакетную обработку, потоки, SQL и машинное обучение в одной платформе.
- Языки: Python, Java, Scala, R; для Python используется PySpark. Один и тот же код можно запускать на ноутбуке и на кластере без изменений.
- Экосистема: Spark Core, Spark SQL, Structured Streaming, MLlib, GraphX.
- **Как работает Spark на примере**: данные кликстрима в Azure Data Lake Storage; фильтр за 24 часа, join с таблицей профилей, топ-5 категорий. Код PySpark в ноутбуке выполняется на драйвере, который строит план задач; cluster manager назначает задачи исполнителям; результаты собираются в DataFrame. Распределение, параллелизм и повторы задач выполняет Spark.
- **Ленивые вычисления**: трансформации (фильтрация, join, выбор столбцов) только записываются в план-DAG; оптимизатор объединяет шаги и уменьшает перемещение данных. Выполнение начинается с действия (action): сбор результатов на драйвер, запись в хранилище, подсчет строк.
- Типичные сценарии: рекомендации в видеосервисах, мониторинг транзакций в реальном времени, анализ логов веб-серверов, панели IoT, обучение моделей, ETL.
- Развертывание: локально, на кластере, в облаке (Azure Databricks, Azure Synapse Analytics, Microsoft Fabric), на Kubernetes.

### 3. Создание кластера Spark
Источник: https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/03-spark-cluster

- Кластер создается в интерфейсе рабочей области Azure Databricks. Параметры: имя; access mode (Standard или Dedicated); архитектура (Multi-node или Single-node); версия Databricks Runtime (определяет версии Spark, Python, Scala и других компонентов); тип VM для воркеров и для драйвера; минимальное и максимальное число воркеров; автомасштабирование; время простоя до автоматического завершения.
- **Access mode**: Standard - несколько пользователей одновременно, изоляция кода; Dedicated - один пользователь или группа, нужен для RDD API, GPU и поддержки R.
- **Архитектура**: Multi-node - драйвер плюс воркеры, для больших данных; Single-node - только драйвер, для небольших данных и библиотек вроде scikit-learn.
- **Как Azure управляет ресурсами**: при создании рабочей области развертывается Databricks appliance как ресурс Azure; служебные ресурсы (ВМ, виртуальная сеть, группа безопасности, учетная запись хранения) размещаются в управляемой группе ресурсов; метаданные (например, запланированные задания) хранятся в базе Azure с гео-репликацией.
- **Control plane** (веб-интерфейс и сервисы, управляемые Microsoft) и **compute plane** (где выполняются нагрузки). Classic compute работает в вашей подписке и виртуальной сети; serverless compute - полностью управляемый.
- Рекомендация модуля: для интерактивной разработки и большинства ETL использовать serverless compute (почти нулевая задержка запуска, автомасштабирование, без настройки кластера).
- Опция: прикрепить кластер к пулу простаивающих узлов для сокращения времени запуска.

### 4. Использование Spark в ноутбуках
Источник: https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/04-use-spark

- Spark используется для пакетной или потоковой обработки (ETL в автоматизированных конвейерах) и для интерактивной аналитики.
- Ноутбук состоит из ячеек с кодом или текстом (Markdown). Можно запускать ячейку, группу или весь ноутбук.
- Мультиязычность: по умолчанию часто Python, но в одном ноутбуке можно переключаться на SQL, Scala и R магическими командами `%sql`, `%scala`, `%r`, `%python`.
- Перед запуском кода ноутбук нужно прикрепить (attach) к вычислительному ресурсу (кластеру или serverless compute); его можно отсоединять и подключать заново.
- **Genie Code** (ранее Databricks Assistant): генерирует код по запросу на естественном языке, объясняет логику, исправляет ошибки, оптимизирует производительность; использует метаданные Unity Catalog (имена таблиц и столбцов). Режимы: чат с естественным языком и слеш-команды `/explain`, `/fix`, `/optimize`; в agent mode может предлагать изменения в нескольких ячейках, которые пользователь принимает или отклоняет.
- Повторно используемый код выносится в файлы (например, .py-модули) в рабочей области; ноутбуки можно запускать друг из друга (`%run` - простой способ) или как многозадачные задания.
- Встроенный интерактивный отладчик для Python-ноутбуков включается в настройках разработчика (breakpoints, пошаговое выполнение, просмотр переменных). Ноутбуки хранят историю версий, ее можно восстановить или очистить; интеграция с Git.

### 5. Работа с файлами данных через Spark
Источник: https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/05-write-spark-code

- Поддерживаемые форматы: CSV, JSON, Parquet, ORC, Avro, Delta. Есть коннекторы к файлам в рабочей области, Azure Data Lake и Blob Storage.
- Типичный процесс: 1) прочитать файл через `spark.read` с правильным форматом и путем; 2) исследовать и трансформировать DataFrame (SQL или DataFrame API); 3) записать результат в нужном формате. Для продакшена лучше явно задавать схему, а не полагаться на вывод схемы.
- **Загрузка CSV** с заголовком и выводом схемы (Python): `spark.read.load('/Volumes/my_catalog/my_schema/my_volume/products.csv', format='csv', header=True, inferSchema=True)`; `display(df.limit(10))`. Эквивалент на Scala: `spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(...)`.
- **Явная схема**: если файл без заголовка, задается `StructType` со `StructField` (ProductID - IntegerType, ProductName - StringType, Category - StringType, ListPrice - FloatType) и `header=False`.
- **Выбор и фильтрация**: `df.select("ProductID", "ListPrice")` возвращает новый DataFrame; сокращенный синтаксис `df["ProductID", "ListPrice"]`; цепочка `df.select(...).where((df["Category"]=="Mountain Bikes") | (df["Category"]=="Road Bikes"))`.
- **Группировка**: `df.select("ProductID", "Category").groupBy("Category").count()`.
- DataFrame декларативны и неизменяемы; выполнение начинается только с действия (display, collect, write).
- **Spark-каталог**: временное представление `df.createOrReplaceTempView("products")` (удаляется по окончании сессии). Постоянные таблицы: `spark.catalog.createTable` (управляемая таблица, при удалении удаляются и данные), `saveAsTable` для сохранения DataFrame, внешняя таблица с `LOCATION` (при удалении данные остаются).
- **Spark SQL API**: `spark.sql("SELECT ProductID, ProductName, ListPrice FROM products WHERE Category IN ('Mountain Bikes', 'Road Bikes')")`.
- **SQL-магия**: `%sql` с запросом `SELECT Category, COUNT(ProductID) AS ProductCount FROM products GROUP BY Category ORDER BY Category` - результат показывается таблицей автоматически.
- Путь к файлам: `/Volumes/<catalog>/<schema>/<volume>/<path>` - рекомендуемый шаблон; корень DBFS и монтирования DBFS устарели и не рекомендуются.

### 6. Визуализация данных
Источник: https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/06-visualize-data

- Результаты DataFrame и SQL-запросов по умолчанию выводятся таблицей; их можно показать как визуализацию и настроить тип диаграммы.
- Типы встроенных визуализаций: столбчатые, линейные и областные (тренды и сравнение категорий); круговые (доли целого, не для временных рядов); гистограмма (распределение); тепловая карта (две категориальные оси и цвет по числу); точечная и пузырьковая (связь чисел); коробчатая (распределения, квартили, выбросы); комбинированная; сводная таблица (pivot); специальные: когорты, счетчик, воронка, карты, облако слов.
- Встроенные графики подходят для быстрого обзора; для полного контроля оформления или уже агрегированных значений используйте графические библиотеки.
- **Matplotlib** (на основе которой построено большинство библиотек Python): данные для нее должны быть в Pandas DataFrame, поэтому используется `toPandas()`. Пример: агрегация количества товаров по категориям через `spark.sql(...)`, затем `plt.bar(...)` с настройкой заголовка, подписей, сетки и поворота подписей по оси X.
- Seaborn - альтернатива для настраиваемых графиков. Matplotlib и Seaborn могут уже быть установлены в кластере в зависимости от версии Databricks Runtime; иначе их можно добавить через библиотеки кластера.

### 7. Упражнение: Spark в Azure Databricks
Источник: https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/07-exercise-databricks-spark

Упражнение (45 минут): с помощью готового скрипта развернуть рабочую область Azure Databricks в подписке Azure, затем в ноутбуке с serverless compute загрузить, преобразовать и проанализировать файлы из Unity Catalog volume. Требуется подписка Azure с административным доступом.

### 8. Проверка знаний
Источник: https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/08-knowledge-check

Итоговый тест модуля (3 минуты). Содержимое вопросов в исходных материалах не приведено.

### 9. Итоги
Источник: https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/09-summary

Spark - ключевая технология для трансформации данных и анализа больших данных; поддержка Spark в Azure Databricks объединяет обработку больших данных в Spark с масштабной аналитикой. Модуль научил описывать архитектуру Spark, создавать и настраивать кластер, описывать сценарии использования, обрабатывать и анализировать файлы, визуализировать данные.

## Важные команды / код / настройки

- Чтение CSV с заголовком (PySpark): `df = spark.read.load('/Volumes/my_catalog/my_schema/my_volume/products.csv', format='csv', header=True, inferSchema=True)`.
- Чтение CSV с явной схемой: `spark.read.load('/Volumes/my_catalog/my_schema/my_volume/product-data.csv', format='csv', schema=productSchema, header=False)`.
- Схема: `StructType([StructField("ProductID", IntegerType()), StructField("ProductName", StringType()), StructField("Category", StringType()), StructField("ListPrice", FloatType())])`.
- Выборка столбцов: `df.select("ProductID", "ListPrice")`.
- Фильтр по категориям: `df.select("ProductName", "ListPrice").where((df["Category"]=="Mountain Bikes") | (df["Category"]=="Road Bikes"))`.
- Группировка: `df.select("ProductID", "Category").groupBy("Category").count()`.
- Временное представление: `df.createOrReplaceTempView("products")`.
- SQL из PySpark: `spark.sql("SELECT ... FROM products WHERE Category IN ('Mountain Bikes', 'Road Bikes')")`.
- Магические команды языка ячейки: `%python`, `%scala`, `%sql`, `%r`.
- Путь к файлам Unity Catalog: `/Volumes/<catalog>/<schema>/<volume>/<path>`.
- Конвертация для Matplotlib: `spark.sql(...).toPandas()`.
- Параметры кластера: access mode (Standard/Dedicated), архитектура (Multi-node/Single-node), Databricks Runtime, тип VM для воркеров и драйвера, минимум и максимум воркеров, автомасштабирование, время простоя.
- Слеш-команды Genie Code: `/explain`, `/fix`, `/optimize`.

## Что запомнить

- Spark обрабатывает данные распределенно и по возможности в памяти; код пишется как обычный DataFrame, а распределение выполняет Spark.
- Трансформации ленивые: выполнение начинается с действия (display, collect, write, count).
- Для Azure Databricks используйте serverless compute для интерактивной работы и ETL, если не нужна тонкая настройка кластера.
- Файлы в Unity Catalog volumes: путь `/Volumes/...`; явная схема надежнее вывода схемы.
- Временное представление живет в сессии, управляемая таблица удаляет данные вместе с собой, внешняя таблица оставляет данные на месте.
- Для сложной визуализации преобразуйте результат в Pandas через `toPandas()` и используйте Matplotlib или Seaborn.

## Связанные материалы

В исходных материалах модуля раздел со ссылками на дополнительные ресурсы не приведен. Упомянутые в тексте материалы: документация Azure Databricks по выбору вычислительных ресурсов (Select and configure compute in Azure Databricks), по пулам (Pool configuration reference), по ноутбукам (Notebooks), по библиотекам кластера (Cluster Libraries).
