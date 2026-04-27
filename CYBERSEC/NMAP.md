## NMAP
**Nmap** (Network Mapper) is a **free and open-source** utility designed for **network discovery and security auditing**. 
It helps to discover host, scan ports, detect the version of the targeted machine, and also the OS of the targeted machine. 

There are 65 535 ports that exist and can be scanned by NMAP

NMAP SWITCHES

Nmap switches are command-line options used to customize and control the behavior of the Nmap (Network Mapper) scanning tool. They allow users to specify scan types, target ports, output formats, timing templates, and detection methods.
To access nmap you just need to type `nmap` in your command line.
Here are the most common options or switches:
- `-sS`: used for `syn scan`
- `-sU`: used for UDP scan
- `-O`: used to detect the Operating system of the target machine
- `-sV`: to detect the version of the services running on the target.
- `-v`: verbosity => `-vv` increase verbosity by 2
- `-oA`: you use to save the nmap results in three major formats
- `-oG`: use to save in a grepable format
- `-A`: for aggressive mode
- `-T`: set the timing template level => `-T5`; for level 5
- `-p`: nmap to only scan a specific port => `-p 80` : to scan port 80
- `-p-`; to scan all the ports
- `--script`: activate a script from the nmap scripting library
- `-script=vuln`: activate all of the scripts in the "vuln" category

### TCP port SCAN 

We use `-sT` to be able to scan for TCP port
This we where the three way handshake comes in 
The three way hand shake consists  of three stages. First the connecting terminal (our attacking machine, in this instance) sends a TCP request to the target server with the SYN flag set. The server then acknowledges this packet with a TCP response containing the SYN flag, as well as the ACK flag. Finally, our terminal completes the handshake by sending a TCP request with the ACK flag set.
Here is an example of a simple scan on the TCP port using `scanme.nmap.org` as our target.

![[swappy-20260427-142741.png]]

### SYN Scans

For `syn scan` we use the switch `-sS`

![[swappy-20260427-144256.png]]

Here are the advantages for a hacker : 
- It can be used to bypass older Intrusion Detection systems as they are looking out for a full three way handshake. This is often no longer the case with modern IDS solutions; it is for this reason that SYN scans are still frequently referred to as "stealth" scans.
- SYN scans are often not logged by applications listening on open ports, as standard practice is to log a connection once it's been fully established. Again, this plays into the idea of SYN scans being stealthy.
- Without having to bother about completing (and disconnecting from) a three-way handshake for every port, SYN scans are significantly faster than a standard TCP Connect scan.
There are also disadvantages like: 
- They require sudo permissions in order to work correctly in Linux. This is because SYN scans require the ability to create raw packets (as opposed to the full TCP handshake), which is a privilege only the root user has by default.
- Unstable services are sometimes brought down by SYN scans, which could prove problematic if a client has provided a production environment for the test.

### UDP Scans

For the UDP scan we use the switch `-sU` 

![[swappy-20260427-150057.png]]
### ICMP network scanning

For ICMP Scanning we use the switch `-sn` and the target IP or domain. Example : `sudo -sn 172.16.0.0`

On first connection to a target network in a black box assignment, our first objective is to obtain a "map" of the network structure -- or, in other words, we want to see which IP addresses contain active hosts, and which do not.
One way to do this is by using Nmap to perform a so called "ping sweep". This is exactly as the name suggests: Nmap sends an ICMP packet to each possible IP address for the specified network. When it receives a response, it marks the IP address that responded as being alive. For reasons we'll see in a later task, this is not always accurate; however, it can provide something of a baseline and thus is worth covering.

To perform a ping sweep, we use the `-sn` switch in conjunction with IP ranges which can be specified with either a hypen (`-`) or CIDR notation. i.e. we could scan the `45.33.32.156` network using:

- Example: `nmap -sn 45.33.32.156`

or

- Example: `nmap -sn 45.33.32.156/24`

or 

- Example: `nmap -sn scanme.nmap.org`
  

The `-sn` switch tells Nmap not to scan any ports -- forcing it to rely primarily on ICMP echo packets (or ARP requests on a local network, if run with sudo or directly as the root user) to identify targets. In addition to the ICMP echo requests, the `-sn` switch will also cause nmap to send a TCP SYN packet to port 443 of the target, as well as a TCP ACK (or TCP SYN if not run as root) packet to port 80 of the target.  

![[swappy-20260427-150437.png]]

### OVERVIEW

The **N**map **S**cripting **E**ngine (NSE) is an incredibly powerful addition to Nmap, extending its functionality quite considerably. NSE Scripts are written in the _Lua_ programming language, and can be used to do a variety of things: from scanning for vulnerabilities, to automating exploits for them. The NSE is particularly useful for reconnaisance, however, it is well worth bearing in mind how extensive the script library is.

There are many categories available. Some useful categories include:

- `safe`:- Won't affect the target
- `intrusive`:- Not safe: likely to affect the target  
    
- `vuln`:- Scan for vulnerabilities
- `exploit`:- Attempt to exploit a vulnerability
- `auth`:- Attempt to bypass authentication for running services (e.g. Log into an FTP server anonymously)
- `brute`:- Attempt to bruteforce credentials for running services
- `discovery`:- Attempt to query running services for further information about the network (e.g. query an SNMP server).

### WORKING WITH THE NSE

Previously we looked very briefly at the `--script` switch for activating NSE scripts from the `vuln` category using `--script=vuln`. It should come as no surprise that the other categories work in exactly the same way. If the command `--script=safe` is run, then any applicable safe scripts will be run against the target (Note: only scripts which target an active service will be activated).

---

To run a specific script, we would use `--script=<script-name>` , e.g. `--script=http-fileupload-exploiter`.

Multiple scripts can be run simultaneously in this fashion by separating them by a comma. For example: `--script=smb-enum-users,smb-enum-shares`.

Some scripts require arguments (for example, credentials, if they're exploiting an authenticated vulnerability). These can be given with the `--script-args` Nmap switch. An example of this would be with the `http-put` script (used to upload files using the PUT method). This takes two arguments: the URL to upload the file to, and the file's location on disk.  For example:

`nmap -p 80 --script http-put --script-args http-put.url='/dav/shell.php',http-put.file='./shell.php'`

Note that the arguments are separated by commas, and connected to the corresponding script with periods (i.e.  `<script-name>.<argument>`).

A full list of scripts and their corresponding arguments (along with example use cases) can be found here https://nmap.org/nsedoc/.

Nmap scripts come with built-in help menus, which can be accessed using `nmap --script-help <script-name>`. This tends not to be as extensive as in the link given above, however, it can still be useful when working locally.

