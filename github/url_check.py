import requests
import csv
from time import time

class URLCheck:
    def __init__(self, csv_path: str, output_csv) -> None:
        self.output_csv = output_csv
        self.csv_path = csv_path
        self.url_idx = 1
        
    def get_info(self, url: str) -> list:
        output = [url]
        response = requests.head(url)
        output.append(response.status_code)
        self.stats[response.status_code] = self.stats.get(response.status_code, 0) + 1
        if response.status_code == 301:
            output.append(response.headers["location"])
            
        return output
    
    def do(self, limit=25000, offset=0, append_file=False) -> dict[int, int]:
        print(f"Offset: {offset}\tLimit: {limit}\t->{offset}-{offset+limit-1}")
        self.stats = {}
        file_append = "a" if append_file else "w"
        
        with open(self.csv_path, newline="") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            with open(self.output_csv, file_append, newline="") as output_file:
                output_writer = csv.writer(output_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                if not file_append:
                    output_writer.writerow(["GitHub URL", "Status", "New location"])
                # skip headers and offset
                for _ in range(offset + 1):
                    next(csv_reader)
                counter = 0
                timer = time()
                for row in csv_reader:
                    if counter == limit:
                        break
                    
                    output_writer.writerow(self.get_info(row[self.url_idx]))
                    counter += 1
                
                timer = time() - timer
        
        print(f"Time: {timer}\tAvg: {timer/(limit)}")
        return self.stats
                    
check = URLCheck("UMLGithub.csv", "checkedURL.csv")
print(check.do(1, 24716, append_file=True))