def choose_llm():

    options = ["groq", "ollama","openai", "azure"]

    print("Please select an LLM provider:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")



    while True:
        try:
            choice = input(f"Enter the number of your LLM (default is 1): ")
            if choice == "" :
                return options[0]
            choice = int(choice)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")




