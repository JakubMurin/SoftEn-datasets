from dotenv import load_dotenv
from os import environ

from .api_chatgpt import APIChatGPT
from .selenium_chatgpt import SeleniumChatGPT


class Context:
    def __init__(self, strategy: str = None):
        load_dotenv()
        
        if strategy is None:
            strategy = environ["STRATEGY"]
        
        if strategy == "api":
            api_key = environ["OPENAI_API_KEY"]
            self.ai_model = environ["AI_MODEL"]
            strategy_class = APIChatGPT(api_key, self.ai_model)
            print(f"Used method: API\t\tmodel:{self.ai_model}")
            
        elif strategy == "selenium":
            strategy_class = SeleniumChatGPT()
            print("Used method: Selenium")
            
        else:
            raise NameError(f"Strategy '{strategy}' doesn`t exist!")
        
        self.strategy = strategy_class

    def execute_query(self, query: str | list[str], promt_ctx: list[dict[str, str]]=[], temperature: float=1, top_p: float=1) -> list[dict]:
        if isinstance(query, str):
            return [self.strategy.execute_query(query, promt_ctx, temperature, top_p)]
        
        return self.strategy.execute_multiple_query(query, promt_ctx, temperature, top_p)

if __name__ == "__main__":

    context = Context()
    
    # query = "Generate longer usecase XML and plantuml source code for corresponding sequence diagram without any your comments"
    query = """
    Suggest a better version of the question in quotes to use instead and show it at beggining of response.
    
    "Generate use case for this sequence diagram without any comments:"
    @startuml
participant "Language SDK" order 10
box "Engine"
participant "Resource Monitor" order 15
participant "Step Generator" order 20
participant "Step Executor" order 25
end box
participant "Resource Provider" order 30

"Language SDK" -> "Resource Monitor" ++ : RegisterResourceRequest(type, name, inputs, options)
"Resource Monitor" -> "Step Generator" ++ : RegisterResourceEvent(type, name, inputs, options)
"Step Generator" -> "Resource Provider" ++ : CheckRequest(type, inputs, old inputs)
"Step Generator" <- "Resource Provider" -- : CheckResponse(inputs', failures)
"Step Generator" -> "Resource Provider" ++ : DiffRequest(type, inputs', old state)
"Step Generator" <- "Resource Provider" -- : DiffResponse(diffs)
"Step Generator" -> "Step Executor" --++ : SameStep(inputs', old state, options)
note left
	This is fire-and-forget on the part of the step generator.
	The step will run in parallel with steps for other resources.
end note
"Resource Monitor" <- "Step Executor" -- : done(old state)
"Language SDK" <- "Resource Monitor" -- : RegisterResourceResponse(urn, ID, old tate)
@enduml
"""
    multi_query = ["introduce self", "what is pyhton"]
    
    result = context.execute_query(query)[0]
    # print("Single query:", repr(result))
    print(result["choices"][0]["message"]["content"])
    
    # result = context.execute_query(multi_query)
    # print("Multiple query:", result)
