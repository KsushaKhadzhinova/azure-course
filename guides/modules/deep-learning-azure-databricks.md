# Глубокое обучение в Azure Databricks

**Источник:** https://learn.microsoft.com/en-us/training/modules/deep-learning-azure-databricks/

## Цель модуля

Познакомиться с основами глубокого обучения и научиться обучать модели на PyTorch в Azure Databricks, включая распределенное обучение через TorchDistributor.

## Ключевые понятия

- **Глубокое обучение (deep learning)** - разновидность машинного обучения на многослойных искусственных нейронных сетях; применяется для компьютерного зрения и обработки естественного языка.
- **Нейрон, веса и смещение (w, b)** - нейрон вычисляет взвешенную сумму входов x, весов w и смещения b, затем применяет функцию активации; веса и смещения подстраиваются при обучении.
- **Loss (функция потерь)** - совокупная разница между предсказаниями и известными метками.
- **Optimizer (оптимизатор)** - алгоритм, который корректирует веса и смещения для уменьшения loss; скорость настраивается learning rate.
- **Epoch (эпоха)** - один полный проход обучения по данным; обучение повторяется до минимизации потерь.
- **Tensor и DataLoader** - данные PyTorch представляются тензорами и подаются в модель батчами через загрузчики данных.
- **TorchDistributor** - открытая библиотека для распределения обучения PyTorch по узлам кластера Spark; доступна в Databricks Runtime ML 13.0 и выше.

## Содержание по урокам

### 1. Введение
URL: https://learn.microsoft.com/en-us/training/modules/deep-learning-azure-databricks/1-introduction

Azure Databricks подходит для обучения глубоких моделей: работает с большими объемами данных, поддерживает масштабируемые GPU-кластеры, а в ML-кластерах предустановлены PyTorch, TensorFlow и Horovod. Модуль фокусируется на PyTorch в Azure Databricks. Для более общего введения в глубокое обучение в источнике рекомендуется отдельный модуль "Train and evaluate deep learning models".

### 2. Концепции глубокого обучения
URL: https://learn.microsoft.com/en-us/training/modules/deep-learning-azure-databricks/2-deep-learning

Искусственные нейроны обрабатывают числовые входы x с весами w и смещением b, а функция активации определяет, передавать ли сигнал дальше. Модель состоит из слоев; для классификации выход - вектор вероятностей классов. Обучение: подача батчей данных, вычисление loss, оптимизатор корректирует веса и смещения, затем цикл повторяется по эпохам. Скорость обучения (learning rate) не должна быть ни слишком низкой (долгое обучение), ни слишком высокой (оптимум может не найтись).

### 3. Обучение моделей с PyTorch
URL: https://learn.microsoft.com/en-us/training/modules/deep-learning-azure-databricks/3-pytorch

Модель определяется классом-наследником `nn.Module` с методом `forward`. Данные готовятся как тензоры и разбиваются на обучающий и тестовый наборы с помощью `DataLoader`. Примеры функций потерь: `cross_entropy` (многоклассовая классификация), `binary_cross_entropy` (бинарная), `mse_loss` (регрессия). Примеры оптимизаторов: Adadelta, Adam, SGD. Отдельные функции train и test: в режиме обучения работает backpropagation, в режиме оценки - без вычисления градиентов. Обучение идет несколько эпох; тестовый набор помогает заметить переобучение (overfitting). Модель сохраняется через `state_dict`, загружается обратно в экземпляр того же класса.

### 4. Распределенное обучение с TorchDistributor
URL: https://learn.microsoft.com/en-us/training/modules/deep-learning-azure-databricks/4-horovod

Для распределения обучения по нескольким узлам кластера используется TorchDistributor (в адресе урока упоминается Horovod, но в тексте описан именно TorchDistributor). Шаги: адаптировать код, вынеся обучение в одну функцию; переместить импорты внутрь этой функции, чтобы избежать ошибок сериализации (pickling); подготовить модель, оптимизатор, функцию потерь и цикл обучения внутри функции; создать `TorchDistributor` и вызвать `.run(...)`. Мониторинг выполняется встроенными инструментами кластера (использование CPU/GPU, памяти).

### 5. Упражнение: обучение глубоких моделей в Azure Databricks
URL: https://learn.microsoft.com/en-us/training/modules/deep-learning-azure-databricks/5-exercise-deep-learning

Практика с PyTorch на Azure Databricks. Нужна подписка Azure с правами администратора.

### 6. Проверка знаний
URL: https://learn.microsoft.com/en-us/training/modules/deep-learning-azure-databricks/7-knowledge-check

Тест модуля. Вопросы в источнике не приведены.

### 7. Итоги
URL: https://learn.microsoft.com/en-us/training/modules/deep-learning-azure-databricks/8-summary

Глубокое обучение обучает сложные модели; Azure Databricks подходит благодаря масштабируемости и работе с data lake. Можно использовать любую библиотеку глубокого обучения, работающую в PySpark (PyTorch, TensorFlow), и распределять обучение по узлам кластера.

## Важные команды / код / настройки

Определение сети PyTorch с тремя слоями:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MyNet(nn.Module):
    def __init__(self):
        super(MyNet, self).__init__()
        self.layer1 = nn.Linear(4, 5)
        self.layer2 = nn.Linear(5, 5)
        self.layer3 = nn.Linear(5, 3)

    def forward(self, x):
        layer1_output = torch.relu(self.layer1(x))
        layer2_output = torch.relu(self.layer2(layer1_output))
        y = self.layer3(layer2_output)
        return y
```

Загрузчики данных (батч 20):

```python
train_loader = td.DataLoader(train_ds, batch_size=20,
    shuffle=False, num_workers=1)
```

Функция потерь и оптимизатор:

```python
loss_criteria = nn.CrossEntropyLoss
learning_rate = 0.001
optimizer = opt.Adam(model.parameters(), lr=learning_rate)
```

Сохранение и загрузка весов:

```python
model_file = '/dbfs/my_model.pkl'
torch.save(model.state_dict(), model_file)

model = myNet()
model.load_state_dict(torch.load(model_file))
```

Запуск распределенного обучения:

```python
from pyspark.ml.torch.distributor import TorchDistributor

distributor = TorchDistributor(num_workers=4)
distributor.run(train_model, dataloader)
```

Требование: TorchDistributor доступен в Databricks Runtime ML 13.0 и выше.

## Что запомнить

- Azure Databricks с GPU-кластерами и предустановленным PyTorch подходит для обучения глубоких моделей на больших данных.
- Цикл обучения: forward pass, вычисление loss, backpropagation, шаг оптимизатора; повторяется по эпохам.
- Тестовый набор помогает заметить переобучение.
- Learning rate критичен: слишком низкий замедляет, слишком высокий мешает найти оптимум.
- Для распределения обучения используйте TorchDistributor, вынося обучение и импорты в одну функцию.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/deep-learning-azure-databricks/
- Best practices for deep learning on Azure Databricks; Train and evaluate deep learning models; Loss functions и Algorithms в документации PyTorch (названия из источника, URL не приведены)
