Domain Name Checker
===================

|Build Status| > Check domain name status in batch, with style!
https://github.com/YF-Tung/domain-name-watcher
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

Requirement
-----------

Python (2 or 3)
No other pip packages required.

Usage example
-------------

-  Add domains you want to check into ``domains.csv``
-  Add mailing config into config.ini
-  ``./domain-name-checker.py``
-  It sends mails when some test failed. Specify
   ``./domain-name-checker.py --always-send-email true`` to force send a
   mail.
-  For further help, type ``./domain-name-checker.py -h``
-  One can also use ``./domain-name-checker.js`` instead as a nodejs
   wrapper of python version

Config.ini example
------------------

.. code:: ini

    [Mail]
    Sender = myname@gmail.com
    Password = mygmailpassword
    Receivers = someone@gmail.com,another@gmail.com
    MailServer = smtp.gmail.com:587

Domains.csv example
-------------------

.. code:: csv

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

License
-------

Distributed under the MIT license. See ``LICENSE`` for more information.

.. |Build Status| image:: https://travis-ci.org/YF-Tung/domain-name-watcher.svg?branch=master
   :target: https://travis-ci.org/YF-Tung/domain-name-watcher
