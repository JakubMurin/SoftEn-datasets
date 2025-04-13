import httpx
import asyncio
import plantuml
from enum import Enum

class ResponseStatus(Enum):
    BAD_REQUEST = 0
    EMPTY_DIAGRAM = -1
    NOT_SEQUENCE = -2
    

class PlantUMLValidation:
    
    def diagram_type(self):
        pass
    
    def __init__(self, server_url: str="http://localhost:8080", show_log: bool=False):
        self.server_url = server_url
        self.show_log = show_log
        
    async def async_validate(self, plantuml_code):
        encoded_diagram = plantuml.deflate_and_encode(plantuml_code)
                
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.server_url}/map/{encoded_diagram}")
            response_status = self.handle_response(response)
                
            if isinstance(response_status, int):
                return response_status

            if response_status is ResponseStatus.EMPTY_DIAGRAM or response_status is ResponseStatus.NOT_SEQUENCE:
                return False
            
            encoded_response = await client.post(f"{self.server_url}/coder", content=plantuml_code)
            if not encoded_response.text:
                return False
            
            response = await client.get(f"{self.server_url}/map/{encoded_response.text}")
            status = self.handle_response(response)
            return status if isinstance(status, int) else False


    def validate(self, plantuml_code: str):
        encoded_diagram = plantuml.deflate_and_encode(plantuml_code)
        
        response = httpx.get(f"{self.server_url}/map/{encoded_diagram}")
        response_status = self.handle_response(response)
                
        if isinstance(response_status, int):
            return response_status

        if response_status is ResponseStatus.EMPTY_DIAGRAM or response_status is ResponseStatus.NOT_SEQUENCE:
            return False
        
        encoded_response = httpx.post(f"{self.server_url}/coder", content=plantuml_code)
        if not encoded_response.text:
            return False
        
        response = httpx.get(f"{self.server_url}/map/{encoded_response.text}")
        status = self.handle_response(response)
        return status if isinstance(status, int) else False
        
    
    def handle_response(self, response: httpx.Response) -> ResponseStatus | int:
        if response.status_code == 200:
            if self.show_log:
                print("Valid diagram", response.status_code)
            return self.is_sequence_diagram(response.headers)
                
        if self.show_log:
            print("Wrong diagram", response.status_code)
        return ResponseStatus.BAD_REQUEST
                
    def is_sequence_diagram(self, headers: object) -> bool | int:
        """Check if it is sequence diagram by header from response and if it is returns number of participants, otherwise False."""
        
        try:
            header_arg = headers['x-plantuml-diagram-description']
        except KeyError:
            if self.show_log:
                print("Diagram is empty")
            return ResponseStatus.EMPTY_DIAGRAM
        
        if "participants" not in header_arg:
            if self.show_log:
                print("This is not sequence diagram!", header_arg)
            return ResponseStatus.NOT_SEQUENCE
        
        count = header_arg.split()[0].lstrip("(")
        if self.show_log:
            print(f"Sequence diagram with {count} participats")
        return int(count)
        

if __name__ == "__main__":
    plantuml_code = "@startuml\nAlice -> Bob: Hello\n@enduml"
    
    plantuml_validator = PlantUMLValidation(show_log=True)
    
    asyncio.run(plantuml_validator.async_validate(plantuml_code))
    plantuml_validator.validate(plantuml_code)