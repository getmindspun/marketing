""" Utility functions """


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
