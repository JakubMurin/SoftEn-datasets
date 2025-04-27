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
            
    
    def fetch_diagram(self, url: str, second_try: bool=False) -> str:
        """
        Fetch diagram from provided url. Url must contain only diagram.
        
        :Returns: string containing diagram if status is 200 otherwise empty sting 
        """
        try:
            response = httpx.get(url)
        
            if response.status_code != 200:
                print(f"URL {url} failed with status code {response.status_code}")
                return ""
        
            return response.text
        
        except httpx.ReadTimeout:
            if not second_try:
                return self.fetch_diagram(url, True)
            
            print(f"Timed out: {url}")
            
        except httpx.ConnectError as e:
            print(f"Connection refused at: {url}")
            raise e
        
    def prepare_object(self, origin: Origin, source_url: str | None, create_date: str | None=None, title: str="", participants: int=0, num_of_actors: int=0, fragments: dict[str, int]={}, ai_model: str="", temperature: float=0, top_p: float=1) -> dict:
        
        file_categ = FileNames.GENERATED_SEQUENCE_DIAGRAM.value if origin is Origin.CHAT_GPT else FileNames.SEQUENCE_DIAGRAM.value
        id = get_next_file_index(os.path.join(self.working_dir, file_categ))
        file = f"{file_categ}\\{id:0{5}}_{file_categ}.puml"
        create_date = create_date if create_date is not None else str(date.today())
        github_repository = self.get_repo_name_github(source_url) if source_url is not None else ""
        
        return_object = {
                         "id": id,
                         "file": file,
                         "date": create_date,
                         "origin": origin.value,
                         "source_url": source_url,
                         "repo": github_repository,
                         "ai_model": ai_model,
                         "temperature": temperature,
                         "top_p": top_p,
                         "actors": num_of_actors,
                         "num_of_participats": participants,
                         "title": title,
                         **fragments,
                        }
        
        return return_object
    
    def process_diagram(self, diagram: str, origin: Origin=Origin.GITHUB, url="", create_date: str|None=None, ai_model: str="", temperature: float=0, top_p: float=0):
        num_of_participats = self.validation.validate(diagram)
                
        if not num_of_participats:
            return
        
        num_of_actors = len(re.findall(r"^ *actor ", diagram, re.MULTILINE))
        title = self.get_diagram_title(diagram)
        fragments = self.get_diagram_fragments(diagram)
        
        seq_data = self.prepare_object(origin, url, create_date, title, num_of_participats, num_of_actors, fragments, ai_model, temperature, top_p)
        
        seq_file_path = os.path.join(self.working_dir, seq_data["file"])
        with open(seq_file_path, "w", encoding="utf-8") as seq_file:
            print(diagram, file=seq_file)
        
        return seq_data
    
    def process_urls(self, file_path: str):
        output_file = open(self.output_file_path, "a", encoding="utf-8")
        
        with open(file_path, "r", encoding="utf-8") as urls_file:
            for line in urls_file:
                line = line.split()
                url = line[0]
                create_date = line[1] if len(line) == 2 else ""
                diagram = self.fetch_diagram(url)
                if not diagram:
                    continue
                
                json_object = self.process_diagram(diagram, url=url, create_date=create_date)
                
                if not json_object:
                    continue
                
                print(json.dumps(json_object), file=output_file)
                 
        output_file.close()
        
    def get_repo_name_github(self, url: str) -> str:
        return "/".join(url.split("/")[3:5])
    
    def get_diagram_title(self, diagram: str) -> str:
        line = re.search(r"^title .*", diagram, flags=re.MULTILINE)
        return line.group().lstrip("title").strip().strip('"') if line else ""
    
    def get_diagram_fragments(self, diagram: str) -> dict[str, str]:
        num_of_alt = len(re.findall(r"^ *alt ", diagram, re.MULTILINE))
        num_of_opt = len(re.findall(r"^ *opt ", diagram, re.MULTILINE))
        num_of_loop = len(re.findall(r"^ *loop ", diagram, re.MULTILINE))
        return {
            "num_of_alt": num_of_alt,
            "num_of_opt": num_of_opt,
            "num_of_loop": num_of_loop
        }
        
if __name__ == "__main__":
    WORKING_DIR = os.getcwd()
    SEQUENCE_GIT_URLS = os.path.join(WORKING_DIR, "github", "new_seq_url_date.txt")
    
    plantuml_files = PlantumlFiles("seq.jsonl", os.path.join(WORKING_DIR, "data", "results"))
    start = time.perf_counter()
    plantuml_files.process_urls(SEQUENCE_GIT_URLS)
    end = time.perf_counter()
    print(end - start, (end - start)/2208, sep="\n")