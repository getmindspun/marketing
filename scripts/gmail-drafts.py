""" List gmail drafts """
from marketing.google import GoogleApiClient


def main():
    """ main entrypoint """
    client = GoogleApiClient()
    for draft in client.gmail.drafts():
        print(draft.id + ": " + draft.subject)


if __name__ == "__main__":
    main()
