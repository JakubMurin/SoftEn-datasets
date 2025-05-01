import json
import os
from datetime import date

import time

from xml_validation import XmlValidation, XmlParams
from utils import *


class XmlFiles:
    """A class used to fetch usecase file, validate it and save with metadata"""
    
    def __init__(self, output_file_name: str, validation_schema_path: str, working_dir: str | None=None):
        self.validation = XmlValidation(validation_schema_path)
        
        self.working_dir = os.getcwd() if working_dir is None else working_dir
        self.output_file_path = os.path.join(self.working_dir, output_file_name)
        
    def prepare_object(self, origin: Origin, source_url: str | None, params: XmlParams, create_date: str | None=None, ai_model: str="", temperature: float=0, top_p: float=0) -> dict:
        
        file_categ = FileNames.GENERATED_USECASE.value if origin is Origin.CHAT_GPT else FileNames.USECASE.value
        id = get_next_file_index(os.path.join(self.working_dir, file_categ))
        file = f"{file_categ}\\{id:0{5}}_{file_categ}.xml"
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
                         "title": params.title,
                         "actors": params.actors,
                         "num_of_steps": params.num_of_steps,
                         "num_of_alt_scenarions": params.num_of_alt_scenarions,
                         "num_of_err_scenarions": params.num_of_err_scenarions,
                        }
        
        return return_object
    
    def process_usecase(self, usecase: str, origin: Origin=Origin.GITHUB, url="", create_date: str | None=None, ai_model: str="", temperature: float=0, top_p: float=0):
        params = self.validation.validate(usecase)
                
        if not params:
            return
        
        uc_data = self.prepare_object(origin, url, params, create_date, ai_model, temperature, top_p)
        
        uc_file_path = os.path.join(self.working_dir, uc_data["file"])
        with open(uc_file_path, "w", encoding="utf-8") as uc_file:
            print(usecase, file=uc_file)
        
        return uc_data
    
    def process_files(self, dir_path: str, url_date_path: str=""):
        output_file = open(self.output_file_path, "a", encoding="utf-8")
        
        url_date = []
        if url_date_path:
            with open(url_date_path, "r", encoding="utf-8") as file:
                for l in file:
                    url_date.append(l.strip().split())
        
        
        for i, file_path in enumerate(get_all_files(dir_path)):
        
            with open(file_path, "r", encoding="utf-8") as uc_file:
                usecase = uc_file.read()

                url, create_date = url_date[i] if len(url_date) > i else ("", "")
                json_object = self.process_usecase(usecase, Origin.GITHUB, url=url, create_date=create_date)
                    
                if not json_object:
                    continue
                    
                print(json.dumps(json_object), file=output_file)
            
        output_file.close()
        
    def get_repo_name_github(self, url: str) -> str:
        return "/".join(url.split("/")[3:5])
    
            
if __name__ == "__main__":
    WORKING_DIR = os.getcwd()
    DTD_SCHEMA = os.path.join(WORKING_DIR, "data\\schemas\\usecase.dtd")
    USECASES_DIR = os.path.join(WORKING_DIR, "data\\usecases")
    USECASES_DATES_DIR = os.path.join(WORKING_DIR, "github", "uc_url_date.txt")
    
    xml_files = XmlFiles("uc.jsonl", DTD_SCHEMA, os.path.join(WORKING_DIR, "data", "results"))
    start = time.perf_counter()
    xml_files.process_files(USECASES_DIR, USECASES_DATES_DIR)
    end = time.perf_counter()
    print(end - start, (end - start)/20, sep="\n")