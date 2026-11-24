# Машинное обучение в продакшене с Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/machine-learning-production-azure-databricks/

## Цель модуля

Понять полный цикл машинного обучения в Azure Databricks: подготовка данных и автоматизация трансформаций, разработка и обучение моделей, управление экспериментами и версиями через MLflow и Unity Catalog, развертывание (онлайн через Mosaic AI Model Serving или пакетно через задания) и поддержка моделей в продакшене.

## Ключевые понятия

- **Машинное обучение (ML workflow)** — сбор данных, EDA, feature engineering, выбор модели, обучение, оценка, оптимизация, развертывание, мониторинг.
- **AutoML** — автоматический подбор алгоритмов, гиперпараметров и оценка моделей.
- **Hyperopt** — библиотека для поиска гиперпараметров.
- **MLflow** — открытая платформа жизненного цикла ML: Tracking, Projects, Models и Model registry.
- **Unity Catalog** — централизованное управление доступом, аудит и lineage для моделей и данных.
- **Mosaic AI Model Serving** — сервис создания производственных API для моделей в реальном времени.
- **Batch inference** — пакетное прогнозирование через задания Azure Databricks на больших данных.
- **Git folders** — интеграция workspace с Git-репозиторием для версионирования.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/machine-learning-production-azure-databricks/1-introduction

Введение: сложность состоит не в обучении модели, а в ее выводе в продакшен. Azure Databricks объединяет инженерию данных и data science. Описан полный цикл: сбор данных, EDA, feature engineering, выбор модели, обучение, оценка (accuracy, precision, recall, ROC AUC), оптимизация, развертывание и мониторинг.

### 2. Automate your data transformations
https://learn.microsoft.com/en-us/training/modules/machine-learning-production-azure-databricks/2-data-pipelines-feature-engineering

Данные рекомендуется хранить в Azure Blob Storage или Azure Data Lake, а доступ управлять через Unity Catalog. Для EDA используются notebooks с Spark SQL или PySpark. Автоматический feature engineering (Featuretools, AutoFeat). Автоматизация через Azure Databricks Jobs (создание задания, настройка кластера и расписания, мониторинг) или через Azure Data Factory (фабрика, pipeline, активности, расписание и мониторинг).

### 3. Explore model development
https://learn.microsoft.com/en-us/training/modules/machine-learning-production-azure-databricks/3-model-development-training

Инструменты разработки: AutoML для выбора алгоритмов и подбора гиперпараметров, Hyperopt для поиска гиперпараметров, обучение на scikit-learn, TensorFlow и PyTorch на распределенном кластере. Эксперименты отслеживаются через MLflow (метаданные, метрики, визуализации). Коллаборация: workspace с Python, R, Scala и SQL, интеграция с Git (подключение репозитория, клонирование, commit и push), CI/CD через Azure DevOps и GitHub Actions.

### 4. Explore model deployment strategies
https://learn.microsoft.com/en-us/training/modules/machine-learning-production-azure-databricks/4-model-deployment-strategies

Развертывание через MLflow. Онлайн-предсказания — Mosaic AI Model Serving (модель логируется в формате MLflow и регистрируется в Unity Catalog или реестре workspace; создаются endpoints). Пакетные предсказания — задания Azure Databricks на Spark. Интеграция с Azure Machine Learning: модель регистрируется в workspace Azure ML и развертывается в batch или real-time endpoint.

### 5. Explore model versioning and lifecycle management
https://learn.microsoft.com/en-us/training/modules/machine-learning-production-azure-databricks/5-model-versioning-lifecycle-management

Компоненты MLflow: Tracking, Projects, Models и Model registry (регистрация, версии, стадии). Unity Catalog добавляет централизованный контроль доступа, аудит и lineage, а также поиск моделей между workspace. Рекомендации: логировать все эксперименты, версионировать модели в реестре, использовать Git, разделять окружения (разработка и продакшен) с четкими критериями перехода между стадиями.

### 6. Exercise - Manage a machine learning model
https://learn.microsoft.com/en-us/training/modules/machine-learning-production-azure-databricks/6-exercise

Практика (около 30 минут): управление моделью машинного обучения в продакшене с Azure Databricks. Нужна подписка Azure с правами администратора.

### 7. Module assessment
https://learn.microsoft.com/en-us/training/modules/machine-learning-production-azure-databricks/7-knowledge-check

Проверочный тест (около 3 минут). Вопросы и ответы в источнике не приведены.

### 8. Summary
https://learn.microsoft.com/en-us/training/modules/machine-learning-production-azure-databricks/8-summary

Итоги: Azure Databricks поддерживает обучение и развертывание моделей в продакшене; интеграция с Azure Machine Learning и другими сервисами Azure покрывает весь жизненный цикл.

## Важные команды / код / настройки

В источнике нет программного кода и CLI-команд. Упомянутые настройки и объекты:

- **Azure Databricks Jobs:** создание задания (имя, notebook или JAR), настройка кластера, расписания и зависимостей, email-уведомления о статусе.
- **Azure Data Factory pipeline:** фабрика, pipeline с activities, параметры источников и приемников, расписание и мониторинг.
- **Git-интеграция:** настройка Git-провайдера в User Settings (GitHub, GitLab, Bitbucket), клонирование репозитория в workspace, commit и push.
- **MLflow:** логирование параметров, метрик и артефактов; регистрация моделей и управление стадиями (staging, production).
- **Unity Catalog:** централизованный контроль доступа к моделям, аудит и lineage.
- **Mosaic AI Model Serving:** создание и опрос endpoints для моделей, зарегистрированных в MLflow-формате.
- **Метрики оценки:** accuracy, precision, recall и area under the ROC curve.

## Что запомнить

- Развертывание начинается с логирования модели в формате MLflow и регистрации в Unity Catalog или реестре workspace.
- Онлайн-предсказания обслуживаются через Mosaic AI Model Serving, пакетные — через задания Azure Databricks на Spark.
- AutoML и Hyperopt автоматизируют выбор алгоритмов и подбор гиперпараметров.
- MLflow отслеживает эксперименты и управляет версиями моделей; Unity Catalog добавляет управление доступом и lineage.
- Разделяйте окружения (разработка и продакшен) и переводите модели между стадиями по четким критериям.

## Связанные материалы

- Azure Databricks AutoML.
- Hyperparameter tuning in Azure Databricks.
- Using MLflow for machine learning lifecycle management in Azure Databricks.
- Git integration with Databricks Git folders.
- Deploy and query a custom model (Mosaic AI Model Serving).
- Deploy models for batch inference and prediction.
- Azure Machine Learning endpoints for inference in production.
- Learn more about Azure Data Factory (упоминается в уроке 2).
