from typing import List

class AbstractAccountCrawler:

    @classmethod
    def crawl_from_temp_accounts(
        cls
    ) -> List[int]:
        if cls.PLATFORM is None:
            raise Exception("can't crawl without a platform?")
            
        print(f"crawling {cls.PLATFORM}")
        return [1, 2, 3]