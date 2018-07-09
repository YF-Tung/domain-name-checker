# Domain Name Checker
> Check domain name status in batch, with style!
[https://github.com/YF-Tung/domain-name-watcher](https://github.com/YF-Tung/domain-name-watcher)

## Requirement

Python (2 or 3)

## Usage example

* Add domains you want to check into `domains.csv`
* Add mailing config into config.ini
* `./domain-name-checker.py`
* It sends mails when some test failed. Specify `./domain-name-checker.py --always-send-email true` to force send a mail.
* For further help, type `./domain-name-checker.py -h`

## Config.ini example
```ini
[Mail]
Sender = myname@gmail.com
Password = mygmailpassword
Receivers = someone@gmail.com,another@gmail.com
MailServer = smtp.gmail.com:587
```

## Domains.csv example
```csv
# Sample file of domains.csv
# Empty lines and lines starting with '#' will be ignored

# Check if this domain is valid
github.com

# Check if this domain is valid, with some description
github.com, I like github

# Check if this domain leads to where it should be
# Since github.com has multiple IP (currently), these may either succeed or fail
github.com, , 192.30.253.112
github.com, github, 192.30.253.112

# Some examples that will fail
no.such.domain
no.such.domain, , 12.34.567.890
github.com, wrong ip, 1.1.1.1
```

## License

Distributed under the MIT license. See ``LICENSE`` for more information.

