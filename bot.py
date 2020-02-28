from linkedin import LISession, LIProfile, LIProfileError
from mails import Mailbox, Message
from datetime import datetime
from sheet import Sheet
import credentials
import time


def construct_sales_url(html):
    from html import unescape

    html = unescape(html)
    prefix = "https://www.linkedin.com/sales/people/"
    key = html.split("profileactions:")[-1].split('"')[0]
    token = html.split('token":"')[-1].split('"')[0]
    return f"{prefix}{key},name,{token}"


def is_sales_profile(html):
    return False if "<title>LinkedIn</title>" in html else True


def obtain_sales_profile(url):
    session = LISession()
    response = session.get(url)
    html = response.text
    if not is_sales_profile(html):
        url = construct_sales_url(html)
        response = session.get(url)
        html = response.text

    session.dump_cookies()
    return html


def dummy_email(first_name, last_name):
    if not first_name or not last_name:
        return "Profile N/A"

    suffix = "DummyEmail.com"
    first = ".".join(first_name.split())
    last = ".".join(last_name.split())
    return f"{first}.{last}@{suffix}"


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_sheet_row(d):
    d["dummy_email"] = dummy_email(d.get("firstname"), d.get("lastname"))
    d["user"] = credentials.USER
    return list(d.values())


def index_emails():
    sheet = Sheet().open()
    for msg in Mailbox():
        url, reply, type_of_msg = Message(*msg).parse()
        html_profile = obtain_sales_profile(url)

        try:
            parsed_profile = LIProfile(html_profile).parse()
        except LIProfileError:
            parsed_profile = {i: "Profile N/A" for i in range(6)}

        row = create_sheet_row(
            {
                "timestamp": timestamp(),
                **parsed_profile,
                "reply": reply,
                "type": type_of_msg,
            }
        )

        print(row)
        time.sleep(3)
        sheet.insert(row)


if __name__ == "__main__":
    index_emails()
