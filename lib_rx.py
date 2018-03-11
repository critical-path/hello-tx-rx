#Definition of terms:
#A host address is a network id plus a host id
#A host is a host address plus a port
#A host can be either a local host or a remote host

from lib_config import HelloConfigurator
from os import getcwd
from os.path import join
from socket import SOCK_DGRAM
from socket import socket
from time import time

class HelloReceiver(object):
  #Instantiate the Hello receiver

  def __init__(self):
    self.settings = {}
    self.socket = socket(type=SOCK_DGRAM)

  #Get all key-value pairs

  def get_settings(self):
    configurator = HelloConfigurator()
    configurator.set_values()
    configurator.edit_values()
    configurator.find_local_host_address()
    configurator.find_host_address_range()
    configurator.find_interval()
    self.settings = configurator.get_values()
 
  #Receive Hello messages

  def receive_messages(self):
    try:
      local_host_address = self.settings["local_host_address"]
      local_port = self.settings["port"]
      local_host = (local_host_address, local_port)

      self.socket.bind(local_host)
    except:
      print("Error: Is interface up?  Is user-defined IP address available?  Exiting...")
      exit()

    while True:
      message = self.socket.recvfrom(2048)

      text = message[0]
      text = text.decode()

      remote_host = message[1]
      remote_host_address = remote_host[0]
      remote_host_port = remote_host[1]

      timestamp = time()

      self.log_message(timestamp, remote_host_address, remote_host_port, text)

  #Write Hello messages to log file

  def log_message(self, *args):
    log_file = self.settings["log_file"]

    timestamp = args[0]
    timestamp = str(timestamp)

    remote_host_address = args[1]

    remote_host_port = args[2]
    remote_host_port = str(remote_host_port)

    text = args[3]

    log_entry = timestamp + " " +\
                remote_host_address + " " +\
                remote_host_port + " "+\
                text + "\n"

    current_working_directory = getcwd()
    path = join(current_working_directory, log_file)

    with open(path, "a") as file:
      file.write(log_entry)

