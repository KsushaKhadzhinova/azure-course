# Инструменты разработки с AI для Azure Cosmos DB

**Источник:** https://learn.microsoft.com/en-us/training/modules/implement-ai-assisted-development-tools-azure-cosmos-db/

## Цель модуля

Научиться выбирать инструмент с AI-поддержкой для сценария Azure Cosmos DB: MCP-серверы для исследования данных и для работы агентов в продакшене, Agent Memory Toolkit для долговременной памяти агента и Agentic Retrieval для многошагового поиска. Модуль также объясняет, что инструмент берет на себя, а что остается ответственностью разработчика: модель данных, мощности, индексация, область ролей и оценка качества ответов.

## Ключевые понятия

- **Azure Cosmos DB for NoSQL** — единое хранилище документов, векторов и полнотекстового содержимого; запросы могут сочетать фильтры, полнотекстовый поиск и векторное сходство.
- **Model Context Protocol (MCP)** — открытый стандарт, через который AI-модель вызывает инструменты сервера по именам.
- **Azure MCP Server** — широкий сервер Azure с инструментами Cosmos DB для разработки; аутентифицируется под identity разработчика.
- **Azure Cosmos DB MCP Toolkit** — самостоятельно развертываемый сервер для работы агентов во время выполнения; использует managed identity и проверяет токены вызывающих.
- **Azure Cosmos DB Shell** — командная строка с опциональным режимом MCP-сервера; инструменты читают, пишут и удаляют данные.
- **Agent Memory Toolkit** — Python SDK в public preview для хранения и обработки памяти агента.
- **Agentic Retrieval** — референсная реализация многошагового RAG с режимами tool-use и decomposed.
- **Azure Cosmos DB Agent Kit** — набор инструкций для AI-агентов, который не подключается к базе данных.
- **Hybrid search и Reciprocal Rank Fusion** — объединение векторного и полнотекстового рангов.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/implement-ai-assisted-development-tools-azure-cosmos-db/1-introduction

Введение: инструменты избавляют от ручной реализации подключения, извлечения данных и схемы памяти. Выбор важнее знания сигнатур методов. MCP не зависит от языка; Agent Memory Toolkit и Agentic Retrieval сейчас написаны на Python и должны рассматриваться по своей зрелости.

### 2. Understand the AI-assisted Azure Cosmos DB toolset
https://learn.microsoft.com/en-us/training/modules/implement-ai-assisted-development-tools-azure-cosmos-db/2-understand-artificial-intelligence-assisted-tools

Три семейства: MCP-серверы (Azure MCP Server, Azure Cosmos DB MCP Toolkit, Azure Cosmos DB Shell), прикладные акселераторы (Agent Memory Toolkit, Agentic Retrieval) и Agent Kit. Описаны решения, которые принимают инструменты: единое хранилище, таксономия памяти с оценкой уверенности, обработка через change feed и цикл многошагового поиска. Отмечен статус выпусков: Azure MCP Server 2.0 доступен широко, 3.0 beta — prerelease, Agent Memory Toolkit — public preview.

### 3. Use the Azure Cosmos DB MCP server
https://learn.microsoft.com/en-us/training/modules/implement-ai-assisted-development-tools-azure-cosmos-db/3-use-cosmos-db-mcp-server

Подключение Azure MCP Server к проекту через `.vscode/mcp.json`, назначение роли Cosmos DB Built-in Data Reader на минимально необходимую область. Инструменты: список аккаунтов, баз и контейнеров, запрос, чтение элемента по ID, последние изменения, полнотекстовый и векторный поиск, вывод схемы. Все инструменты Azure Cosmos DB только читают. Текстовый поиск требует полнотекстового индекса, векторный — векторного индекса и развертывания embedding-модели. Вывод схемы показывает только top-level свойства.

### 4. Use the agent toolkits
https://learn.microsoft.com/en-us/training/modules/implement-ai-assisted-development-tools-azure-cosmos-db/4-use-agent-toolkits

Установка Agent Memory Toolkit, создание клиента с Entra ID, запись реплик диалога, запуск обработки, поиск фактов с порогом уверенности и получение сводки пользователя. Контейнеры создаются через управляющую плоскость (ARM, Azure CLI или портал), так как Entra ID не авторизует создание баз и контейнеров через данные. Для Agentic Retrieval описаны клонирование репозитория, `config.yaml`, скрипты загрузки и поиска, режимы `tool-use` (по умолчанию) и `decomposed`, а также параметр `--k-diverse`. Для ингестии нужна роль Cosmos DB Built-in Data Contributor.

### 5. Choose the right tool and understand its scope
https://learn.microsoft.com/en-us/training/modules/implement-ai-assisted-development-tools-azure-cosmos-db/5-choose-tool-understand-scope

Таблица соответствия потребности и инструмента: Agent Kit — рекомендации для кода; Azure MCP Server — исследование контейнера при разработке; Azure Cosmos DB MCP Toolkit — запросы агента во время выполнения; Agent Memory Toolkit — память пользователя; Agentic Retrieval — сложные вопросы по многим документам; SDK — все, что не укладывается в готовые шаблоны. Разделены зоны ответственности: модель данных, стоимость и пропускная способность, область безопасности, качество ответов. Для выбора предлагается три вопроса.

### 6. Exercise - Inspect Azure Cosmos DB with Azure MCP server
https://learn.microsoft.com/en-us/training/modules/implement-ai-assisted-development-tools-azure-cosmos-db/6-exercise-inspect-azure-cosmos-db-azure-mcp-server

