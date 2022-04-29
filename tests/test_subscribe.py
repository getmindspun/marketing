from marketing import models


def test_unsubscribe(client, session):
    contact = models.Contact.create(email="test@example.com")
    contact.resubscribe()
    session.add(contact)
    session.commit()

    assert not contact.unsubscribed

    res = client.get("/unsubscribe", params={"id": contact.id})
    res.raise_for_status()

    session.rollback()
    assert contact.unsubscribed


def test_unsubscribe_bad_id(client, database):
    res = client.get("/unsubscribe", params={"id": "123"})
    assert res.status_code == 400


def test_resubscribe(client, session):
    contact = models.Contact.create(email="test@example.com")
    contact.unsubscribe()
    session.add(contact)
    session.commit()

    res = client.get("/resubscribe", params={"id": contact.id})
    res.raise_for_status()

    session.rollback()
    assert not contact.unsubscribed


def test_resubscribe_bad_id(client, database):
    res = client.get("/resubscribe", params={"id": "123"})
    assert res.status_code == 400
