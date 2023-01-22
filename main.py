import datetime
import email
import imaplib
import json

from config_reader import ConfigReader

config = ConfigReader()
log = []
a_week_ago = (datetime.datetime.today() - datetime.timedelta(days=7)).date()

M=imaplib.IMAP4_SSL(config.imap_server,config.imap_port)
M.login(config.gmail_username,config.gmail_password)
M.select()
typ, data = M.search(None, 'UNSEEN')
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    if (datetime.datetime.strptime(msg['Date'][:25], '%a, %d %b %Y %H:%M:%S').date()) < a_week_ago:
        log.append({'subject': msg["Subject"], 'from':msg['From'], 'date': msg['Date']})
        M.uid("STORE",num, '+X-GM-LABELS', '(autoread)')
        M.uid("STORE",num, '+FLAGS', '\\Seen')
    else:
        M.uid("STORE",num, '-FLAGS', '\\Seen')
M.close()
M.logout()

with open('log_file.json', 'a') as f:
    json.dump(log, f, indent=4, ensure_ascii=False)
