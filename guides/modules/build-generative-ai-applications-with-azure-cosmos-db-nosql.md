# Создание генеративных AI-приложений с Azure Cosmos DB for NoSQL и Python

**Источник:** https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/

## Цель модуля

Научиться строить генеративное AI-приложение на Python, которое работает с приватными данными: сохранять и извлекать векторы в Azure Cosmos DB for NoSQL, выполнять similarity search, реализовать retrieval augmented generation (RAG) и оркестрировать модели через LangChain.

## Ключевые понятия

- **Azure Cosmos DB for NoSQL** — полностью управляемая распределенная NoSQL-база; может выступать и как хранилище данных, и как векторное хранилище.
- **Embedding (вектор)** — числовое представление текста или другого объекта; близость векторов отражает семантическую близость исходных данных.
- **Vector Search** — поиск по похожести векторов, а не по точному совпадению полей.
- **Vector embedding policy** — политика контейнера, описывающая путь к вектору, тип данных, размерность и функцию расстояния.
- **Vector indexing policy** — политика индекса: flat, quantizedFlat или diskANN.
- **VectorDistance** — системная функция запроса, которая вычисляет расстояние между векторами.
- **RAG (retrieval augmented generation)** — приём, при котором найденные в базе документы добавляются в промпт LLM.
- **Function calling** — механизм, при котором модель формирует JSON с параметрами вызова функции, а приложение выполняет ее и возвращает результат модели.
- **LangChain** — фреймворк оркестрации LLM, embedding-моделей и баз данных.
- **Microsoft Entra ID RBAC** — аутентификация без ключей через `DefaultAzureCredential`.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/1-introduction

Введение: что такое генеративные AI-приложения, почему выбраны Python и Azure Cosmos DB for NoSQL, зачем нужен RAG для работы с корпоративными данными, которых нет в обучении LLM.

### 2. Configure the Vector Search and storage feature of Azure Cosmos DB NoSQL
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/2-configure-vector-search-storage-for-azure-cosmos-db-nosql

Векторный поиск хранит embeddings рядом с исходными данными в одном документе. Функция включается в портале (раздел Features) или через Azure CLI. Vector embedding policy задается при создании контейнера, так как для существующих контейнеров функция не поддерживается. Описаны типы индексов и их ограничения по размерности.

### 3. Exercise - Enable the Azure Cosmos DB for NoSQL Vector Search feature
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/3-exercise-enable-azure-cosmos-db-nosql-vector-search

Практика (около 10 минут): создать группу ресурсов, зарегистрировать resource providers, развернуть Azure Cosmos DB и подготовить локальную среду. Нужна подписка Azure с правами администратора.

### 4. Generate embeddings using Azure OpenAI Service
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/4-generate-embeddings

Embeddings создаются моделями Azure OpenAI (text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large). Размерность вектора задается моделью: text-embedding-3-large по умолчанию создает 3072 измерения. Описаны шаблоны интеграции: Azure Function с change feed trigger, пакетная обработка в Azure Data Factory и микросервис.

### 5. Exercise - Generate vector embeddings with Azure OpenAI and store them in Azure Cosmos DB for NoSQL
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/5-exercise-generate-and-store-vectors

Практика (около 20 минут): сгенерировать векторы через Azure OpenAI и сохранить их в Azure Cosmos DB. Продолжение упражнения из урока 3.

### 6. Build Generative AI applications with Azure Cosmos DB NoSQL and Python
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/6-build-generative-ai-applications

Настройка виртуального окружения, зависимости через requirements.txt, аутентификация Entra ID RBAC, архитектура с отдельными frontend (Streamlit) и backend (FastAPI), system prompt как persona, function calling с двумя вызовами LLM.

### 7. Perform vector searches using Azure Cosmos DB for NoSQL from a Generative AI application
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/7-perform-vector-search

Порядок векторного поиска: создать embeddings, задать vector embedding path в политике контейнера, добавить индекс, заполнить контейнер, получить embedding запроса и выполнить запрос с VectorDistance. Всегда использовать TOP N, иначе растут RU и задержка.

### 8. Exercise - Build a Generative AI application with Python and Azure Cosmos DB for NoSQL
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/8-exercise-build-generative-ai-applications

Практика (около 20 минут): собрать приложение на Python. Продолжение упражнений 3 и 5.

### 9. Integrate LangChain orchestration to improve efficiency and code maintainability in a Python Generative AI application
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/9-integrate-langchain-orchestration

Azure Cosmos DB интегрируется с LangChain и Semantic Kernel. LangChain упрощает RAG и function calling: функции и tools оформляются как переиспользуемые компоненты вместо ручной оркестрации через клиент Azure OpenAI.

