from abc import ABC, abstractmethod

from services.log_parser import LogInfo


class BaseReport(ABC):
    def __init__(self, log_records: list[LogInfo]):
        self.log_records = log_records

    @abstractmethod
    def build(self):
        """biuld the report"""
        pass

    @abstractmethod
    def export(self) -> str:
        """export report to string"""
        pass
