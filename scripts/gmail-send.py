""" Send gmail """
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from marketing.google import GoogleApiClient

html = """\
<html>
  <body>
    <p><b>Python Mail Test</b><br>
    <span style="color:red">Hello World</span>
    </p>
  </body>
</html>
"""


def main():
    """ main entrypoint """
    parser = argparse.ArgumentParser()
    parser.add_argument("--sender", required=True)
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", default="Gmail test")
    args = parser.parse_args()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = args.subject
    msg["From"] = args.sender
    msg["To"] = args.to

    part = MIMEText(html, "html")
    msg.attach(part)

    client = GoogleApiClient()
    client.gmail.send(msg)


if __name__ == "__main__":
    main()
