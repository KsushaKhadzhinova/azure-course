Source: https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview

Note

Access to this page requires authorization. You can try signing in or changing directories.

Access to this page requires authorization. You can try changing directories.

# What is Azure Functions?

Azure Functions is a serverless solution that allows you to build robust apps while using less code, and with less infrastructure and lower costs. Instead of worrying about deploying and maintaining servers, you can use the cloud infrastructure to provide all the up-to-date resources needed to keep your applications running.

You focus on the code that matters most to you, in the most productive language for you, and Azure Functions handles the rest. For a list of supported languages, see [Supported languages in Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/supported-languages).

## Scenarios

Functions provides a comprehensive set of event-driven [triggers and bindings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings) that connect your functions to other services without having to write extra code.

The following list includes common integrated scenarios that use Functions.

| If you want to... | then... |
|---|---|
| [Process file uploads](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scenarios#process-file-uploads) | Run code when a file is uploaded or changed in blob storage. |
| [Process data in real time](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scenarios#real-time-stream-and-event-processing) | Capture and transform data from event and IoT source streams on the way to storage. |
| [Build AI-enabled apps](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scenarios#build-ai-enabled-apps) | Make data and APIs available to AI clients, and add AI reasoning to event-driven applications. |
| [Run scheduled task](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scenarios#run-scheduled-tasks) | Execute data clean-up code on predefined timed intervals. |
| [Build a scalable web API](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scenarios#build-a-scalable-web-api) | Implement a set of REST endpoints for your web applications using HTTP triggers. |
| [Build a serverless workflow](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scenarios#build-a-serverless-workflow) | Create an event-driven workflow from a series of functions using Durable Functions. |
| [Respond to database changes](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scenarios#respond-to-database-changes) | Run custom logic when a document is created or updated in a database. |
| [Create reliable message systems](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scenarios#create-reliable-message-systems) | Process message queues using Azure Queue Storage, Service Bus, or Event Hubs. |
| [Integrate with SaaS and business services](https://learn.microsoft.com/en-us/azure/azure-functions/functions-connectors-overview) | Use managed connectors to respond to events and call operations in services such as Microsoft 365, Teams, and SharePoint. |

These scenarios allow you to build event-driven systems using modern architectural patterns. For more information, see [Azure Functions scenarios](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scenarios).

## Development lifecycle

Functions supports you through every stage of app development:

1. **Code** in [C#, Java, JavaScript, PowerShell, Python, or Go](https://learn.microsoft.com/en-us/azure/azure-functions/supported-languages), or use [custom handlers](https://learn.microsoft.com/en-us/azure/azure-functions/functions-custom-handlers) for languages like Rust.
2. **Develop and debug** locally with [Visual Studio, Visual Studio Code, Maven, and other tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-local).
3. **Deploy** to Azure using [CLI, CI/CD pipelines, or your IDE](https://learn.microsoft.com/en-us/azure/azure-functions/functions-deployment-technologies).
4. **Monitor** performance and diagnose issues with built-in [Azure Monitor and Application Insights](https://learn.microsoft.com/en-us/azure/azure-functions/functions-monitoring) integration.

## Hosting options

Functions provides various [hosting options](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale) for your business needs and application workload.

| Hosting option | Description |
|---|---|
| [Flex Consumption plan](https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-plan) | **Recommended.** Fast event-driven scaling, virtual network integration, and pay-as-you-go billing. |
| [Premium plan](https://learn.microsoft.com/en-us/azure/azure-functions/functions-premium-plan) | Always-warm instances for the fastest response times, unlimited execution duration, and virtual network integration. |
| [Dedicated plan](https://learn.microsoft.com/en-us/azure/azure-functions/dedicated-plan) | Run functions in an existing App Service plan with predictable scaling and costs. |
| [Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/functions-overview) | Deploy fully customized containerized function apps alongside microservices in Azure Container Apps. |
| [Consumption plan](https://learn.microsoft.com/en-us/azure/azure-functions/consumption-plan) | Legacy serverless plan (Windows only). Use the Flex Consumption plan for new apps. |

For a detailed comparison, see [Azure Functions hosting options](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale).

## Related content

- [Azure Functions scenarios](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scenarios)
- [Get started with Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-get-started)

