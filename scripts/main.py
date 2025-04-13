from itertools import product
from string import Template
import httpx
import json
import time
import re
import os

from chatgpt.context import Context
from xml_validation import XmlValidation, get_all_files
from plantuml_validation import PlantUMLValidation
from plantuml_files import PlantumlFiles

WORKING_DIR = os.getcwd()
DATA_PATH = os.path.join(WORKING_DIR, "data")
RESULT_DATA_PATH = os.path.join(WORKING_DIR, "data\\results")
SEQUENCE_GIT_URLS_PATH = os.path.join(WORKING_DIR, "github\\scripts\\output.txt")
DTD_SCHEME_PATH = os.path.join(WORKING_DIR, "data\\schemas\\usecase.dtd")

params = {
    "temperture": [0.5, 0.6, 0.7, 0.8],
    "alternative_steps": [True, False],
    "domain": ["banking", "healthcare", "education"]
}

template_usecase_query = Template("Create a use case based on the following sequence diagram without any comments: $sequence")
template_sequence_query = Template("Create a plantuml sequence diagram based on the following usecase without any comments: $usecase")

context = Context()
xml_validator = XmlValidation(DTD_SCHEME_PATH)

def calculate_price(prompt_tokens: int, completion_tokens: int) -> float:
    input_price = 0.0000005
    output_price = 0.0000015
    
    return prompt_tokens * input_price + completion_tokens * output_price

############### SEQUENCE -> USECASE ###############

# with open(SEQUENCE_GIT_URLS_PATH, "r") as sequence_git:
#     with open("test.json", "w") as file:
#         for url in sequence_git:
#             start = time.time()
#             result = httpx.get(url.strip())
#             puml_diagram = result.text
                    
#             query = template_usecase_query.substitute(sequence=puml_diagram)
#             result = context.execute_query(query)[0]
#             to_json = json.loads(result)
#             print(calculate_price(to_json["usage"]["prompt_tokens"], to_json["usage"]["completion_tokens"]), "$")
#             print(result, file=file)
            
#             xml_validator.validate_file(os.path.join(WORKING_DIR, "data\\usecases\\01.xml"))

#             end = time.time()
#             print(end - start)
#             break

############### USECASE -> SEQUENCE ###############
plantumlfiles = PlantumlFiles()
output_file = open("sequence_diagrams.jsonl", "a", encoding="utf-8")

# paths = get_all_files(DATA_PATH, "usecases")
# for path in paths:
#     with open(path, "r", encoding="utf-8") as file:
#         useCase = file.read()

#     promt_ctx = [{"role": "user", "content": "Based on the following use case, create a sequence diagram in plantuml without any comments."},
#                  {"role": "user", "content": "In sequence diagram if name of element is multiple words, put it in quotation marks and give diagram title"}]
#     query = f"Here is use case {useCase}"
    
#     result = context.execute_query(query, promt_ctx)[0]
#     content = result["choices"][0]["message"]["content"]
    
#     # domain = re.search(r"\{\{(.*)\}\}", content).group(1)
#     seq_diag = re.search(r"(@startuml.*@enduml)", content, re.DOTALL)
    
#     if seq_diag is None:
#         continue
    
#     json_object = plantumlfiles.prosess_diagram(seq_diag.group(1))
        
#     if json_object is not None:
#         print(json_object, file=output_file)
    
# output_file.close()

# Using temperature
with open(os.path.join(WORKING_DIR, "data\\usecases\\01.xml"), "r", encoding="utf-8") as file:
    useCase = file.read()
for i in [0.6, 0.8, 1, 1.2, 1.4]:

    promt_ctx = [{"role": "user", "content": "Based on the following use case, create a sequence diagram in plantuml without any comments."},
                 {"role": "user", "content": "In sequence diagram if name of element is multiple words, put it in quotation marks and give diagram title"}]
    query = f"Here is use case {useCase}"
    
    result = context.execute_query(query, promt_ctx, temperature=i)[0]
    content = result["choices"][0]["message"]["content"]
    
    # domain = re.search(r"\{\{(.*)\}\}", content).group(1)
    seq_diag = re.search(r"(@startuml.*@enduml)", content, re.DOTALL)
    
    if seq_diag is None:
        continue
    
    json_object = plantumlfiles.prosess_diagram(seq_diag.group(1))
        
    if json_object is not None:
        print(json_object, file=output_file)
    
output_file.close()


############### PROMPT ###############
# example_diagam = """@startuml
# autoactivate on
# hide footbox

# actor User
# participant System
# participant "Database" as DB

# User -> System : Request Data
# System -> DB : Query Data
# alt Data Found
#     return Return Data
#     loop Process Data
#         System -> System : Process Data
#     end
#     System - -> User : Display Data
# else Data Not Found
#     activate DB
#     System <- - DB : Return Error
#     User <- - System : Display Error
# end
# @enduml"""

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



# for temp, asteps, domain in product(*params.values()):
#     print(temp, asteps, domain)