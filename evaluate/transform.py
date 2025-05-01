import os
import json
import random
import shutil
from lxml import etree
import time

WORKING_DIR = os.getcwd()
DATA_DIR = os.path.join(WORKING_DIR, "data", "results")
EVAL_DIR = os.path.join(WORKING_DIR, "evaluate")
ALL_FILE_PATH = os.path.join(DATA_DIR, "all.jsonl")
OUT_FILE_PATH = os.path.join(EVAL_DIR, "eval.jsonl")

def transform_step(pair) -> str:
    i, el = pair
    step = f"{i}. {el.text}"
    if not step.endswith("."):
        step += "."
    return step

start = time.perf_counter()

# num_of_selected = 100
# num_of_entries = 8220

# indexes = list(range(num_of_entries))
# random.shuffle(indexes)
# indexes = indexes[:num_of_selected]

all_file = open(ALL_FILE_PATH, "r", encoding="utf-8")
# out_file = open(OUT_FILE_PATH, "a", encoding="utf-8")

for i, entry in enumerate(all_file):
    # if i not in indexes:
    #     continue
    
    data = json.loads(entry)
    
    file_name = data["uc_file"].split("\\")[-1].replace(".xml", ".txt")
    
    with open(os.path.join(DATA_DIR, data["uc_file"]), "r", encoding="utf-8") as uc_file:
        uc = uc_file.read()
        
    # shutil.copyfile(os.path.join(DATA_DIR, data["seq_file"]), os.path.join(EVAL_DIR, "seq"))
        
    xml_tree = etree.fromstring(uc.encode())
    steps_el = xml_tree.find("mainSequence")
    steps = map(transform_step, enumerate(steps_el, 1))
    
    with open(os.path.join(EVAL_DIR, "uc_txt", file_name), "w", encoding="utf-8") as t_file:
        print(*steps, sep="\n", file=t_file)
    # print(entry, end="", file=out_file)
            
            
all_file.close()
# out_file.close()

# with open(OUT_FILE_PATH, "r", encoding="utf-8") as out_file:
#     for entry in out_file:
#         data = json.loads(entry)
#         shutil.copy(os.path.join(DATA_DIR, data["seq_file"]), os.path.join(EVAL_DIR, "seq"))
    
print(f"Total time: {time.perf_counter() - start}")