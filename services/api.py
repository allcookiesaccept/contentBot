from concurrent.futures import ThreadPoolExecutor
import httpx


class DescriptionsDownloaderHTTPX:
    def __init__(self):
        self.results = []

    def fetch_data(self, url):
        try:
            with httpx.Client() as client:
                response = client.get(url)
                data = response.json()
                if data["status"] == "success":
                    description = data["data"]["DETAIL_TEXT"]
                    return url, description
                else:
                    return url, ""
        except httpx.RequestError as e:
            return url, str(e)

    def worker(self, url):
        page, description = self.fetch_data(url)
        self.results.append({"url": page, "description": description})

    def scrape(self, urls, num_threads) -> list:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(self.worker, urls)

        return self.results


from queue import Queue
from threading import Thread
import requests


class DescriptionsDownloader:
    def __init__(self):
        self.url_queue = Queue()
        self.results = []

    def fetch_data(self, url):
        try:
            response = requests.get(url).json()
            if response["status"] == "success":
                description = response["data"]["DETAIL_TEXT"]
                return url, description
        except requests.RequestException as e:
            return url, str(e)

    def worker(self):
        while True:
            url = self.url_queue.get()
            page, description = self.fetch_data(url)
            self.results.append({"url": page, "description": description})
            self.url_queue.task_done()

    def scrape(self, urls, num_threads) -> list:
        for url in urls:
            self.url_queue.put(url)
        for _ in range(num_threads):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()
        self.url_queue.join()

        return self.results
