from abc import ABC, abstractmethod
from typing import Any


class CaseProvider(ABC):
    @abstractmethod
    def search_cases(self, query: str, filters: dict[str, Any]) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_case(self, case_id: str) -> dict[str, Any] | None:
        raise NotImplementedError
