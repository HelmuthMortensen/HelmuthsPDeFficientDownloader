import pandas as pd

from cli.excel_handler.download_tracker import (
    read_downloaded_ids,
    record_successful_downloads,
    reset_downloaded_pdfs,
)


def test_read_downloaded_ids_returns_empty_when_workbook_is_missing(tmp_path):
    assert read_downloaded_ids(tmp_path / "downloaded.xlsx") == set()


def test_record_successful_downloads_only_records_successful_ids(tmp_path):
    path = tmp_path / "downloaded.xlsx"
    record_successful_downloads(
        [
            {"success": True, "index": 12},
            {"success": False, "index": 13},
        ],
        path,
    )
    record_successful_downloads([{"success": True, "index": 14}], path)

    assert read_downloaded_ids(path) == {12, 14}


def test_reset_downloaded_pdfs_clears_records_and_keeps_id_column(tmp_path):
    path = tmp_path / "downloaded.xlsx"
    pd.DataFrame({"id": [12, 14]}).to_excel(path, index=False)

    reset_downloaded_pdfs(path)

    assert read_downloaded_ids(path) == set()
    assert list(pd.read_excel(path).columns) == ["id"]
