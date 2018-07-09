#!/usr/bin/env python

import csv
import subprocess

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
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
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

def print_summary(result_list):
  cnt = {}
  for result in result_list:
    cnt[result] = cnt.get(result, 0) + 1
  print ('Summary:')
  for state in State.get_list():
    if state in cnt:
      string = '\t' + State.to_color_string(state) + ' : ' + str(cnt[state]) + ' domain'
      if cnt[state] > 1:
        string += 's'
      print (string)

def main():
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
  for domain in domain_list:
    output_message_list = []
    result_list.append(domain.check(output_message_list))
    
    for output_message in output_message_list:
      print (output_message)

  print_summary(result_list)

if __name__ == "__main__":
  main()

