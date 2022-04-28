""" Hubspot delete contact """
import argparse
import sys

from dotenv import load_dotenv

from marketing.hubspot import HubspotClient

load_dotenv()


def main():
    """ main entrypoint """
    parser = argparse.ArgumentParser()
    parser.add_argument("email")
    args = parser.parse_args()

    client = HubspotClient()

    contact = client.get_contact_by_email(args.email)
    if not contact:
        print("Not found: " + args.email)
        sys.exit(1)

    client.archive_contact(contact.id)


if __name__ == "__main__":
    main()
