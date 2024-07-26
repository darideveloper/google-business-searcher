import os
from time import sleep

from dotenv import load_dotenv

from libs.scraper import Scraper
from libs.csv_urils import CsvWriter
from libs.xlsx import SpreadsheetManager

# Env vaiables
load_dotenv()
WAIT_TIME = int(os.getenv("WAIT_TIME"))

# Paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(CURRENT_DIR, "data")
EXCEL_FILE = os.path.join(DATA_FOLDER, "input.xlsx")
OUTPUT_CSV = os.path.join(DATA_FOLDER, "output.csv")
SCREENSHOTS_FOLDER = os.path.join(CURRENT_DIR, "screenshots")
HEADLESS = os. getenv("SHOW_BROWSER") == "False"


def main():
    
    print("Starting...")
    
    # Create folders
    os.makedirs(DATA_FOLDER, exist_ok=True)
    os.makedirs(SCREENSHOTS_FOLDER, exist_ok=True)
    
    # Validate if excel file exists
    if not os.path.exists(EXCEL_FILE):
        print(f"Error: File '{EXCEL_FILE}' not found")
        print("Please make sure the file exists and try again")
        quit()
    
    # Start libs
    scraper = Scraper(
        headless=HEADLESS,
        screenshots_folder=SCREENSHOTS_FOLDER
    )
    csv_writer = CsvWriter(OUTPUT_CSV)
    ss_manager = SpreadsheetManager(EXCEL_FILE)
    
    # Read excel data
    ss_manager.set_sheet("Sheet1")
    bussinesses_data = ss_manager.get_data()
    
    # valdiate excel columns
    header = ["Name", "Phone"]
    header_sheet = bussinesses_data[0]
    for header_element, header_sheet_element in zip(header, header_sheet):
        if header_element != header_sheet_element:
            print(f"Error: Column '{header_element}' not found in sheet 'Sheet1'")
            print("Excel should have the following columns in the following order:")
            print(" ".join(header))
            quit()
    
    # Write csv header
    csv_writer.write_row(
        "w",
        ["Name", "Phone", "Web Page", "Creation Date"]
    )

    # Scrape each business
    for row in bussinesses_data[1:]:
        business_name, business_phone, *_ = row
        
        max_row_num = len(bussinesses_data) - 1
        current_row_num = bussinesses_data.index(row)
        counter = f"{current_row_num}/{max_row_num}"
        print(f"({counter}) Searching '{business_name}' - {business_phone}...")
        
        web_page = scraper.get_web_page(business_name, business_phone)
        
        # Skip if not found
        if not web_page:
            print("\tWeb page not found, skipping...")
            continue
        
        print(f"\tWeb page found: {web_page}")
        
        # Log web page
        creation_date = scraper.get_creation_date(web_page)
        
        if not creation_date:
            print("\tCreation date not found, skipping...")
            continue
        
        # Log creation date
        print(f"\tCreation date found: {creation_date}")
        
        csv_writer.write_row(
            "a",
            [business_name, business_phone, web_page, creation_date]
        )
        
        # Wait between requests
        sleep(WAIT_TIME)
        

if __name__ == "__main__":
    main()