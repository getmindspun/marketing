from datetime import datetime
from marketing import models


def test_pixel(client, session):
    contact = models.Contact.create(email="test@example.com")
    session.add(contact)

    campaign = models.Campaign.create(name="rolling")
    session.add(campaign)

    campaign_email = models.CampaignEmail.create(
        template="template"
    )
    campaign_email.campaign = campaign
    session.add(campaign_email)

    sent = models.Sent.create(
        sent_at=datetime.utcnow(),
        email_id="123",
        message_id="456",
        thread_id="789"
    )
    sent.contact = contact
    sent.campaign_email = campaign_email
    session.add(sent)
    session.commit()

    assert not sent.opened

    res = client.get("/pixel.png", params={"id": sent.id})
    assert res.status_code == 200

    session.rollback()
    assert sent.opened


def test_pixel_missing_id(client, mocker):
    logger_warning = mocker.patch("marketing.main.logger.warning")
    res = client.get("/pixel.png")
    assert res.status_code == 422
    logger_warning.assert_called_once()
