import pandas as pd
import httpx
import xml.etree.ElementTree as ET


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
        response = httpx.get(url)
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
        ...

    def collect_donor_feeds(self):
        ...
