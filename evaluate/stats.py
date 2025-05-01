import os
import json

from plantuml import PlantUML

WORKING_DIR = os.getcwd()
DATA_DIR = os.path.join(WORKING_DIR, "data", "results")
EVAL_DIR = os.path.join(WORKING_DIR, "evaluate")
EVAL_FILE_PATH = os.path.join(EVAL_DIR, "eval.jsonl")

def stats():
    plantuml = PlantUML("http://www.plantuml.com/plantuml/img/")
    md_file = open(os.path.join(EVAL_DIR, "comparison.md"), "w", encoding="utf-8")
    eval_file = open(EVAL_FILE_PATH, "r", encoding="utf-8")

    puml_count = 0
    error_count = 0
    other_count = 0

    for entry in eval_file:
        data = json.loads(entry)
        
        uc_file_name = data["uc_file"].split("\\")[-1]
        seq_file_name = data["seq_file"].split("\\")[-1]
        
        seq_puml_path = os.path.join(EVAL_DIR, "seq", seq_file_name)
        gen_puml_path = os.path.join(EVAL_DIR, "output_pumls", uc_file_name.replace(".xml", ".puml"))
        try:
            with open(gen_puml_path, "r", encoding="utf-8") as gen_file:
                content = gen_file.read()
        except FileNotFoundError:
            continue
            
        if content.startswith("[Error]"):
            error_count += 1
        elif content.startswith("@startuml"):
            puml_count += 1
            
            with open(os.path.join(DATA_DIR, data["uc_file"]), "r", encoding="utf-8") as uc_file:
                uc = uc_file.read()
            
            seq_img_name = os.path.join("images", seq_file_name.replace("puml", "png"))
            plantuml.processes_file(seq_puml_path, os.path.join(EVAL_DIR, seq_img_name))
            
            gen_img_name = os.path.join("images", uc_file_name.replace("xml", "png"))
            plantuml.processes_file(gen_puml_path, os.path.join(EVAL_DIR, gen_img_name))
                        
            print(f"## {uc_file_name}\n```xml\n{uc}```\n### seq\n![]({seq_img_name})\n### gen_seq\n![]({gen_img_name})\n", file=md_file)
            
        else:
            other_count += 1


    print(f"Puml: {puml_count}, Error: {error_count}, other: {other_count}")
    md_file.close()
    eval_file.close()
    
stats()