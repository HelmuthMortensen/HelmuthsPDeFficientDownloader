import pandas as pd
from pathlib import Path

from cli.excel_handler.excel_reader import excel_reader, excel_list_cleaner

def test_excel_reader_loads_excel(tmp_path):
    df = pd.DataFrame(
        {
            "id":[1, 2],
            "url":["url1", "url2"],
            "alt url": ["backup1", "backup2"],
        }
    )

    file = tmp_path / "test.xlsx"
    df.to_excel(file, index=False)

    urls, backups, no_backups, link_index = excel_reader(tmp_path, "test.xlsx")

    assert list(urls) == ["url1", "url2"]
    assert list(backups) == ["backup1", "backup2"]
    assert list(no_backups) == [False, False]
    assert list(link_index) == [1, 2]

def test_excel_reader_missing_backups(tmp_path):
    df = pd.DataFrame(
        {
            "id": [1],
            "url": ["url1"],
            "alt url": [None],
        }
    )

    file = tmp_path / "test.xlsx"
    df.to_excel(file, index=False)

    _, _, no_backups, _ = excel_reader(tmp_path, "test.xlsx")

    assert no_backups[0]

def test_excel_list_cleaner_uses_backup_when_url_missing():
    
    urls = pd.Series([None])
    backups = pd.Series(["backup.pdf"])
    no_backups = pd.Series([False])

    urls, backups, no_backups = excel_list_cleaner(
        urls, backups, no_backups
    )

    assert urls[0] == "backup.pdf"

def test_excel_list_cleaner_removes_row_when_all_missing():

    urls = pd.Series([None])
    backups = pd.Series([None])
    no_backups = pd.Series([False])

    urls, backups, no_backups = excel_list_cleaner(
        urls, backups, no_backups
    )
    assert len(urls) == 0
    assert len(backups) == 0

def test_excel_reader_removes_nan(tmp_path):
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "url": [
                "https://site.com/a.pdf",
                None
            ],
            "alt url": [
                "https://backup.com/a.pdf",
                None,
            ],
        }
    )

    file = tmp_path / "test.xlsx"
    df.to_excel(file, index=False)

    urls, backups, no_backups, link_index = excel_reader(tmp_path, "test.xlsx")

    assert len(urls) == 2
    assert urls[0] == "https://site.com/a.pdf"
    assert pd.isna(urls[1])

def test_cleaner_removes_row_when_url_and_backup_is_missing():

    urls = pd.Series([None])
    backups = pd.Series([None])
    no_backups = pd.Series([True])

    urls, backups, no_backups = excel_list_cleaner(
        urls, backups, no_backups
    )

    print(f"urls is of type: {type(urls)}")

    assert len(urls) == 0
    assert len(backups) == 0
    assert len(no_backups) == 0