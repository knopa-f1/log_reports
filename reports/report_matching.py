from reports.handlers_report import HandlersReport

AVAILABLE_REPORTS = {
    "handlers": HandlersReport,  # name of report in parameters: class of report
}

def get_report_class(report_name: str):
    report_class = AVAILABLE_REPORTS.get(report_name)
    if not report_class:
        raise ValueError(f"Неизвестный отчет '{report_name}'. Доступные варианты: {', '.join(AVAILABLE_REPORTS)}")
    return report_class