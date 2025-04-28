import argparse
import os

from reports.report_matching import AVAILABLE_REPORTS


def parse_args():
    parser = argparse.ArgumentParser(description="Анализатор логов для формирования отчетов.")

    parser.add_argument(
        'log_files',
        metavar='log_file',
        type=str,
        nargs='+',
        help="Пути к файлам логов для анализа"
    )

    parser.add_argument(
        '--report',
        type=str,
        required=True,
        choices=AVAILABLE_REPORTS.keys(),
        help="Тип отчета для генерации"
    )

    args = parser.parse_args()

    # checks
    for file_path in args.log_files:
        if not os.path.isfile(file_path):
            parser.error(f"Файл не найден: {file_path}")

    if args.report not in AVAILABLE_REPORTS:
        parser.error(f"Неизвестный тип отчета '{args.report}'. Доступные: {', '.join(AVAILABLE_REPORTS.keys())}")

    return args
