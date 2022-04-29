""" Manage subscription endpoint(s) """
from fastapi import Depends, Query
from fastapi.responses import Response

from marketing import models, utils
from marketing.main import app


@app.get("/pixel.png")
def pixel(
        email_id: str = Query(..., alias="id"),
        session: models.Session = Depends(utils.get_session),
) -> Response:
    """ Return a tracking pixel for email open """
    email = session.query(models.Sent).get(email_id)
    if email:
        email.open()
        session.commit()

    return Response(
        content=utils.asset("pixel.png"),
        media_type="image/png"
    )
