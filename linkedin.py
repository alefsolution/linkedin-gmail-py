from bs4 import BeautifulSoup
import credentials
import requests
import pickle
import json
import os


class LISession(requests.Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cookie_file_path = credentials.__file__.replace("__init__.py", "cookies")
        self.headers = credentials.linkedin_headers
        self.cookies = self._construct_cookies()

    def _construct_cookies(self):
        if not os.path.exists(self.cookie_file_path):
            return requests.utils.cookiejar_from_dict(
                dict(p.split("=", 1) for p in self.headers["cookie"].split("; "))
            )
        else:
            if self.headers.get("cookie"):
                del self.headers["cookie"]

            return self._load_cookies()

    def _load_cookies(self):
        with open(self.cookie_file_path, "rb") as f:
            return pickle.load(f)

    def dump_cookies(self):
        with open(self.cookie_file_path, "wb") as f:
            pickle.dump(self.cookies, f)


class LIProfile:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")

    def find_payload(self):
        for code in self.soup.findAll("code"):
            if "firstName" in code.text and "companyName" in code.text:
                self.payload = json.loads(code.text.strip())
                return

        raise LIProfileError

    def parse(self):
        self.find_payload()

        work = self.payload.get("positions", [{}])
        return {
            "firstname": self.payload.get("firstName"),
            "lastname": self.payload.get("lastName"),
            "location": self.payload.get("location"),
            "company": work[0].get("companyName"),
            "title": work[0].get("title"),
            "profile": self.payload.get("flagshipProfileUrl"),
        }


class LIProfileError(Exception):
    pass
