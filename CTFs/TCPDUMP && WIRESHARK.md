## TCPDUMP
It's a command line packet analyzer used to capture and inspect network traffic in real time.
Basics syntax in the terminal : `sudo tcpdump`

![[swappy-20260424-143035.png]]

SYNTAX:

`tcpdump [option] [filter expression]`

Main options
- `-i <interface>` → select interface
- `-n` → disable DNS resolution
- `-v`, `-vv`, `-vvv` → verbosity levels
- `-c <count>` → capture limited packets
- `-w <file>` → write to file
- `-r <file>` → read from file

CAPTURE HTTP TRAFFIC

First to be able to see the different interfaces available on the network
`sudo tcpdump -D`
Now you will have a list of interfaces available on that network then you can start capturing the traffic from HTTP
`sudo tcpdump -i wlan0 port 80

FILTERING BY `IPs`

First to be able to see the different IPs available on the network
`sudo nmap -sn [IP of the subnet or router ]/24
Now you will be able to filter traffic of the IP you want
`sudo tcpdump host 192.168.100.1`

![[swappy-20260424-151652.png]]

FILTER BY PORT

Here you can listen to a specific port example: `sudo tcpdump port 22`
You can also listen to a range of ports like between two ports Example: `sudo tcpdump portrange 20-25`

![[swappy-20260424-152352.png]]

NOTE: Capturing traffic can be time consuming so in the picture above i was breaking it.

SAVE CAPTURE TO FILE

Syntax: `sudo tcpdump -w capture.pcap` will save captures into capture.pcap

then: `sudo tcpdump -r capture.pcap` this allows you to read the from the file you have saved the capture into.

![[swappy-20260424-153730.png]]

INTERPRETING OUTPUT

Example:
`14:32:10.123456 IP 192.168.1.5.443 > 192.168.1.10.52344: Flags [P.], seq 1:21, ack 1, win 229, length 20`

Interpretation:
- Timestamp → `14:32:10.123456`
- Protocol → `IP`
- Source → `192.168.1.5.443`
- Destination → `192.168.1.10.52344`
- Flags → `[P.]`
- Sequence/Ack numbers
- Payload length

TCP flags overview:
- `S` → SYN (start connection)
- `F` → FIN (close)
- `P` → PUSH (data transfer)
- `R` → RESET

COMMON PORTS

- 22(ssh)
- 80(HTTP)
- 443(HTTPS)
- 445(SMB)
- 3389(RDP)
- 53(DNS)

## WIRESHARK

Wireshark is  used to capture and inspect network traffic in real-time.
It's like TCPDUMP but with a graphic user interface. 

Here i'm going to go through some basic things about wireshark like how it looks like, how to apply some filters...
This is how is looks like when you open it: 

![[swappy-20260424-190416.png]]

Here is how it looks like when you open a file in wireshark

![[swappy-20260424-194354.png]]

Here after applying the filter to show me all the packets captures that has a specific IP defined

![[swappy-20260424-193602.png]]

Here after applying a filter for a specific protocol

![[swappy-20260424-194122.png]]

After applying a filter we ca start checking information about that specific capture

![[swappy-20260424-195253.png]]
Th red section are the information about the packet that we have captured.

