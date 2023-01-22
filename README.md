# Email Reader

Wanted to make this script to mark old emails as read, Gmail didn't have it built in so I had to find a hacky way of doing it myself.

To run it you need to create a `config.yml` file and put these variables in

```yaml
imap_server: imap.gmail.com
imap_port: 993
gmail_username: (Your Gmail address)
gmail_password: (Create an App password in you Google account security settings)
```

Then just run the script with:
`python3 main.py`
