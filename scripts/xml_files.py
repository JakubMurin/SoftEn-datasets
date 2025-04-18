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
        
    def prepare_object(self, origin: Origin, source_url: str | None, params: XmlParams, ai_model: str="", temperature: float=1, top_p: float=1) -> dict:
        
        file_categ = FileNames.GENERATED_USECASE.value if origin is Origin.CHAT_GPT else FileNames.USECASE.value
        id = get_next_file_index(os.path.join(self.working_dir, file_categ))
        file = f"{file_categ}\{id:0{5}}_{file_categ}.xml"
        current_date = str(date.today())
        github_repository = self.get_repo_name_github(source_url) if source_url is not None else ""
        
        return_object = {
                         "id": id,
                         "file": file,
                         "date": current_date,
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
    
    def process_usecase(self, usecase: str, origin: Origin=Origin.GITHUB, url="", ai_model: str="", temperature: float=1, top_p: float=1):
        params = self.validation.validate(usecase)
                
        if not params:
            return
        
        uc_data = self.prepare_object(origin, url, params, ai_model, temperature, top_p)
        
        file_categ = FileNames.GENERATED_USECASE.value if origin is Origin.CHAT_GPT else FileNames.USECASE.value
        uc_file_path = os.path.join(self.working_dir, uc_data["file"])
        with open(uc_file_path, "w", encoding="utf-8") as uc_file:
            print(usecase, file=uc_file)
        
        return uc_data
    
    def process_files(self, dir_path: str):
        output_file = open(self.output_file_path, "a", encoding="utf-8")
        
        for file_path in get_all_files(dir_path):
        
            with open(file_path, "r") as uc_file:
                usecase = uc_file.read()
                    
                json_object = self.process_usecase(usecase)
                    
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
    
    xml_files = XmlFiles("uc.jsonl", DTD_SCHEMA, os.path.join(WORKING_DIR, "data", "results"))
    start = time.perf_counter()
    xml_files.process_files(USECASES_DIR)
    end = time.perf_counter()
    print(end - start, (end - start)/30, sep="\n")