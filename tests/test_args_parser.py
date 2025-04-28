import pytest
import sys
from unittest import mock
from utils.args_parser import parse_args


def test_parse_args_valid():
    sys.argv = ['main.py', 'fixtures/app1.log', 'fixtures/app2.log', '--report', 'handlers']

    with mock.patch('os.path.isfile', return_value=True):
        args = parse_args()

    assert args.log_files == ['fixtures/app1.log', 'fixtures/app2.log']
    assert args.report == 'handlers'


def test_parse_args_wrong_report():
    sys.argv = ['main.py', 'fixtures/app1.log', 'fixtures/app2.log', '--report', 'wrong_report']

    with mock.patch('os.path.isfile', return_value=True):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_wrong_files():
    sys.argv = ['main.py', 'fixtures/app1.log', 'fixtures/wrong_file.log', '--report', 'wrong_report']

    with mock.patch('os.path.isfile', side_effect=lambda path: path != 'fixtures/wrong_file.log'):
        with pytest.raises(SystemExit):
            parse_args()
