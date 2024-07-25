import os
from dotenv import load_dotenv

from libs.scraper import Scraper

load_dotenv()
WAIT_TIME = int(os.getenv("WAIT_TIME"))


def main():

    Scraper([
        ["DELMAR GARDENS OF MERAMEC VALLEY", "(636) 343-0016"],
        ["CALHOUN NURSING & REHAB CENTER", "(618) 576-2278"],
        ["GREENBRIER NURSING AND REHABILITATION CENTER", "(501) 679-0860"],
        
    ], WAIT_TIME)


if __name__ == "__main__":
    main()