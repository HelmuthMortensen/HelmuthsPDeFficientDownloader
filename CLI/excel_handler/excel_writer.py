import pandas as pd
from pathlib import Path


def write_report(report):
    '''
    Function for taking the output of the async pdf downloader and writing a report to an excel sheet.
    '''

    df = pd.DataFrame(report)

    output_path = Path("download_report.xlsx")

    df.to_excel(output_path, index=False)

    return output_path