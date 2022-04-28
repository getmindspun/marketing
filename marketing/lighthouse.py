""" Lighthouse """
import json
import os
import subprocess
from urllib.parse import urlparse

import addict
from tld import get_tld

from . import settings


def lighthouse(
        url: str,
        path: str = None,
        quiet: bool = True,
        local: bool = False
):
    """ Run lighthouse """
    parsed = urlparse(url)
    tld = get_tld(url, as_object=True)
    if not path:
        path = os.path.join(
            "./store", parsed.hostname, "reports", tld.domain
        )

    os.makedirs(os.path.dirname(path), exist_ok=True)

    cmd = [
        "npx",
        "lighthouse",
        url,
        "--config-path=lighthouse.config.json",
        "--output='html,json'",
        "--output-path=" + path
    ]

    if local:
        cmd.extend([
            "--chrome-flags='--headless --no-sandbox'"
        ])
    else:
        cmd.extend([
            "---hostname=" + settings.BROWSER_IP,
            "--port=9222"
        ])

    if quiet:
        cmd.append("--quiet")

    subprocess.run(cmd, check=True)

    with open(path + ".report.json", encoding="utf-8") as fp:
        return addict.Dict(json.load(fp))
