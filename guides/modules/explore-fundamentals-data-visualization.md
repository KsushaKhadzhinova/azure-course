# Основы моделирования данных и визуализации в Power BI

**Источник:** https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-data-visualization/

## Цель модуля

Изучить основные принципы аналитического моделирования данных и визуализации, используя Microsoft Power BI, и создать интерактивный отчет в Power BI Desktop.

## Ключевые понятия

- **Power BI** - набор инструментов и сервисов, основная нагрузка Microsoft Fabric для создания интерактивных визуализаций.
- **Power BI Desktop** - приложение Windows для импорта данных, создания модели и отчетов.
- **Power BI service** - облачный сервис для публикации отчетов, расписаний обновления и совместного доступа.
- **Semantic model (семантическая модель)** - модель с мерами, связями и иерархиями, на которой строятся отчеты; может использоваться в нескольких отчетах.
- **Measure и dimension** - measure это числовое значение для анализа (например, выручка), dimension это сущность для группировки и фильтрации (например, продукт, клиент, время).
- **Таблицы фактов и измерений** - факты хранят события с числовыми значениями, измерения - атрибуты для группировки. Схема звезды (star schema) связывает факты с измерениями; снежинка (snowflake) добавляет дополнительные таблицы детализации.
- **Иерархия (hierarchy)** - уровни для детализации (drill up / drill down), например год - месяц - день.
- **Direct Lake** - режим хранения, который загружает Delta-таблицы из OneLake в память без копирования в модель; обновление выполняется как легкая операция framing.
- **Copilot и AI-функции** - помощь в суммаризации отчетов, создании страниц и написании DAX; Narrative, Key influencers, Decomposition tree.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-data-visualization/1-introduction

Моделирование данных и визуализация лежат в основе BI-нагрузок и поддерживают отчетность и принятие решений. Модуль использует Power BI для демонстрации принципов.

### 2. Инструменты и процесс работы Power BI
URL: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-data-visualization/2-power-bi

Типичный процесс: создание модели и отчетов в Power BI Desktop, публикация в Power BI service, где отчеты используются, обновляются по расписанию и распространяются. Power BI интегрирован в Microsoft Fabric: рабочие пространства (workspaces), семантические модели, режим Direct Lake, веб-редактирование отчетов. Copilot требует рабочей области на платной емкости Fabric (F2 или выше), Power BI Premium (P1 или выше) или Fabric Copilot capacity. Narrative Visual генерирует текстовую сводку и без лицензии Copilot; режим Copilot у него требует лицензии.

### 3. Основные концепции моделирования данных
URL: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-data-visualization/3-data-modeling

Аналитическая модель (семантическая модель в Fabric и Power BI) строится из связанных таблиц и определяет меры и измерения. Таблицы измерений содержат уникальный ключ и атрибуты, обычно есть таблица времени. Таблицы фактов содержат события. Импортированные данные (Import mode) хранятся в колоночном in-memory хранилище VertiPaq. Иерархии позволяют детализировать агрегаты. В Power BI модель настраивается в представлении Model view: связи, иерархии, типы данных и форматы. Для данных в OneLake используется Direct Lake.

### 4. Соображения по визуализации данных
URL: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-data-visualization/4-data-visualizations

Перечислены распространенные визуализации: таблицы и текст (карточки для ключевых показателей), столбчатые и линейчатые диаграммы (сравнение категорий), линейные графики (тренды, часто во времени), круговые диаграммы (доли от целого), точечные диаграммы (связь двух мер), карты (сравнение по географии). Интерактивность: выбор элемента в одной визуализации фильтрует связанные. AI-функции: Smart narratives, Copilot (рекомендуемая замена визуала Q&A, который будет выведен из эксплуатации в феврале 2027 года), Key influencers и Decomposition tree.

### 5. Упражнение: изучение основ визуализации данных в Power BI
URL: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-data-visualization/5-exercise-power-bi

Практика; нужен компьютер с Microsoft Windows.

### 6. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-data-visualization/6-knowledge-check

Тест модуля с выбором лучшего ответа. Вопросы в источнике не приведены.

### 7. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-data-visualization/7-summary

Моделирование и визуализация помогают извлекать инсайты. Модуль учит описывать процесс создания отчетов в Power BI, принципы моделирования, типы визуализаций и создание интерактивного отчета в Power BI Desktop. Следующий шаг в источнике - сертификация Azure Data Fundamentals.

## Важные команды / код / настройки

В источнике нет команд или кода. Настройки, упомянутые в тексте:

- Лицензирование Copilot: рабочая область на Fabric capacity F2 или выше, Power BI Premium P1 или выше, либо Fabric Copilot capacity.
- Режимы хранения модели: Import (данные в VertiPaq) и Direct Lake (Delta-таблицы в OneLake).
- Представление Model view в Power BI Desktop: создание связей, иерархий, задание типов данных и форматов.

## Что запомнить

- Power BI Desktop создает модель и отчеты, Power BI service публикует и распространяет их.
- Семантическая модель содержит меры (что считаем) и измерения (по чему группируем).
- Схема звезды: таблицы фактов связаны с таблицами измерений; снежинка добавляет детализирующие таблицы.
- Выбирайте тип визуализации по задаче: сравнение категорий - столбцы, тренд - линия, доля - круговая диаграмма, связь двух мер - точечная.
- Direct Lake позволяет работать с Delta-таблицами в OneLake без копирования данных в модель.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/explore-fundamentals-data-visualization/
- Сертификация Azure Data Fundamentals (упомянута в источнике, URL не приведен)
