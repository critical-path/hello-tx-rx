## HelloSender and HelloReceiver

With HelloSender and HelloReceiver, hosts on a single subnet exchange UDP datagrams on a continuous basis, making it easy to determine when they can or cannot communicate with each other.

## Dependencies

HelloSender and HelloReceiver consist of Python files (.py), bash files (.sh), systemd files (.service), and regular old text files (.txt).  The Python files require Python 3.x.  The bash and systemd files require Linux environments that support bash and systemd.  The text files require nothing.

## Files

- lib_config.py - Python library for configurator
- lib_log.py - Python library for log analyzer
- lib_rx.py - Python library for receiver
- lib_tx.py - Python library for sender

- app_log.py - Python application for log analyzer
- app_rx.py - Python application for receiver
- app_tx.py - Python application for sender

- hello_firewall.service - systemd unit configuration for firewall opener (to poke a hole in the firewall)
- hello_rx.service - systemd unit configuration for receiver
- hello_tx.service - systemd unit configuration for sender

- config.txt - configuration file
- log.txt - log file

- get_status.sh - bash script to get status of hosts
- open_firewall.sh - bash script to open firewall
- set_up.sh - bash script to set everything up

## Installing HelloSender and HelloReceiver

1. Download this repository.

2. Extract the contents.

3. Open config.txt in your favorite text editor.

4. Change the follow key-value pairs as necessary:
   
   - network_id is your network/subnet address (by default, 192.168.1.0).

   - first_host_id is the host address for the first participating host (by default, 1).

   - last_host_id is the host address for the last participating address (by default, 254).  Try to avoid using the broadcast address here.

   - local_host_id is the host address for the local host (by default, 1).

   - port is the UDP port number (by default, 65000).

   - frequency is the number of seconds between each tranmission of a UDP datagram (by default, 5).

   - text is the string in each UDP datagram (by default, Hello).

   
   Do not change either of the following key-value pairs:

   - encoding is the original character encoding of the string in each UDP datagram (by default, UTF-8).

   - log_file is the name of the log file (by default, log.txt).
   

   Putting all of this together, the default configuration is for the local host (192.168.1.1) to use HelloReceiver to listen on UDP port 65000 for UDP datagrams from itself and remote hosts 192.168.1.2-192.168.1.254.  The local host will also use HelloSender to send UDP datagrams to itself and the same set of remote hosts.  The local host will send datagrams at a rate of one every five seconds, meaning that it will take 1270 seconds, or just over 21 minutes, to say "Hello" to each remote host.  Easy, right? 

5. Open open_firewall.sh in your favorite text editor.

6. Make sure that the network address and subnet mask (by default, 192.168.1.0/24) match your configuration settings as defined in config.txt.

7. Run set_up.sh, watching as it creates directories, moves files, links files, enables services, and starts services.

```
./set_up.sh
```

8. If set_up.sh will not run, then you may need to change its file mode.  Toggle the "x" bit to enable execution.

```
chmod +x ./set_up.sh
```

9. If set_up.sh runs but encounters some sort of failure, then take a look at the error messages in bash.  You may have to execute some of the intended setup commands by hand.

10. Repeat this process for every host, making sure that configuration settings are consistent (except for local_host_id, which should be unique to each host).

## Using systemd (the boring stuff)

If everything goes as planned, systemd will run the HelloSender service, HelloReceiver service, and HelloFirewallOpener service whenever a configured host boots up.  The standard systemd commands apply.

```
systemctl status hello_rx hello_tx hello_firewall
systemctl stop hello_rx hello_rx hello_firewall
systemctl start hello_rx hello_tx hello_firewall
systemctl restart hello_rx hello_tx hello_firewall
```

## Using HelloSender, HelloReceiver, and their friend, HelloLogAnalyzer (the fun stuff)

As long as the HelloSender service and the HelloReceiver service are running, configured hosts attempt to exchange UDP datagrams with each other.  When they receive datagrams, they write them to a log file.  Using HelloLogAnalyzer, they evaluate whether they have received datagrams within the expected timeframe (2 * the number of seconds between sending each datagram * the number of configured hosts = 2540 seconds, by default).  To see what the log says about each host, run get_status.sh.

```
./get_status.sh
```

