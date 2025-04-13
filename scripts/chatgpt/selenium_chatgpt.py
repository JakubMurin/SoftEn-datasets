from .libs.selenium_chat import ChatGPTAutomation

from .strategy import Strategy

class SeleniumChatGPT(Strategy):
    def __init__(self):
        # Define the path where the chrome driver is installed on your computer
        self.chrome_driver_path = r""

        # the syntax r'"..."' is required because the space in "Program Files" in the chrome path
        self.chrome_path = r'""'
    
    def execute_query(self, query: str) -> dict:
        chatgpt = ChatGPTAutomation(self.chrome_path, self.chrome_driver_path)
        
        chatgpt.send_prompt_to_chatgpt(query)
        completion = chatgpt.return_last_response()
        
        chatgpt.quit()
        
        return {
            "query": query,
            "response" : completion
        }
    
    def execute_multiple_query(self, query: list[str]) -> list[dict]:
        completions = []
        
        chatgpt = ChatGPTAutomation(self.chrome_path, self.chrome_driver_path)
        
        for q in query:
            chatgpt.send_prompt_to_chatgpt(q)
            completion = chatgpt.return_last_response()
            
            completions.append({
                "query": query,
                "response" : completion
            })
    
        chatgpt.quit()
        
        return completions
