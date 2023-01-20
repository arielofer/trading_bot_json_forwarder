import re
from base64 import urlsafe_b64decode, urlsafe_b64encode


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def parse_message(payload):
    mimeType = payload.get("mimeType")
    body = payload.get("body")
    data = body.get("data")
    alert_json = ""
    if mimeType == "text/html":
        text = urlsafe_b64decode(data).decode()
        try:
            alert_json = re.search(
                r"(\{  &#[^}]+\})", text).group(1).replace('&#34;', '"')
            print(alert_json)
            with open("alert_json.txt", "wt") as f:
                f.write(alert_json)
        except AttributeError:
            print("[ERROR] didnt find the json :(")

    # if the email payload is text plain
    else:
        text = urlsafe_b64decode(data).decode()
        try:
            alert_json = re.search(r"(\{[^}]+\})", text).group(1)
            print(alert_json)
            with open("alert_json.txt", "wt") as f:
                f.write(alert_json)
        except AttributeError:
            print("[ERROR] didnt find the json :(")


def parse_parts(parts):
    """
    Utility function that parses the content of an email partition
    """
    if parts:
        for part in parts:
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(part.get("parts"))

            parse_message(part)
