import importlib

from typing import List
from .abstract.account import AbstractAccountCrawler

class MasterCrawler:

    @classmethod
    def update_accounts_from_temp_accounts(
        cls, short_name: str
    ) -> List[int]:
        account_crawler = cls._get_and_init_account_crawler(short_name)

        new_ids = account_crawler.crawl_from_temp_accounts()
        account_crawler.destroy()

        return new_ids

    @classmethod
    def _get_and_init_account_crawler(
        cls, short_name: str
    ) -> AbstractAccountCrawler:
        base_cls = cls._get_base_crawler(short_name)
        cls._initialize_session(short_name)

        account_crawler = base_cls.get_crawler("Account")
        return account_crawler

    @classmethod
    def _get_base_crawler(cls, short_name: str):
        class_name = f"Base{short_name}"
        path_name = f"campaign_crawler.{short_name.lower()}.base"
        try:
            mod = importlib.import_module(path_name)
            base_cls = getattr(mod, class_name)
        except Exception:
            raise Exception(
                "{path} does not have class {name}".format(
                    path=path_name, name=class_name
                )
            )
        return base_cls

    @classmethod
    def _initialize_session(cls, short_name: str):
        base_cls = cls._get_base_crawler(short_name)
        session = short_name
        base_cls.initialize(session)
