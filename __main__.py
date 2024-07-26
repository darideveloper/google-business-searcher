import os
from time import sleep

from dotenv import load_dotenv

from libs.scraper import Scraper
from libs.csv_urils import CsvWriter

# Env vaiables
load_dotenv()
WAIT_TIME = int(os.getenv("WAIT_TIME"))

# Paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(CURRENT_DIR, "data.xlsx")
OUTPUT_CSV = os.path.join(CURRENT_DIR, "output.csv")


def main():
    
    # TODO: Extract data from excel
    bussinesses_data = [
        ["DELMAR GARDENS OF MERAMEC VALLEY", "(636) 343-0016"],
        ["CALHOUN NURSING & REHAB CENTER", "(618) 576-2278"],
        ["GREENBRIER NURSING AND REHABILITATION CENTER", "(501) 679-0860"]
    ]
    
    # TODO: valdiate excel columns
    
    # Start scraper
    scraper = Scraper()
    
    # Start csv writer
    csv_writer = CsvWriter(OUTPUT_CSV)
    
    # Write csv header
    csv_writer.write_row(
        "w",
        ["Business Name", "Phone", "Web Page", "Creation Date"]
    )

    # Scrape each business
    for row in bussinesses_data:
        business_name, business_phone = row
        
        print(f"Searching '{business_name}' - {business_phone}...")
        
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

    input("Done! Press enter to exit...")


if __name__ == "__main__":
    main()