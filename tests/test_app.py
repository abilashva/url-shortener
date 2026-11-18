import pytest

from shortener import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "test.db"))
    return app.test_client()


def test_shorten_and_redirect(client):
    res = client.post("/shorten", json={"url": "https://example.com/page"})
    assert res.status_code == 201
    code = res.get_json()["code"]
    redirect = client.get("/" + code)
    assert redirect.status_code == 302
    assert redirect.headers["Location"] == "https://example.com/page"


def test_invalid_url(client):
    res = client.post("/shorten", json={"url": "not-a-url"})
    assert res.status_code == 400


def test_custom_alias_and_duplicate(client):
    ok = client.post("/shorten", json={"url": "https://a.com", "alias": "mylink"})
    assert ok.status_code == 201
    dup = client.post("/shorten", json={"url": "https://b.com", "alias": "mylink"})
    assert dup.status_code == 409


def test_click_counter(client):
    code = client.post("/shorten", json={"url": "https://example.com"}).get_json()["code"]
    client.get("/" + code)
    client.get("/" + code)
    assert client.get("/stats/" + code).get_json()["clicks"] == 2


def test_unknown_code(client):
    assert client.get("/doesnotexist").status_code == 404
