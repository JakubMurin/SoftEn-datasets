import json
import httpx
import re
import os

import time

from plantuml_validation import PlantUMLValidation

class PlantumlFiles:
    """A class used to fetch plantuml file, validate it and save with metadata"""
    
    def __init__(self, output_file_path: str | None=None, validation_url: str="http://localhost:8080"):
        self.validation = PlantUMLValidation(validation_url)
        
        if output_file_path is None:
            self.output_file_path = "sequence_diagrams.jsonl"
            with open(self.output_file_path, "w", encoding="utf-8") as file:
                pass
        else:
            self.output_file_path = output_file_path
            
    
    def fetch_diagram(self, url: str) -> str:
        """Fetch diagram from provided url. Url must contain only diagram.
        
        :Returns: string containing diagram if status is 200 otherwise empty sting 
        """
        
        response = httpx.get(url)
        
        if response.status_code != 200:
            print(f"URL {url} failed with status code {response.status_code}")
            return ""
        
        return response.text
        
    def prepare_json(self, diagram: str, source_url: str | None, participants: int=0) -> str:
        
        github_repository = self.get_repo_name_github(source_url) if source_url is not None else ""
        # pouzit regex na medzery
        num_of_actors = diagram.count("\nactor ")
        title = self.get_diagram_title(diagram)
        
        return_object = {"title": title,
                         "actors": num_of_actors,
                         "num_of_participats": participants,
                         "repo": github_repository,
                         "diagram_source_url": source_url,
                         "sequence_diagram": diagram}
        
        return json.dumps(return_object)
    
    def prosess_diagram(self, diagram, url=""):
        num_of_participats = self.validation.validate(diagram)
                
        if not num_of_participats:
            return
        
        return self.prepare_json(diagram, url, num_of_participats)
    
    def process_urls(self, file_path: str):
        output_file = open(self.output_file_path, "a", encoding="utf-8")
        
        with open(file_path, "r", encoding="utf-8") as urls_file:
            for url in urls_file:
                url = url.strip()
                diagram = self.fetch_diagram(url)
                if not diagram:
                    continue
                
                json_object = self.prosess_diagram(diagram, url)
                
                if not json_object:
                    continue
                
                print(json_object, file=output_file)
                 
        output_file.close()
        
    def get_repo_name_github(self, url: str) -> str:
        return "/".join(url.split("/")[3:5])
    
    def get_diagram_title(self, diagram: str) -> str:
        line = re.search(r"^title .*", diagram, flags=re.MULTILINE)
        return line.group().lstrip("title").strip().strip('"') if line else ""
        
if __name__ == "__main__":
    WORKING_DIR = os.getcwd()
    SEQUENCE_GIT_URLS = os.path.join(WORKING_DIR, "github\\scripts\\output.txt")
    
    plantuml_files = PlantumlFiles()
    start = time.perf_counter()
    plantuml_files.process_urls(SEQUENCE_GIT_URLS)
    end = time.perf_counter()
    print(end - start, (end - start)/30, sep="\n")
