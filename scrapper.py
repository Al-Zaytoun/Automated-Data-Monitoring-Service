import requests
import filecmp
from bs4 import BeautifulSoup
from win11toast import toast
import json


TARGET_URL = "https://github.com/SimplifyJobs/Summer2026-Internships?tab=readme-ov-file"
SWE_TABLE_ID = "user-content--software-engineering-internship-roles"
DATA = []
def retrieve_data(target_url):
    
    try:
        response = requests.get(target_url)

        if response.status_code == 200:
            print("Successfully requested.")
            return response.text

    except Exception as e:
        print(f"An unexpected error occured: {e}")
        return 

with open("output.txt", "r", encoding="UTF-8") as file:
    UNPARSED_DATA = file.read()

def parse_data(unparsed_data):
    
    soup = BeautifulSoup(unparsed_data, "html.parser")

    # Find direct parent of anchor, then get all siblings from the table
    try:
        anchor = soup.find("a", id=SWE_TABLE_ID)
        
        parent_header = anchor.find_parent("div")
        target_table = parent_header.find_next_sibling("markdown-accessiblity-table")

        rows = target_table.find_all("tr")

        with open("parsed_output.txt", "w", encoding="UTF-8") as file:
            for row in rows:
                row_text = row.get_text(separator=" | ", strip=True)
                parts = row_text.split(" | ")

                if (len(parts) >= 3 and parts[0] != "Company"):
                    DATA.append({
                        "Company": parts[0],
                        "Role": parts[1],
                        "Location": parts[2]
                    })
                file.write(row.get_text(separator=" | ", strip=True) + "\n")
    
    
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        return []
    
    return DATA

def handle_notification(length, company, job, location):
    if length >= 1:
        toast(f"New Job Update: {company}: {job}\n{location}")
    else:
        toast(f"New Job Updates:\n{length} added jobs.")

def is_files_different(file1, file2):
    return filecmp.cmp(file1, file2)

def main():
    pass

data = parse_data(UNPARSED_DATA)


