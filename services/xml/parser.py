import pandas as pd
import requests
import xml.etree.ElementTree as ET
from db.data import FEEDS, COLUMNS
from config.logger import logger

class XMLParser:
    FEEDS = FEEDS
    COLUMNS = COLUMNS

    def __init__(self):
        logger.info("Starting Parsing")
        self.parser_type = None  # will get the value in the child
        self.site_acceptor = None  # will get the value in the child

    def get_offers_from_xml(self, url: str) -> list:
        response = requests.get(url)
        text = response.text
        root = ET.fromstring(text)

        return root.findall(".//offer")

    def extract_empty_products_data(self, xml_offers) -> pd.DataFrame:
        offers = []

        for offer in xml_offers:
            id = offer.get("id")
            external = offer.find("param[@name='external']").text
            offers.append(
                {
                    "id": id,
                    "external": external,
                }
            )

        if len(offers) > 0:
            df = pd.DataFrame(offers)
            return df
        else:
            return pd.DataFrame(columns=["id", "external"])

    def create_empty_products_df(self) -> pd.DataFrame:
        xml_offers = None

        if type(self.parser_type) == str and type(self.site_acceptor) == str:

            empty_product_slugs = self.parser_type.split("_")
            empty_product_string = (
                f"{empty_product_slugs[0]}out_{empty_product_slugs[1]}"
            )

            try:
                empty_product_feed = self.FEEDS[self.site_acceptor][
                    empty_product_string
                ]
                xml_offers = self.get_offers_from_xml(empty_product_feed)
            except Exception as ex:
                print(ex)
        else:
            raise Exception(
                f"Parser type:{str(self.parser_type)}\tSitename:{str(self.site_acceptor)}"
            )

        empty_products = self.extract_empty_products_data(xml_offers)

        return empty_products

    def collect_donor_feeds(self) -> list:
        if type(self.parser_type) == str and type(self.site_acceptor) == str:
            try:
                self.donor_feeds = list(
                    x[self.parser_type] for x in self.FEEDS.values()
                )
                self.donor_feeds.remove(
                    self.FEEDS[self.site_acceptor][self.parser_type]
                )
            except Exception as ex:
                raise ()
        else:
            raise Exception(
                f"Parser type:{str(self.parser_type)}\tSitename:{str(self.site_acceptor)}"
            )

        return self.donor_feeds
