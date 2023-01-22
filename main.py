import imaplib
import email
import json
from config_reader import ConfigReader

config = ConfigReader()
log = []

M=imaplib.IMAP4_SSL(config.imap_server,config.imap_port)
M.login(config.gmail_username,config.gmail_password)
M.select()
typ, data = M.search(None, 'UNSEEN')
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    log.append({'subject': msg["Subject"], 'from':msg['From'], 'date': msg['Date']})
    M.store(num, '+FLAGS', '\\Seen')
M.close()
M.logout()

with open('log_file.json', 'a') as f:
    json.dump(log, f, indent=4, ensure_ascii=False)
