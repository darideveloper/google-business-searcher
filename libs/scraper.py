from time import sleep
from urllib.parse import quote

from libs.web_scraping import WebScraping


class Scraper(WebScraping):
    
    def __init__(self, bussinesses_data: list, wait_time: int):
        """ Setup scraper

        Args:
            bussinesses_data (list): businesses data from excel: [name, phone]
            wait_time (int): Time to wait between requests
        """
        
        # Instance data
        self.bussinesses_data = bussinesses_data
        self.wait_time = wait_time
        
        # Start scraper
        super().__init__()
        
        # Autorun
        self.extract_pages()
        
    def __get_web_page__(self, business_name: str, business_phone: str) -> str:
        """ Get web page searching in google with business name and phone

        Args:
            business_name (str): Business name
            business_phone (str): Business phone

        Returns:
            str: Web page
        """
        
        selectors = {
            "results": '#search > div > div div[data-hveid] a[jsname]'
        }
        
        # Load page
        search_params = quote(f"{business_name} {business_phone}")
        google_url = f"https://www.google.com/search?q={search_params}"
        self.set_page(google_url)
        self.refresh_selenium()
        
        # Get result lins
        results_links = self.get_attribs(selectors["results"], "href")
        results_links = list(map(self.__get_clean_domain__, results_links))
        
        # Firnd the first link with a business word in the url
        business_name_words = business_name.split(" ")
        for result_link in results_links:
            for word in business_name_words:
                if word.lower() in result_link:
                    return result_link
                        
        # Default empty domain
        return ""
    
    def __get_clean_domain__(self, link: str) -> str:
        """ Clean domain from link

        Args:
            link (str): Link

        Returns:
            str: Clean domain
        """
        
        base_domain = link.split("/")[2]
        domain = f"https://{base_domain}"
        return domain
           
    def __get_created_date__(self, web_page: str) -> str:
        """ Search page in weveback machine and get creation date

        Args:
            web_page (str): _description_
            
        Returns:
            str: creation date
        """
        
        return ""
    
    def extract_pages(self):
        """ Extract each page from excel data and save in output csv """
        
        for row in self.bussinesses_data:
            business_name, business_phone = row
            
            print(f"Searching '{business_name}' - {business_phone}...")
            
            web_page = self.__get_web_page__(business_name, business_phone)
            
            # Skip if not found
            if not web_page:
                print("\tWeb page not found, skipping...")
                continue
            
            print(f"\tWeb page found: {web_page}")
            
            # creation_date = self.__get_created_date__(web_page)
            # print(creation_date, web_page)
            
            # Wait between requests
            sleep(self.wait_time)
    