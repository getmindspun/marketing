""" Hubspot get contact """
import argparse
from marketing.hubspot import HubspotClient


def main():
    """ main entrypoint """
    parser = argparse.ArgumentParser()
    parser.add_argument("email")
    args = parser.parse_args()

    client = HubspotClient()

    contact = client.get_contact_by_email(args.email)
    if contact:
        print(contact)
    else:
        print("Not found: " + args.email)


if __name__ == "__main__":
    main()
