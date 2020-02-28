pip3 install -r requirements.txt
set file=credentials/__init__.py

mkdir credentials
echo linkedin_headers = {} >> %file%
echo IMAP = "imap.gmail.com" >> %file%
echo USER = "" >> %file%
echo PWD = "" >> %file%
echo "COPY credentials.json to CREDENTIALS FOLDER!!!!"
pause
python sheet.py >> %file%

