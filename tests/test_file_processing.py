import pytest
from services.file_processing import process_file
from unittest.mock import patch, mock_open

@pytest.mark.asyncio
async def test_process_file_valid():
    mock_file = ("""2025-03-26 12:26:58,000 INFO django.request: GET /admin/login/ 201 OK [192.168.1.81]"
                 2025-03-26 12:27:50,000 ERROR django.request: Internal Server Error: /api/v1/auth/login/ [192.168.1.33] - OSError: No space left on device""")
    with patch("builtins.open", mock_open(read_data=mock_file)):
        result = await process_file('mock_file.log')
        assert len(result) == 2

        assert result[0].event == "django.request"
        assert result[0].handler == "/admin/login/"
        assert result[0].status == "201"

        assert result[1].event == "django.request"
        assert result[1].handler == "/api/v1/auth/login/"
        assert result[1].status == "Internal Server Error"
        assert result[1].level == "ERROR"

@pytest.mark.asyncio
async def test_process_file_empty():
    with patch("builtins.open", mock_open(read_data="")):
        result = await process_file('empty_log.log')
        assert len(result) == 0
