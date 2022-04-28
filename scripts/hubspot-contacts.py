""" Hubspot list contacts """
from marketing.hubspot import HubspotClient


def main():
    """ main entrypoint """
    client = HubspotClient()
    for contact in client.crm.contacts.get_all():
        print(contact)


if __name__ == "__main__":
    main()
