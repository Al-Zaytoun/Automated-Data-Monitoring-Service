import requests
from bs4 import BeautifulSoup
from win11toast import toast
import time
import datetime
import os
from pathlib import Path

# This gets the folder where scrapper.py is actually sitting
BASE_DIR = Path(__file__).resolve().parent

# Now define your file paths relative to that folder
PARSED_FILE = BASE_DIR / "parsed_output.txt"
LOG_FILE = BASE_DIR / "notification_history.txt"

TARGET_URL = "https://github.com/SimplifyJobs/Summer2026-Internships?tab=readme-ov-file"
SWE_TABLE_ID = "user-content--software-engineering-internship-roles" ## Particular table_id for swe internships

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
    DATA = []
    
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
    message = f"{company}: {job} ({location})"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Keep the Toast
    if length == 1:
        toast(f"New Job Update: \n{message}", duration="long")
    
    # 2. Multiple jobs put on board
    elif length > 1:
        toast(f"New Job Updates: {length} added jobs.", duration="long")

    # 3. Save to a log file so you never miss it
    with open("notification_history.txt", "a", encoding="UTF-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def data_compare_job_lengths(data1, data2):
    return abs(len(data1)) - abs(len(data2))

def main():
    # We need a baseline to compare against
    # Let's start by getting the current list of jobs
    print("Initializing baseline data...")
    previous_data = parse_data(UNPARSED_DATA)
    
    while True:
        print("\nChecking for updates...")
        
        # 1. Fetch fresh data (using your retrieve_data function)
        fresh_html = retrieve_data(TARGET_URL)
        
        if fresh_html:
            # 2. Parse the fresh data
            # Note: Clear DATA list or use a local variable inside parse_data 
            # to avoid the list growing infinitely every loop!
            current_data = parse_data(fresh_html)
            
            # 3. Compare lengths
            diff = data_compare_job_lengths(current_data, previous_data)
            
            if diff > 0:
                print(f"Alert! {diff} new job(s) found.")
                
                # Get the most recent job (assuming it's at the top or bottom)
                new_job = current_data[0] 
                
                # 4. Notify
                handle_notification(
                    diff, 
                    new_job["Company"], 
                    new_job["Role"], 
                    new_job["Location"]
                )
                
                # Update baseline so we don't notify for the same jobs again
                previous_data = current_data
            else:
                print("No new jobs found.")

        # 5. Wait (e.g., check every 30 minutes)
        print("Sleeping for 30 minutes...")
        time.sleep(1800) 

if __name__ == "__main__":
    main()


