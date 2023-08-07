import datetime
import pandas as pd
from services.xml.parser import XMLParser
from services.api import DescriptionsDownloaderHTTPX

class DescriptionMatcher(XMLParser):
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

    def extract_product_description_urls(self, xml_offers) -> pd.DataFrame:
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
