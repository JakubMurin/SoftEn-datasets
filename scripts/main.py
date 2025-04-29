from itertools import product
from string import Template
import httpx
import json
import time
import re
import os

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

def merge_metadata(uc_data: dict, seq_data: dict, name: str="") -> dict:
    """
    Returns final representation of dataset entry
    """
    uc_data = {"uc_" + key: value for key, value in uc_data.items()}
    seq_data = {"seq_" + key: value for key, value in seq_data.items()}
    return {
        "name": name,
        "origin": "semi-synthetic",
        **uc_data,
        **seq_data,
    }
    
def save_error(save_path: str, given_data: dict, temp: float, top_p: float, type_e: str, content: str):
    with open(save_path, "a", encoding="utf-8") as wrong_file:
        data = {"type": type_e, "data": given_data, "temperature": temp, "top_p": top_p, "content": content}
        print(json.dumps(data), file=wrong_file)
            

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
def seq_uc():
    xml_files = XmlFiles("uc.jsonl", DTD_SCHEME_PATH, RESULT_DATA_PATH)
    seq_data_path = os.path.join(RESULT_DATA_PATH, "seq.jsonl")
    output_file = open(os.path.join(RESULT_DATA_PATH, "all.jsonl"), "a", encoding="utf-8")
    usecase_file = open(os.path.join(RESULT_DATA_PATH, "uc.jsonl"), "a", encoding="utf-8")

    with open(DTD_SCHEME_PATH, "r") as file:
        dtd = file.read()
        
    price = 0
    start = time.perf_counter()
    counter = 0

    with open(seq_data_path, "r", encoding="utf-8") as seq_entry:
        for seq in seq_entry:
            seq_data = json.loads(seq)
            print(seq_data["file"])
            
            if seq_data["origin"] == Origin.CHAT_GPT.value:
                continue
                        
            for value, is_temp in product(*params.values()):
                counter += 1
                
                temp, top_p = (round(value + 0.4, 1), 1) if is_temp else (1, value)
                
                seq_path = os.path.join(RESULT_DATA_PATH, seq_data["file"])
                with open(seq_path, "r", encoding="utf-8") as file:
                    sequence_diag = file.read()

                promt_ctx = [{"role": "user", "content": "Based on the following sequence diagram, create a usecase in xml for following DTD scheme and return it without any comments."},
                            {"role": "user", "content": f"Here is DTD scheme {dtd} and dont mention DOCTYPE in response."},
                            {"role": "user", "content": "For mainSequence steps use id in format S1, for asteps A1 and steps inside A1S1, for esteps E1 and steps inside E1S1"},
                            {"role": "developer", "content": "Make sure the actor is visible in each step and try write full sentences with active verb phrases that describe the sub-goals getting completed."}, #Cockburn 117 steps 5.-6.
                            ]
                query = f"Here is sequence diagram in plantuml {sequence_diag}"
                
                result = context.execute_query(query, promt_ctx, temp, top_p)[0]
                content = result["choices"][0]["message"]["content"]
                
                price += calculate_price(result["usage"]["prompt_tokens"], result["usage"]["completion_tokens"])
                
                usecase = re.search(r"(<useCase[\s\S]*</useCase>)", content, re.DOTALL)
                if usecase is None:
                    save_error(os.path.join(RESULT_DATA_PATH, "wrong_uc.jsonl"), seq_data, temp, top_p, "Wrong response", content)
                    continue
                
                usecase = usecase.group(1).replace('<!DOCTYPE useCase SYSTEM "usecase.dtd">', "")
                            
                uc_data = xml_files.process_usecase(usecase, Origin.CHAT_GPT, "", None, context.ai_model, temp, top_p)
                
                if uc_data is None:
                    save_error(os.path.join(RESULT_DATA_PATH, "wrong_uc.jsonl"), seq_data, temp, top_p, "Wrong format", content)
                    continue
                    
                name = seq_data["title"] if seq_data["title"] else uc_data["title"]
                print(json.dumps(uc_data), file=usecase_file)
                print(json.dumps(merge_metadata(uc_data, seq_data, name=name)), file=output_file)

            
    output_file.close()
    usecase_file.close()
    
    total = time.perf_counter() - start
    print(f"Total time: {total}", f"Average time: {total / counter}", f"price: {price}$")

