import datetime
import email
import imaplib
import json

from config_reader import ConfigReader
def parse_date(unformatted_date):
    for fmt in ('%a, %d %b %Y', '%d %b %Y %H:%M'):
        try:
            return datetime.datetime.strptime(unformatted_date, fmt).date()
        except ValueError:
            pass
    raise ValueError('no valid date format found', unformatted_date)

config = ConfigReader()
log = []
days_to_look_back = 14
time_delta = (datetime.datetime.today() - datetime.timedelta(days=days_to_look_back)).date()

M=imaplib.IMAP4_SSL(config.imap_server,config.imap_port)
M.login(config.gmail_username,config.gmail_password)
M.select()
typ, data = M.search(None, 'UNSEEN')
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    if parse_date(msg['Date'][:16].strip()) < time_delta:
        log.append({'subject': msg["Subject"], 'from':msg['From'], 'date': msg['Date']})
        M.uid("STORE",num, '+X-GM-LABELS', '(autoread)')
        M.uid("STORE",num, '+FLAGS', '\\Seen')
    else:
        M.uid("STORE",num, '-FLAGS', '\\Seen')
M.close()
M.logout()

with open('log_file.json', 'a') as f:
    json.dump(log, f, indent=4, ensure_ascii=False)
