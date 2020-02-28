from urllib.parse import unquote
from bs4 import BeautifulSoup
from imbox import Imbox
import credentials


class Mailbox:
    REGULAR = [
        "notifications-noreply@linkedin.com",
        "messaging-digest-noreply@linkedin.com",
    ]

    INVITE = ["messages-noreply@linkedin.com"]

    def __init__(self):
        self.imap = credentials.IMAP
        self.user = credentials.USER
        self.pwd = credentials.PWD

    def __iter__(self):
        """
        Iterator over unread messages only
        """
        with Imbox(self.imap, username=self.user, password=self.pwd, ssl=True) as box:
            for uid, msg in box.messages(unread=True):
                sender = msg.sent_from[0].get("email")
                if sender in Mailbox.REGULAR:
                    yield uid, msg, box, "Regular Response"

                if (
                    sender in Mailbox.INVITE
                    and msg.subject == "Reply to LinkedIn Invitation"
                ):
                    yield uid, msg, box, "Invite Response"


class Message:
    def __init__(self, uid, msg, box, type_of_msg):
        self.uid = uid
        self.msg = msg
        self.box = box
        self.type = type_of_msg

    def _extract_url(self, text, delimiter):
        return unquote(
            "https://" + text.split("https://", 1)[-1].split(delimiter)[0].strip()
        )

    def _extract(self, text, html):
        if 26 * "=" in text:
            url = self._extract_url(text, "\r\n")
            return url, text.split(26 * "=")[1].strip()

        elif 18 * "-" in text:
            url = self._extract_url(text, "):")
            return url, text.split(18 * "-")[1].strip()

        url = text.split("profile: ")[-1].split()[0].strip()
        text = BeautifulSoup(html, "html.parser").get_text()
        reply = text.split("View Invite")[0].strip().split("\xa0")[-1].strip()
        return url, reply

    def _mark_as_read(self):
        self.box.mark_seen(self.uid)

    def parse(self):
        text = self.msg.body.get("plain", [""])[0]
        html = self.msg.body.get("html", [""])[0]
        url, reply = self._extract(text, html)

        self._mark_as_read()
        return url, reply, self.type
