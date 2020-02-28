Replies checker
===============

Reads gmail boxes, and indexes all messages from linkedin to gsheet.


Deployment instructions
=======================

- Go to gmail and allow to use `less secure apps`
- SELECT ALL MAILS AND MARK THEM AS READ
- `https://console.developers.google.com/project`
- Run `_setup.bat` and dont forget to copy credentials file when prompted
- Fill the `credentials/__init__.py` file
- Open PowerShell as ADMIN and run `_setup_scheduler.ps1` to schedule task
- add Sheet shortcut to DESKTOP
- If there are more users on server, add them to universal SHEET by running
```
python sheet.py Universal <Server Name> Replies
```
