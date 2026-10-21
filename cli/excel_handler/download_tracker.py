import pandas as pd

from config import DOWNLOADED_PDFS_EXCEL


ID_COLUMN = "id"


def read_downloaded_ids(path=DOWNLOADED_PDFS_EXCEL):
    if not path.exists():
        return set()

    downloaded = pd.read_excel(path)
    if ID_COLUMN not in downloaded.columns:
        raise ValueError(f"Tracking workbook must contain an '{ID_COLUMN}' column: {path}")

    return set(downloaded[ID_COLUMN].dropna())


def record_successful_downloads(results, path=DOWNLOADED_PDFS_EXCEL):
    successful_ids = {
        result["index"] for result in results if result["success"]
    }
    if not successful_ids:
        return path

    path.parent.mkdir(parents=True, exist_ok=True)
    all_downloaded_ids = read_downloaded_ids(path) | successful_ids
    pd.DataFrame({ID_COLUMN: list(all_downloaded_ids)}).to_excel(path, index=False)
    return path


def reset_downloaded_pdfs(path=DOWNLOADED_PDFS_EXCEL):
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(columns=[ID_COLUMN]).to_excel(path, index=False)
    return path
