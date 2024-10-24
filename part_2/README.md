![CrewAI and Criteo](../images/crewai-criteo-transparent.png)
# Part 2 Crew [WORK IN PROGRESS]

Welcome to the Part2 Crew project, powered by [crewAI](https://crewai.com).

This part creates a Crew to:

1. Retrieve the first 100 campaigns for an account
2. Use campaigns with a budget to create a pie chart with using the campaign budget
3. Create a report about the campaigns budget, including the chart

## Installation

Ensure you have Python >=3.12 <=3.13 installed on your system. This part uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
or
pipx install poetry
```

## Clone the repository

The reporitory is hosted in GitHub, use this command to clone the repo:

```
git clone https://github.com/helipilot50/criteo-retail-media-crew-ai.git
```

Navigate to the repo and change directory to `part_2`

```
cd part_2
```

Next, install the dependencies:

```bash
poetry install 
```

and finally invoke the shell

```
poetry shell
```

## Running Part 2

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the part_2 Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The part_2 Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

### Agents

- **campaign_manager** - Reads campaigns for a specific account
- **visualizer_agent** - Visualize campaign data
- **campaign_reporter_agent** - Report writer for campaign data

### Tasks

- **fetch_campaigns_task** - Gets a collection campaigns for a specific account {account_id}.
  Use the page index and page size parameters to get the first 100 campaigns for the account, and ignore the campaign if the budget is not provided or is less than 1.
- **campaigns_budget_pie_chart** - Creates a pie chart from the budget data in the campaigns collection.
- **campaigns_report** - Creates a report in Markdown format, with the data from the campaigns collection. It has a table with the campaign name, start date, budget, and budgetSpent and a pie chart of the campaign budgets.

### Tools

Tools are used by agents and tasks to acomplish work or use knowledge that the LLM models _are not trained for_, such as proprietary information. In this case, to access Criteo's APIs and use MatPlotLib to draw charts.

The custom tools for this part are are located in the `tools` directory.

## References

Reference materials used to create this example:

- Criteo Retail Media API [documentation](https://developers.criteo.com/retail-media/docs/welcome-to-criteo)
- CrewAI [documentation](https://docs.crewai.com)
- CrewAI [GitHub repository](https://github.com/joaomdmoura/crewai)
- Pydantic [documentation](https://docs.pydantic.dev/latest/)
- Poetry [documentation](https://python-poetry.org/docs/)
