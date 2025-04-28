import re
from datetime import datetime

class LogInfo:
    def __init__(self, timestamp, level, event, request_type=None, handler=None, status=None, ip = None, message=None):
        self.timestamp = timestamp
        self.level = level
        self.event = event
        self.request_type = request_type
        self.handler = handler
        self.status = status
        self.ip = ip
        self.message = message

    def __str__(self):
        return (f"LogInfo(timestamp={self.timestamp}, level={self.level}, event={self.event}, "
                f"request_type={self.request_type}, handler={self.handler}, status_code={self.status}, "
                f"ip={self.ip}, message={self.message})")


def parse_log_line(file_line)->LogInfo|None:
    general_pattern = re.compile(r'(\S+ \S+),(\d{3}) (INFO|DEBUG|WARNING|ERROR|CRITICAL) (\S+): (.*)')
    match_general = general_pattern.match(file_line)

    if match_general:
        timestamp_str = match_general.group(1) + ',' + match_general.group(2)
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
        level = match_general.group(3)
        event = match_general.group(4)
        message = match_general.group(5)

        if event == 'django.request':
            if level == 'ERROR':
                django_request_pattern = re.compile(r'(.+?): (\S+) \[([^]]+)] - (.*)')
                match_django_request = django_request_pattern.search(message)

                if match_django_request:
                    status = match_django_request.group(1)
                    handler = match_django_request.group(2)
                    ip = match_django_request.group(3)
                    rest_message = match_django_request.group(4)
                    return LogInfo(timestamp, level, event, None, handler, status, ip, rest_message)

            else:
                django_request_pattern = re.compile(r'(\S+) (\S+) (\d+) (\S+) \[([^]]+)](.*)')
                match_django_request = django_request_pattern.search(message)

                if match_django_request:
                    request_type = match_django_request.group(1)
                    handler = match_django_request.group(2)
                    status_code = match_django_request.group(3)
                    ip = match_django_request.group(5)
                    rest_message = match_django_request.group(6)
                    return LogInfo(timestamp, level, event, request_type, handler, status_code, ip, rest_message)

        return LogInfo(timestamp, level, event, message=message)

    return None
