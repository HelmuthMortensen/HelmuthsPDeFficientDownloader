from cli.pdf_handler.async_pdf_download import test_url

import asyncio

asyncio.run(
    test_url("https://www.hul.co.in/files/hul-integrated-annual-report-2024-25.pdf")
)