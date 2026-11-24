# Что ещё в Azure стоит собрать, по ролям (DE / BA / BI / DA / AI / ML / DS / DevOps)

Уже собрано: основы (AZ-900/DP-900), RBAC, ADLS Gen2, Functions, Data Factory, Synapse, Event Hubs + Stream Analytics, часть Cosmos DB, Databricks, Storage security.

## Data Engineering (DE)
- **Microsoft Fabric**: OneLake, Lakehouse, Data Factory in Fabric, Real-Time Intelligence (преемник Synapse/ADF).
- **Azure Databricks** + **Unity Catalog**, Delta Lake, Delta Live Tables, Workflows.
- **Azure SQL Database / Managed Instance**, **Azure Database for PostgreSQL**; миграция (DMS).
- **Microsoft Purview** (каталог, lineage, data quality), **Azure Data Explorer (Kusto)**.
- **Azure Key Vault**, Managed Identity, Private Endpoint, VNet для пайплайнов.
- **Azure Monitor / Log Analytics** для мониторинга пайплайнов; **Azure Batch**, **HDInsight** (legacy).

## BI / DA (аналитика)
- **Power BI** (Service, DAX, модели, Direct Lake, Row-level security, gateways).
- **Synapse Serverless SQL**, **Fabric Warehouse**, **Azure Analysis Services**.
- Visualization: Azure Data Explorer dashboards, Grafana (Azure Managed Grafana).

## BA / системный анализ
- **Power Platform**: Power Apps, Power Automate, Dataverse.
- **Azure DevOps Boards**, **Logic Apps**, **API Management**, **Service Bus / Event Grid** (интеграции), Azure Well-Architected Framework (требования NFR).

## AI / ML / DS
- **Azure Machine Learning** (workspace, pipelines, MLOps, endpoints, AutoML, MLflow).
- **Azure AI Foundry / Azure OpenAI**, **AI Search** (RAG, векторный поиск), **Document Intelligence**, **AI Language / Speech / Vision**.
- **Azure Databricks ML**, **Cosmos DB для AI (vector search)**.
- Responsible AI, content safety, мониторинг и оценка LLM-приложений.

## DevOps / Cloud
- **Azure DevOps Pipelines** и **GitHub Actions** для Azure (AZ-400), **Bicep / ARM / Terraform**.
- **AKS / Container Apps / ACR**, **App Service**, **Azure Functions** (deploy, slots).
- **Networking**: VNet, NSG, Private Link, Front Door, Application Gateway, DNS.
- **Security**: Entra ID (бывший Azure AD), Conditional Access, Defender for Cloud, Azure Policy, Key Vault.
- **Governance / FinOps**: Management Groups, Cost Management, tags, Azure Advisor, Landing Zones.
- **Monitoring**: Azure Monitor, Application Insights, Log Analytics, KQL, Alerts.

## Сертификации-ориентиры
AZ-900, DP-900, **DP-203** (снят, но материалы полезны), **DP-700** (Fabric DE), **PL-300** (Power BI), **AI-900 / AI-102**, **DP-100** (ML), **AZ-104 / AZ-305**, **AZ-400**, **AZ-500**.

## Рекомендуемый порядок следующего сбора
1. Microsoft Fabric + Databricks/Unity Catalog (DE, самый близкий к PDP).
2. Key Vault, Managed Identity, networking, Monitor/KQL (нужно всем ролям).
3. Power BI/DAX (BI/DA).
4. Azure ML + AI Foundry/OpenAI/AI Search (AI/ML/DS).
5. DevOps: Bicep/Terraform, Pipelines/GitHub Actions, AKS.
