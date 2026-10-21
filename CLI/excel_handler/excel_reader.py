import pandas as pd
from pathlib import Path

from config import DEFAULT_EXCEL, EXCEL_SHEETS


def excel_reader(filepath=EXCEL_SHEETS, filename=DEFAULT_EXCEL, skip_ids=()):
    '''
    Simple function for reading the excel and returning the needed column lists.
    
    input:
        filepath - Path to folder containing the excel. Defaults to current_loc.parent.parent / sheets
        filename - Str for the name of the excel sheet to be read.

    output:
        url_list - List of Str-URLs in the "url" column 
        url_backup_list - List of Str-URLs in the "alt url" column
        no_backups - List of backups containing no links at all.
        link_index - list of int link indeces from original Excel

    '''

    excel_path = filepath / filename
    excel = pd.read_excel(excel_path)

    if skip_ids:
        excel = excel.loc[~excel["id"].isin(skip_ids)]

    for column in ("url", "alt url"):
        excel[column] = excel[column].replace(r"^\s*$", pd.NA, regex=True)

    has_url = excel["url"].notna() | excel["alt url"].notna()
    excel = excel.loc[has_url]

    link_index = excel["id"]
    url_list = excel["url"]
    url_backup_list = excel["alt url"]
    no_backups = pd.isna(url_backup_list)
    url_list, url_backup_list, no_backups = excel_list_cleaner(url_list, url_backup_list, no_backups)

    return (
        url_list.reset_index(drop=True),
        url_backup_list.reset_index(drop=True),
        no_backups.reset_index(drop=True),
        link_index.reset_index(drop=True),
    )


def excel_list_cleaner(url_list, url_backup_list, no_backups):
    '''
    Function for cleaning the lists returned by the excel reader, such as missing url's.

    input:
        url_list - List from previous function
        url_backup_list - List from previous function
        no_backups - List from previous function

    output:
        url_list - List of urls cleaned
        url_backup_list - List of backup urls cleaned
        no_backups - List of no backups booleans cleaned
    '''

    # We want to check if there are any missing links in the primary url column, and if so, take the one in the backup.
    missing_links = pd.isna(url_list)

    for i, link in enumerate(missing_links):
        if link == True: 
            if url_backup_list[i]:
                url_list[i] = url_backup_list[i]
            else:
                url_list.pop(i)
                url_backup_list.pop(i)
                no_backups.pop(i)

    return url_list, url_backup_list, no_backups