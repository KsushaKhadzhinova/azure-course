# Создание решений машинного обучения в Azure Databricks

**Источник** https://learn.microsoft.com/en-us/training/paths/build-operate-machine-learning-solutions-azure-databricks

## О курсе

Обучение, отслеживание и развертывание моделей машинного и глубокого обучения на Azure Databricks.

- **Уровень:** средний (Intermediate)
- **Роль:** Data Scientist
- **Продукты и сервисы:** Azure Databricks
- **Предварительные требования:** Опыт работы с Python для изучения данных и обучения моделей с open-source фреймворками (Scikit-Learn, PyTorch, TensorFlow). В источнике рекомендовано предварительно пройти путь Create machine learning models.

## Чему научитесь

- Обучение предиктивных моделей и работа с Apache Spark в Azure Databricks.
- Управление жизненным циклом моделей с помощью MLflow.
- Подбор гиперпараметров и AutoML.
- Глубокое обучение и развертывание моделей в производство.

## Модули

1. **Знакомство с Azure Databricks**. Понять назначение Azure Databricks как единой платформы для data engineering, data science, machine learning и аналитики: создать workspace, освоить интерфейс, основные рабочие нагрузки, ключевые понятия и инструменты управления данными (Unity Catalog и Microsoft Purview). [guide](../modules/explore-azure-databricks.md)
2. **Использование Apache Spark в Azure Databricks**. Понять архитектуру Apache Spark, создать и настроить кластер Spark в Azure Databricks, использовать Spark в ноутбуках для обработки и анализа файлов данных (чтение, трансформация, SQL-запросы, запись) и визуализировать результаты. [guide](../modules/use-apache-spark-azure-databricks.md)
3. **Машинное обучение в Azure Databricks**. Освоить базовый процесс машинного обучения в Azure Databricks: подготовка данных, обучение и оценка модели на примере Spark MLlib (принципы применимы и к другим фреймворкам). [guide](../modules/machine-learning-azure-databricks.md)
4. **MLflow в Azure Databricks**. Научиться использовать MLflow в Azure Databricks для отслеживания экспериментов обучения моделей, регистрации моделей и их публикации для инференса. [guide](../modules/mlflow-azure-databricks.md)
5. **Подбор гиперпараметров с Optuna в Azure Databricks**. Научиться систематически подбирать гиперпараметры моделей машинного обучения с помощью библиотеки Optuna в Azure Databricks, отслеживать испытания (trials) через MLflow и масштабировать оптимизацию на кластер Spark. [guide](../modules/hyperparameters-azure-databricks.md)
6. **AutoML в Azure Databricks**. Научиться использовать AutoML в Azure Databricks, чтобы автоматизировать обучение моделей: система перебирает разные алгоритмы и значения гиперпараметров и сокращает усилия, необходимые для создания эффективных решений машинного обучения. [guide](../modules/automl-azure-databricks.md)
7. **Глубокое обучение в Azure Databricks**. Познакомиться с основами глубокого обучения и научиться обучать модели на PyTorch в Azure Databricks, включая распределенное обучение через TorchDistributor. [guide](../modules/deep-learning-azure-databricks.md)
8. **Машинное обучение в продакшене с Azure Databricks**. Понять полный цикл машинного обучения в Azure Databricks: подготовка данных и автоматизация трансформаций, разработка и обучение моделей, управление экспериментами и версиями через MLflow и Unity Catalog, развертывание (онлайн через Mosaic AI Model Serving или пакетно через задания) и поддержка моделей в продакшене. [guide](../modules/machine-learning-production-azure-databricks.md)

## Ключевые технологии и понятия

- Azure Databricks
- Data lakehouse (озеро-хранилище)
- Delta Lake
- Unity Catalog
- Metastore
- Workspace (рабочая область)
- Control plane / Compute plane
- Cluster (кластер)
- Serverless / Classic compute
- Databricks Runtime
- Lakeflow Jobs
- SQL warehouse
- MLflow
- Microsoft Purview

## Для каких ролей полезно

- Data Scientist (DS, специалист по данным)

## Источники

- Учебный путь/курс: https://learn.microsoft.com/en-us/training/paths/build-operate-machine-learning-solutions-azure-databricks
- Модуль «Знакомство с Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/
- Модуль «Использование Apache Spark в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/
- Модуль «Машинное обучение в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/
- Модуль «MLflow в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/mlflow-azure-databricks/
- Модуль «Подбор гиперпараметров с Optuna в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/hyperparameters-azure-databricks/
- Модуль «AutoML в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/automl-azure-databricks/
- Модуль «Глубокое обучение в Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/deep-learning-azure-databricks/
- Модуль «Машинное обучение в продакшене с Azure Databricks»: https://learn.microsoft.com/en-us/training/modules/machine-learning-production-azure-databricks/
