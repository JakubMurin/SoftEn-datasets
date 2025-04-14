import json
import httpx
import re
import os
from datetime import date

import time

from plantuml_validation import PlantUMLValidation
from utils import *

class PlantumlFiles:
    """A class used to fetch plantuml file, validate it and save with metadata"""
    
    def __init__(self, output_file_name: str, working_dir: str | None=None, validation_url: str="http://localhost:8080"):
        self.validation = PlantUMLValidation(validation_url)
        
        self.working_dir = os.getcwd() if working_dir is None else working_dir
        self.output_file_path = os.path.join(self.working_dir, output_file_name)
            
    
    def fetch_diagram(self, url: str) -> str:
        """
        Fetch diagram from provided url. Url must contain only diagram.
        
        :Returns: string containing diagram if status is 200 otherwise empty sting 
        """
        
        response = httpx.get(url)
        
        if response.status_code != 200:
            print(f"URL {url} failed with status code {response.status_code}")
            return ""
        
        return response.text
        
    def prepare_object(self, origin: Origin, source_url: str | None, title: str="", participants: int=0, num_of_actors: int=0, fragments: list[str]=[], temperature: float=1, top_p: float=1) -> dict:
        
        file_categ = FileNames.GENERATED_SEQUENCE_DIAGRAM.value if Origin is Origin.CHAT_GPT else FileNames.SEQUENCE_DIAGRAM.value
        id = get_next_file_index(os.path.join(self.working_dir, file_categ))
        file = f"{id:0{5}}_{file_categ}.puml"
        current_date = str(date.today())
        github_repository = self.get_repo_name_github(source_url) if source_url is not None else ""
        
        return_object = {
                         "id": id,
                         "file": file,
                         "date": current_date,
                         "origin": origin.value,
                         "source_url": source_url,
                         "repo": github_repository,
                         "temperature": temperature,
                         "top_p": top_p,
                         "actors": num_of_actors,
                         "num_of_participats": participants,
                         "title": title,
                         "fragments": fragments,
                        }
        
        return return_object
    
    def prosess_diagram(self, diagram: str, origin: Origin=Origin.GITHUB, url="", temperature: float=1, top_p: float=1):
        num_of_participats = self.validation.validate(diagram)
                
        if not num_of_participats:
            return
        
        # pouzit regex na medzery
        num_of_actors = diagram.count("\nactor ")
        title = self.get_diagram_title(diagram)
        fragments = self.get_diagram_fragments(diagram)
        
        seq_data = self.prepare_object(origin, url, title, num_of_participats, num_of_actors, fragments, temperature, top_p)
        
        file_categ = FileNames.GENERATED_SEQUENCE_DIAGRAM.value if Origin is Origin.CHAT_GPT else FileNames.SEQUENCE_DIAGRAM.value
        seq_file_path = os.path.join(self.working_dir, file_categ, seq_data["file"])
        with open(seq_file_path, "w", encoding="utf-8") as seq_file:
            print(diagram, file=seq_file)
        
        return seq_data
    
    def process_urls(self, file_path: str):
        output_file = open(self.output_file_path, "a", encoding="utf-8")
        
        with open(file_path, "r", encoding="utf-8") as urls_file:
            for url in urls_file:
                url = url.strip()
                diagram = self.fetch_diagram(url)
                if not diagram:
                    continue
                
                json_object = self.prosess_diagram(diagram, url=url)
                
                if not json_object:
                    continue
                
                print(json.dumps(json_object), file=output_file)
                 
        output_file.close()
        
    def get_repo_name_github(self, url: str) -> str:
        return "/".join(url.split("/")[3:5])
    
    def get_diagram_title(self, diagram: str) -> str:
        line = re.search(r"^title .*", diagram, flags=re.MULTILINE)
        return line.group().lstrip("title").strip().strip('"') if line else ""
    
    def get_diagram_fragments(self, diagram: str) -> list[str]:
        # TODO
        return []
        
if __name__ == "__main__":
    WORKING_DIR = os.getcwd()
    SEQUENCE_GIT_URLS = os.path.join(WORKING_DIR, "github\\scripts\\output.txt")
    
    plantuml_files = PlantumlFiles("seq.jsonl", os.path.join(WORKING_DIR, "data", "results"))
    start = time.perf_counter()
    plantuml_files.process_urls(SEQUENCE_GIT_URLS)
    end = time.perf_counter()
    print(end - start, (end - start)/30, sep="\n")