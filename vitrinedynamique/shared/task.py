from typing import Any
from abc import ABC
from vitrinedynamique.shared.responseobj import Response


class Task(ABC):
    def execute(self) -> Response:
        pass

    def data(self) -> Any:
        return None
