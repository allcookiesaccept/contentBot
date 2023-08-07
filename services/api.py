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
