import pytest


def preflight(client, origin):
    return client.options(
        "/subscribers",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )


@pytest.mark.parametrize("origin", ["http://localhost:5173", "http://127.0.0.1:5173"])
def test_preflight_allows_frontend_origins(client, origin):
    res = preflight(client, origin)

    assert res.status_code == 200
    assert res.headers["access-control-allow-origin"] == origin


def test_preflight_rejects_foreign_origin(client):
    res = preflight(client, "https://evil.example")

    assert res.status_code == 400
    assert "access-control-allow-origin" not in res.headers