# seq_uc()
########### WRONG CORRECTION ##############
def wrong_seq_uc(wrong_uc_data_path: str):
    xml_files = XmlFiles("uc.jsonl", DTD_SCHEME_PATH, RESULT_DATA_PATH)
    output_file = open(os.path.join(RESULT_DATA_PATH, "all.jsonl"), "a", encoding="utf-8")
    usecase_file = open(os.path.join(RESULT_DATA_PATH, "uc.jsonl"), "a", encoding="utf-8")

    with open(DTD_SCHEME_PATH, "r") as file:
        dtd = file.read()
        
    price = 0
    start = time.perf_counter()
    counter = 0

    with open(wrong_uc_data_path, "r", encoding="utf-8") as wrong_uc_entry:
        for wrong_uc in wrong_uc_entry:
            wrong_uc_data = json.loads(wrong_uc)
            seq_data = wrong_uc_data["data"]
            print(f"id: {seq_data["id"]}, origin: {seq_data["origin"]}, temperature: {wrong_uc_data["temperature"]}, top_p: {wrong_uc_data["top_p"]}")
                        
            counter += 1
            
            temp, top_p = wrong_uc_data["temperature"], wrong_uc_data["top_p"]
            
            seq_path = os.path.join(RESULT_DATA_PATH, seq_data["file"])
            with open(seq_path, "r", encoding="utf-8") as file:
                sequence_diag = file.read()

            promt_ctx = [{"role": "user", "content": "Based on the following sequence diagram, create a usecase in xml for following DTD scheme and return it without any comments."},
                        {"role": "user", "content": f"Here is DTD scheme {dtd} and dont mention DOCTYPE in response."},
                        {"role": "user", "content": "For mainSequence steps use id in format S1, for asteps A1 and steps inside A1S1, for esteps E1 and steps inside E1S1"},
                        {"role": "developer", "content": "Make sure the actor is visible in each step and try write full sentences with active verb phrases that describe the sub-goals getting completed."}, #Cockburn 117 steps 5.-6.
                        ]
            query = f"Here is sequence diagram in plantuml {sequence_diag}"
            
            result = context.execute_query(query, promt_ctx, temp, top_p)[0]
            content = result["choices"][0]["message"]["content"]
            
            price += calculate_price(result["usage"]["prompt_tokens"], result["usage"]["completion_tokens"])
            
            usecase = re.search(r"(<useCase[\s\S]*</useCase>)", content, re.DOTALL)
            if usecase is None:
                save_error(os.path.join(RESULT_DATA_PATH, "wrong_uc.jsonl"), seq_data, temp, top_p, "Wrong response", content)
                continue
            
            usecase = usecase.group(1).replace('<!DOCTYPE useCase SYSTEM "usecase.dtd">', "")
                        
            uc_data = xml_files.process_usecase(usecase, Origin.CHAT_GPT, "", None, context.ai_model, temp, top_p)
            
            if uc_data is None:
                save_error(os.path.join(RESULT_DATA_PATH, "wrong_uc.jsonl"), seq_data, temp, top_p, "Wrong format", content)
                continue
                
            name = seq_data["title"] if seq_data["title"] else uc_data["title"]
            print(json.dumps(uc_data), file=usecase_file)
            print(json.dumps(merge_metadata(uc_data, seq_data, name=name)), file=output_file)

            
    output_file.close()
    usecase_file.close()
    
    total = time.perf_counter() - start
    print(f"Total time: {total}", f"Average time: {total / counter}", f"price: {price}$")

