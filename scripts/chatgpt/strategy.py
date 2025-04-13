from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute_query(self, query: str, promt_ctx: list[dict[str, str]]=[]):
        pass
    
    @abstractmethod
    def execute_multiple_query(self, query: list[str], promt_ctx: list[dict[str, str]]=[]):
        pass
