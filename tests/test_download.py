"""Exercise real HTTP transfers, checksum failures, and safe ZIP handling."""

import functools
import hashlib
import http.server
import threading
import zipfile

import pytest


@pytest.fixture
def server(tmp_path, monkeypatch):
    # Local test traffic must not be sent through an institutional HTTP proxy.
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost")
    monkeypatch.setenv("no_proxy", "127.0.0.1,localhost")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(tmp_path))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield tmp_path, f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()
    httpd.server_close()
    thread.join()


def test_partial_download_handles_server_without_range_and_checks_hash(server, tmp_path):
    from napari_workshop.download import download_file

    root, base = server
    payload = b"real microscopy transfer test" * 100
    (root / "remote.bin").write_bytes(payload)
    output = tmp_path / "downloads"
    output.mkdir()
    (output / "remote.bin.part").write_bytes(payload[:10])
    spec = {
        "name": "remote.bin",
        "url": base + "/remote.bin",
        "size": len(payload),
        "checksum": "md5:" + hashlib.md5(payload).hexdigest(),
    }
    path = download_file(spec, output)
    assert path.read_bytes() == payload
    assert not path.with_suffix(".bin.part").exists()
    mtime = path.stat().st_mtime_ns
    download_file(spec, output)
    assert path.stat().st_mtime_ns == mtime


def test_bad_checksum_never_publishes_complete_file(server, tmp_path):
    from napari_workshop.download import download_file

    root, base = server
    (root / "wrong.bin").write_bytes(b"wrong")
    spec = {
        "name": "wrong.bin",
        "url": base + "/wrong.bin",
        "size": 5,
        "checksum": "md5:" + hashlib.md5(b"right").hexdigest(),
    }
    with pytest.raises((ValueError, RuntimeError), match="checksum|Checksum"):
        download_file(spec, tmp_path / "output", attempts=1)
    assert not (tmp_path / "output/wrong.bin").exists()


def test_unsafe_zip_cannot_escape_destination(tmp_path):
    from napari_workshop.download import extract_teaching

    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("../escape", b"bad")
    with pytest.raises(ValueError, match="Unsafe|unsafe"):
        extract_teaching(archive, tmp_path / "teaching")
    assert not (tmp_path / "escape").exists()
