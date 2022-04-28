""" Hubspot company program """
import argparse
import sys

from tld import get_fld

from marketing.hubspot import HubspotClient
from marketing.lighthouse import lighthouse
from marketing import utils


def main():
    """ main entrypoint """
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--score", type=float)
    args = parser.parse_args()

    client = HubspotClient()

    domain = get_fld(args.url)

    company = client.get_company_by_domain(domain)
    if not company:
        print("Not found: " + domain, file=sys.stderr)
        sys.exit(1)

    if not args.score:
        report = lighthouse(args.url)
        score = utils.lighthouse_score_from_report(report)
    else:
        score = args.score

    print("Base lighthouse score: " + str(score))

    client.update_company_property(
        company.id, lighthouse_base_score=str(score)
    )


if __name__ == "__main__":
    main()
