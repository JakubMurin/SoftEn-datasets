from itertools import product
from string import Template
import httpx
import json
import time
import re
import os
import csv

from chatgpt.context import Context
from xml_validation import XmlValidation
from xml_files import XmlFiles
from plantuml_validation import PlantUMLValidation
from plantuml_files import PlantumlFiles
from utils import *

WORKING_DIR = os.getcwd()
DATA_PATH = os.path.join(WORKING_DIR, "data")
RESULT_DATA_PATH = os.path.join(WORKING_DIR, "data\\results")
SEQUENCE_GIT_URLS_PATH = os.path.join(WORKING_DIR, "github\\scripts\\output.txt")
DTD_SCHEME_PATH = os.path.join(WORKING_DIR, "data\\schemas\\usecase.dtd")


params = {
    "values": [0.2, 0.4, 0.6, 0.8, 1],
    "is_temp": [True, False],
}

template_usecase_query = Template("Create a use case based on the following sequence diagram without any comments: $sequence")
template_sequence_query = Template("Create a plantuml sequence diagram based on the following usecase without any comments: $usecase")

context = Context()

def calculate_price(prompt_tokens: int, completion_tokens: int) -> float:
    input_price = 0.0000005
    output_price = 0.0000015
    
    return prompt_tokens * input_price + completion_tokens * output_price

def merge_metadata(uc_data: dict, seq_data: dict) -> dict:
    """
    Returns final representation of dataset entry
    """
    uc_data = {"uc_" + key: value for key, value in uc_data.items()}
    seq_data = {"seq_" + key: value for key, value in seq_data.items()}
    return {
        "name": "",
        "domain": "",
        "origin": "semi-synthetic",
        **uc_data,
        **seq_data,
    }
    
def jsonl_to_csv(jsonl_file_path: str, csv_file_name: str):
    csv_file = open(csv_file_name, "x", newline="", encoding="utf-8")
    writer = csv.DictWriter(csv_file, [])
    
    header_required = True
    with open(jsonl_file_path, "r", encoding="utf-8") as jsonl_file:
        for line in jsonl_file:
            json_data = json.loads(line.strip())
            
            if header_required:
                writer.fieldnames = json_data.keys()
                writer.writeheader()
                header_required = False
            
            writer.writerow(json_data)
    
    csv_file.close()
            

############### SEQUENCE -> USECASE ###############

# xml_validator = XmlValidation(DTD_SCHEME_PATH)
# sequence_git = open(SEQUENCE_GIT_URLS_PATH, "r", encoding="utf-8")

# with open("test.json", "w") as file:
#     for url in sequence_git:
#         start = time.time()
#         result = httpx.get(url.strip())
#         puml_diagram = result.text
                
#         query = template_usecase_query.substitute(sequence=puml_diagram)
#         result = context.execute_query(query)[0]
#         to_json = json.loads(result)
#         print(calculate_price(to_json["usage"]["prompt_tokens"], to_json["usage"]["completion_tokens"]), "$")
#         print(result, file=file)
        
#         xml_validator.validate_file(os.path.join(WORKING_DIR, "data\\usecases\\01.xml"))

#         end = time.time()
#         print(end - start)
#         break
    
# sequence_git.close()

###### FINAL ######
# xml_files = XmlFiles("uc.jsonl", DTD_SCHEME_PATH, RESULT_DATA_PATH)
# seq_data_path = os.path.join(RESULT_DATA_PATH, "seq.jsonl")
# output_file = open(os.path.join(RESULT_DATA_PATH, "all.jsonl"), "a", encoding="utf-8")
# usecase_file = open(os.path.join(RESULT_DATA_PATH, "uc.jsonl"), "a", encoding="utf-8")

# with open(DTD_SCHEME_PATH, "r") as file:
#     dtd = file.read()

# with open(seq_data_path, "r", encoding="utf-8") as seq_entry:
#     price = 0
#     for seq in seq_entry:
#         seq_data = json.loads(seq)
#         if seq_data["origin"] == Origin.CHAT_GPT:
#             continue
        
#         start = time.perf_counter()
        
#         for value, is_temp in product(*params.values()):
            
#             if is_temp:
#                 temp, top_p = round(value + 0.4, 1), 1
#             else:
#                 temp, top_p = 1, value
            
