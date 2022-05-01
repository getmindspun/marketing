""" Manage subscription endpoint(s) """
import logging
from fastapi import Depends, Query
from fastapi.responses import Response

from marketing import models, utils
from marketing.main import app

logger = logging.getLogger(__name__)


@app.get("/pixel.png")
def pixel(
        email_id: str = Query(..., alias="id"),
        session: models.Session = Depends(utils.get_session),
) -> Response:
    """ Return a tracking pixel for email open """
    email: models.Sent = session.query(models.Sent).get(email_id)
    if email:
        logger.info("Email opened by %s: %s", email.contact.email, email_id)
        email.open()
        session.commit()

    return Response(
        content=utils.asset("pixel.png"),
        media_type="image/png"
    )