Практика (около 45 минут): подключить AI-ассистента к каталогу CosmicWorks через MCP-сервер, задавать запросы на естественном языке и изучать вызовы инструментов и результаты. Нужна подписка Azure и учетная запись GitHub с доступом к GitHub Copilot.

### 7. Module assessment
https://learn.microsoft.com/en-us/training/modules/implement-ai-assisted-development-tools-azure-cosmos-db/7-knowledge-check

Проверочный тест (около 5 минут). Вопросы и ответы в источнике не приведены.

### 8. Summary
https://learn.microsoft.com/en-us/training/modules/implement-ai-assisted-development-tools-azure-cosmos-db/8-summary

Итоги: выбор инструмента с обоснованием, хранение документов и векторов в одном контейнере, разделение MCP-серверов по моментам работы, Agent Memory Toolkit и Agentic Retrieval. Инструменты задают шаблон, а модель данных, индексацию, роли и оценку качества определяет разработчик.

## Важные команды / код / настройки

**Конфигурация Azure MCP Server для проекта (`.vscode/mcp.json`):**

```
{
  "servers": {
    "Azure MCP Server": {
      "command": "npx",
      "args": ["-y", "@azure/mcp@3.0.0-beta.49", "server", "start"]
    }
  }
}
```

Требуется Node.js 22 или новее. Аутентификация идет под identity разработчика (`az login`).

**Назначение роли чтения данных Cosmos DB на уровне базы:**

```
az cosmosdb sql role assignment create \
    --account-name <account-name> \
    --resource-group <resource-group> \
    --scope "/dbs/cosmicworks" \
    --principal-id <your-object-id> \
    --role-definition-id 00000000-0000-0000-0000-000000000001
```

Роль: Cosmos DB Built-in Data Reader. Для векторного поиска дополнительно нужна роль Cognitive Services OpenAI User на ресурсе Azure OpenAI.

**Установка Agent Memory Toolkit:** `pip install azure-cosmos-agent-memory==0.3.0b2`. Примеры используют модели gpt-5.4-mini и text-embedding-3-small (размерность 1536).

**Клиент памяти (фрагмент из источника):**

```
import os
from azure.cosmos.agent_memory import CosmosMemoryClient

memory = CosmosMemoryClient(
    cosmos_database="ai_memory",
    cosmos_container="memories",
    ai_foundry_endpoint=os.environ["AI_FOUNDRY_ENDPOINT"],
    embedding_deployment_name="text-embedding-3-small",
    embedding_dimensions=1536,
    chat_deployment_name="gpt-5.4-mini",
    use_default_credential=True,
)

memory.connect_cosmos(endpoint=os.environ["COSMOS_DB_ENDPOINT"])
```

`AI_FOUNDRY_ENDPOINT` — endpoint Azure OpenAI для ресурса Foundry без `/openai/v1/`. Методы: `upsert_memory(...)`, `process_now(...)`, `search_cosmos(search_terms=..., user_id=..., top_k=5, min_confidence=0.7)`, `get_user_summary(user_id=...)`. Эпизоды добавляются при `include_episodes=True`; `enable_turn_embeddings` включает эмбеддинги реплик.

**Agent Framework (prerelease):** `pip install agent-framework-azure-cosmos-memory --pre`; класс `CosmosMemoryContextProvider`, хуки `before_run` и `after_run`.

**Agentic Retrieval:**

```
python cosmos_db_upload.py --config config.yaml

python dynamic_retriever.py \
    --mode decomposed \
    --config config.yaml \
    --questions-path data/questions-answers.json
```

Режим по умолчанию — `tool-use`. `--k-diverse` работает только в режиме decomposed и по умолчанию отключен. В `config.yaml` в примере стоит `use_rbac_auth: false`, его нужно выставить вручную.

**Provisioning Agent Memory Toolkit:** три основных контейнера памяти плюс счетчики и lease-контейнеры, иерархические ключи партиций. `cosmos_throughput_mode` по умолчанию `serverless`; также доступен autoscale с максимумом RU/s.

**Ограничения инструментов из урока 3:**

- Schema inference: только top-level свойства, вложенные объекты и массивы возвращаются как `object` или `array`.
- Полнотекстовый поиск (`FullTextContains`) работает по словам, а не по подстроке.
- Инструменты Azure Cosmos DB в Azure MCP Server только читают; сам сервер в целом не read-only, и это задается его опцией read-only.

## Что запомнить

- Azure MCP Server — инструмент разработки под вашей identity; Azure Cosmos DB MCP Toolkit — инструмент для агента в продакшене с managed identity.
- Роль, назначенная на уровне аккаунта, дает доступ ко всем контейнерам; назначайте область на нужную базу или контейнер.
- Текстовый и векторный поиск требуют индексов, а векторные запросы должны использовать ту же embedding-модель и размерность, что и хранимые данные.
- Agent Memory Toolkit и Agentic Retrieval добавляют стоимость и задержку (обработка, несколько раундов моделей), поэтому их нужно измерять.
- Качество ответов и модель данных остаются ответственностью разработчика; инструмент этого не решает.

## Связанные материалы

- Azure MCP Server tools for Azure Cosmos DB.
- Get started with the Azure MCP Server in Visual Studio Code.
- Azure Cosmos DB MCP Toolkit.
- Agent Memory Toolkit.
- Agentic Retrieval Toolkit.
- Microsoft Agent Framework.
- Vector search in Azure Cosmos DB for NoSQL.
- Full-text search in Azure Cosmos DB for NoSQL.
- Design multi-agent memory architectures with Azure Cosmos DB (упоминается в уроке 4).