#             seq_path = os.path.join(RESULT_DATA_PATH, "seq", seq_data["file"])
#             with open(seq_path, "r", encoding="utf-8") as file:
#                 sequence_diag = file.read()

#             promt_ctx = [{"role": "user", "content": "Based on the following sequence diagram, create a usecase in xml for following DTD scheme and return it without any comments."},
#                         {"role": "user", "content": f"Here is DTD scheme {dtd} and dont mention DOCTYPE in response."},
#                         {"role": "user", "content": "For mainSequence steps use id in format S1, for asteps A1 and steps inside A1S1, for esteps E1 and steps inside E1S1"},
#                         {"role": "developer", "content": "Make sure the actor is visible in each step and try write full sentences with active verb phrases that describe the sub-goals getting completed."}, #Cockburn 117 steps 5.-6.
#                         ]
#             query = f"Here is sequence diagram in plantuml {sequence_diag}"
            
#             result = context.execute_query(query, promt_ctx, temp, top_p)[0]
#             content = result["choices"][0]["message"]["content"]
            
#             price += calculate_price(result["usage"]["prompt_tokens"], result["usage"]["completion_tokens"])
            
#             # domain = re.search(r"\{\{(.*)\}\}", content).group(1)
#             usecase = content.replace("```xml", "").replace("```", "").replace('<!DOCTYPE useCase SYSTEM "usecase.dtd">', "")
                        
#             uc_data = xml_files.process_usecase(usecase, Origin.CHAT_GPT, "", context.ai_model, temp, top_p)
            
#             if uc_data is None:
#                 with open(os.path.join(RESULT_DATA_PATH, "wrong_uc.jsonl"), "a", encoding="utf-8") as wrong_file:
#                     data = {"seq": seq_data, "temperature": temp, "top_p": top_p, "content": content}
#                     print(json.dumps(data), file=wrong_file)
#                 continue
                
#             print(json.dumps(uc_data), file=usecase_file)
#             print(json.dumps(merge_metadata(uc_data, seq_data)), file=output_file)
            
#         print(time.perf_counter() - start, f"price: {price}$")
#         break
    
# output_file.close()
# usecase_file.close()

############### USECASE -> SEQUENCE ###############
plantumlfiles = PlantumlFiles("seq.jsonl", RESULT_DATA_PATH)
# usecase_data_path = os.path.join(RESULT_DATA_PATH, "uc.jsonl")
# output_file = open(os.path.join(RESULT_DATA_PATH, "all.jsonl"), "a", encoding="utf-8")
# seq_file = open(os.path.join(RESULT_DATA_PATH, "seq.jsonl"), "a", encoding="utf-8")

# with open(usecase_data_path, "r", encoding="utf-8") as usecases_data_file:
#     price = 0
#     for uc in usecases_data_file:
#         uc_data = json.loads(uc)
#         if uc_data["origin"] == Origin.CHAT_GPT:
#             continue
        
#         start = time.perf_counter()
        
#         for value, is_temp in product(*params.values()):
            
#             if is_temp:
#                 temp, top_p = round(value + 0.4, 1), 1
#             else:
#                 temp, top_p = 1, value
            
#             uc_path = os.path.join(RESULT_DATA_PATH, "uc", uc_data["file"])
#             with open(uc_path, "r", encoding="utf-8") as file:
#                 useCase = file.read()

#             promt_ctx = [{"role": "user", "content": "Based on the following use case, create a sequence diagram in plantuml without any comments."},
#                         {"role": "user", "content": "In sequence diagram if name of element is multiple words, put it in quotation marks and give diagram title"}]
#             query = f"Here is use case {useCase}"
            
#             result = context.execute_query(query, promt_ctx, temp, top_p)[0]
#             content = result["choices"][0]["message"]["content"]
            
#             price += calculate_price(result["usage"]["prompt_tokens"], result["usage"]["completion_tokens"])
            
#             # domain = re.search(r"\{\{(.*)\}\}", content).group(1)
#             seq_diag = re.search(r"(@startuml.*@enduml)", content, re.DOTALL)
            