wrong_uc_data_path = os.path.join(RESULT_DATA_PATH, "wrong_uc1.jsonl")
wrong_seq_uc(wrong_uc_data_path)

############### USECASE -> SEQUENCE ###############
def uc_seq():
    plantumlfiles = PlantumlFiles("seq.jsonl", RESULT_DATA_PATH)
    usecase_data_path = os.path.join(RESULT_DATA_PATH, "uc.jsonl")
    output_file = open(os.path.join(RESULT_DATA_PATH, "all.jsonl"), "a", encoding="utf-8")
    seq_file = open(os.path.join(RESULT_DATA_PATH, "seq.jsonl"), "a", encoding="utf-8")

    price = 0
    start = time.perf_counter()
    counter = 0

    with open(usecase_data_path, "r", encoding="utf-8") as usecases_data_file:
        for uc in usecases_data_file:            
            uc_data = json.loads(uc)
            print(uc_data["file"])
            
            if uc_data["origin"] == Origin.CHAT_GPT.value:
                continue
                        
            for value, is_temp in product(*params.values()):
                counter += 1
                
                temp, top_p = (round(value + 0.4, 1), 1) if is_temp else (1, value)
                
                uc_path = os.path.join(RESULT_DATA_PATH, uc_data["file"])
                with open(uc_path, "r", encoding="utf-8") as file:
                    useCase = file.read()

                promt_ctx = [
                    {"role": "user", "content": "Based on the following use case, create a sequence diagram in plantuml without any comments."},
                    {"role": "user", "content": "In sequence diagram if name of element is multiple words, put it in quotation marks and give diagram title"},
                    ]
                query = f"Here is use case {useCase}"
                
                result = context.execute_query(query, promt_ctx, temp, top_p)[0]
                content = result["choices"][0]["message"]["content"]
                
                price += calculate_price(result["usage"]["prompt_tokens"], result["usage"]["completion_tokens"])
                
                seq_diag = re.search(r"(@startuml.*@enduml)", content, re.DOTALL)
                
                if seq_diag is None:
                    save_error(os.path.join(RESULT_DATA_PATH, "wrong_seq.jsonl"), uc_data, temp, top_p, "Wrong response", content)
                    continue
                
                seq_data = plantumlfiles.process_diagram(seq_diag.group(1), Origin.CHAT_GPT, "", None, context.ai_model, temp, top_p)
                    
                if seq_data is None:
                    save_error(os.path.join(RESULT_DATA_PATH, "wrong_seq.jsonl"), uc_data, temp, top_p, "Wrong diagram", content)
                    continue
                    
                name = uc_data["title"] if uc_data["title"] else seq_data["title"]
                print(json.dumps(seq_data), file=seq_file)
                print(json.dumps(merge_metadata(uc_data, seq_data, name=name)), file=output_file)
                
        
    output_file.close()
    seq_file.close()
    
    total = time.perf_counter() - start
    print(f"Total time: {total}", f"Average time: {total / counter}", f"price: {price}$")
    
# uc_seq()

