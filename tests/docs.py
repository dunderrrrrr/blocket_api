import os
import shutil
import tempfile

from mkdocs.commands.build import build
from mkdocs.config import load_config


def test_mkdocs_valid_config() -> None:
    config = load_config("mkdocs.yml")
    assert config["site_name"] == "Blocket-API.se"


def test_mkdocs_build() -> None:
    tmpdir = tempfile.mkdtemp()
    config = load_config("mkdocs.yml")
    config["site_dir"] = tmpdir
    build(config)

    index = os.path.join(tmpdir, "index.html")
    assert os.path.exists(index)
    shutil.rmtree(tmpdir)
