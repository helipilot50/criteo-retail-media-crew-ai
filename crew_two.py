from crewai import Agent, Crew, Process, Task
from tools.accounts import AccountsTool
from tools.auth import AuthTool
from tools.campaigns import CampaignsList
from tools.lineitems import (
    AuctionLineitems, 
    PreferredLineitems
)
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
    tools=[AccountsTool(token=token)],
    cache=True,
    verbose=True,
    max_retry_limit=2,
)
writer = Agent(
    role='Content Writer',
    goal='Craft engaging blog posts about the AI industry',
    backstory='A skilled writer with a passion for technology.',
    verbose=True
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

campaign_manager = Agent(
    role = 'Retail Media Campaign Manager',
    goal = 'Maintain retail media campaigns and lineitems including preferred lineitems and auction lineitems',
    backstory = 'You are the Retail Media Campaign Manager. You are responsible for managing campaigns for a retail media accounts.',
    allow_delegation=False,
    cache=True,
    verbose=True,
    max_retry_limit=2,
    tools=[CampaignsList(token=token),
           PreferredLineitems(token=token),
           AuctionLineitems(token=token)
        ],
)
    
accounts =  Task(
    description = 'List all the Retail Media accounts accessible to the account manager.',
    expected_output =  'A formatted list of accounts accessible to the account manager, including all relevant details.',
    agent=account_manager,
    
)
    
campaigns = Task(
    description = 'List all the Retail Media campaigns accessible to every account. Use the {accountId} of each account to get the campaigns and limit your iterations using the total items and total pages. Put the campaigns into a single table.',
    expected_output = 'A formatted list of campaigns for each {accountId}, including all relevant details.',
    agent=campaign_manager,
    context=[accounts]
)

write_campaigns = Task(
    description="""
    write the {campaigns} as a table in markdown format with the title 'Campaigns', 
    """,
    expected_output='1 table in Markdown format',
    agent=writer,
    asynch=True,
    context=[campaigns],
    tools=[DirectoryReadTool(directory='./output'), FileReadTool()],
    output_file='output/chapter-2-campaigns.md'  
)
    

# auction_lineitems = Task(
#     description = 'List all the Retail Media auction lineitems accessible for every campaign. Use the {campaignId} of each campaign to get the lineitems.',
#     expected_output = 'A formatted list of lineitems accessible for each {campaignId}, including all relevant details.',
#     agent=campaign_manager,
#     asynch=True,
#     context=[campaigns]
# )

# preferred_lineitems = Task(
#     description = 'List all the Retail Media preferred lineitems accessible for every campaign. Use the {campaignId} of each campaign to get the lineitems.',
#     expected_output = 'A formatted list of lineitems accessible for each {campaignId}, including all relevant details.',
#     agent=campaign_manager,
#     asynch=True,
#     context=[campaigns]
# )


# write_lineitems = Task(
#     description="""
#     If there are preferred lineitems write the preffered {PreferredLineitems} as a table in markdown format with the title 'Preferred Lineitems' else write 'No Preferred Lineitems', 
#     if there are auction lineitems write the auction {Auctionlineitems} as a table in markdown format with the title 'Auction Lineitems' else write 'No Auction Lineitems',
#     """,
#     expected_output='3 tables in Markdown format',
#     agent=writer,
#     context=[preferred_lineitems, auction_lineitems],
#     tools=[DirectoryReadTool(directory='./output'), FileReadTool()],
#     output_file='output/chapter-2-lineitems.md'  
# )


    
crew =  Crew(
    agents=[account_manager],
    tasks=[accounts, campaigns, write_campaigns], #, preferred_lineitems, auction_lineitems, write_lineitems],
    process=Process.sequential,
    verbose=True,
)
