from typing import Generator


def read_file_sync(file_path: str)-> Generator[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()
