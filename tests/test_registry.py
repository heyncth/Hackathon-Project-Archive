from pathlib import Path

import pytest
import yaml

from hpa.registry import RegistryError, get_source, load_registry, sources_for_adapter


def test_load_registry_from_repo_root():
    root = Path(__file__).resolve().parents[1]
    sources = load_registry(root)
    assert len(sources) >= 3
    ids = {s["id"] for s in sources}
    assert {"github-search", "devpost-galleries", "local-fixtures"} <= ids


def test_registry_rejects_missing_fields(tmp_path: Path):
    (tmp_path / "sources").mkdir()
    (tmp_path / "sources" / "sources.yaml").write_text(
        yaml.safe_dump({"sources": [{"id": "x"}]}), encoding="utf-8"
    )
    with pytest.raises(RegistryError):
        load_registry(tmp_path)


def test_registry_missing_file(tmp_path: Path):
    with pytest.raises(RegistryError):
        load_registry(tmp_path)


def test_sources_for_adapter_and_get_source():
    root = Path(__file__).resolve().parents[1]
    sources = load_registry(root)
    github = sources_for_adapter(sources, "github")
    assert len(github) == 1
    assert get_source(sources, "github-search")["adapter"] == "github"
    with pytest.raises(RegistryError):
        get_source(sources, "nope")
