import json
from chainlit import ChainlitApp, ChainlitTask
from part_3.crew import Part3Crew

from dotenv import load_dotenv

load_dotenv()

# Define a Chainlit task
class CrewAITask(ChainlitTask):
    def run(self):
        inputs = {"accountId": "26", "startDate": "2023-01-01", "endDate": "2023-01-31"}
    
        # Execute the CrewAI task
        result = Part3Crew().crew().kickoff(inputs=inputs)
        result_output = result.output_json
        
        # Return the output in JSON format
        return json.dumps(result_output, indent=2)

# Create a Chainlit app
app = ChainlitApp()

# Add the CrewAI task to the Chainlit app
app.add_task(CrewAITask())

# Run the Chainlit app
if __name__ == "__main__":
    app.run()