### 10. Exercise - Implement RAG with LangChain and Azure Cosmos DB for NoSQL Vector Search
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/10-exercise-implement-rag-with-langchain

Практика (около 20 минут): реализовать RAG с LangChain и векторным поиском Azure Cosmos DB. Требует выполнения предыдущих упражнений модуля.

### 11. Knowledge check
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/11-knowledge-check

Проверочный тест (около 5 минут). Вопросы и ответы в источнике не приведены.

### 12. Summary
https://learn.microsoft.com/en-us/training/modules/build-generative-ai-applications-with-azure-cosmos-db-nosql/12-summary

Итоги: построить приложение с приватными данными, сохранять и извлекать векторы, выполнять similarity search и оркестрировать модели через LangChain. Ссылки на дополнительные материалы: Vector Search in Azure Cosmos DB for NoSQL, function calling в Azure OpenAI Service, интеграции с LLM-оркестраторами.

## Важные команды / код / настройки

**Включение Vector Search через Azure CLI:**

```
az cosmosdb update \
 --resource-group <resource-group-name> \
 --name <cosmos-db-account-name> \
 --capabilities EnableNoSQLVectorSearch
```

**Поля container vector policy:**

- `path` — путь к свойству с векторами.
- `datatype` — тип элементов вектора; по умолчанию Float32.
- `dimensions` — размерность вектора; определяется моделью embeddings.
- `distanceFunction` — Euclidean (по умолчанию), cosine или dot product.

**Типы vector index policy:**

| Тип | Описание | Макс. размерность |
|---|---|---|
| flat | Векторы хранятся в том же индексе, что и другие индексируемые свойства | 505 |
| quantizedFlat | Векторы сжимаются перед записью в индекс | 4096 |
| diskANN | Индекс на основе DiskANN для приближенного поиска | 4096 |

**Создание embeddings (Python):**

```
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

# Enable Microsoft Entra ID RBAC authentication
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential,
    "https://cognitiveservices.azure.com/.default"
)

# Instantiate an Azure OpenAI client
client = AzureOpenAI(
    api_version = AZURE_OPENAI_API_VERSION,
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    azure_ad_token_provider = token_provider
)

# Generate embeddings for input text
response = client.embeddings.create(
    input = "Build Generative AI applications with Python and Azure Cosmos DB for NoSQL",
    model = "text-embedding-3-large"
)

# Retrieve the generated embedding
embedding = response.data[0].embedding
```

**Запрос векторного поиска (NoSQL):**

```
SELECT TOP 5 c.name, c.description, VectorDistance(c.embedding, [1,2,3]) AS SimilarityScore 
FROM c 
ORDER BY VectorDistance(c.embedding, [1,2,3])
```

Всегда используйте `TOP N`: без него поиск возвращает больше совпадений, что повышает стоимость в RU и задержку.

**Виртуальное окружение и зависимости:**

- Создание: `python -m venv .venv`
- Активация в PowerShell: `.venv\Scripts\Activate.ps1`
- Активация в cmd.exe: `.venv\Scripts\activate.bat`
- Установка из файла: `pip install -r requirements.txt`

Пример `requirements.txt` из источника: azure-cosmos==4.9.0, azure-identity==1.19.0, fastapi==0.115.5, openai==1.55.2, pydantic==2.10.2, requests==2.32.3, streamlit==1.40.2, uvicorn==0.32.1.

**Function calling:** нужны два вызова LLM. Первый передает массив `tools` с `tool_choice = "auto"` и получает запросы на вызов функций. Приложение выполняет функции и добавляет результаты с ролью `tool`. Второй вызов формирует финальный ответ.

**Persona через system prompt:** системный промпт добавляется первым элементом в список `messages` с ролью `system`.

## Что запомнить

- Vector Search в Azure Cosmos DB включается отдельно, а vector embedding policy задается при создании нового контейнера.
- Размерность вектора должна совпадать с моделью embeddings (text-embedding-3-large создает 3072 измерения по умолчанию) и поддерживаться выбранным типом индекса.
- В запросах VectorDistance всегда указывайте TOP N.
- RAG передает в промпт LLM документы, найденные по векторному поиску, и позволяет работать с приватными данными.
- Function calling требует двух вызовов модели и выполнения функций в приложении; LangChain упрощает эту оркестрацию.

## Связанные материалы

- Vector Search in Azure Cosmos DB for NoSQL.
- How to use function calling with Azure OpenAI Service.
- Integrations with large language model (LLM) orchestrators.
- Модули и упражнения этого курса: Enable Azure Cosmos DB for NoSQL Vector Search; Generate vector embeddings with Azure OpenAI and store them in Azure Cosmos DB for NoSQL; Build a Generative AI app with Python and Azure Cosmos DB for NoSQL.
