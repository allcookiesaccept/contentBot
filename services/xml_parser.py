import pandas as pd
import requests
import xml.etree.ElementTree as ET
import logging
import datetime
import re


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

    def open_xml(self, url):
        response = requests.get(url)
        return response.text

    def get_offers(self, xml_response):
        root = ET.fromstring(xml_response)
        return root.findall("./shop/offers/offer")

    def extract_empty_products_data(self, xml_offers):
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

    def extract_photo_products_data(self, xml_offers):
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

    def extract_products_descriptions(self, xml_offers):
        offers = []

        for offer in xml_offers:
            id = offer.get("id")
            description_tag = offer.find("description")
            if description_tag is not None:
                description = description_tag.text
                description = description.replace("<![CDATA[ ", "").replace(" ]]>", "")
                offers.append(
                    {
                        "id": id,
                        "descriptions": description,
                    }
                )

        df = pd.DataFrame(offers)

        return df

    def _replace_image_link(self, link, site_acceptor):
        new_link = str(link).replace("http:", "https:").replace("www.", "cdn.")
        new_link = new_link.replace("iport", site_acceptor)
        return new_link

    def _replace_description_links(self, description, site_acceptor):
        text = str(description)
        new_text = re.sub(
            r"https://cdn\..*?\.ru/", f"https://cdn\.{site_acceptor}\.ru/", text
        )
        return new_text


class PhotoFiller(XMLParser):
    def __init__(self):
        super().__init__()

    def __call__(self, site_acceptor, site_donor):
        try:
            no_photo = self.get_offers(
                self.open_xml(self.FEEDS[site_acceptor]["without_photos"])
            )
            no_photo_df = self.extract_empty_products_data(no_photo)
            photo = self.get_offers(
                self.open_xml(self.FEEDS[site_donor]["with_photos"])
            )
            photo_df = self.extract_photo_products_data(photo)
            merged_df = pd.merge(
                no_photo_df, photo_df, how="left", left_on="id", right_on="id"
            )
            merged_df.dropna(inplace=True)
            merged_df.drop(columns=["id"], inplace=True)
            merged_df["pictures"] = merged_df["pictures"].apply(
                lambda x: self._replace_image_link(x, site_acceptor)
            )

            merged_df.rename(
                columns=dict(
                    zip(merged_df.columns, self.COLUMNS[site_acceptor]["photo_upload"])
                ),
                inplace=True,
            )
            # file_name = f'photos_from_{site_donor}_to_{site_acceptor}_{datetime.date.today()}.csv'
            # merged_df.to_csv(file_name, encoding='utf-8', sep=';', index=False)
            return merged_df
        except Exception as e:
            print({e})


class DescriptionFiller(XMLParser):
    def __init__(self):
        super().__init__()

    def __call__(self, site_acceptor, site_donor):
        try:
            no_descriptions = self.get_offers(
                self.open_xml(self.FEEDS[site_acceptor]["without_description"])
            )
            no_descriptions_df = self.extract_empty_products_data(no_descriptions)
            descriptions = self.get_offers(
                self.open_xml(self.FEEDS[site_donor]["with_description"])
            )
            descriptions_df = self.extract_products_descriptions(descriptions)
            merged_df = pd.merge(
                no_descriptions_df,
                descriptions_df,
                how="left",
                left_on="id",
                right_on="id",
            )
            merged_df.dropna(inplace=True)
            merged_df.drop(columns=["id"], inplace=True)
            merged_df["descriptions"] = merged_df["descriptions"].apply(
                lambda x: self._replace_description_links(x, site_acceptor)
            )
            file_name = f"descriptions_from_{site_donor}_to_{site_acceptor}_{datetime.date.today()}.csv"
            merged_df.rename(
                columns=dict(
                    zip(
                        merged_df.columns,
                        self.COLUMNS[site_acceptor]["description_upload"],
                    )
                ),
                inplace=True,
            )
            merged_df.to_csv(file_name, encoding="utf-8", sep=";", index=False)
            return merged_df
        except Exception as e:
            print({e})
