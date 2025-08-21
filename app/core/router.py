from typing import Any, Callable, Dict, List, Tuple

from app.logs.logger import logger


class Route:
    def __init__(self, name: str, callback: Callable):
        self.name: str = name
        self.callback: Callable = callback


class Router:
    def __init__(self, *args: Tuple[Route]):
        self.routes = args

    def go_to(self, name: str, instance, route_kwargs: Dict[str, Any]):
        search_result: List[Route] = list(filter(lambda e: e.name == name, self.routes))
        if len(search_result) > 0:
            instance.page = search_result[0]
            instance.page.callback(instance, **route_kwargs)
        else:
            logger.warning("Unknown route")

    def get_route(self, name: str):
        search_result: List[Route] = list(filter(lambda e: e.name == name, self.routes))
        if len(search_result) > 0:
            return search_result[0]
        else:
            logger.warning("Unknown route")
