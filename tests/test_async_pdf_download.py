import pytest
import asyncio
import aiohttp

from cli.pdf_handler.async_pdf_download import download_single_pdf


class MockResponse:
    def __init__(self, content):
        self.content = content

    async def read(self):
        return self.content

    def raise_for_status(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


class MockSession:
    def __init__(self):
        self.calls = 0

    def get(self, url, timeout=None):

        self.calls += 1

        if self.calls == 1:
            # Primary URL returns HTML
            return MockResponse(b"<html>Not a PDF</html>")

        # Backup URL returns valid PDF header
        return MockResponse(b"%PDF-1.7 fake pdf")


@pytest.mark.asyncio
async def test_download_uses_backup_when_primary_not_pdf():

    session = MockSession()

    result = await download_single_pdf(
        session=session,
        semaphore=asyncio.Semaphore(1),
        url="https://primary.com/file.pdf",
        backup_url="https://backup.com/file.pdf",
        backup_missing=False,
        link_index=1,
        timeout=aiohttp.ClientTimeout(total=5),
    )

    assert result["success"] is True
    assert result["used_backup"] is True