from openai import OpenAI

from strategy import Strategy

class APIChatGPT(Strategy):
    def __init__(self, api_key):

        self.client = OpenAI(
            api_key=api_key
        )
    
    def execute_query(self, query: str) -> dict:        
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "user", "content": query},
            ],
            # number of alternative completions
            n=1,
            # limitation for testing
            max_tokens=10
        )

        return {
            "query": query,
            "response" : completion
        }
    
    def execute_multiple_query(self, query: list[str]) -> list[dict]:
        completions = []
        
        for q in query:
            completions.append(self.execute_query(q))
            
        return completions