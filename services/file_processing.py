import asyncio
import logging

from services.log_parser import parse_log_line
from utils.file_utils import read_file_sync

logger = logging.getLogger(__name__)


async def process_file(file_path: str):
    logger.debug(f"Обработка файла: {file_path}")
    log_records = []
    loop = asyncio.get_running_loop()
    file_lines = await loop.run_in_executor(None, read_file_sync, file_path)
    for line in file_lines:
        logger.debug(f"Обработка строки: {line}")
        log_info = parse_log_line(line)
        logger.debug(f'Результат обработки: {log_info}')
        if log_info:
            log_records.append(log_info)
    return log_records


async def process_files(files:list[str]):
    tasks = [asyncio.create_task(process_file(file_path)) for file_path in files]
    all_log_records = await asyncio.gather(*tasks)
    return [log_record for records in all_log_records for log_record in records]
