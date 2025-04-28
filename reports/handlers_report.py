from collections import defaultdict

from reports.base_report import BaseReport
from services.log_parser import LogInfo


class HandlersReport(BaseReport):

    LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def __init__(self, log_records: list[LogInfo]):
        super().__init__(log_records)
        self.handler_data = defaultdict(lambda: defaultdict(int))  # handler -> level -> count
        self.total_requests = 0

    def build(self):
        for record in self.log_records:
            if record.event == "django.request" and record.handler:
                self.handler_data[record.handler][record.level.upper()] += 1
                self.total_requests += 1

    def export(self) -> str:
        lines = [f"Total requests: {self.total_requests}\n"]
        header = "{:<24}".format("HANDLER") + "".join(f"{lvl:<8}" for lvl in self.LEVELS)
        lines.append(header)

        for handler in sorted(self.handler_data):
            line = "{:<24}".format(handler)
            for lvl in self.LEVELS:
                count = self.handler_data[handler].get(lvl, 0)
                line += f"{count:<8}"
            lines.append(line)

        total_by_level = {lvl: 0 for lvl in self.LEVELS}
        for handler in self.handler_data.values():
            for lvl in self.LEVELS:
                total_by_level[lvl] += handler.get(lvl, 0)

        total_line = "{:<24}".format("") + "".join(f"{total_by_level[lvl]:<8}" for lvl in self.LEVELS)
        lines.append(total_line)

        return "\n".join(lines)
