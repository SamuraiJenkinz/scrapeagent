"""Storage helpers for local filesystem + Azure Blob."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

try:
    from azure.storage.blob import BlobClient
except ImportError:  # pragma: no cover
    BlobClient = None  # type: ignore


class Writer(Protocol):
    def write_text(self, content: str) -> Path:
        ...


def write_locally(target: Path, content: str) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


def upload_blob(
    conn_str: str,
    container: str,
    blob_name: str,
    content: str,
) -> None:
    if BlobClient is None:
        raise RuntimeError("azure-storage-blob is not installed.")
    client = BlobClient.from_connection_string(
        conn_str=conn_str, container_name=container, blob_name=blob_name
    )
    client.upload_blob(content, overwrite=True)

