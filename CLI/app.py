import typer
from pathlib import Path
from loguru import logger
import subprocess
import asyncio
import sys


# IMPORT FROM OTHER MODULES HERE
from pdf_handler.pdf_downloader import download_pdf
from pdf_handler.async_pdf_download import download_pdf_async
from excel_handler.excel_reader import excel_reader, excel_list_cleaner
from excel_handler.excel_writer import write_report
from excel_handler.download_tracker import (
    read_downloaded_ids,
    record_successful_downloads,
    reset_downloaded_pdfs,
)
from config import PROJ_ROOT, EXCEL_SHEETS, PDF_DOWNLOAD_FOLDER, DEFAULT_EXCEL
from joke_handler.joker import joke_returner


app = typer.Typer(help="Hi! Welcome to the PDF Downloader app. We are happy to have you here with us. \n Commands are listed below:",
                  no_args_is_help=True)

@app.command("download-con")
def async_download(
    max_connections: int = typer.Option(20, help="Maximum concurrent downloads allowed.")
):
    '''
    Downloads PDFs using a concurrent implementation. (fast)
    '''
    url_list, backup_list, backup_missing, link_index = excel_reader(
        skip_ids=read_downloaded_ids()
    )

    results, run_report = asyncio.run(
        download_pdf_async(url_list, backup_list, backup_missing, link_index,timeout_for_links=30 , max_connections=max_connections)
    )
    record_successful_downloads(results)

    typer.echo("\nDownload complete!")

    typer.echo(
        f"Successful downloads: {run_report['successes']}"
    )

    typer.echo(
        f"Failed downloads: {len(run_report['failures'])}"
    )

    if run_report["failures"]:
        typer.echo(
            f"Failed indices: {run_report['failures']}"
        )

    output_file = write_report(results)

    typer.echo(f"Results report saved to {output_file}")

@app.command("download-seq")
def download():
    '''
    Download PDFs using a sequential implementation. (slow)
    '''

    url_list, backup_list, backup_missing, link_index = excel_reader(
        skip_ids=read_downloaded_ids()
    )
    results = download_pdf(url_list, backup_list, backup_missing, link_index)
    record_successful_downloads(results)

    typer.echo("Download complete")

@app.command("reset")
def reset():
    """Clear the downloaded-PDF tracking sheet."""
    reset_downloaded_pdfs()
    typer.echo("Downloaded-PDF tracking sheet cleared.")

@app.command("tell-me-a-joke")
def joke():
    '''
    Get some jokes. (funny)
    '''
    joke_returner()
    logger.info("Jokes have been told.")


if __name__ == "__main__":
    app()
