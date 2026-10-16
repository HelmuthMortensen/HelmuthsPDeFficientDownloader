import pandas as pd
from pathlib import Path

from cli.excel_handler.excel_writer import write_report


def test_write_report_creates_excel(tmp_path):

    report = [{
        "success": True, "index": 10, "filename": "test_report.pdf", "used_backup": False, "fail_reason": None
    }]

    outfile = tmp_path / "report.xlsx"

    result = write_report(report, output_path=outfile)

    assert result.exists()


