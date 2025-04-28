import asyncio
import logging

from reports.handlers_report import HandlersReport
from reports.report_matching import get_report_class
from services.file_processing import process_files
from utils.args_parser import parse_args

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

async def main():
    args = parse_args()

    log_files = args.log_files
    report_type = args.report

    logger.debug(f"Обрабатываем файлы: {log_files}, тип отчета: {report_type}")
    log_records = await process_files(log_files)

    report_class = get_report_class(report_type)
    report = report_class(log_records)
    report.build()
    print(report.export())



if __name__ == "__main__":
    asyncio.run(main())
