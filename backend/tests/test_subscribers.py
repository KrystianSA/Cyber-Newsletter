import pytest

from app.database import get_db
from app.main import app
from app.models import Subscriber


def test_new_email_is_saved(client, db, count_subscribers):
    res = client.post("/subscribers", json={"email": "jan@x.pl"})

    assert res.status_code == 201
    assert res.json() == {"message": "ok"}
    assert count_subscribers() == 1
    assert db.query(Subscriber).one().email == "jan@x.pl"


def test_duplicate_email_gives_same_response_and_no_second_row(client, count_subscribers):
    first = client.post("/subscribers", json={"email": "jan@x.pl"})
    second = client.post("/subscribers", json={"email": "jan@x.pl"})

    assert second.status_code == 201
    assert second.json() == {"message": "ok"}
    assert count_subscribers() == 1
    # Ochrona przed enumeracją: nowy i istniejący adres są nie do odróżnienia.
    assert (second.status_code, second.json()) == (first.status_code, first.json())


@pytest.mark.parametrize("email", ["abc", "a@", ""])
def test_invalid_email_returns_422_and_saves_nothing(client, count_subscribers, email):
    res = client.post("/subscribers", json={"email": email})

    assert res.status_code == 422
    assert count_subscribers() == 0


def test_missing_email_field_returns_422(client, count_subscribers):
    res = client.post("/subscribers", json={})

    assert res.status_code == 422
    assert count_subscribers() == 0


def test_non_json_body_returns_422(client, count_subscribers):
    res = client.post(
        "/subscribers",
        content="email=jan@x.pl",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert res.status_code == 422
    assert count_subscribers() == 0


def test_email_case_is_normalized_so_variants_are_one_subscriber(
    client, db, count_subscribers
):
    first = client.post("/subscribers", json={"email": "Jan@x.pl"})
    second = client.post("/subscribers", json={"email": "jan@x.pl"})

    assert first.status_code == second.status_code == 201
    assert count_subscribers() == 1
    assert db.query(Subscriber).one().email == "jan@x.pl"


def test_session_still_works_after_duplicate_rollback(client, db, count_subscribers):
    # Jedna współdzielona sesja dla wszystkich żądań: gdyby po IntegrityError
    # nie było rollback(), następny zapis padłby na „zatrutej" sesji.
    app.dependency_overrides[get_db] = lambda: db
    try:
        assert client.post("/subscribers", json={"email": "a@x.pl"}).status_code == 201
        assert client.post("/subscribers", json={"email": "a@x.pl"}).status_code == 201
        assert client.post("/subscribers", json={"email": "b@x.pl"}).status_code == 201
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert count_subscribers() == 2
