from crewai import Task
from textwrap import dedent



class RetailMediaTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    # def shom_me (self, agent, var1, var2):
    #     return Task(
    #         description=dedent(
    #             f"""
    #         Do something as part of task 1
            
    #         {self.__tip_section()}
    
    #         Make sure to use the most recent data as possible.
    
    #         Use this variable: {var1}
    #         And also this variable: {var2}
    #     """
    #         ),
    #         agent=agent,
    #     )

    def show_my_accounts(self, agent):
        return Task(
            description=dedent(
                f"""
            Find all the Retail Media Accounts I can access and output them.
                                       
            {self.__tip_section()}

            Make sure to format the output as a table
        """
            ),
            agent=agent,
        )