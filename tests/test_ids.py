from hpa.ids import canonical_repo_url, slugify


def test_slugify_basic():
    assert slugify("Fixture Alpha") == "fixture-alpha"
    assert slugify("  Hello, World!  ") == "hello-world"


def test_slugify_stable_and_ascii():
    assert slugify("Café Démo") == "cafe-demo"
    assert slugify("!!!") == "untitled"


def test_canonical_repo_url_github_normalizes_case_and_slash():
    a = canonical_repo_url("https://GitHub.com/Foo/Bar/")
    b = canonical_repo_url("http://github.com/foo/bar")
    assert a == b == "https://github.com/foo/bar"


def test_canonical_repo_url_strips_query_and_fragment():
    assert canonical_repo_url("https://github.com/a/b?x=1#frag") == "https://github.com/a/b"


def test_canonical_repo_url_adds_scheme():
    assert canonical_repo_url("github.com/a/b") == "https://github.com/a/b"
