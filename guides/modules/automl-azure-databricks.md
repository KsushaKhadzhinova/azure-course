# AutoML в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/automl-azure-databricks/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/automl-azure-databricks/<юнит>`)

## Цель модуля

Научиться использовать AutoML в Azure Databricks, чтобы автоматизировать обучение моделей: система перебирает разные алгоритмы и значения гиперпараметров и сокращает усилия, необходимые для создания эффективных решений машинного обучения.

## Ключевые понятия

- **AutoML** — функция Azure Databricks, которая автоматизирует обучение и оценку модели с разными комбинациями алгоритма и гиперпараметров.
- **Experiment run (запуск эксперимента)** — каждый запуск AutoML обучает одну модель с определенной комбинацией алгоритма и гиперпараметров; запуски отслеживаются через MLflow.
- **MLflow** — механизм, которым Azure Databricks ведет учет запусков и моделей, созданных ими, чтобы можно было найти лучшую модель и развернуть ее в продуктиве.
- **Таблица обучающих данных** — таблица в Hive metastore рабочей области, содержащая признаки (features) и целевую метку (label).
- **Target label (целевая метка)** — поле, которое модель должна предсказывать.
- **Primary metric (основная метрика)** — метрика, по которой определяется лучшая модель (например, `precision` в примере кода).
- **Типы моделей** — классификация (classification), регрессия (regression) и прогнозирование (forecasting); для кластеризации в интерфейсе также указан тип clustering.
- **Preprocessing (предобработка)** — AutoML генерирует код для типичных задач: кодирование категориальных переменных, масштабирование числовых, обработка null-значений и несбалансированных наборов данных.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/automl-azure-databricks/1-introduction
Подбор алгоритма и гиперпараметров итеративен и требует экспериментов. AutoML в Azure Databricks автоматизирует обучение и валидацию моделей и заметно снижает усилия на запуск и отслеживание экспериментов.

### 2. What is AutoML?
Источник: https://learn.microsoft.com/en-us/training/modules/automl-azure-databricks/2-what-automl
AutoML создает несколько запусков эксперимента. Вы указываете таблицу с данными и метрику для оптимизации; каждый MLflow-запуск выдает блокнот с кодом предобработки и обучением модели. Результаты сортируются по качеству, лучшую модель можно выбрать, зарегистрировать и развернуть. Данные готовятся в виде таблицы в Hive metastore (например, загрузкой файла через портал).

### 3. Use AutoML in the Azure Databricks user interface
Источник: https://learn.microsoft.com/en-us/training/modules/automl-azure-databricks/3-automl-user-interface
Эксперименты создаются и управляются через графический интерфейс портала Azure Databricks. Настройки эксперимента: кластер, тип модели, таблица с данными, целевое поле, уникальное имя эксперимента, метрика оценки, фреймворки обучения, максимальное время, положительная метка (только для бинарной классификации), временной столбец (только для прогнозирования), место сохранения моделей (MLflow artifacts или хранилище DBFS). Во время работы видны дочерние запуски, и лучшая модель показывается первой; эксперимент можно остановить, когда модель устраивает.

### 4. Use code to run an AutoML experiment
Источник: https://learn.microsoft.com/en-us/training/modules/automl-azure-databricks/4-automl-code
Для автоматизированных MLOps-процессов эксперимент запускается кодом через Python-библиотеку AutoML API с методами `classify`, `regress` или `forecast`.

### 5. Exercise - Use AutoML in Azure Databricks
Источник: https://learn.microsoft.com/en-us/training/modules/automl-azure-databricks/5-exercise-automl
Практическое задание: обучить модель классификации с помощью AutoML в Azure Databricks (около 30 минут, нужна подписка Azure с правами администратора).

### 6. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/automl-azure-databricks/6-knowledge-check
Проверка знаний по модулю (в исходнике текст отсутствует).

### 7. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/automl-azure-databricks/7-summary
AutoML сокращает время и усилия на обучение моделей. Эксперименты можно запускать интерактивно в портале или в скриптах через AutoML API, что позволяет встроить AutoML в MLOps-решение.

## Важные команды / код / настройки

Пример из модуля (запуск классификации и получение лучшей модели):

```python
from databricks import automl

# Get the training data
train_df = spark.sql("SELECT * FROM penguins")

# Configure and initiate the AutoML experiment
summary = automl.classify(train_df, target_col="Species",
                          primary_metric="precision", timeout_minutes=5)

# Get the best model
model_uri = summary.best_trial.model_path
```

## Что запомнить

- AutoML перебирает комбинации алгоритмов и гиперпараметров и обучает модель в каждом запуске.
- Входные данные — таблица в Hive metastore с признаками и целевой меткой.
- Результаты ранжируются по основной метрике; лучшую модель можно зарегистрировать и развернуть.
- Эксперимент запускается через UI портала Azure Databricks или кодом (`classify`, `regress`, `forecast`).
- Каждый запуск AutoML сопровождается блокнотом с кодом предобработки, который можно изучить.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/automl-azure-databricks/
- Документация Azure Databricks: «What is AutoML?» (упоминается в уроке 7 и уроке 2).
- Документация Azure Databricks: «How Azure Databricks AutoML works» (алгоритмы и преобразования AutoML).
- Документация Azure Databricks: «Train ML models with Azure Databricks AutoML Python API».
- Связанный модуль: MLflow в Azure Databricks (`mlflow-azure-databricks`).
