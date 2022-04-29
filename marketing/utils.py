""" Utility functions """
import os
from fastapi.requests import Request
from mako.template import Template

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")


def get_domain_from_email(email: str) -> str:
    """ Parse and return the domain from the given email """
    tokens = email.split("@")
    return tokens[1]


def lighthouse_score_from_report(report: dict) -> int:
    """ Get the permance score from the specified report """
    score = report.categories.performance.score
    if score < 1:
        score = score * 100
    return int(score)


def public_url(hostname: str) -> str:
    """ Create the default public url """
    return "https://" + hostname.replace(".", "-") + ".mindspun.site"


def get_session(request: Request):
    """ Session dependency """
    return request.state.session


def isoformat(value) -> str:
    """ UTC isoformat """
    result = value.isoformat()
    if "+" not in result:
        result = result + "+00:00"
    return result


def template(name: str, **kwargs) -> str:
    """ Render the HTML as a Mako template """
    if not name.endswith(".html"):
        name = name + ".html"
    path = os.path.join(TEMPLATE_PATH, name)
    return Template(filename=path).render(**kwargs)


def asset_path(name: str) -> str:
    """ Return the file path of an asset """
    return os.path.join(ASSETS_PATH, name)


def asset(name: str) -> bytes:
    """ Return a binary asset """
    path = asset_path(name)
    with open(path, "rb") as fp:
        return fp.read()
