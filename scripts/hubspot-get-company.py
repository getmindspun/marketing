""" Hubspot company program """
import argparse
from marketing.hubspot import HubspotClient


def main():
    """ main entrypoint """
    parser = argparse.ArgumentParser()
    parser.add_argument("domain")
    args = parser.parse_args()

    client = HubspotClient()

    company = client.get_company_by_domain(args.domain)
    if company:
        print(company)
    else:
        print("Not found: " + args.domain)


if __name__ == "__main__":
    main()
