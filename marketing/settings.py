""" Settings """
import os

HUBSPOT_API_KEY = os.environ["HUBSPOT_API_KEY"]

BROWSER_IP = os.environ.get("BROWSER_IP", "137.184.183.28")

GOOGLE_API_SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.modify"
]
