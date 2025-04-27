import os

WORKING_DIR = os.getcwd()
GITHUB_DIR = os.path.join(WORKING_DIR, "github")

# with open(os.path.join(GITHUB_DIR, "scripts", "total_seq.txt"), "r") as file:
#     total = set()
#     for url in file:
#         total.add(url.strip())
        
# with open(os.path.join(GITHUB_DIR, "scripts", "actor_puml.txt"), "r") as file:
#     uniq = set()
#     for l in file:
#         l = l.strip()
#         if l not in total:
#             uniq.add(l)
        
# with open(os.path.join(GITHUB_DIR, "scripts", "new_uniq.txt"), "a") as file:
#     for url in uniq:
#         print(url, file=file)


with open(os.path.join(GITHUB_DIR, "scripts", "total_seq_date.txt"), "r") as file:
    total = set()
    for url in file:
        total.add(url.strip())
        
with open(os.path.join(GITHUB_DIR, "scripts", "aaaaaa.txt"), "a") as file:
    for url in total:
        print(url, file=file)


# From Github paper only 91 diagrams