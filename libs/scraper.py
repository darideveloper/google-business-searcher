from urllib.parse import quote

from libs.web_scraping import WebScraping


class Scraper(WebScraping):
    
    def __init__(self):
        """ Setup scraper

        Args:
            wait_time (int): Time to wait between requests
        """
        
        # Start scraper
        super().__init__()
        
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
           
    def get_created_date(self, web_page: str) -> str:
        """ Search page in weveback machine and get creation date

        Args:
            web_page (str): _description_
            
        Returns:
            str: creation date
        """
        
        return ""