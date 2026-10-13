from pathlib import Path

from loguru import logger


# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT is located at: {PROJ_ROOT}")

EXCEL_SHEETS = PROJ_ROOT / "sheets"
PDF_DOWNLOAD_FOLDER = PROJ_ROOT / "PDFs"
DEFAULT_EXCEL = "GRI_2017_2025.xlsx"

