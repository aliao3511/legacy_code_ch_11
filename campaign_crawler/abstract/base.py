import importlib

from ..config import Config

class AbstractBase:

    REQUIRED_ATTRS = ("PLATFORM_SHORT_NAME",)

    @classmethod
    def initialize(cls, session):
        for attr in cls.REQUIRED_ATTRS:
            if not hasattr(cls, attr) or getattr(cls, attr) is None:
                raise Exception(f"missing required attribute {attr}")

        platform = cls.PLATFORM_SHORT_NAME

        cls.SESSION = session
        cls.PLATFORM = platform

        if getattr(Config, "PLATFORM") is None:
            Config.PLATFORM = platform

    @classmethod
    def destroy(cls):
        cls.SESSION = None
        cls.PLATFORM = None

        Config.PLATFORM = None

    @classmethod
    def get_crawler(cls, name: str):
        platform_name = cls.PLATFORM
        path_name = platform_name.lower()
        class_name = f"{platform_name}{name}Crawler"
        path_name = f"campaign_crawler.{path_name}.{name.lower()}"

        try:
            mod = importlib.import_module(path_name)
            crawler = getattr(mod, class_name)
        except Exception:
            raise Exception(
                "{path} does not have class {name}".format(
                    path=path_name, name=class_name
                )
            )
        return crawler

    