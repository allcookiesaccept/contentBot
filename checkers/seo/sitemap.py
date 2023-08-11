import requests
from db.data import SITEMAPS
from config.logger import logger
from concurrent.futures import ThreadPoolExecutor

class SitemapChecker:

    def __init__(self):
        logger.info("Start Sitemap checker")
        self.sitemaps = SITEMAPS
        self.return_message_elements = []

    def __call__(self) -> str:

        self.__check_sitemaps()
        if len(self.return_message_elements) > 0:
            return '\n'.join(x for x in self.return_message_elements)
        else:
            return "Все сайтмапы на месте"

    def __check_sitemaps(self):

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.__check_sitemap, item) for item in self.sitemaps]
            for future in futures:
                result = future.result()
                if result:
                    self.return_message_elements.append(result)

    def __check_sitemap(self, item):
        project = item['site']
        back_url = item['back sitemap']
        front_url = item['front sitemap']
        front_status = requests.get(front_url).status_code
        back_status = requests.get(back_url).status_code

        if front_status == 404 or back_status == 404:
            check_result = f'{project}: {front_status} - {front_url}|{back_status} - {back_url}'
            return check_result

        return None

