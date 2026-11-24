# Создание шаблонов ресурсов для Azure Cosmos DB for NoSQL

**Источник:** https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/

## Цель модуля

Научиться автоматизировать создание ресурсов Azure Cosmos DB for NoSQL (аккаунт, база данных, контейнер) с помощью шаблонов Azure Resource Manager (ARM, JSON) и Bicep, а также управлять throughput и политиками индексации через шаблоны.

## Ключевые понятия

- **Azure Resource Manager (ARM) template** - JSON-файл с описанием инфраструктуры и конфигурации; деплоится в Azure.
- **Bicep** - альтернативный язык описания шаблонов; в Azure деплоится так же, как JSON.
- **Microsoft.DocumentDB/databaseAccounts** - ресурс аккаунта (без привязки к API; без указания API считается NoSQL).
- **Microsoft.DocumentDB/databaseAccounts/sqlDatabases** - ресурс базы данных NoSQL API, дочерний для аккаунта.
- **Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers** - ресурс контейнера с partition key, throughput и indexing policy.
- **dependsOn (JSON) / parent (Bicep)** - описание связи родительских и дочерних ресурсов.
- **autoscaleSettings.maxThroughput** - максимальный throughput для контейнера с автомасштабированием (в примере 1000 RU/s).
- **indexingPolicy** - политика индексации контейнера (включенные и исключенные пути).
- **az deployment group create** - команда Azure CLI для деплоя шаблона в группу ресурсов.

## Содержание по урокам

### 1. Introduction
https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/1-introduction

Автоматизация создания ресурсов упрощает развертывание новых окружений, восстановление и масштабирование. В модуле используются оба синтаксиса - JSON и Bicep. Цели: назвать три основных типа ресурсов, создать и задеплоить JSON- и Bicep-шаблоны для аккаунта, базы или контейнера, управлять throughput и индексацией.

### 2. Understand Azure Resource Manager resources
https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/2-understand-azure-resource-manager-resources

Все ресурсы Cosmos DB находятся в провайдере ресурсов Microsoft.DocumentDB. Три основных типа образуют иерархию: аккаунт, база данных и контейнер. В шаблонах также можно создавать хранимые процедуры, пользовательские функции, pre- и post-триггеры.

### 3. Author Azure Resource Manager templates
https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/3-author-azure-resource-manager-templates

Пошагово строится JSON-шаблон: пустой шаблон со схемой и `resources`, затем ресурс аккаунта (минимум: name, location, databaseAccountOfferType, locations), база (name, properties.resource.id, dependsOn на аккаунт) и контейнер (name, resource.id, partitionKey.paths; опционально throughput и indexingPolicy). Рекомендуется задавать throughput через `options` контейнера, а не отдельным ресурсом throughputSettings.

### 4. Configure database or container resources
https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/4-configure-database-container-resources

Те же ресурсы описываются в Bicep. Отличия: не нужен пустой шаблон, связь задается свойством `parent` вместо `dependsOn`. Если ресурс уже существует из предыдущего деплоя, ARM пропускает его, что удобно для инкрементальной сборки шаблона.

### 5. Configure throughput with an Azure Resource Manager template
https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/5-configure-throughput-azure-resource-manager-template

Деплой выполняется командой `az deployment group create` с аргументами `--resource-group` и `--template-file`. Дополнительно можно задать `--name` и параметры (inline или файлом `@parameters.json`). Деплой Bicep-файла выполняется той же командой, меняется только расширение файла.

### 6. Manage index policies through Azure Resource Manager templates
https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/6-manage-index-policies

Политика индексации переносится в `properties.resource.indexingPolicy` без изменений в JSON. В Bicep нужно убрать кавычки у имен свойств, заменить двойные кавычки в значениях на одинарные и убрать запятые. Чтобы обновить политику у существующего контейнера, достаточно изменить только `indexingPolicy` и повторно выполнить деплой: остальные свойства контейнера сохранятся.

### 7. Exercise: Create an Azure Cosmos DB for NoSQL container using Azure Resource Manager templates
https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/7-exercise-create-container-using-azure-resource-manager-templates

Практическое задание (около 15 минут). Нужна подписка Azure с правами администратора; в инструкции: создать resource group, настроить локальное окружение, включить resource providers.

### 8. Knowledge check
https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/8-knowledge-check

Проверка знаний (около 5 минут). Текст в источнике не приведен.

### 9. Summary
https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/9-summary

Модуль показал, как автоматизировать деплой и управление аккаунтами, базами и контейнерами Cosmos DB через ARM и Bicep. В Microsoft.DocumentDB есть и другие ресурсы, которые в модуле не рассматривались.

