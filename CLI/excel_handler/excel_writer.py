import pandas as pd
from pathlib import Path


def write_report(report, output_path = Path("download_report.xlsx")):
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

    df.to_excel(output_path, index=False)

    return output_path