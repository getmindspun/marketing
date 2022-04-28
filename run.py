""" Setup a new contact via URL/email """
import argparse
import subprocess
import typing
from urllib.parse import urlparse

from tld import get_fld

from marketing.hubspot import HubspotClient
from marketing.lighthouse import lighthouse
from marketing import utils


def ssh(server: str, args: typing.Union[str, typing.List[str]], **kwargs):
    """ Run a SSH command on the given server """
    cmd = ["ssh", server]
    if isinstance(args, str):
        cmd.append(args)
    else:
        cmd.extend(args)

    check = kwargs.pop("check", False)
    return subprocess.run(cmd, check=check, **kwargs)


def dir_exists(server: str, name: str):
    """ Check if a remote directory exists """
    process = ssh(server, "bash -c '[ -d " + name + " ]'")
    return process.returncode == 0


def crawler_manage(server: str, args: typing.List[str], **kwargs):
    """ Run docker-compose run -rm crawler manage ... """
    cmd = [
        "docker-compose", "-f", "/var/mindspun/docker-compose.yaml",
        "run", "--rm", "crawler", "manage"
    ]
    cmd.extend(args)

    check = kwargs.pop("check", True)
    return ssh(server, cmd, check=check, **kwargs)


def setup(server: str, url: str, public_url: str = None):
    """ Run the shield setup command """
    origin_url = url.scheme + "://" + url.netloc

    if not public_url:
        public_url = utils.public_url(url.hostname)

    cmd = ["setup", "--origin-url", origin_url, "--public-url", public_url]
    crawler_manage(server, cmd)


def main():
    """ Main entrypoint """
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--server", default="x0")
    parser.add_argument("--public-url", default=None)
    parser.add_argument("--force-all", action="store_true", default=False)
    args = parser.parse_args()

    url = urlparse(args.url)

    public_url = args.public_url
    if not public_url:
        public_url = utils.public_url(url.hostname)

    if not dir_exists(args.server, "/var/mindspun/store/" + url.hostname):
        setup(args.server, args.url, public_url=public_url)

    cmd = ["run", url.hostname, "--max-pages=1", "--url", args.url]
    if args.force_all:
        cmd.append("--force-all")
    else:
        cmd.append("--force")

    crawler_manage(args.server, cmd, )

    client = HubspotClient()

    domain = get_fld(args.url)

    company = client.get_company_by_domain(domain)
    if not company:
        company = client.create_company(args.url)

    contact = client.get_contact_by_email(args.email)
    if not contact:
        client.create_contact(args.email, company.id)

    lighthouse_base_score = company.lighthouse_base_score
    if not lighthouse_base_score:
        report = lighthouse(args.url)
        lighthouse_base_score = utils.lighthouse_score_from_report(report)
        client.update_company_property(
            company.id, lighthouse_base_score=lighthouse_base_score
        )
        print("Lighthouse base score: " + str(lighthouse_base_score))

    lighthouse_optimized_score = company.lighthouse_optimized_score
    if not lighthouse_optimized_score:
        report = lighthouse(public_url)
        lighthouse_optimized_score = utils.lighthouse_score_from_report(report)
        client.update_company_property(
            company.id, lighthouse_optimized_score=lighthouse_optimized_score
        )
        print("Lighthouse optimized score: " + str(lighthouse_optimized_score))


if __name__ == "__main__":
    main()
