""" Send gmail from draft """
import argparse
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from marketing import utils
from marketing.google import GoogleApiClient

footer = """
<div style="width:100%;text-align:left">
<p>
Don"t want to receive emails from me?
<a href="https://api.mindspun.com/marketing/unsubscribe?id={{contact_id}}">
Unsubscribe
</a>
<!--
<img src="https://api.mindspun.com/marketing/pixel.png?id={{email_id}}">
-->
</p>
</div>
"""

followup_html = """
<div>
<h1>Hey, still there?</h1>
<p>We haven"t heard from you so...</p>
</div>
"""


def main():
    """ main entrypoint """
    parser = argparse.ArgumentParser()
    parser.add_argument("--sender", required=True)
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", required=True)
    args = parser.parse_args()

    client = GoogleApiClient()
    draft = client.gmail.get_draft_by_subject(args.subject)
    if draft is None:
        print("Draft not found: " + args.subject, file=sys.stderr)
        sys.exit(1)

    html = draft.html()
    html += footer

    for email in args.to.split(","):
        email = email.strip()

        data = {"email": email}

        msg = MIMEMultipart("alternative")
        msg["To"] = email
        msg["From"] = args.sender
        msg["Subject"] = utils.render(draft.subject, **data)

        part = MIMEText(html, "html")
        msg.attach(part)

        result = client.gmail.send(msg)

        message = client.gmail.get_message(result["id"])
        message_id = utils.get_message_header_value(message, "Message-Id")

        followup = MIMEMultipart("alternative")
        followup["To"] = email
        followup["From"] = args.sender
        followup["Subject"] = utils.render(draft.subject, **data)
        followup["In-Reply-To"] = message_id
        followup["References"] = message_id

        part = MIMEText(followup_html + footer, "html")
        followup.attach(part)

        result = client.gmail.send(
            followup,
            thread_id=result["threadId"]
        )
        print(result)


if __name__ == "__main__":
    main()
