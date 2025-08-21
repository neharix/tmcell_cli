from typing import Tuple

from app.config import settings


class Path:
    def __init__(self, name: str, path: str):
        self.name: str = name
        self.path: str = path


class Paths:
    def __init__(self, *args: Tuple[Path]):
        self.routes: Tuple[Path] = args

    def get_url_of(self, name: str):
        search_result = list(filter(lambda e: e.name == name, self.routes))
        if len(search_result) > 0:
            return settings.service_url + search_result[0].path
