from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.accounts import AccountsTool, BrandsTool, RetailersTool
from tools.auth import AuthTool
from tools.search import SearchTools

auth = AuthTool()
auth_response = auth._run()
token = auth_response['access_token']

@CrewBase
class RetailMediaCrew():
    """Retail Media Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def account_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['account-manager'],
						tools=[AccountsTool(token=token), RetailersTool(token=token), BrandsTool(token=token)],
            allow_delegation=False,
						verbose=True
        )
    @agent
    def company_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['company_researcher'],
            tools=[
              SearchTools.search_internet,
              SearchTools.search_linkedin,
              SearchTools.search_instagram,
              SearchTools.open_page,
            ],
            allow_delegation=False,
            verbose=True
        )
    
    @task
    def my_accounts(self) -> Task:
        return Task(
            config=self.tasks_config['list_my_accounts_task'],
            agent=self.account_manager()
        )
    
    
    @task
    def account_retailers(self) -> Task:
        return Task(
            config=self.tasks_config['list_retailers_for_an_account_task'],
            agent=self.account_manager(),
        )
    
    # @task
    # def account_brands(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['list_brands_for_an_account_task'],
    #         agent=self.account_manager(),
    #     )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Retail Media crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )