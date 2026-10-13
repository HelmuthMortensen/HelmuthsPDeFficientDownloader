import typer
from pathlib import Path
from loguru import logger
import subprocess


# IMPORT FROM OTHER MODULES HERE
from pdf_handler.pdf_downloader import download_pdf
from excel_handler.excel_reader import excel_reader, excel_list_cleaner
from config import PROJ_ROOT, EXCEL_SHEETS, PDF_DOWNLOAD_FOLDER, DEFAULT_EXCEL


app = typer.Typer(help="Hi! Welcome to the PDF Downloader app. We are happy to have you here with us. \n Commands are listed below:")

@app.command("download")
def download():
    '''
    Download PDFs specified by the excel sheet.
    '''

    url_list, backup_list, backup_missing, link_index = excel_reader()
    download_pdf(url_list, backup_list, backup_missing, link_index)

    typer.echo("Download complete")

@app.command("Nothing")
def nothing_here():
    '''
    This is just a test for now
    '''
    logger.info("Just testing")
    pass

print(app.registered_commands)
if __name__ == "__main__":
    app()

