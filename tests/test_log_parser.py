import pytest
from datetime import datetime

from services.log_parser import LogInfo, parse_log_line


def test_parse_log_line_valid_info():
    log_line = "2025-03-26 12:26:58,000 INFO django.request: GET /admin/login/ 201 OK [192.168.1.81]"
    expected = LogInfo(
        timestamp=datetime(2025, 3, 26, 12, 26, 58, 000),
        level="INFO",
        event="django.request",
        request_type="GET",
        handler="/admin/login/",
        status="201",
        ip="192.168.1.81",
        message=""
    )
    result = parse_log_line(log_line)
    assert result.level == expected.level
    assert result.event == expected.event

def test_parse_log_line_valid_error():
    log_line = "2025-03-26 12:27:50,000 ERROR django.request: Internal Server Error: /api/v1/auth/login/ [192.168.1.33] - OSError: No space left on device"
    expected = LogInfo(
        timestamp=datetime(2025, 3, 26, 12, 27, 50, 000),
        level="ERROR",
        event="django.request",
        handler="/api/v1/auth/login/",
        status="Internal Server Error",
        ip="192.168.1.33",
        message="- OSError: No space left on device"
    )
    result = parse_log_line(log_line)
    assert result.status == expected.status
    assert result.handler == expected.handler

def test_parse_log_line_invalid():
    log_line = ""
    result = parse_log_line(log_line)
    assert result is None

def test_parse_log_line_general_log():
    log_line = "2025-04-28 12:34:56,789 WARNING some.event: Something unexpected happened"
    expected = LogInfo(
        timestamp=datetime(2025, 4, 28, 12, 34, 56, 789000),
        level="WARNING",
        event="some.event",
        message="Something unexpected happened"
    )
    result = parse_log_line(log_line)
    assert result.level == expected.level
    assert result.event == expected.event
