import httpx
import asyncio
import plantuml
import time
import requests
from enum import Enum

class DiagramType(Enum):
    SEQUENCE = "participants"
    USE_CASE = "entities" #class, component, state, object, deployment
    ACTIVITY = "activity"
    

class PlantUMLValidation:
    
    def diagram_type(self):
        pass
    
    def __init__(self, server_url: str="http://localhost:8080", show_log: bool=False):
        self.server_url = server_url
        self.show_log = show_log
        
    async def async_validate(self, plantuml_code):
        start = time.perf_counter()
        encoded_diagram = plantuml.deflate_and_encode(plantuml_code)
        end = time.perf_counter()
        print("plantuml encoding time:", end - start)
                
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.server_url}/map/{encoded_diagram}")
            
            final_end = time.perf_counter()
            print("total time async:", final_end - start)
            
            if response.status_code == 200:
                if self.show_log:
                    print("Valid diagram", response.status_code, response.headers['x-plantuml-diagram-description'])
                return
            
            if self.show_log:
                print("Wrong diagram", response.status_code)
            return False

    def validate(self, plantuml_code:str):
        start = time.perf_counter()
        encoded_diagram = plantuml.deflate_and_encode(plantuml_code)
        end = time.perf_counter()
        print("plantuml encoding time:", end - start)
        
        response = requests.get(f"{self.server_url}/map/{encoded_diagram}")
        
        if response.status_code == 200:
            print("Valid diagram", response.status_code, response.headers['x-plantuml-diagram-description'])
        else:
            print("Wrong diagram", response.status_code)
                
        final_end = time.perf_counter()
        print("total time:", final_end - start)
        

if __name__ == "__main__":
    plantuml_code = "@startuml\nAlice -> Bob: Hello\n@enduml"
    
    plantuml_validator = PlantUMLValidation()
    
    asyncio.run(plantuml_validator.async_validate(plantuml_code))
    plantuml_validator.validate(plantuml_code)
