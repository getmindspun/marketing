""" Hubspot company program """
import argparse
import sys

from dotenv import load_dotenv

from marketing.hubspot import HubspotClient

load_dotenv()


def main():
    """ main entrypoint """
    parser = argparse.ArgumentParser()
    parser.add_argument("domain")
    args = parser.parse_args()

    client = HubspotClient()

    company = client.get_company_by_domain(args.domain)
    if not company:
        print("Not found: " + args.domain)
        sys.exit(1)

    client.archive_company(company.id)


if __name__ == "__main__":
    main()
