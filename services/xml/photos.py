import datetime
import pandas as pd
from services.xml.parser import XMLParser
from services.csv import CSVFile


class PhotoMatcher(XMLParser):
    def __init__(self):
        super().__init__()
        self.type = "photo"

    def __call__(self, site_acceptor: str) -> CSVFile:
        self.site_acceptor = site_acceptor
        self.collect_donor_feeds()
        file_name = f"photos_for_{site_acceptor}_{datetime.date.today()}.csv"

        try:
            self.no_photos_dataframe: pd.DataFrame = self.create_empty_products_df()
            self.no_photo_codes: list = self.no_photos_dataframe["id"].to_list()
            self.parsed_photos: pd.DataFrame = self.extract_photos()
            merged_dataframe = self.merge_dataframes()

            return CSVFile(file_name, merged_dataframe, self.type)

        except Exception as ex:
            print(f"{ex}")

    def create_empty_products_df(self) -> pd.DataFrame:
        try:
            xml_offers = self.get_offers_from_xml(
                self.FEEDS[self.site_acceptor]["without_photos"]
            )
            empty_products = self.extract_empty_products_data(xml_offers)
            return empty_products
        except Exception as ex:
            print(ex)

    def collect_donor_feeds(self) -> list:
        self.donor_feeds = list(x["with_photos"] for x in self.FEEDS.values())
        self.donor_feeds.remove(self.FEEDS[self.site_acceptor]["with_photos"])
        return self.donor_feeds

    def extract_photos(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=["id", "pictures"])

        for feed in self.donor_feeds:
            xml_offers = self.get_offers_from_xml(feed)
            feed_df = self.extract_photo_products_data(xml_offers=xml_offers)
            df = pd.concat([df, feed_df])
            parsed_codes = feed_df["id"]
            parsed_codes.drop_duplicates(inplace=True)
            parsed_codes = parsed_codes.to_list()
            for code in parsed_codes:
                self.no_photo_codes.remove(code)

        return df

    def extract_photo_products_data(self, xml_offers) -> pd.DataFrame:
        offers = []
        for offer in xml_offers:
            id = offer.get("id")
            pictures_tag = offer.find("picture")
            if pictures_tag is not None and id in self.no_photo_codes:
                pictures = pictures_tag.text.split(",")
                offers.append(
                    {
                        "id": id,
                        "pictures": pictures,
                    }
                )

        if len(offers) > 0:
            df = pd.DataFrame(offers)
            return df.explode("pictures")
        else:
            return pd.DataFrame(columns=["id", "pictures"])

    def merge_dataframes(self) -> pd.DataFrame:
        df = pd.merge(
            self.no_photos_dataframe,
            self.parsed_photos,
            how="left",
            left_on="id",
            right_on="id",
        )

        df.dropna(inplace=True)
        df.drop(columns=["id"], inplace=True)
        df["pictures"] = df["pictures"].apply(lambda x: self._replace_image_link(x))

        df.rename(
            columns=dict(
                zip(df.columns, self.COLUMNS[self.site_acceptor]["photo_upload"])
            ),
            inplace=True,
        )

        return df

    def _replace_image_link(self, link) -> str:
        new_link = str(link).replace("http:", "https:").replace("www.", "cdn.")
        new_link = new_link.replace("iport", self.site_acceptor)
        return new_link
