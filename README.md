# Criteo Relail Media API and CrewAI 
![](images/crewai-criteo-transparent.png)

This is the companion code to Medium articles than explain how to use CrewAI with Criteo's Retail Media API

## Before you begin

Take these steps to setup these code examples

### Prerequisites

Ensure you have Python >=3.12 <=3.13 installed on your system. This part uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
or
pipx install poetry
```

### Clone the repository

The reporitory is hosted in GitHub, use this command to clone the repo:

```
git clone https://github.com/helipilot50/criteo-retail-media-crew-ai.git
```

## Companion code parts

The repository is divided into several parts, one for each medium article. Each part is a mini project and is self-contained; therefore, it is not dependent on another part.

### [Part 1](part_1/README.md)

A simple example of CrewAI using tools to call Retail Media APIs for:

- Accounts
- Brands
- Retailers

It is an introduction that demonstrates the technology needed and a basic project setup

### [Part 2](part_2/README.md)

A more complex Crew that creates a budget report on Campaigns for a specific Account.

It uses custom tools to:

- Access Campaigns
- Create charts

This crew has several tasks that culminate in the final report
