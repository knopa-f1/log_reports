import pytest
from collections import defaultdict
from reports.handlers_report import HandlersReport
from services.log_parser import LogInfo


@pytest.fixture
def log_records():
    return [
        LogInfo(timestamp=None, level="INFO", event="django.request", handler="handler1", status=None, ip=None,
                message=None),
        LogInfo(timestamp=None, level="ERROR", event="django.request", handler="handler1", status=None, ip=None,
                message=None),
        LogInfo(timestamp=None, level="INFO", event="django.request", handler="handler2", status=None, ip=None,
                message=None),
        LogInfo(timestamp=None, level="DEBUG", event="django.request", handler="handler1", status=None, ip=None,
                message=None),
        LogInfo(timestamp=None, level="CRITICAL", event="django.request", handler="handler2", status=None, ip=None,
                message=None),
    ]


def test_handlers_report_build(log_records):
    report = HandlersReport(log_records)
    report.build()

    assert report.handler_data["handler1"]["INFO"] == 1
    assert report.handler_data["handler1"]["ERROR"] == 1
    assert report.handler_data["handler1"]["DEBUG"] == 1
    assert report.handler_data["handler2"]["INFO"] == 1
    assert report.handler_data["handler2"]["CRITICAL"] == 1
    assert report.total_requests == 5


def test_handlers_report_export(log_records):
    report = HandlersReport(log_records)
    report.build()
    result = report.export()

    assert result.startswith("Total requests: 5")

    assert "HANDLER" in result
    assert "INFO" in result
    assert "ERROR" in result
    assert "DEBUG" in result
    assert "CRITICAL" in result

    assert "handler1" in result
    assert "handler2" in result
