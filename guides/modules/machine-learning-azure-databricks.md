# Машинное обучение в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/ (базовый URL юнитов: `https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/<юнит>`)

## Цель модуля

Освоить базовый процесс машинного обучения в Azure Databricks: подготовка данных, обучение и оценка модели на примере Spark MLlib (принципы применимы и к другим фреймворкам).

## Ключевые понятия

- **Features (признаки, x) и label (метка, y)** — входные характеристики объекта и значение, которое модель должна предсказать; модель — функция y = f(x).
- **Supervised learning (обучение с учителем)** — модель обучается на данных с известными метками. Включает регрессию (числовая метка) и классификацию (дискретный класс; бинарную и многоклассовую).
- **Unsupervised learning (обучение без учителя)** — обучение только на признаках; основной вид — кластеризация (clustering).
- **Spark MLlib (Spark ML)** — библиотека машинного обучения для Spark; предпочтительный API — на основе DataFrame.
- **Data cleansing (очистка данных)** — работа с пропусками (NULL), ошибками, выбросами, неверными типами данных и несбалансированностью.
- **Feature engineering (конструирование признаков)** — создание новых признаков, дискретизация, кодирование категорий, масштабирование числовых значений.
- **Training / validation split (разбиение на обучающую и проверочную выборки)** — обычно около 70% данных для обучения и 30% для валидации; переобученная (overfitted) модель хорошо предсказывает только обучающие данные.
- **Hyperparameters (гиперпараметры)** — настройки алгоритма, которые задаются заранее (например, `maxIter`, `regParam`).
- **Pipeline (конвейер)** — цепочка трансформеров и оценщиков (evaluators), которая завершается алгоритмом обучения и дает модель.

## Содержание по урокам

### 1. Introduction
Источник: https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/1-introduction
Машинное обучение лежит в основе большинства решений ИИ. Azure Databricks предоставляет платформу на базе Apache Spark с поддержкой Scikit-Learn, PyTorch, TensorFlow и др.; в модуле примеры даны на Spark MLlib.

### 2. Understand principles of machine learning
Источник: https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/2-understand-machine-learning
Описаны виды ML: supervised (регрессия и классификация) и unsupervised (кластеризация). Пример регрессии — прогноз количества проданных мороженых; пример классификации — предсказание наличия диабета. Кластеризация полезна, когда готовых категорий нет (например, сегментация клиентов).

### 3. Machine learning in Azure Databricks
Источник: https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/3-machine-learning-azure-databricks
Data scientists выполняют загрузку, исследование, подготовку, обучение и оценку моделей; ML-инженеры развертывают и управляют ими. При создании кластера можно выбрать ML-runtime: CPU-based для классического ML или GPU-based для глубокого обучения. Работа ведется в интерактивных блокнотах на PySpark.

### 4. Prepare data for machine learning
Источник: https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/4-prepare-data-for-machine-learning
Подготовка включает очистку данных (пропуски, ошибки, выбросы, неверные типы, несбалансированность классов) и конструирование признаков (производные признаки, дискретизация, кодирование категорий, масштабирование). Основной класс — Spark DataFrame. В MLlib для кодирования строк используется `StringIndexer`; шаги можно объединить в pipeline.

### 5. Train a machine learning model
Источник: https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/5-train-model
Обучение — подгонка алгоритма (fit) под обучающие данные. Выборка делится на обучающую и проверочную. Типы алгоритмов классификации: логистическая регрессия, деревья решений, ансамбли. Гиперпараметры управляют поведением алгоритма (случайность, число итераций, число ветвей дерева).

### 6. Evaluate a machine learning model
Источник: https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/6-evaluate-model
Оценка проводится на проверочных данных. Для регрессии — MSE, RMSE, R² (класс `RegressionEvaluator`). Для классификации — accuracy, precision, recall, F1 (класс `MulticlassClassificationEvaluator`); accuracy может вводить в заблуждение при несбалансированных классах. Для кластеризации — Silhouette (класс `ClusteringEvaluator`), значения от 1 до -1.

### 7. Exercise - Train a machine learning model in Azure Databricks
Источник: https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/7-exercise-machine-learning-databricks
Практика (около 45 минут): обучение модели классификации на Spark-кластере Databricks. Нужна подписка Azure с правами администратора.

### 8. Module assessment
Источник: https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/8-knowledge-check
Проверка знаний по модулю (в исходнике текст отсутствует).

### 9. Summary
Источник: https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/9-summary
Azure Databricks — масштабируемая платформа для очистки и предобработки данных, обучения и оценки моделей с помощью разных ML-фреймворков и утилит.

## Важные команды / код / настройки

Чтение данных и очистка в DataFrame:

```python
df = spark.read.format("csv").option("header", "true").load("/myfolder/mydata.csv")
df = spark.sql("SELECT * FROM mytable")
clean_data = df.dropna().select(col("column1").astype("string"),
                                col("column2").astype("float"))
```

Кодирование строковых значений:

```python
from pyspark.ml.feature import StringIndexer

encoder = StringIndexer(inputCol="catCol", outputCol="catColCode")
encoded_data = encoder.fit(data).transform(data)
```

Обучение логистической регрессии:

```python
from pyspark.ml.classification import LogisticRegression

lr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=10, regParam=0.3)
model = lr.fit(training_df)
```

Оценка регрессии:

```python
from pyspark.ml.evaluation import RegressionEvaluator

predictions_df = model.transform(validation_df)
evaluator = RegressionEvaluator()
evaluator.setPredictionCol("prediction")
mse = evaluator.evaluate(predictions_df, {evaluator.metricName: "mse"})
rmse = evaluator.evaluate(predictions_df, {evaluator.metricName: "rmse"})
r2 = evaluator.evaluate(predictions_df, {evaluator.metricName: "r2"})
```

Оценка классификации:

```python
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(predictionCol="prediction", labelCol="label")
accuracy = evaluator.evaluate(predictions_df, {evaluator.metricName:"accuracy"})
# Per-class: precisionByLabel, recallByLabel, fMeasureByLabel (с evaluator.metricLabel)
# Combined: weightedPrecision, weightedRecall, weightedFMeasure
```

Оценка кластеризации:

```python
from pyspark.ml.evaluation import ClusteringEvaluator

evaluator = ClusteringEvaluator(predictionCol="prediction")
silhouetteVal = evaluator.evaluate(predictions_df)
```

Рекомендуемый тип кластера: ML runtime (CPU для классического ML, GPU для глубокого обучения).

## Что запомнить

- Модель — функция y = f(x): признаки на входе, предсказанная метка на выходе.
- Обычно около 70% данных — для обучения, около 30% — для валидации; это защита от переобучения.
- Очистка данных (пропуски, выбросы, типы, дисбаланс) и конструирование признаков занимают большую часть подготовки.
- Выбор метрики зависит от задачи: MSE/RMSE/R² для регрессии, accuracy/precision/recall/F1 для классификации, Silhouette для кластеризации.
- Accuracy может быть обманчивой при несбалансированных классах: модель, всегда предсказывающая самый частый класс, даст высокую accuracy.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/
- Документация Azure Databricks: Introduction to Databricks Machine Learning (упоминается в уроке 9).
- Связанные модули: AutoML в Azure Databricks (`automl-azure-databricks`), Подбор гиперпараметров (`hyperparameters-azure-databricks`), MLflow в Azure Databricks (`mlflow-azure-databricks`).
