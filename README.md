## HelloSender and HelloReceiver

With HelloSender and HelloReceiver, hosts on a single subnet exchange UDP datagrams on a continuous basis, making it easy to determine when they can or cannot communicate with each other.

## Dependencies

HelloSender and HelloReceiver consist of Python files (.py), bash files (.sh), systemd files (.service), and regular old text files (.txt).  The Python files require Python 3.x.  The bash and systemd files require Linux environments that support bash and systemd (for example, CentOS 7).  The text files require nothing.

## Files

__Python__:
- lib_config.py - library for HelloConfigurator
- lib_log.py - library for HelloLogAnalyzer
- lib_rx.py - library for HelloReceiver
- lib_tx.py - library for HelloSender

- app_log.py - application for HelloLogAnalyzer
- app_rx.py - application for HelloReceiver
- app_tx.py - application for HelloSender

__systemd__:
- hello_firewall.service - unit configuration for firewall opener (to poke a hole in the firewall)
- hello_rx.service - unit configuration for HelloReceiver
- hello_tx.service - unit configuration for HelloSender

__text__:
- config.txt - configuration file
- log.txt - log file

__bash__:
- get_status.sh - script to get status of hosts
- open_firewall.sh - script to open firewall
- set_up.sh - script to set everything up (install)
- tear_down.sh - script to tear everything down (uninstall)

## Installing HelloSender and HelloReceiver

To install HelloSender and HelloReceiver, follow these instructions.  They work for CentOS 7 __as long as it is not running inside of a container__. They may work for other distributions of Linux, but the directory for systemd unit configuration files may differ from the one specified in the setup script.

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
   

   Putting all of this together, the default configuration is for the local host (192.168.1.1) to use HelloReceiver to listen on UDP port 65000 for UDP datagrams from itself and remote hosts 192.168.1.2-192.168.1.254.  The local host will also use HelloSender to send datagrams to itself and the same set of remote hosts.  The local host will send datagrams at a rate of one every five seconds, meaning that it will take 1270 seconds, or just over 21 minutes, to say "Hello" to each remote host. 

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

## Using systemd

If everything goes as planned, systemd will run the HelloSender service, the HelloReceiver service, and the HelloFirewallOpener service whenever a configured host boots up.  The standard systemd commands are available.

```
sudo systemctl status hello_rx hello_tx hello_firewall
sudo systemctl stop hello_rx hello_rx hello_firewall
sudo systemctl start hello_rx hello_tx hello_firewall
sudo systemctl restart hello_rx hello_tx hello_firewall
```

## Using HelloSender, HelloReceiver, and HelloLogAnalyzer

As long as the HelloSender service and the HelloReceiver service are running, configured hosts attempt to exchange UDP datagrams with each other.  When they receive datagrams, they write them to a log file.  Using HelloLogAnalyzer, they evaluate whether they have received datagrams within the expected timeframe (2 * the number of seconds between sending each datagram * the number of configured hosts).  

To see what the log says about each host, run get_status.sh.

```
/var/lib/hello-tx-rx/get_status.sh

192.168.1.1 [ hello ]
192.168.1.2 [ hello ]
192.168.1.3 [ no hello ]
...
192.168.1.254 [ hello ]
```

## Thoughts on getting started

To get a sense of how HelloSender and HelloReceiver work, configure them to send and receive UDP datagrams on the loopback address.  In config.txt, set network_id to 127.0.0.0, first_host_id to 1, last_host_id to 1, and local_host_id to 1.  Then, in open_firewall.sh, set the source and destination addresses to 127.0.0.1/32.  

## What's the point?

Maybe this has some utility in the Internet of Things.