#             if seq_diag is None:
#                 with open(os.path.join(RESULT_DATA_PATH, "wrong.jsonl"), "a", encoding="utf-8") as wrong_file:
#                     data = {"uc": uc_data, "temperature": temp, "top_p": top_p, "content": content}
#                     print(json.dumps(data), file=wrong_file)
#                 continue
            
#             seq_data = plantumlfiles.process_diagram(seq_diag.group(1), Origin.CHAT_GPT, "", context.ai_model, temp, top_p)
                
#             if seq_data is not None:
#                 print(json.dumps(seq_data), file=seq_file)
#                 print(json.dumps(merge_metadata(uc_data, seq_data)), file=output_file)
            
#         print(time.perf_counter() - start, f"price: {price}$")
#         break
    
# output_file.close()
# seq_file.close()

# Using temperature
# with open(os.path.join(WORKING_DIR, "data\\usecases\\01.xml"), "r", encoding="utf-8") as file:
#     useCase = file.read()

# for i in [0.6, 0.8, 1, 1.2, 1.4]:

#     promt_ctx = [{"role": "user", "content": "Based on the following use case, create a sequence diagram in plantuml without any comments."},
#                  {"role": "user", "content": "In sequence diagram if name of element is multiple words, put it in quotation marks and give diagram title"}]
#     query = f"Here is use case {useCase}"
    
#     result = context.execute_query(query, promt_ctx, temperature=i)[0]
#     content = result["choices"][0]["message"]["content"]
    
#     # domain = re.search(r"\{\{(.*)\}\}", content).group(1)
#     seq_diag = re.search(r"(@startuml.*@enduml)", content, re.DOTALL)
    
#     if seq_diag is None:
#         continue
    
#     json_object = plantumlfiles.process_diagram(seq_diag.group(1))
        
#     if json_object is not None:
#         print(json_object, file=output_file)
    
# output_file.close()


############### PROMPT ###############
example_diagam = """@startuml
autoactivate on
hide footbox

actor User
participant System
participant "Database" as DB

User -> System : Request Data
System -> DB : Query Data
alt Data Found
    return Return Data
    loop Process Data
        System -> System : Process Data
    end
    System --> User : Display Data
else Data Not Found
    activate DB
    System <-- DB : Return Error
    User <-- System : Display Error
end
@enduml"""

# with open(os.path.join(WORKING_DIR, "data\\usecases\\01.xml"), "r") as file:
#     example_use_case = file.read()

# with open(DTD_SCHEME_PATH, "r") as file:
#     dtd = file.read()

# promt_ctx = [{"role": "user", "content": f"Here is example of sequence diagram: {example_diagam}"},
#              {"role": "user", "content": f"Here is dtd scheme for usecase: {dtd}"},
#              {"role": "user", "content": "How whould you formulate prompt to get sequence diagram in format plantuml as example from usecase in dtd scheme? Expected behaviour: I will provide you usecase, prompt and you reply only with sequence diagram in plantuml"},
#              {"role": "assistant", "content": """
#               To generate a sequence diagram in PlantUML format based on the provided use case defined in the DTD scheme, the prompt could be formulated as follows:

# ---

# **Prompt:**
# Please provide the use case details according to the DTD scheme. Include the name, description, actors, preconditions, success end conditions, failure end conditions, trigger, main sequence steps, alternative steps, and error steps.

# ---

# By providing the use case information as requested in the prompt, a sequence diagram in PlantUML format can then be created based on the input. Let me know if you have a specific use case to work on."""},
#              {"role": "user", "content": "No, I expect prompt similar to this: Create a sequence diagram based on the following usecase without any comments"}
#             ]

# result = context.execute_query("a", promt_ctx)[0]
# pt, ct, tt = result["usage"]["prompt_tokens"], result["usage"]["completion_tokens"], result["usage"]["total_tokens"]
# print(f"Tokens used:\tprompt_tokens: {pt} + completion_tokens: {ct} = {tt}", f"price {calculate_price(pt, ct)}$")
# print(result["choices"][0]["message"]["content"])

# jsonl_to_csv(os.path.join(RESULT_DATA_PATH, "all.jsonl"), os.path.join(RESULT_DATA_PATH, "all.csv"))


print(plantumlfiles.process_diagram(example_diagam, Origin.CHAT_GPT, "", context.ai_model))