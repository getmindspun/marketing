""" Send gmail from draft """
import argparse

from marketing import utils
from marketing.google import GoogleApiClient


def main():
    """ main entrypoint """
    parser = argparse.ArgumentParser()
    parser.add_argument("--thread-id", "--id", required=True)
    args = parser.parse_args()

    client = GoogleApiClient()
    messages = client.gmail.service.users().threads().get(
        userId="me", id=args.thread_id
    ).execute().get("messages")
    for msg in messages:
        print(msg["id"] + ": " + utils.get_message_header_value(msg, "From"))


if __name__ == "__main__":
    main()
