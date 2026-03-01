import requests
from bs4 import BeautifulSoup
"""
Dedicated file for visiting the website, and extracting the required data
"""

TARGET_URL = "https://github.com/SimplifyJobs/Summer2026-Internships?tab=readme-ov-file"
SWE_TABLE_ID = "user-content--software-engineering-internship-roles"

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

def extract_data(unparsed_data):
    
    soup = BeautifulSoup(unparsed_data, "html.parser")

    # Find direct parent of anchor, then get all siblings from the table
    try:
        anchor = soup.find("a", id=SWE_TABLE_ID)
        
        parent_header = anchor.find_parent("div")
        target_table = parent_header.find_next_sibling("markdown-accessiblity-table")

        rows = target_table.find_all("tr")
        with open("parsed_output.txt", "w", encoding="UTF-8") as file:
            for row in rows:
                file.write(row.get_text(separator=" | ", strip=True) + "\n")
    
    
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        return 


extract_data(UNPARSED_DATA)