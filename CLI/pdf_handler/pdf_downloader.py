import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm

# For downloading PDFs
import requests

# Importing the relevant paths from config
from config import PDF_DOWNLOAD_FOLDER

def download_pdf(url_list, backup_list, backup_missing, link_index, timeout_for_links=30):
    '''
    A PDF downloader.
    '''

    PDF_DOWNLOAD_FOLDER.mkdir(exist_ok=True)

    for i, url in enumerate(tqdm(url_list)):

        split_text = url.split("/") # Pretty sure we can delete some of this now
        split_text_2 = split_text[-1].split("?") # This as well. But it works, so lets keep it!
        if len(split_text_2) > 1:
            filename = split_text_2[0]
        else:
            filename = split_text[-1]

        while Path(filename).suffix:
            filename = Path(filename).stem
        filename = f"{link_index[i]}_" + filename + ".pdf"

        save_path = PDF_DOWNLOAD_FOLDER / filename
        
        try:
            r = requests.get(url, timeout=timeout_for_links)
            r.raise_for_status()

            if not is_pdf(r):
                raise ValueError("Primary URL is not a valid PDF.")

        except (requests.RequestException, ValueError):
            if backup_missing[i]:
                continue
            try:
                r = requests.get(backup_list[i],  timeout=timeout_for_links)
                r.raise_for_status()

                if not is_pdf(r):
                    raise ValueError("Secondary URL is not a valid PDF.")
            except (requests.RequestException, ValueError):
                continue

        with open(save_path, "wb") as f:
            f.write(r.content)
        # Alternative pathlib write: save_path.write_bytes(r.content)


def is_pdf(response):
    '''
    Tiny function to check whether downloaded file constitutes a valid PDF (that is, starts with the correct byte input)
    '''
    return response.content.startswith(b"%PDF-")