# Part3 Crew

Welcome to the Part3 Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

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

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/part_3/config/agents.yaml` to define your agents
- Modify `src/part_3/config/tasks.yaml` to define your tasks
- Modify `src/part_3/crew.py` to add your own logic, tools and specific args
- Modify `src/part_3/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:


```bash
panel serve src/part_3/ui_main.py --autoreload
```

This command initializes the part_3 Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## References

Reference materials used to create this example:

- Criteo Retail Media API [documentation](https://developers.criteo.com/retail-media/docs/welcome-to-criteo)
- CrewAI [documentation](https://docs.crewai.com)
- CrewAI [GitHub repository](https://github.com/joaomdmoura/crewai)
- Pydantic [documentation](https://docs.pydantic.dev/latest/)
- Poetry [documentation](https://python-poetry.org/docs/)
- ChainLit [Medium article](https://medium.com/@pratyush.talent/using-human-as-tool-with-crewai-in-chainlit-da063dea0e31) and [documentation](https://docs.chainlit.io/get-started/overview)
- Another chainglit [article](https://krishankantsinghal.medium.com/supercharge-your-conversational-ai-integrating-chainlit-and-crewai-for-powerful-interactions-ca8a50ec1851)
- [How to create an interactive ui for crewai](https://medium.com/gitconnected/how-to-create-an-interactive-ui-for-crewai-applications-e4d3fae0dbf8)