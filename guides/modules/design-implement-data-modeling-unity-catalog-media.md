# Проектирование и реализация моделирования данных в Unity Catalog (медиафайлы модуля)

**Источник:** https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/

## Цель модуля

По названию модуля и его структуре: проектирование и реализация моделирования данных в Unity Catalog (выбор способа приема данных, форматов файлов, партиционирования, моделей измерений и гранулярности таблиц фактов).

## Ключевые понятия

Исходные уроки этого модуля содержат только изображения (файлы .png), а текст уроков в источнике отсутствует. Поэтому понятия ниже перечислены только по названиям изображений, без пояснений из содержимого:

- **Требования и проектирование (requirements-driven design framework)** - основа проектирования, по названию урока 2.
- **Способы извлечения данных (extraction types)** - full, incremental, streaming.
- **Инструменты приема данных (ingestion tool landscape)** - Auto Loader, COPY INTO, Azure Data Factory, Lakeflow Connect.
- **Форматы файлов и табличные форматы** - структура файлов Parquet и Iceberg.
- **Партиционирование (partitioning)** - когда оно применимо и каких ошибок избегать.
- **Медленно меняющиеся измерения (SCD)** - типы 0 и 1 и сравнение с temporal tables (SCD Type 2).
- **Гранулярность таблиц фактов (granularity)** - что она означает и как применяется.
- **Пропуск данных (data skipping)** - основы механизма, по названию урока 11.

## Содержание по урокам

Для каждого урока в источнике указан только файл-изображение. Текстового содержания нет.

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/1-introduction
Текстовое содержание в исходных данных отсутствует (файл урока не сохранен как текст).

### 2. Проектирование для извлечения данных
Изображения: https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/media/2-apply-requirements-driven-design-framework.png, .../media/2-design-for-change-data-capture.png, .../media/2-identify-source-file-type-characteristics.png, .../media/2-understand-extraction-types-full.png, .../media/2-understand-extraction-types-streaming.png (вариант incremental сохранен без текста).

### 3. Инструменты приема данных
Изображения: https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/media/3-auto-loader.png, .../media/3-azure-data-factory.png, .../media/3-copy-into.png, .../media/3-decision-framework.png, .../media/3-lakeflow-connect.png, .../media/3-understand-ingestion-tool-landscape.png.

### 4. Форматы файлов и табличные форматы
Изображения: https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/media/4-file-formats-versus-table-formats.png, .../media/4-iceberg-layout.png, .../media/4-parquet-file-layout.png.

### 5. Партиционирование
Изображения: https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/media/5-avoid-common-partition-mistakes.png, .../media/5-determine-when-partitioning-applies.png.

### 6. Медленно меняющиеся измерения
Изображения: https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/media/6-slowly-changing-dimension-type-0.png, .../media/6-slowly-changing-dimension-type-1.png. Урок 8 (temporal tables versus SCD Type 2) сохранен без текста.

### 7. Таблицы фактов и гранулярность
Изображения: https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/media/9-apply-granularity-fact-tables.png, .../media/9-understand-what-granularity-represents.png.

### 8. Пропуск данных (data skipping)
Изображение: https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/media/11-understand-data-skipping-fundamentals.png.

### 9. Критерии выбора
Изображение: https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/media/10-evaluate-decision-criteria.png.

## Важные команды / код / настройки

В исходных материалах текстового кода, команд и настроек нет (только изображения), поэтому раздел пуст.

## Что запомнить

- Исходные уроки модуля представлены только изображениями без текста; полное содержание нужно открыть по ссылкам модуля.
- Темы модуля: выбор способа приема данных (Auto Loader, COPY INTO, Azure Data Factory, Lakeflow Connect), форматы файлов и таблиц (Parquet, Iceberg), партиционирование, SCD, гранулярность фактов, пропуск данных.
- Урок по пропуску данных (data skipping) и критериям выбора также представлен только изображениями.
- Для проверки содержания откройте страницы уроков по адресам модуля в браузере.
- Не полагайтесь на этот конспект как на полный материал: здесь нет фактов сверх названий уроков.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/design-implement-data-modeling-unity-catalog/
