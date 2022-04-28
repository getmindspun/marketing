""" Hubspot create company """
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
    if company:
        print("Company already exists: " + args.domain)
        sys.exit(1)

    company = client.create_company(args.domain)
    print(company)


if __name__ == "__main__":
    main()
