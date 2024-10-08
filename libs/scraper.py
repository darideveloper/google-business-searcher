import os
from urllib.parse import quote
from datetime import datetime

from libs.web_scraping import WebScraping


class Scraper(WebScraping):
    
    def __init__(self, headless: bool, screenshots_folder: str):
        """ Setup scraper

        Args:
            headless (bool): Run scraper in headless mode
            wait_time (int): Time to wait between requests
        """
        
        # Start scraper
        super().__init__(
            headless=headless,
        )
        
        # Instance variables
        self.screenshots_folder = screenshots_folder
        
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
    
    def __save_screenshot__(self, function_name: str, identifier: str):
        """ Save screenshot of the current page

        Args:
            function_name (str): Function name
            identifier (str): Identifier (web page or business name)
        """
        
        screenshot_path = os.path.join(
            self.screenshots_folder,
            f"{function_name}_{identifier}.png"
        )
        self.screenshot(screenshot_path)
        
    def get_web_page(self, business_name: str, business_phone: str) -> str:
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
        self.refresh_selenium(time_units=0.1)
        
        # Get result lins
        results_links = self.get_attribs(selectors["results"], "href")
        results_links = list(filter(
            lambda link: link is not None and link.strip() != "",
            results_links
        ))
        results_links = list(map(self.__get_clean_domain__, results_links))
        
        # Remove .gov links
        results_links = list(filter(
            lambda link: ".gov" not in link,
            results_links
        ))
        
        # find the first link with a business word in the url
        business_name_words = business_name.split(" ")
        for result_link in results_links:
            for word in business_name_words:
                if word.lower() in result_link:
                    return result_link
            
        # Default empty domain
        self.__save_screenshot__("get_web_page", business_name)
        return ""
           
    def get_creation_date(self, web_page: str) -> str:
        """ Search page in weveback machine and get creation date

        Args:
            web_page (str): _description_
            
        Returns:
            str: creation date YYYY-MM-DD
        """
        
        selectors = {
            "creation_date": ".captures-range-info a",
        }
        
        archive_url = f"https://web.archive.org/web/20240000000000*/{web_page}"
        self.set_page(archive_url)
        
        # Try to get creation date 3 times
        creation_date_str = ""
        for _ in range(3):
            self.refresh_selenium(time_units=1)
            creation_date_str = self.get_text(selectors["creation_date"])
                    
        # Validate creation date found
        if not creation_date_str:
            base_domain = web_page.split("/")[2]
            self.__save_screenshot__("get_creation_date", base_domain)
            return ""
        
        # Convert to YYYY-MM-DD
        try:
            creation_date_str = creation_date_str.replace(".", "")
            creation_date = datetime.strptime(creation_date_str, "%B %d, %Y")
        except ValueError:
            print(f"Error converting date: {creation_date_str}")
            return ""
        creation_date_format = creation_date.strftime("%Y-%m-%d")
        return creation_date_format