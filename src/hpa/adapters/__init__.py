from hpa.adapters.base import RawCandidate, SearchAdapter, SearchFailure
from hpa.adapters.devpost import DevpostAdapter
from hpa.adapters.fixture import FixtureAdapter
from hpa.adapters.github import GitHubAdapter

ADAPTERS = {
    "github": GitHubAdapter,
    "devpost": DevpostAdapter,
    "fixture": FixtureAdapter,
}


def build_adapter(name: str, source: dict) -> SearchAdapter:
    try:
        cls = ADAPTERS[name]
    except KeyError:
        raise SearchFailure(f"unknown adapter: {name}") from None
    return cls(source)


__all__ = [
    "ADAPTERS",
    "DevpostAdapter",
    "FixtureAdapter",
    "GitHubAdapter",
    "RawCandidate",
    "SearchAdapter",
    "SearchFailure",
    "build_adapter",
]
