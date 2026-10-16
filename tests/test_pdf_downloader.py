from types import SimpleNamespace
import requests

from cli.pdf_handler.pdf_downloader import download_pdf

def test_falls_back_to_backup_when_primary_not_pdf(monkeypatch):
    calls = []

    def fake_get(url, timeout=None):
        calls.append(url)

        if url == "primary":
            return SimpleNamespace(
                content=b"<html>Access Denied</html>",
                raise_for_status=lambda:None,
            )
        if url == "backup":
            return SimpleNamespace(
                content=b"%PDF-1.7 fake pdf",
                raise_for_status=lambda:None
            )

    monkeypatch.setattr(
        "cli.pdf_handler.pdf_downloader.requests.get",
        fake_get
    )

    download_pdf(
        url_list=["primary"],
        backup_list=["backup"],
        backup_missing=[False],
        link_index=[1],
    )

    assert calls == ["primary", "backup"]


def test_falls_back_when_primary_raises(monkeypatch):
    calls = []

    def fake_get(url, timeout=None):
        calls.append(url)

        if url == "primary":
            raise requests.HTTPError("404")

        return SimpleNamespace(
            content=b"%PDF-1.7 fake pdf",
            raise_for_status=lambda: None,
        )

    monkeypatch.setattr(
        "cli.pdf_handler.pdf_downloader.requests.get",
        fake_get,
    )

    download_pdf(
        ["primary"],
        ["backup"],
        [False],
        [1]
    )

    assert calls == ["primary", "backup"]