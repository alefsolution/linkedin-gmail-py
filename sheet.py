from oauth2client.service_account import ServiceAccountCredentials
import credentials
import webbrowser
import gspread
import time
import sys
import os


class Sheet:
    AUTH_PATH = credentials.__file__.replace("__init__.py", "credentials.json")
    SCOPE = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            Sheet.AUTH_PATH, Sheet.SCOPE
        )
        self.client = gspread.authorize(self.credentials)
        self.prefix = "https://docs.google.com/spreadsheets/d"
        self.empty_cols = 2
        self.empty_vals = self.empty_cols * [None]

    def create(self):
        filename = "Linkedin " + Sheet.AUTH_PATH.split(os.sep)[-3]
        if sys.argv[1:]:
            filename = " ".join(sys.argv[1:])

        sheet = self.client.create(filename)
        time.sleep(5)
        return sheet

    def share(self, sheet):
        sheet.share(None, perm_type="anyone", role="writer")
        url = f"{self.prefix}/{sheet.id}"
        sheet = self.client.open_by_url(url).sheet1
        header = [
            "Ship to CRM (y)",
            "Status",
            "Timestamp",
            "First Name",
            "Last Name",
            "Location",
            "Company",
            "Title",
            "Profile",
            "Reply",
            "Reply Type",
            "Dummy Email",
            "User",
        ]
        sheet.insert_row(header, index=1, value_input_option="USER_ENTERED")
        print(f'URL = "{url}"')
        webbrowser.open(url)

        if sys.argv[1:]:
            os.chdir("..")
            for replies_folder in [x for x in os.listdir() if x.startswith("replies_")]:
                path = os.path.join(replies_folder, "credentials", "__init__.py")
                with open(path, "a") as f:
                    f.write(f'URL_UNI = "{url}"')

    def open(self):
        self.sheet = self.client.open_by_url(credentials.URL).sheet1

        if credentials.__dict__.get("URL_UNI"):
            self.sheet_uni = self.client.open_by_url(
                credentials.__dict__.get("URL_UNI")
            ).sheet1

        return self

    def insert(self, values):
        values = self.empty_vals + values
        self.sheet.insert_row(values, index=2, value_input_option="USER_ENTERED")

        if credentials.__dict__.get("URL_UNI"):
            self.sheet_uni.insert_row(
                values, index=2, value_input_option="USER_ENTERED"
            )


if __name__ == "__main__":
    sheet = Sheet()
    new_sheet = sheet.create()
    sheet.share(new_sheet)
