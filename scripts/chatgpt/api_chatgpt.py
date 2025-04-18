from openai import OpenAI

from . import strategy

class APIChatGPT(strategy.Strategy):
    def __init__(self, api_key, model="gpt-3.5-turbo-0125"):
        self.model = model

        self.client = OpenAI(
            api_key=api_key
        )
    
    def execute_query(self, query: str, promt_ctx: list[dict[str, str]]=[], temperature: float=1, top_p: float=1) -> dict:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                *promt_ctx,
                {"role": "user", "content": query},
            ],
            # number of alternative completions
            n=1,
            # limitation for testing
            # max_tokens=10
            temperature=temperature,
            top_p=top_p
        )

        return completion.model_dump()
    
    def execute_multiple_query(self, query: list[str], promt_ctx: list[dict[str, str]]=[]) -> list[dict]:
        completions = []
        
        for q in query:
            completions.append(self.execute_query(q, promt_ctx))
            
        return completions