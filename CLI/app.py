import typer
from pathlib import Path
from loguru import logger
import subprocess
import asyncio


# IMPORT FROM OTHER MODULES HERE
from cli.pdf_handler.pdf_downloader import download_pdf
from cli.pdf_handler.async_pdf_download import download_pdf_async
from cli.excel_handler.excel_reader import excel_reader, excel_list_cleaner
from cli.excel_handler.excel_writer import write_report
from cli.config import PROJ_ROOT, EXCEL_SHEETS, PDF_DOWNLOAD_FOLDER, DEFAULT_EXCEL
from cli.joke_handler.joker import joke_returner


app = typer.Typer(help="Hi! Welcome to the PDF Downloader app. We are happy to have you here with us. \n Commands are listed below:")

@app.command("download-con")
def async_download(
    max_connections: int = typer.Option(20, help="Maximum concurrent downloads allowed.")
):
    '''
    Downloads PDFs using a concurrent implementation (fast)
    '''
    url_list, backup_list, backup_missing, link_index = excel_reader()

    results, run_report = asyncio.run(
        download_pdf_async(url_list, backup_list, backup_missing, link_index,timeout_for_links=30 , max_connections=max_connections)
    )

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

    url_list, backup_list, backup_missing, link_index = excel_reader()
    download_pdf(url_list, backup_list, backup_missing, link_index)

    typer.echo("Download complete")

@app.command("tell-me-a-joke")
def joke():
    '''
    Get some jokes.
    '''
    joke_returner()
    logger.info("Jokes have been told.")

print(app.registered_commands)
if __name__ == "__main__":
    app()

