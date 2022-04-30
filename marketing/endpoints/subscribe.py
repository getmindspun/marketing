""" Manage subscription endpoint(s) """
from fastapi import Depends, Query, exceptions
from fastapi.responses import HTMLResponse

from marketing import models, utils
from marketing.main import app


@app.get("/unsubscribe")
def unsubscribe(
        contact_id: str = Query(..., alias="id"),
        session: models.Session = Depends(utils.get_session),
) -> HTMLResponse:
    """ Validate the user via the API key and return user info """
    contact = session.query(models.Contact).get(contact_id)
    if not contact:
        raise exceptions.HTTPException(400)

    contact.unsubscribe()
    models.Pending.delete_for_contact(
        session, contact_id=contact_id, commit=False
    )
    session.commit()

    return HTMLResponse(
        content=utils.render_template("unsubscribed", contact_id=contact_id)
    )


@app.get("/resubscribe")
def resubscribe(
        contact_id: str = Query(..., alias="id"),
        session: models.Session = Depends(utils.get_session),
) -> HTMLResponse:
    """ Validate the user via the API key and return user info """
    contact = session.query(models.Contact).get(contact_id)
    if not contact:
        raise exceptions.HTTPException(400)

    contact.resubscribe()
    session.commit()

    return HTMLResponse(
        content=utils.render_template("resubscribed", contact_id=contact_id)
    )
