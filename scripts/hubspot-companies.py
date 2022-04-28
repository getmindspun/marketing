""" Hubspot list companies """
from marketing.hubspot import HubspotClient


def main():
    """ main entrypoint """
    client = HubspotClient()
    for company in client.crm.companies.get_all():
        print(company)


if __name__ == "__main__":
    main()
