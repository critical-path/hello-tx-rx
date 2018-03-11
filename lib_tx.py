#Definition of terms:
#A host address is a network id plus a host id
#A host is a host address plus a port
#A host can be either a local host or a remote host

from lib_config import HelloConfigurator
from socket import SOCK_DGRAM
from socket import socket
from time import sleep

class HelloSender(object):
  #Instantiate the Hello sender

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

  #Send Hello messages to all
  #hosts in specified range
  #at specified frequency

  def send_messages(self):
    host_address_range = self.settings["host_address_range"]
    port = self.settings["port"]
    frequency = self.settings["frequency"]
    text = self.settings["text"]
    encoding = self.settings["encoding"]

    bytes_text = bytes(text, encoding)

    while True:
      for host_address in host_address_range:
        try:
          remote_host = (host_address, port)
          self.socket.sendto(bytes_text, remote_host)
          sleep(frequency)
        except:
          print("Error: Is interface up?  Is user-defined IP address available?  Exiting...")
          exit()

