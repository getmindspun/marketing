#!/usr/bin/env python3
""" CLI """
import os
from datetime import datetime, timedelta
import subprocess

import sqlalchemy
import click

import alembic
from alembic.config import Config

from sqlalchemy_utils import database_exists, create_database

from marketing import models, settings


@click.group()
def cli():
    """ Mindspun CLI """


@cli.command()
def migrate():
    """ Migrate the database schema """
    path = os.path.join(os.path.dirname(settings.__file__), "alembic.ini")
    cfg = Config(path)

    database_url = str(settings.DATABASE_URL)
    if not database_exists(database_url):
        create_database(database_url)

    engine = sqlalchemy.create_engine(database_url)
    inspect = sqlalchemy.inspect(engine)
    if inspect.has_table("migrations"):
        alembic.command.upgrade(cfg, "head")
    else:
        models.BASE.metadata.create_all(engine)
        alembic.command.stamp(cfg, "head")


@cli.command()
@click.option("--name", prompt=True)
@click.option("--force", "-y", is_flag=True)
def delete_campaign(name: str, force: bool):
    """ Delete an existing campaign """
    session = models.Session()

    campaign = models.Campaign.get_by_name(session, name=name)
    if not campaign:
        click.echo(f"Campaign not found '{name}'")
        return

    if not force:
        click.confirm(
            f"Do you want to PERMANENTLY delete '{name}'?", abort=True
        )
    session.delete(campaign)
    session.commit()
    click.echo(f"Campaign '{name}' deleted.")


@cli.command()
@click.option("--name", prompt=True)
def add_campaign(name: str):
    """ Add a new (empty) campaign """
    session = models.Session()

    campaign = models.Campaign.create(
        name=name
    )
    session.add(campaign)
    session.commit()

    click.echo(f"Campaign '{name}' created.")


@cli.command()
@click.option("--email-id", "--id", prompt=True, )
def delete_email_from_campaign(email_id: str):
    """ Delete a campaign by id """
    session = models.Session()

    email = session.query(models.CampaignEmail).get(email_id)
    if not email:
        click.echo(f"Campaign email not found '{email_id}'")
        return

    session.delete(email)
    session.commit()
    click.echo(f"Campaign email '{email_id}' deleted.")


@cli.command()
@click.option("--name", "--campaign", prompt="Campaign name")
@click.option("--template", prompt="Email template")
@click.option("--delay", default=0, show_default=True)
@click.option("--order", default=-1, show_default=False)
def add_email_to_campaign(name: str, template: str, delay: int, order: int):
    """ Add a new (empty) campaign """
    session = models.Session()

    campaign = models.Campaign.get_by_name(session, name)
    if not campaign:
        click.echo(f"Campaign not found '{name}'")
        return

    if order < 0:
        order = 0
        if campaign.emails:
            order = campaign.emails[-1].order + 1000

    email = models.CampaignEmail.create(
        campaign_id=campaign.id,
        template=template,
        send_delay=delay,
        order=order
    )
    session.add(email)
    session.commit()
    click.echo(f"Campaign email created '{email.id}' with order {order}")


@cli.command()
@click.option("--email", prompt="Contact email")
@click.option("--name", "--campaign", prompt="Campaign name")
@click.option("--data", prompt=True, default="{}")
def add_contact_to_campaign(email: str, name: str, data: str):
    """ Add a new (empty) campaign """
    session = models.Session()

    contact = models.Contact.get_by_email(session, email)
    if not contact:
        contact = models.Contact.create(email=email)
        session.add(contact)
        session.commit()
        click.echo(f"Contact created '{email}'")

    campaign = models.Campaign.get_by_name(session, name)
    if not campaign:
        click.echo(f"Campaign not found '{name}'")
        return

    last = None
    for campaign_email in campaign.emails:
        send_at = datetime.utcnow() +\
                  timedelta(seconds=campaign_email.send_delay)
        pending = models.Pending.create(
            campaign_id=campaign.id,
            contact_id=contact.id,
            send_at=send_at,
            prior_email_id=last.id if last else None,
            data=data
        )
        session.add(pending)

    session.commit()

    count = len(campaign.emails)
    click.echo(f"Contact '{email}' added to campaign '{name}': {count} emails")


@cli.command()
def send():
    """ Send any pending emails """


@cli.command(context_settings=dict(
    ignore_unknown_options=True
))
@click.argument("uvicorn_args", nargs=-1, type=click.UNPROCESSED)
def runserver(uvicorn_args):
    """ Start a test server """
    cmd = [
        "uvicorn", "wp.main:app", "--debug"
    ] + list(uvicorn_args)
    subprocess.run(" ".join(cmd), shell=True, check=True)


if __name__ == "__main__":
    cli()
