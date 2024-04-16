from dotenv import load_dotenv
from os import environ

from api_chatgpt import APIChatGPT
from selenium_chatgpt import SeleniumChatGPT


class Context:
    def __init__(self, strategy: str = None):
        load_dotenv()
        
        if strategy is None:
            strategy = environ["STRATEGY"]
        
        if strategy == "api":
            api_key = environ["OPENAI_API_KEY"]
            strategy_class = APIChatGPT(api_key)
            print("Used method: API")
            
        elif strategy == "selenium":
            strategy_class = SeleniumChatGPT()
            print("Used method: Selenium")
            
        else:
            raise NameError(f"Strategy '{strategy}' doesn`t exist!")
        
        self.strategy = strategy_class

    def execute_query(self, query: str | list[str]):
        if isinstance(query, str):
            return self.strategy.execute_query(query)
        
        return self.strategy.execute_multiple_query(query)

if __name__ == "__main__":

    context = Context("selenium")
    
    query = "generate use case"
    multi_query = ["introduce yourself", "what is pyhton"]
    
    result = context.execute_query(query)
    print("Single query:", repr(result))
    
    result = context.execute_query(multi_query)
    print("Multiple query:", result)
