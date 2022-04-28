""" Hubspot create contact """
import argparse
import sys

from dotenv import load_dotenv

from marketing.hubspot import HubspotClient
from marketing import utils

load_dotenv()


def main():
    """ main entrypoint """
    parser = argparse.ArgumentParser()
    parser.add_argument("email")
    parser.add_argument("--domain")
    args = parser.parse_args()

    client = HubspotClient()

    domain = args.domain
    if not domain:
        domain = utils.get_domain_from_email(args.email)

    company = client.get_company_by_domain(domain)
    if not company:
        print("Company doesn't exist: " + domain)
        sys.exit(1)

    contact = client.create_contact(args.email, company.id)
    print(contact)


if __name__ == "__main__":
    main()