########### WRONG CORRECTION ##############
def uc_seq_wrong(wrong_sequence_data_path: str):
    plantumlfiles = PlantumlFiles("seq.jsonl", RESULT_DATA_PATH)
    output_file = open(os.path.join(RESULT_DATA_PATH, "all.jsonl"), "a", encoding="utf-8")
    seq_file = open(os.path.join(RESULT_DATA_PATH, "seq.jsonl"), "a", encoding="utf-8")

    price = 0
    start = time.perf_counter()
    counter = 0

    with open(wrong_sequence_data_path, "r", encoding="utf-8") as wrong_sequence_data_file:
        for wrong_seq in wrong_sequence_data_file:            
            wrong_seq_data = json.loads(wrong_seq)
            uc_data = wrong_seq_data["data"]
            print(f"id: {uc_data["id"]}, origin: {uc_data["origin"]}, temperature: {wrong_seq_data["temperature"]}, top_p: {wrong_seq_data["top_p"]}")
                        
            counter += 1
            
            temp, top_p = wrong_seq_data["temperature"], wrong_seq_data["top_p"]
            
            uc_path = os.path.join(RESULT_DATA_PATH, uc_data["file"])
            with open(uc_path, "r", encoding="utf-8") as file:
                useCase = file.read()

            promt_ctx = [
                {"role": "user", "content": "Based on the following use case, create a sequence diagram in plantuml without any comments."},
                {"role": "user", "content": "In sequence diagram if name of element is multiple words, put it in quotation marks and give diagram title"},
                ]
            query = f"Here is use case {useCase}"
            
            result = context.execute_query(query, promt_ctx, temp, top_p)[0]
            content = result["choices"][0]["message"]["content"]
            
            price += calculate_price(result["usage"]["prompt_tokens"], result["usage"]["completion_tokens"])
            
            seq_diag = re.search(r"(@startuml.*@enduml)", content, re.DOTALL)
            
            if seq_diag is None:
                save_error(os.path.join(RESULT_DATA_PATH, "wrong_seq.jsonl"), uc_data, temp, top_p, "Wrong response", content)
                continue
            
            seq_data = plantumlfiles.process_diagram(seq_diag.group(1), Origin.CHAT_GPT, "", None, context.ai_model, temp, top_p)
                
            if seq_data is None:
                save_error(os.path.join(RESULT_DATA_PATH, "wrong_seq.jsonl"), uc_data, temp, top_p, "Wrong diagram", content)
                continue
                
            name = uc_data["title"] if uc_data["title"] else seq_data["title"]
            print(json.dumps(seq_data), file=seq_file)
            print(json.dumps(merge_metadata(uc_data, seq_data, name=name)), file=output_file)
                
        
    output_file.close()
    seq_file.close()
    
    total = time.perf_counter() - start
    print(f"Total time: {total}", f"Average time: {total / counter}", f"price: {price}$")

# wrong_sequence_data_path = os.path.join(RESULT_DATA_PATH, "wrong_seq1.jsonl")
# uc_seq_wrong(wrong_sequence_data_path)

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
#     System --> User : Display Data
# else Data Not Found
#     activate DB
#     System <-- DB : Return Error
#     User <-- System : Display Error
# end
# @enduml"""

# with open(os.path.join(WORKING_DIR, "data\\usecases\\01.xml"), "r") as file:
#     example_use_case = file.read()

# with open(DTD_SCHEME_PATH, "r") as file:
#     dtd = file.read()
    
# promt_ctx = [
#                 {"role": "developer", "content": "Based on the following use case, create a sequence diagram in plantuml without any comments."},
#                 {"role": "assistant", "content": "Noted."},
#                 {"role": "user", "content": "In sequence diagram if name of element is multiple words, put it in quotation marks and give diagram title"},
#                 {"role": "assistant", "content": "OK"},
#                 {"role": "user", "content": "Analyze the given software engineering diagram and classify it into an appropriate application domain like Banking, Education, Healthcare, Finance, etc. based on its context. Add only domain after diagram as last line of response inside {{}}"},
#                 ]

# query = f"Here is use case {example_use_case}"
            
# result = context.execute_query(query, promt_ctx, 1, 0.8)[0]
# content = result["choices"][0]["message"]["content"]

# price = calculate_price(result["usage"]["prompt_tokens"], result["usage"]["completion_tokens"])

# domain = re.search(r"\{\{(.*)\}\}", content).group(1)
# seq_diag = re.search(r"(@startuml.*@enduml)", content, re.DOTALL)

# print(content)
# print(price, domain, "\n", seq_diag)

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


# print(plantumlfiles.process_diagram(example_diagam, Origin.CHAT_GPT, "", context.ai_model))