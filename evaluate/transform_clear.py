import os
import json
from lxml import etree

WORKING_DIR = os.getcwd()
DATA_DIR = os.path.join(WORKING_DIR, "data", "results")
UC_FILE_PATH = os.path.join(DATA_DIR, "uc.jsonl")
EVAL_DIR = os.path.join(WORKING_DIR, "evaluate")

def transform_step(pair) -> str:
    i, el = pair
    step = f"{i}. {el.text}"
    if not step.endswith("."):
        step += "."
    return step

all_file = open(UC_FILE_PATH, "r", encoding="utf-8")

for i, entry in enumerate(all_file):
    data = json.loads(entry)
    
    file_name = data["uc_file"].split("\\")[-1].replace(".xml", ".txt")
    
    with open(os.path.join(DATA_DIR, data["uc_file"]), "r", encoding="utf-8") as uc_file:
        uc = uc_file.read()
                
    xml_tree = etree.fromstring(uc.encode())
    steps_el = xml_tree.find("mainSequence")
    steps = map(transform_step, enumerate(steps_el, 1))
    
    with open(os.path.join(EVAL_DIR, "uc_txt", file_name), "w", encoding="utf-8") as t_file:
        print(*steps, sep="\n", file=t_file)
            
all_file.close()