from itertools import product

params = {
    "temperture": [0.5, 0.6, 0.7, 0.8],
    "alternative_steps": [True, False],
    "domain": ["banking", "healthcare", "education"]
}

for temp, asteps, domain in product(*params.values()):
    print(temp, asteps, domain)