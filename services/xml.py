import pandas
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import datetime
from services.api import DescriptionsDownloader, DescriptionsDownloaderHTTPX


class XMLParser:
    FEEDS = {
        "iport": {
            "without_photos": "https://api.iport.ru/files/export/iport_no_photo.xml",
            "with_photos": "https://api.iport.ru/files/export/iport_photo.xml",
            "without_description": "https://api.iport.ru/files/export/iport_no_description.xml",
            "with_description": "https://api.iport.ru/files/export/iport_description.xml",
        },
        "nbcomputers": {
            "without_photos": "https://api.nbcomputers.ru/files/export/nb_no_photo.xml",
            "with_photos": "https://api.nbcomputers.ru/files/export/nb_photo.xml",
            "without_description": "https://api.nbcomputers.ru/files/export/nb_no_description.xml",
            "with_description": "https://api.nbcomputers.ru/files/export/nb_description.xml",
        },
        "nbcomgroup": {
            "without_photos": "https://api.nbcomgroup.ru/files/export/b2b_no_photo.xml",
            "with_photos": "https://api.nbcomgroup.ru/files/export/b2b_photo.xml",
            "without_description": "https://api.nbcomgroup.ru/files/export/b2b_no_description.xml",
            "with_description": "https://api.nbcomgroup.ru/files/export/b2b_description.xml",
        },
        "samsungstore": {
            "without_photos": "https://api.samsungstore.ru/files/export/samsung_no_photo.xml",
            "with_photos": "https://api.samsungstore.ru/files/export/samsung_photo.xml",
            "without_description": "https://api.samsungstore.ru/files/export/samsung_no_description.xml",
            "with_description": "https://api.samsungstore.ru/files/export/samsung_description.xml",
        },
        "s-centres": {
            "without_photos": "https://api.s-centres.ru/files/export/sony_no_photo.xml",
            "with_photos": "https://api.s-centres.ru/files/export/sony_photo.xml",
            "without_description": "https://api.s-centres.ru/files/export/sony_no_description.xml",
            "with_description": "https://api.s-centres.ru/files/export/sony_description.xml",
        },
        "micenter": {
            "without_photos": "https://api.micenter.ru/files/micenter/export/micenter_no_photo.xml",
            "with_photos": "https://api.micenter.ru/files/micenter/export/micenter_photo.xml",
            "without_description": "https://api.micenter.ru/files/micenter/export/micenter_no_description.xml",
            "with_description": "https://api.micenter.ru/files/micenter/export/micenter_description.xml",
        },
    }

    COLUMNS = {
        "iport": {
            "photo_upload": ["IE_XML_ID", "IP_PROP62"],
            "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
        },
        "nbcomputers": {
            "photo_upload": ["IE_XML_ID", "IP_PROP976"],
            "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
        },
        "nbcomgroup": {
            "photo_upload": ["IE_XML_ID", "IP_PROP1989"],
            "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
        },
        "samsungstore": {
            "photo_upload": ["IE_XML_ID", "IP_PROP3964"],
            "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
        },
        "s-centres": {
            "photo_upload": ["IE_XML_ID", "IP_PROP4884"],
            "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
        },
        "micenter": {
            "photo_upload": ["IE_XML_ID", "IP_PROP4885"],
            "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
        },
    }

    def __init__(self):
        ...

    def get_offers_from_xml(self, url: str) -> list:
        response = requests.get(url)
        text = response.text
        root = ET.fromstring(text)

        return root.findall(".//offer")

    def extract_empty_products_data(self, xml_offers) -> pandas.DataFrame:
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

        return pd.DataFrame(offers)