## Важные команды / код / настройки

**Минимальный пустой JSON-шаблон:**
```
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
  ]
}
```

**Аккаунт (JSON):**
```
{
  "type": "Microsoft.DocumentDB/databaseAccounts",
  "apiVersion": "2024-04-15",
  "name": "[concat('csmsarm', uniqueString(resourceGroup().id))]",
  "location": "[resourceGroup().location]",
  "properties": {
    "databaseAccountOfferType": "Standard",
    "locations": [
      {
        "locationName": "westus"
      }
    ]
  }
}
```

**Контейнер с autoscale 1000 RU/s и partition key `/categoryId` (JSON):**
```
{
  "type": "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers",
  "apiVersion": "2024-04-15",
  "name": "[concat('csmsarm', uniqueString(resourceGroup().id), '/cosmicworks/products')]",
  "dependsOn": [
    "[resourceId('Microsoft.DocumentDB/databaseAccounts', concat('csmsarm', uniqueString(resourceGroup().id)))]",
    "[resourceId('Microsoft.DocumentDB/databaseAccounts/sqlDatabases', concat('csmsarm', uniqueString(resourceGroup().id)), 'cosmicworks')]"
  ],
  "properties": {
    "resource": {
      "id": "products",
      "partitionKey": {
        "paths": [
          "/categoryId"
        ]
      }
    },
    "options": {
      "autoscaleSettings": {
        "maxThroughput": 1000
      }
    }
  }
}
```

**Аккаунт (Bicep):**
```
resource Account 'Microsoft.DocumentDB/databaseAccounts@2024-04-15' = {
  name: 'csmsbicep${uniqueString(resourceGroup().id)}'
  location: resourceGroup().location
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: 'westus'
      }
    ]
  }
}
```

**База и контейнер (Bicep, связь через `parent`):**
```
resource Database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-04-15' = {
  parent: Account
  name: 'cosmicworks'
  properties: {
    resource: {
      id: 'cosmicworks'
    }
  }
}

resource Container 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-04-15' = {
  parent: Database
  name: 'customers'
  properties: {
    resource: {
      id: 'customers'
      partitionKey: {
        paths: [
          '/regionId'
        ]
      }
    },
    options: {
      autoscaleSettings: {
        maxThroughput: 1000
      }
    }
  }
}
```

**Политика индексации (JSON, фрагмент `resource.indexingPolicy`):**
```
"indexingPolicy": {
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    {
      "path": "/price/*"
    }
  ],
  "excludedPaths": [
    {
      "path": "/*"
    }
  ]
}
```

**Та же политика в Bicep:**
```
indexingPolicy: {
  indexingMode: 'consistent'
  automatic: true
  includedPaths: [
    {
      path: '/address/*'
    }
  ]
  excludedPaths: [
    {
      path: '/*'
    }
  ]
}
```

**Деплой (Azure CLI):**
```
az deployment group create \
    --resource-group '<resource-group>' \
    --template-file '.\template.json'

az deployment group create \
    --resource-group '<resource-group>' \
    --name '<deployment-name>' \
    --template-file '.\template.json'

az deployment group create \
    --resource-group '<resource-group>' \
    --template-file '.\template.json' \
    --parameters name='<value>'

az deployment group create \
    --resource-group '<resource-group>' \
    --template-file '.\template.json' \
    --parameters '@.\parameters.json'

az deployment group create \
    --resource-group '<resource-group>' \
    --template-file '.\template.bicep'
```

Замечание: в итоговом JSON-шаблоне модуля для контейнера указана версия `apiVersion` 2021-05-15, тогда как в остальных примерах используется 2024-04-15.

## Что запомнить

- Три основных ресурса Cosmos DB в ARM/Bicep: аккаунт (`databaseAccounts`), база (`sqlDatabases`), контейнер (`containers`); они образуют иерархию.
- В JSON связь задается через `dependsOn`, в Bicep через `parent`.
- Throughput контейнера удобнее задавать через `options.autoscaleSettings.maxThroughput`, а не отдельным ресурсом throughputSettings.
- Политика индексации задается в `properties.resource.indexingPolicy`; при обновлении достаточно изменить этот блок и повторить деплой.
- Один и тот же `az deployment group create` деплоит и JSON, и Bicep.

## Связанные материалы

- Модуль: https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/
- В источнике упоминаются (без ссылок в тексте): Quickstart: Create an Azure Cosmos DB and a container by using an ARM template; Bicep documentation; ARM template documentation; Microsoft.DocumentDB | databaseAccounts; Microsoft.DocumentDB | databaseAccounts | sqldatabases; Microsoft.DocumentDB | databaseAccounts | sqldatabases | containers.
