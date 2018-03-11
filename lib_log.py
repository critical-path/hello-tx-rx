#Definition of terms:
#A host address is a network id plus a host id
#A host is a host address plus a port
#A host can be either a local host or a remote host

from lib_config import HelloConfigurator
from os import getcwd
from os.path import join
from re import compile
from re import findall
from time import time

class HelloLogAnalyzer(object):
  #Instantiate the Hello receiver

  def __init__(self):
    self.settings = {}

  #Get all key-value pairs

  def get_settings(self):
    configurator = HelloConfigurator()
    configurator.set_values()
    configurator.edit_values()
    configurator.find_local_host_address()
    configurator.find_host_address_range()
    configurator.find_interval()
    self.settings = configurator.get_values()

  #Helper function to get all
  #host addresses from configuration file

  def get_host_addresses(self):
    host_address_range = self.settings["host_address_range"]

    host_addresses = {}

    for host_address in host_address_range:
      host_addresses[host_address] = ""

    return host_addresses

  #Helper function to get all
  #log entries from log file

  def get_log_entries(self):
    log_file = self.settings["log_file"]

    log_entries = ""

    current_working_directory = getcwd()
    path = join(current_working_directory, log_file)

    with open(path) as file:
      for line in file:
        log_entries += line
 
    return log_entries

  #Helper function to get
  #timestamp of last Hello message

  def get_last_hello(self, log_entries):
    last_log = log_entries[len(log_entries) - 1]
    last_log = last_log.split()
    last_hello = last_log[0]
    last_hello = float(last_hello)
    
    return last_hello

  #Helper function to check
  #whether last Hello message
  #was received within two intervals

  def check_interval(self, timestamp):
    interval = self.settings["interval"]

    current_time = time()

    if (current_time - timestamp) <= 0:
      return "clock_not_synchronized"
    elif (current_time - timestamp) <= (interval * 2):
      return True
    else:
      return False

  #Helper function to sort results

  def sort_results(self, host_addresses):
    results = []

    for key, value in host_addresses.items():
      host_address = key
      status = value
      results.append([host_address, status])

    sorted_results = sorted(results)

    return sorted_results

   #Helper function to print results

  def print_results(self, results):

    for result in results:
      host_address = result[0]
      status = result[1]

      if status == "clock_not_synchronized":
        print("\033[38;5;166m" + "Clock not synchronized" + "\033[000m")
      elif status == True:
        print("\033[000m" + host_address + " [\033[38;5;154m ok \033[000m]")
      elif status == False:
        print("\033[000m" + host_address + " [\033[38;5;160m not ok \033[000m]")

  #Determine whether hosts are alive

  def analyze_log(self):
    host_addresses = self.get_host_addresses()
    log_entries = self.get_log_entries()

    for key in host_addresses.keys():
      host_address = key
      pattern = compile("[\d]*[.][\d]*[\s]" + host_address + "[\s][\d]*[\s][\w]*[\n]")
      matches = findall(pattern, log_entries)

      if not matches:
        host_addresses[host_address] = False
      elif matches:
        last_hello = self.get_last_hello(matches)
        host_addresses[host_address] = self.check_interval(last_hello)

    sorted_results = self.sort_results(host_addresses)
    self.print_results(sorted_results)
