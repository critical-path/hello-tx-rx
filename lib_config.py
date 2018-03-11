#Definition of terms:
#A host address is a network id plus a host id
#A host is a host address plus a port
#A host can be either a local host or a remote host

from os import getcwd
from os.path import join

class HelloConfigurator(object):
  #Instantiate the Hello configurator

  def __init__(self):
    self.file = "config.txt"
    self.settings = {} 

  #Open the configuration file,
  #iterate over each line,
  #and set each key-value pair

  def set_values(self):
    current_working_directory = getcwd()
    path = join(current_working_directory, self.file)

    with open(path) as file:
      for line in file:
        try:
          line = line.strip()
          line = line.split("=")
          key = line[0]
          value = line[1]
          self.settings[key] = value
        except:
          pass

  #Convert some of the values
  #from strings to integers

  def edit_values(self):
    self.settings["first_host_id"] = int(self.settings["first_host_id"])
    self.settings["last_host_id"] = int(self.settings["last_host_id"])
    self.settings["port"] = int(self.settings["port"])
    self.settings["frequency"] = int(self.settings["frequency"])

  #Obtain address of local host

  def find_local_host_address(self):
    network_id = self.settings["network_id"]
    network_id = network_id[ : -1]

    local_host_id = self.settings["local_host_id"]

    local_host_address = network_id + local_host_id

    self.settings["local_host_address"] = local_host_address

  #Obtain the full range of hosts
  #(local host and remote hosts)
  #to which to send Hello messages

  def find_host_address_range(self):
    network_id = self.settings["network_id"]
    network_id = network_id[ : -1]

    first_host_id = self.settings["first_host_id"]
    last_host_id = self.settings["last_host_id"]

    host_address_range = []

    for index in range(first_host_id, last_host_id + 1):
      index = str(index)
      host_address = network_id + index
      host_address_range.append(host_address)

    self.settings["host_address_range"] = host_address_range

  #Obtain the amount of time
  #between each Hello message
  #received by a given host

  #If the local host sends Hello
  #messages every five seconds,
  #and if there are four remote hosts,
  #then each remote host
  #should receive a Hello message
  #every 20 seconds

  def find_interval(self):
    host_address_range = self.settings["host_address_range"]
    frequency = self.settings["frequency"]

    number_addresses = len(host_address_range)
    interval = number_addresses * frequency

    self.settings["interval"] = interval

  #Return all key-value pairs

  def get_values(self):
    return self.settings
