# MLflow в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/<юнит>`)

## Цель модуля

Научиться использовать MLflow в Azure Databricks для отслеживания экспериментов обучения моделей, регистрации моделей и их публикации для инференса.

## Ключевые понятия

- **MLflow** — открытая платформа для сквозного управления операциями машинного обучения (MLOps); встроена в Azure Databricks.
- **MLflow Tracking** — отслеживание экспериментов: логирование параметров, версий библиотек, метрик оценки и выходных файлов каждого запуска (run).
- **Experiment (эксперимент)** — коллекция запусков обучения; полезна для сравнения изменений и моделей с разными гиперпараметрами.
- **MLflow Projects** — упаковка кода для воспроизводимого запуска; поддерживаются окружения Conda и Docker.
- **MLflow Models** — стандартизированный формат упаковки моделей; поддерживает модели из популярных библиотек, например Scikit-Learn, PyTorch и MLlib.
- **MLflow Model Registry** — реестр моделей, в котором модели регистрируются и версионируются; используется для развертывания и обслуживания моделей.
- **Inferencing (инференс)** — использование модели для предсказания меток по новым признакам.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/1-introduction
MLflow позволяет data scientists отслеживать эксперименты, а ML-инженерам — развертывать и управлять моделями. В модуле показано, как отслеживать эксперименты и регистрировать и публиковать модели.

### 2. Capabilities of MLflow
Источник: https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/2-capabilities-of-mlflow
Описаны четыре компонента MLflow: Tracking, Projects, Models и Model Registry. Tracking позволяет аудировать и сравнивать результаты прошлых запусков; Models дает стандартный формат; Registry служит основой для развертывания и обслуживания моделей.

### 3. Run experiments with MLflow
Источник: https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/3-run-experiments
Эксперимент создается автоматически при старте запуска. Параметры и метрики логируются внутри блока `mlflow.start_run()`. По умолчанию имя эксперимента совпадает с именем блокнота; его можно изменить через переменную окружения `MLFLOW_EXPERIMENT_NAME`. Просмотреть параметры, метрики и артефакты запуска можно на странице Experiments в портале Azure Databricks.

### 4. Register and serve models with MLflow
Источник: https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/4-register-serve-models
Регистрация модели позволяет отслеживать ее версии и обслуживать ее (real-time, streaming или batch-инференс) без написания прикладного кода. Модель можно зарегистрировать вручную из интерфейса эксперимента или автоматически, передав `registered_model_name` в `log_model`. Можно регистрировать несколько версий модели и сравнивать их. Для инференса модель можно опубликовать как real-time сервис с HTTP-эндпоинтом, использовать для потокового инференса по Delta-таблице признаков или для пакетного инференса.

### 5. Exercise - Use MLflow in Azure Databricks
Источник: https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/5-exercise-use-mlflow
Практика (около 45 минут): запуск эксперимента MLflow и развертывание модели для real-time инференса. Нужна подписка Azure с правами администратора.

### 6. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/6-knowledge-check
Проверка знаний по модулю (в исходнике текст отсутствует).

### 7. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/7-summary
MLflow упрощает управление процессом обучения и моделями в Azure Databricks, давая data scientists и ML-инженерам productivity-преимущества.

## Важные команды / код / настройки

Логирование запуска с параметрами и метрикой:

```python
with mlflow.start_run():
    mlflow.log_param("input1", input1)
    mlflow.log_param("input2", input2)
    # Perform operations here like model training.
    mlflow.log_metric("rmse", rmse)
```

Логирование модели с автоматической регистрацией (`registered_model_name`):

```python
with mlflow.start_run():
    # code to train model goes here

    # log the model itself (and the environment it needs to be used)
    unique_model_name = "my_model-" + str(time.time())
    mlflow.spark.log_model(spark_model=model,
                           artifact_path=unique_model_name
                           conda_env=mlflow.spark.get_default_conda_env(),
                           registered_model_name="my_model")
```

Настройка имени эксперимента: переменная окружения `MLFLOW_EXPERIMENT_NAME`.

## Что запомнить

- MLflow Tracking фиксирует параметры, метрики и артефакты каждого запуска эксперимента.
- Эксперимент создается автоматически при старте первого запуска; имя по умолчанию — имя блокнота.
- Регистрация модели в Model Registry дает версии модели и основу для ее развертывания.
- Модель можно обслуживать как real-time HTTP-сервис, для потокового или пакетного инференса.
- MLflow Models дает стандартный формат упаковки, поддерживающий модели из популярных библиотек.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/
- Документация Azure Databricks: MLflow guide (упоминается в уроке 7).
- Документация MLflow: Models — список поддерживаемых flavors (упоминается в уроке 2).
- Связанные модули: AutoML в Azure Databricks (`automl-azure-databricks`), Hyperparameter tuning в Azure Databricks (`hyperparameters-azure-databricks`).
