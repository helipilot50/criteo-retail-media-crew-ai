from crewai_tools import SerperDevTool

# Initialize the tool for internet searching capabilities
tool = SerperDevTool()


def test_search():
    # Search for the term "CrewAI" on the internet
    results = tool.run(search_query="jimmy carr tour 2025")

    # Check if the search results are not empty
    assert len(results) > 0

    print("search results",results)