class PhotoFiller(XMLParser):
    def __init__(self):
        super().__init__()
        self.type = "photo"

    def __call__(self, site_acceptor, site_donor):
        try:
            no_photo = self.get_offers_from_xml(
                self.FEEDS[site_acceptor]["without_photos"]
            )
            no_photo_df = self.extract_empty_products_data(no_photo)

            photo = self.get_offers_from_xml(self.FEEDS[site_donor]["with_photos"])
            photo_df = self.extract_photo_products_data(photo)

            merged_df = pd.merge(
                no_photo_df, photo_df, how="left", left_on="id", right_on="id"
            )

            merged_df.dropna(inplace=True)
            merged_df.drop(columns=["id"], inplace=True)
            merged_df["pictures"] = merged_df["pictures"].apply(
                lambda x: self._replace_image_link(x, site_acceptor)
            )

            file_name = (
                f"photos_from_{site_donor}_to_{site_acceptor}_{datetime.date.today()}.csv"
            )
            merged_df.rename(
                columns=dict(
                    zip(merged_df.columns, self.COLUMNS[site_acceptor]["photo_upload"])
                ),
                inplace=True,
            )

            return file_name, merged_df, self.type

        except Exception as e:
            print({e})

    def extract_photo_products_data(self, xml_offers) -> pandas.DataFrame:
        offers = []

        for offer in xml_offers:
            id = offer.get("id")
            pictures_tag = offer.find("picture")
            if pictures_tag is not None:
                pictures = pictures_tag.text.split(",")
                offers.append(
                    {
                        "id": id,
                        "pictures": pictures,
                    }
                )

        df = pd.DataFrame(offers)

        return df.explode("pictures")

    def _replace_image_link(self, link, site_acceptor) -> str:
        new_link = str(link).replace("http:", "https:").replace("www.", "cdn.")
        new_link = new_link.replace("iport", site_acceptor)
        return new_link


class DescriptionFiller(XMLParser):
    def __init__(self):
        super().__init__()
        self.downloader = DescriptionsDownloaderHTTPX()
        self.type = "description"

    def __call__(self, site_acceptor, site_donor) -> (str, pd.DataFrame, str):
        try:
            no_descriptions = self.get_offers_from_xml(
                self.FEEDS[site_acceptor]["without_description"]
            )
            no_descriptions_df = self.extract_empty_products_data(no_descriptions)
            print(f'no_descriptions_df_created')
            print(no_descriptions_df.columns)


            descriptions = self.get_offers_from_xml(
                self.FEEDS[site_donor]["with_description"]
            )
            descriptions_df = self.extract_product_description_urls(descriptions)
            print(descriptions_df.columns)
            print(f'descriptions_df_created')

            merged_df = pd.merge(
                no_descriptions_df,
                descriptions_df,
                how="left",
                left_on="id",
                right_on="id",
            )

            print(f'tables merged')
            print(merged_df.columns)
            merged_df.dropna(inplace=True)
            print(f'na dropped')

            urls = merged_df["url"].to_list()
            print(f'urls_to_list')
            print(urls)

            descriptions = self.downloader.scrape(urls, 10)
            print(f'descriptions_scraped')
            print(descriptions)

            descriptions_table = pd.DataFrame(descriptions)
            print(f'description_table_created')
            # print(descriptions_table)

            merged_df = pd.merge(
                merged_df, descriptions_table, how="left", right_on="url", left_on="url"
            )
            print(f'description_table_merged')

            merged_df.drop(columns=["id", "url"], inplace=True)
            print(f'description_table_dropped')
            merged_df.rename(
                columns=dict(
                    zip(merged_df.columns, self.COLUMNS[site_acceptor]["description_upload"])
                ),
                inplace=True,
            )
            print(f'description_table_columns_renamed')

            file_name = f"{site_donor}_{site_acceptor}_{datetime.date.today()}.csv"
            print(f'file_name_created')

            print(file_name, merged_df, self.type)
            return file_name, merged_df, self.type
        except Exception as e:
            print({e})

    def extract_product_description_urls(self, xml_offers) -> pandas.DataFrame:
        offers = []
        for offer in xml_offers:
            id = offer.get("id")
            url = offer.find("url")
            offers.append(
                {
                    "id": id,
                    "url": url.text,
                }
            )
        return pd.DataFrame(offers)
