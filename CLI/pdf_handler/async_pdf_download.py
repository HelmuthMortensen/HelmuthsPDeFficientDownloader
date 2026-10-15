from pathlib import Path
import aiohttp
import asyncio
import aiofiles
from tqdm import tqdm


# Importing the relevant paths from config
from config import PDF_DOWNLOAD_FOLDER


# We define the maximum number of connections at once using a Semaphore




def is_pdf(content:bytes) -> bool:
    return content.startswith(b'%PDF-')

async def download_single_pdf(
        session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, url: str, backup_url: str,
        backup_missing: bool, link_index: int, timeout: aiohttp.ClientTimeout ):
    '''
    Asynchronous download of a single pdf file from a link given.

    input:
        session - 
        semaphore -
        url - 
        backup_url - 
        backup_missing - 
        link_index - 
        timeout - 

    output:
        True/False - Whether the file was succesfully downloaded
    '''
    download_url = url
    async with semaphore:
        try:
            async with session.get(url, timeout=timeout) as response:
                response.raise_for_status()
                content = await response.read()

                if not is_pdf(content):
                    raise ValueError("Primary URL is not a valid PDF.")

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as err:

            if backup_missing:
                return {"success": False,
                        "index": link_index,
                        "filename": None,
                        "used_backup": False,
                        "fail_reason": str(err)
                }

            try:
                async with session.get(backup_url, timeout=timeout) as response:
                    response.raise_for_status()
                    content = await response.read()

                    if not is_pdf(content):
                        raise ValueError("Secondary URL is not a valid PDF.")
                    else:
                        download_url = backup_url

            except (
                aiohttp.ClientError, asyncio.TimeoutError, ValueError,
            ) as err:
                return {"success": False,
                        "index": link_index,
                        "filename": None,
                        "used_backup": True,
                        "fail_reason": str(err)}

    filename = download_url.split("/")[-1].split("?")[0]

    while Path(filename).suffix:
        filename = Path(filename).stem

    filename = f"{link_index}_{filename}.pdf"

    save_path = PDF_DOWNLOAD_FOLDER / filename

    # For Synchronous I/O disk saving, just use write_bytes.
    # save_path.write_bytes(content)

    # But we want the asynchronous package here.

    async with aiofiles.open(save_path, "wb") as f:
        await f.write(content)

    return {"success": True,
            "index": link_index,
            "filename": filename,
            "used_backup": download_url == backup_url,
            "fail_reason": None}


async def download_pdf_async(
        url_list, backup_list, backup_missing,
        link_index, timeout_for_links = 30, max_connections = 20 ):
    '''
    Function for combining multiple asynchronous downloads into one session.
    
    '''
    PDF_DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(max_connections)

    timeout_for_links = aiohttp.ClientTimeout(total=timeout_for_links)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/141.0.0.0 Safari/537.36"
        )
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [
            download_single_pdf(
                session=session,
                semaphore=semaphore,
                url=url_list[i],
                backup_url=backup_list[i],
                backup_missing = backup_missing[i],
                link_index = link_index[i],
                timeout=timeout_for_links,
            )
            for i in range(len(url_list)
                           )
        ]

        results = []

        # Let's do some statistics for successful and failed runs.
        success_count = 0
        failed_indices = []

        for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            result = await task
            
            results.append(result)

            if result["success"]:
                success_count += 1
            else:
                failed_indices.append(result["index"])

        run_result = {
            "successes": success_count,
            "failures": failed_indices
        }

        return results, run_result