![CrewAI and Criteo](../images/crewai-criteo-transparent.png)
# Part1 Crew

Welcome to the Part 1 of the Criteo Retail Media API, powered by [crewAI](https://crewai.com). This is a simple example showing how to:

- Obtain an Accress token using client credentials
- Call the **Accounts** API to get a list of Accounts
- Call the **Brands** API to get a list of Brands
- Call the **Retailers** API to get a list of Retailer
- Perform super simple analytics

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:

```bash
poetry lock
```

```bash
poetry install
```

### Customizing

**Add these environment variables into the `.env` file**
```
CRITEO_CLIENT_ID=
CRITEO_CLIENT_SECRET=

RETAIL_MEDIA_API_URL=https://api.criteo.com/2024-07/retail-media/

# only if you use Azure
AZURE_OPENAI_API_KEY=
ZURE_OPENAI_DEPLOYMENT=
AZURE_API_KEY=
AZURE_API_BASE=
AZURE_API_VERSION=

# only if you use GROQ
GROQ_API_KEY=
```

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ poetry shell
$ crewai run
```

or

```bash
$ poetry shell
poetry run part_1
```

This command initializes the part-1 Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The part-1 Crew is composed of a single AI agents, with unique roles, goals, and tools. These agent performs on a series of tasks, defined in `config/tasks.yaml`, leveraging it's skills to achieve complex objective. The `config/agents.yaml` file outlines the capabilities and configurations of the agent in the crew.


