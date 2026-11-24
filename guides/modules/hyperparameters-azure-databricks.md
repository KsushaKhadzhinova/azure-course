# Подбор гиперпараметров с Optuna в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/hyperparameters-azure-databricks/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/hyperparameters-azure-databricks/<юнит>`)

## Цель модуля

Научиться систематически подбирать гиперпараметры моделей машинного обучения с помощью библиотеки Optuna в Azure Databricks, отслеживать испытания (trials) через MLflow и масштабировать оптимизацию на кластер Spark.

## Ключевые понятия

- **Hyperparameter (гиперпараметр)** — настройка процесса обучения, которая задается до обучения и не выводится из данных (например, regularization rate в логистической регрессии или learning rate в нейросетях). Значения, выученные из данных, называются parameters.
- **Hyperparameter tuning (подбор гиперпараметров)** — систематическая проверка комбинаций значений для поиска лучшей конфигурации.
- **Optuna** — открытая Python-библиотека для подбора гиперпараметров; в модуле используется вместо альтернативы Ray Tune.
- **Objective function (целевая функция)** — функция, которая обучает и оценивает модель и возвращает число, которое Optuna минимизирует.
- **Search space (пространство поиска)** — диапазоны значений, задаваемые методами `trial.suggest_int`, `trial.suggest_float`, `trial.suggest_categorical`.
- **Sampler (алгоритм поиска)** — например, TPE (Tree-structured Parzen Estimator), байесовский метод, который выбирает новые значения на основе предыдущих результатов; по умолчанию рекомендуется TPE.
- **Study (исследование)** — контейнер, который хранит все испытания, их результаты и лучшие найденные параметры.
- **Trial (испытание)** — один запуск оптимизации с конкретным набором гиперпараметров; записывает значения параметров, результат целевой функции и метаданные.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/hyperparameters-azure-databricks/1-introduction
Гиперпараметры влияют на обучение и качество модели; их выбор критичен. Подбор гиперпараметров — систематическая проверка комбинаций. В Azure Databricks для этого используется Optuna, которая итеративно исследует пространство гиперпараметров.

### 2. Optimize hyperparameters with Optuna
Источник: https://learn.microsoft.com/en-us/training/modules/hyperparameters-azure-databricks/2-understand
Порядок работы: определить целевую функцию, создать study и запустить оптимизацию. Целевая функция принимает объект trial, предлагает значения гиперпараметров, обучает и оценивает модель и возвращает число, которое нужно минимизировать (например, отрицательную точность). По умолчанию используется TPE-сэмплер; `study.optimize` вызывает целевую функцию до заданного числа испытаний и возвращает лучшую комбинацию (`study.best_params`).

### 3. Review trials
Источник: https://learn.microsoft.com/en-us/training/modules/hyperparameters-azure-databricks/3-review
Результаты испытаний можно смотреть двумя способами: через MLflow run каждого испытания (интеграция Optuna с MLflow в Azure Databricks) или через классы Study и Trial в коде, перебирая `study.trials`.

### 4. Scale hyperparameter optimization
Источник: https://learn.microsoft.com/en-us/training/modules/hyperparameters-azure-databricks/4-scale
Spark позволяет распределять вычисления по узлам кластера, и Optuna поддерживает распределенную оптимизацию через интеграцию с Apache Spark, класс `optuna.integration.SparkOptimizer`. Преимущества: автоматическое распределение испытаний по worker-узлам, отказоустойчивость и восстановление, интеграция с MLflow, поддержка распределенных и нераспределенных ML-библиотек.

### 5. Exercise - Optimize hyperparameters for machine learning in Azure Databricks
Источник: https://learn.microsoft.com/en-us/training/modules/hyperparameters-azure-databricks/5-exercise-use-mlflow
Практика (около 45 минут): использовать Optuna для оптимизации гиперпараметров алгоритма классификации. Нужна подписка Azure с правами администратора.

### 6. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/hyperparameters-azure-databricks/6-knowledge-check
Проверка знаний по модулю (в исходнике текст отсутствует).

### 7. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/hyperparameters-azure-databricks/7-summary
Optuna предоставляет эффективный и простой в использовании фреймворк для запуска испытаний оптимизации гиперпараметров; вместе с интеграцией в Azure Databricks и MLflow он подходит для распределенного подбора.

## Важные команды / код / настройки

Целевая функция с LogisticRegression (Spark MLlib) и подбор гиперпараметров:

```python
def objective(trial):
  from pyspark.ml.classification import LogisticRegression
  from pyspark.ml.evaluation import MulticlassClassificationEvaluator

  data_df = get_training_data()  # This is just an example!
  splits = data_df.randomSplit([0.7, 0.3])
  training_df = splits[0]
  validation_df = splits[1]

  # Suggest hyperparameters using Optuna's trial object
  max_iter = trial.suggest_int('Iterations', 1, 10)
  reg_param = trial.suggest_float('Regularization', 0.0, 1.0)

  # Train a model using the suggested hyperparameters
  lr = LogisticRegression(labelCol="label", featuresCol="features",
              maxIter=max_iter,
              regParam=reg_param)
  model = lr.fit(training_df)

  # Evaluate the model
  predictions = model.transform(validation_df)
  eval = MulticlassClassificationEvaluator(labelCol="label",
                       predictionCol="prediction",
                       metricName="accuracy")
  accuracy = eval.evaluate(predictions)

  # Optuna minimizes the objective, so return negative accuracy
  return -accuracy
```

Создание study с TPE-сэмплером и запуск оптимизации:

```python
import optuna

sampler = optuna.samplers.TPESampler()
study = optuna.create_study(direction="minimize", sampler=sampler)

study.optimize(objective, n_trials=100)

print("Best param values: ", study.best_params)
```

Распределенная оптимизация со Spark:

```python
from optuna.integration import SparkOptimizer
import mlflow

spark_optimizer = SparkOptimizer(study_name="distributed_study",
                               storage="sqlite:///example.db",
                               n_trials=100)

with mlflow.start_run():
    study = spark_optimizer.run_study(objective, direction="minimize")
    print("Best param values: ", study.best_params)
    print("Best value: ", study.best_value)
```

Методы подбора значений: `trial.suggest_int(name, low, high)`, `trial.suggest_float(name, low, high)`, `trial.suggest_categorical(name, choices)`.

## Что запомнить

- Гиперпараметры задаются до обучения; подбор — это систематический перебор комбинаций.
- Целевая функция Optuna должна возвращать значение для минимизации (например, отрицательную точность).
- По умолчанию используется TPE-сэмплер; `study.optimize(objective, n_trials=...)` запускает поиск.
- Каждое испытание можно просматривать как MLflow run или через объекты Study и Trial.
- Для масштабирования на кластер Spark используется `optuna.integration.SparkOptimizer`.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/hyperparameters-azure-databricks/
- Документация Azure Databricks: Hyperparameter tuning (упоминается в уроке 7).
- Документация Optuna: полный список методов suggest и распределенная оптимизация (упоминаются в уроках 2–4).
- Связанные модули: MLflow в Azure Databricks (`mlflow-azure-databricks`), AutoML в Azure Databricks (`automl-azure-databricks`).
