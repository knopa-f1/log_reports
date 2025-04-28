from reports.report_matching import get_report_class
from reports.handlers_report import HandlersReport
import pytest

def test_get_report_class_valid():
    report_class = get_report_class("handlers")
    assert report_class == HandlersReport

def test_get_report_class_invalid():
    with pytest.raises(ValueError):
        get_report_class("invalid_report")
