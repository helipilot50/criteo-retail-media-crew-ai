from crewai import Agent, Crew, Process, Task
from tools.accounts import AccountsTool, BrandsTool, RetailersTool
from tools.auth import AuthTool
from tools.search import SearchTools

from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
)

auth = AuthTool()
auth_response = auth._run()
token = auth_response['access_token']

account_manager = Agent(
    role = 'Retail Media Account Manager',
    goal = 'List and maintain retail media accounts including brands, retailers and campaigns.',
    backstory = 'You are the Retail Media Account Manager. You are responsible for managing all retail media accounts.',
    allow_delegation=False,
    cache=True,
    verbose=True,
    max_retry_limit=2,
    # tools=[
    #     AccountsTool(token=token),
    #     RetailersTool(token=token),
    #     BrandsTool(token=token)],
    max_iter = 2
)
writer = Agent(
    role='Content Writer',
    goal='Craft beautiful makrdown documents for the Retail Media accounts, retailers and brands.',
    backstory='A skilled writer with a passion for technology.',
    verbose=True
)


researcher = Agent(
    role = 'Company Researcher',
    goal = 'Analyze company {company_name} industry trends, competitor activities, and popular hashtags on Linkedin. And perform research on the latest trends, hashtags, and competitor activities using your Search tools.',
    backstory = 'Armed with a keen eye for digital trends and a deep understanding of the Linkedin landscape, you excel at uncovering actionable insights from social media data. Your analytical skills are unmatched, providing a solid foundation for strategic decisions in content creation. You are great at identifying the latest trends and the best hashtags for a given campaign.',
    tools=[
        SearchTools.search_internet,
        SearchTools.search_linkedin,
        SearchTools.search_instagram,
        SearchTools.open_page,
    ],
    allow_delegation=False,
    cache=True,
    verbose=True,
)

analyst = Agent(
            
    role='Campaign Performance Analyst',
    goal="""
        Analyse active lineitems and campaigns. 
        Discover underperforming campaigns and lineitems. 
        Provide recommendations to improve performance.
        """,
    backstory = """
        You're the most experienced online advertising analyst with an indepth backgroud in retail and online advertising.
        You combine various analytical insights to formulate
        strategic campaign performance advice. You are now working for
        a super important customer you need to impress.
        You are passionate about data and  work with leading edge technologies in online industry:
        You have 7 years experience in Data Science or Data Analytics
        Masters degree or higher in a quantitative field (Engineering, Mathematics, Computer Science, Physics, etc.)
        Fluency in the core toolkit of Data Science/Data Analytics, SQL, Python, Spark, etc. 
        Outstanding analytical skills: passion for translating data-speak into relevant, compelling stories
        A background in the digital industry or consulting is a plus
        You have the combination of technical skills, passion for learning, and the soft skills to work with all personality types in a dynamic environment
        You are fluent in English
        """,

        allow_delegation=False,
        cache=True,
        verbose=True,
)
    
accounts =  Task(
    description = 'List all the Retail Media accounts accessible to the account manager.',
    expected_output =  'A formatted list of accounts accessible to the account manager, including all relevant details.',
    agent=account_manager,
    tools=[AccountsTool(token=token)],
    
)
    
account_retailers = Task(
    description = 'List all the Retail Media retailers accessible for an account. Use the {accountId} to get the retailers .',
    expected_output = 'A formatted list of retailers accessible to an account, including all relevant details.',
    agent=account_manager,
    tools=[RetailersTool(token=token)],
    context=[accounts]
)

account_brands = Task(
    description = 'List all the Retail Media brands accessible for an account. Use the {accountId} to get the brands.',
    expected_output = 'A formatted list of brands accessible to an account, including all relevant details.',
    agent=account_manager,
    tools=[BrandsTool(token=token)],
    context=[accounts]
)

# writers
write_accounts = Task(
    description='Write the {accounts} as a table in markdown format with the title "Accounts"',
    expected_output='Markdown with a table for accounts',
    agent=writer,
    context=[accounts],
    tools=[DirectoryReadTool(directory='./output'), FileReadTool()],
    output_file='output/chapter-1-accounts.md'  
)

write_retailers = Task(
    description='Write the {retailers}  as a table in markdown format with the title "Retailers"',
    expected_output='Markdown table for retailers',
    agent=writer,
    context=[account_retailers],
    tools=[DirectoryReadTool(directory='./output'), FileReadTool()],
    output_file='output/chapter-1-retailers.md'  
)

write_brands = Task(
    description='Write the {brands} as a table in markdown format with the title "Brands"',
    expected_output='Markdown document with a table for brands',
    agent=writer,
    context=[account_brands],
    tools=[DirectoryReadTool(directory='./output'), FileReadTool()],
    output_file='output/chapter-1-brands.md'  
)

    
crew =  Crew(
    agents=[account_manager, writer],
    tasks=[accounts,  account_retailers, account_brands, write_retailers, write_brands, write_accounts],
    process=Process.sequential,
    verbose=True,
)