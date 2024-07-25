import os
from time import sleep

from dotenv import load_dotenv

from libs.scraper import Scraper

load_dotenv()
WAIT_TIME = int(os.getenv("WAIT_TIME"))


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
        
        # creation_date = self.__get_created_date__(web_page)
        # print(creation_date, web_page)
        
        # Wait between requests
        sleep(WAIT_TIME)


if __name__ == "__main__":
    main()