import httpx
import asyncio
import plantuml

class PlantUMLGenerator:
    def __init__(self, server_url="http://localhost:8080/png"):
        self.server_url = server_url

    async def generate(self, plantuml_code):
        encoded_diagram = plantuml.deflate_and_encode(plantuml_code)
        print(encoded_diagram)
        url = f"{self.server_url}/{encoded_diagram}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            
            if response.status_code == 200:
                print("Valid diagram", response.status_code, response.headers['x-plantuml-diagram-description'])
            else:
                print("Wrong diagram", response.status_code)


if __name__ == "__main__":
    plantuml_code = """
    @startum
    Alice -> Bob: Hello
    @enduml
    """
    
    generator = PlantUMLGenerator()
    asyncio.run(generator.generate(plantuml_code))
