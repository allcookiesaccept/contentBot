import datetime
import pandas as pd
from services.xml.parser import XMLParser
from services.api import DescriptionsDownloaderHTTPX, DescriptionsDownloader
from services.csv import CSVFile


class DescriptionMatcher(XMLParser):
    def __init__(self):
        super().__init__()
        self.parser_type = "with_description"

    def __call__(self, site_acceptor) -> CSVFile:
        self.site_acceptor = site_acceptor
        self.collect_donor_feeds()
        self.downloader = DescriptionsDownloader()
        file_name = f"descriptions_for_{site_acceptor}_{datetime.date.today()}.csv"

        try:
            self.no_descriptions_dataframe: pd.DataFrame = (
                self.create_empty_products_df()
            )
            self.no_description_codes: list = self.no_descriptions_dataframe[
                "id"
            ].to_list()
            self.description_links_dataframe = self.extract_description_links()
            if len(self.description_links_dataframe) > 0:
                self.collected_descriptions = self.collect_descriptions()
                merged_dataframe = self.merge_dataframes()
                return CSVFile(file_name, merged_dataframe, self.parser_type)
            else:
                return "No descriptions"
        except Exception as e:
            print({e})



    def extract_description_links(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=["id", "url"])

        for feed in self.donor_feeds:
            xml_offers = self.get_offers_from_xml(feed)
            feed_df: pd.DataFrame = self.extract_description_products_data(xml_offers)
            df = pd.concat([df, feed_df])
            parsed_codes = feed_df["id"]
            parsed_codes.drop_duplicates(inplace=True)
            for code in parsed_codes:
                self.no_description_codes.remove(code)

        return df

    def extract_description_products_data(self, xml_offers) -> pd.DataFrame:
        offers = []
        for offer in xml_offers:
            id = offer.get("id")
            url = offer.find("url")
            if url is not None and id in self.no_description_codes:
                offers.append(
                    {
                        "id": id,
                        "url": url.text,
                    }
                )

        if len(offers) > 0:
            df = pd.DataFrame(offers)
            return df
        else:
            return pd.DataFrame(columns=["id", "url"])

    def collect_descriptions(self) -> pd.DataFrame:
        description_links = self.description_links_dataframe["url"].to_list()
        descriptions = self.downloader.scrape(description_links, 10)
        descriptions_dataframe = pd.DataFrame(descriptions)
        df = pd.merge(
            descriptions_dataframe,
            self.description_links_dataframe,
            how="left",
            left_on="url",
            right_on="url",
        )
        return df

    def merge_dataframes(self):
        df = pd.merge(
            self.no_descriptions_dataframe,
            self.collected_descriptions,
            how="left",
            left_on="id",
            right_on="id",
        )
        df.drop(columns=["id", "url"], inplace=True)
        df.rename(
            columns=dict(
                zip(df.columns, self.COLUMNS[self.site_acceptor]["description_upload"])
            ),
            inplace=True,
        )
        df.dropna(inplace=True)
        print(df.shape[0])
        if len(df) == 0:
            return pd.DataFrame(columns=['id', 'description'])

        return df
