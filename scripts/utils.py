import os
import csv
import json

from enum import Enum


class Origin(Enum):
    GITHUB = "github"
    CHAT_GPT = "chatgpt"
    
    def __str__(self):
        return str(self.value)
    
class FileNames(Enum):
    """
    File name and also foolder name for that type
    """
    SEQUENCE_DIAGRAM = "seq"
    GENERATED_SEQUENCE_DIAGRAM = "seq_gen"
    USECASE = "uc"
    GENERATED_USECASE = "uc_gen"

def get_next_file_index(folder_path: str, extension: str | None=None) -> int:
    """
    File names is in format xxxxx_(seq | seq_gen | usecase | usecase_gen).(puml | xml)
    
    :Returns: int of next number for file name
    """
    
    folder_path = os.path.join(folder_path)
    names = os.listdir(folder_path)
    
    if extension is not None:
        names = list(filter(lambda p: p.endswith(extension), names))
    if not names:
        return 1
    last = sorted(names)[-1]
    last_number = last.split("_")[0]
    
    return int(last_number) + 1

def get_all_files(path: str, folder_name: str="") -> list[str]:
    folder_path = os.path.join(path, folder_name)
    files = os.listdir(folder_path)
    xml_files = filter(lambda p: p.endswith(".xml"), files)
    return list(map(lambda p: os.path.join(folder_path, p), xml_files))

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