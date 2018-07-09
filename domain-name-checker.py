#!/usr/bin/env python

import sys
import argparse
import csv
import subprocess
import ConfigParser
import smtplib
import re
import datetime
from email.mime.text import MIMEText

DOMAIN_LIST_FILE = 'domains.csv'

class State:
  OK = 'OK'
  NotFound = 'Not found'
  NotAsExpected = 'Not as expected'
  InvalidQuery = 'Invalid query'

  @staticmethod
  def get_list():
    return [State.OK, State.NotFound, State.NotAsExpected, State.InvalidQuery]

  @staticmethod
  def to_color_string(state):
    if state == State.OK:
      return bcolors.OKGREEN + State.OK + bcolors.ENDC
    else:
      return bcolors.FAIL + state + bcolors.ENDC

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Domain:
  def __init__(self, row):
    self.init_empty()
    length = len(row)
    if length == 0:
      return

    self.name = row[0].strip()
    if length >= 2 and row[1].strip() != '':
      self.desc = row[1].strip()
    if length >= 3:
      self.expected = row[2].strip()
    self.init = True
  def init_empty(self):
    self.init = False
    self.name = ''
    self.desc = '(No description)'
    self.expected = ''
  def toString(self):
    return ('Domain: "' + self.name
        + '", description = "' + self.desc
        + '", expected ip = "' + self.expected + '"')
  def check(self, output_message_list = None):
    return_state, return_string = State.OK, ''
    if not self.init:
      return_string = 'Wrong format'
      return_state = State.InvalidQuery
    else:
      ADDRESS_PREFIX = 'Address: '
      try:
        output_bytes = subprocess.check_output(["nslookup", self.name])
        output_lines = [str(byte_arr) for byte_arr in output_bytes.split(b'\n')]
        address_lines = [line[len(ADDRESS_PREFIX):] for line in output_lines if line.startswith(ADDRESS_PREFIX)]
        address = '(Not found)'
        if len(address_lines) == 0:
          return_state = State.NotFound
        else:
          address = address_lines[0]
          if self.expected == '' or self.expected == address:
            return_state = State.OK
          else:
            return_state = State.NotAsExpected
      except subprocess.CalledProcessError:
        return_state = State.NotFound
        address = '(Not found)'

      return_string = 'Domain: "' + bcolors.BOLD + self.name + bcolors.ENDC \
                      + '" (' + self.desc + '), expected ip = "' + self.expected \
                      + '", found ip = "' + address \
                      + '", return_state = ' + State.to_color_string(return_state)

    if output_message_list != None:
      output_message_list.append(return_string)
    return return_state

def summary(result_list):
  cnt = {}
  for result in result_list:
    cnt[result] = cnt.get(result, 0) + 1
  rv = 'Summary:'
  for state in State.get_list():
    if state in cnt:
      string = '\t' + State.to_color_string(state) + ' : ' + str(cnt[state]) + ' domain'
      if cnt[state] > 1:
        string += 's'
      rv += '\n' + string
  rv += '\nDate: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
  return rv

def send_email(result_list, output_message_list, config, always_send_email):
  if len([ x for x in result_list if x != State.OK]) == 0:
    print ('All test passed.')
    if always_send_email:
      print('Sending email anyway.')
    else:
      return
  body = summary(result_list) + '\n\n' + '\n'.join(output_message_list)
  ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
  body = ansi_escape.sub('', body)
  msg = MIMEText(body)
  msg['Subject'] = '[DomainNameChecker] Domain name check result'
  sender = config.get('Mail', 'Sender')
  passwd = config.get('Mail', 'Password')
  msg['From'] = sender
  msg['To'] = config.get('Mail', 'Receivers')

  smtp = smtplib.SMTP(config.get("Mail", "MailServer"))
  smtp.ehlo()
  smtp.starttls()
  smtp.login(sender, passwd)

  smtp.sendmail(msg['From'], msg['To'], msg.as_string())
  print ('Mail sent to ' + msg['To'])

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--always-send-email', dest = 'always_send_email', help = 'Send an email even if all test passed. Default: False',  default = False, type = bool)
  args = parser.parse_args()
  config = ConfigParser.ConfigParser()
  config.read('config.ini')
  cnt = 0
  domain_list = []
  with open(DOMAIN_LIST_FILE) as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
      if len(row) == 0 or len(row[0]) == 0 or row[0][0] == '#':
        continue
      domain_obj = Domain(row)
      if domain_obj.init:
        domain_list.append(domain_obj)
        cnt += 1
    print (str(cnt) + ' domains found')

  result_list = []
  output_message_list = []
  for domain in domain_list:
    result_list.append(domain.check(output_message_list))
    
  for output_message in output_message_list:
    print (output_message)

  print(summary(result_list))
  send_email(result_list, output_message_list, config, args.always_send_email)

if __name__ == "__main__":
  main()

