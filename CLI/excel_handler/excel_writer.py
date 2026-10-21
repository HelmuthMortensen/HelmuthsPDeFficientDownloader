import pandas as pd
from pathlib import Path
import time

from config import DOWNLOAD_REPORTS_LOCATION


def write_report(report):
    '''
    Function for taking the output of the async pdf downloader and writing a report to an excel sheet.

    input:
        report - List of dict, in the structure of the download_single_pdf function
                    "success": True,
                    "index": link_index,
                    "filename": filename,
                    "used_backup": download_url == backup_url,
                    "fail_reason": None}

    output:
        output_path - Str path to Excel location
    '''

    df = pd.DataFrame(report)

    # Create the folder if it does not exist:
    DOWNLOAD_REPORTS_LOCATION.mkdir(parents=True, exist_ok=True)

    file_name = time.localtime()
    output_loc = DOWNLOAD_REPORTS_LOCATION / f"download_report_{file_name[0]}{file_name[1]}{file_name[2]}.xlsx"

    df.to_excel(output_loc, index=False)

    return output_loc