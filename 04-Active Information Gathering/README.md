# 4. - Active Information Gathering

 Once you have gathered enough information about your target, using open web resources, and other passive information gathering techiniques, you can further gather relevant information from other, more specific services.

## 4.1 - DNS Enumeration

DNS is often a lucrative source for active information gathering. DNS offers a variety of information about public (and private) organization servers, such as IP addresses, server names, and server functionality.

### 4.1.1 - Interacting with a DNS Server

A DNS server will usually divulge DNS and mail server information for the domain it has authoroty over. This is a necessity, as public requests for mail and DNS server addresses make up the basic Internet experience.
We'll use the **host** command, together with the **-t** (type) parameter to discover both the DNS and mail servers for the **megacorpone.com** domain.

```
root@kali:~# host -t ns megacorpone.com
megacorpone.com name server ns1.megacorpone.com.
megacorpone.com name server ns3.megacorpone.com.
megacorpone.com name server ns2.megacorpone.com.

root@kali:~# host -t mx megacorpone.com
megacorpone.com mail is handled by 50 mail.megacorpone.com.
megacorpone.com mail is handled by 60 mail2.megacorpone.com.
megacorpone.com mail is handled by 10 fb.mail.gandi.net.
megacorpone.com mail is handled by 20 spool.mail.gandi.net.
```

By default, every configured domain should provide at least the DNS and mail servers responsible for the domain.

### 4.1.2 - Automating Lookups

Now that we have some initital data from the **megacorpone.com** domain, we can continue to use additional DNS queries to discover more host names and IP addresses belonging to **megacorpone.com**. For example, we can assume that the **megacorpone.com**ain has a web server, probably with the hostname **www**.
We can test this theory using the **host** command once again.

```
root@kali:~# host www.megacorpone.com
www.megacorpone.com has address 38.100.193.76
```

Now, let's check if **megacorpone.com** also has a server with the hostname *idontexist*. Notice the difference between the query outputs.

```
root@kali:~# host idontexist.megacorpone.com
idontexist.megacorpone.com has address 92.242.140.20
Host idontexist.megacorpone.com not found: 3(NXDOMAIN)
```

### 4.1.3 - Forward Lookup Brute Force

Taking the previous concept a step further, we can automate the Forward DNS Lookup of commmon host names using the **host** command and a Bash script. We can create a short (or long) list of possible hostnames and loop the **host** command to try each one.

```
root@kali:~# echo www > list.txt
root@kali:~# echo ftp >> list.txt
root@kali:~# echo mail >> list.txt
root@kali:~# echo owa >> list.txt
root@kali:~# echo proxy >> list.txt
root@kali:~# echo router >> list.txt
root@kali:~# for ip in $(cat list.txt);do host $ip.megacorpone.com;done
```

Is this simplified example, we notice that the hostnames **www**, **router**, and **mail** have been discovered through this brute-force attack.

### 4.1.4 - Reverse Lookup Brute Force

Our DNS forward brute-force enumeration revealed a set of scattered IP addresses. If the DNS adminitrator of**megacorpone.com** configured PTR records for the domain, we might find out some more domain names that were missed during the forward lookup brute-force phase, by probing the range of these found addresses in a lopp.

```
root@kali:~# for ip in $(seq 155 190);do host 50.7.67.$ip;done | grep -v "not found"
155.67.7.50.in-addr.arpa domain name pointer mail.megacorpone.com.
162.67.7.50.in-addr.arpa domain name pointer www.megacorpone.com.
163.67.7.50.in-addr.arpa domain name pointer mail2.megacorpone.com.
164.67.7.50.in-addr.arpa domain name pointer www2.megacorpone.com.
165.67.7.50.in-addr.arpa domain name pointer beta.megacorpone.com.
170.67.7.50.in-addr.arpa domain name pointer ns3.megacorpone.com.
178.67.7.50.in-addr.arpa domain name pointer syslog.megacorpone.com.
						...
```

### 4.1.5 - DNS Zone Transfers

A zone transfer is similar to a database replication act between related DNS servers. This process includes the copying of the zone file from a master DNS server to a slave server. The zone file contains a list of all the DNS names configured for that zone.
A successful zone transfer does not directly result in a network breach. However, it does facilitate the process. The **host** command syntax for preforming a zone transfer is as follows.

> host -l [domain name] [dns server address]

from our previous host command, we noticed that two DNS servers serve the **megacorpone.com** domain: ns1 and ns2. Let's try a zone transfer.

* NS1

```
root@kali:~# host -l megacorpone.com ns1.megacorpone.com
Using domain server:
Name: ns1.megacorpone.com
Address: 38.100.193.70#53
Aliases: 

Host megacorpone.com not found: 5(REFUSED)
; Transfer failed.

```

* NS2
```
root@kali:~# host -l megacorpone.com ns2.megacorpone.com
Using domain server:
Name: ns2.megacorpone.com
Address: 38.100.193.80#53
Aliases: 

megacorpone.com name server ns1.megacorpone.com.
megacorpone.com name server ns2.megacorpone.com.
megacorpone.com name server ns3.megacorpone.com.
admin.megacorpone.com has address 38.100.193.83
beta.megacorpone.com has address 38.100.193.69
fs1.megacorpone.com has address 38.100.193.82
intranet.megacorpone.com has address 38.100.193.81
mail.megacorpone.com has address 38.100.193.84
mail2.megacorpone.com has address 38.100.193.73
					...
```

In this case, *ns1* refused us our zone transfer request, while *ns2* allowed it. The result is a full dump of the zone file for the **megacorpone.com** domain, providing us a convenient list of IPs and DNS names for the **megacorpone.com** domain.

To perform a zone transfer with the **host** command, we need to parameters: the analyzed domain name and the name server address.

> host -l [domain name] [dns server address] | grep "has address"

Script:
##### [rev-dns-lookup.sh](#)

### 4.1.6 - Relevant Tools in Kali Linux

Several tools exist in Kali Linux to aid us in DNS enumeration and most of them perform the same tasks we have already covered in DNS enumeration.

#### 4.1.6.1 - DNSRecon

##### [DNSRecon](https://tools.kali.org/information-gathering/dnsrecon)

DNSRecon is an advanced, modern DNS enumeration script written in Python.

> root@kali:~# dnsrecon -d [domain name] -t axfr
> root@kali:~# dnsrecon -d megacorpone.com -t axfr

#### 4.1.6.2 - DNSEnum

DNSEnum is another popular DNS enumeration tool. Runnign this script against the **zonetransfer.me** domain, which specifically allows zone transfers.

> root@kali:~# dnsenum [domain name]

<br>

> root@kali:~# dnsenum zonetransfer.me

### 4.1.7 - Exercicies

1. Find the DNS servers for the megacorpone.com domain.

```
host -t ns megacorpone.com
megacorpone.com name server ns1.megacorpone.com.
megacorpone.com name server ns3.megacorpone.com.
megacorpone.com name server ns2.megacorpone.com.
```

2. Write a smal Bash Script to attempt a zone transfer from a domain.

> [rev-dns-lookup.sh](#)

3. Use **dnsrecon** to attempt a zone transfer from a domain.

> root@kali:~# dnsrecon -d megacorpone.com -t axfr

## 4.2 - Port Scanning

**Please note that port scanning is illegal in many countries.**

Port scanning is the process of checking for open TCP or UDP ports on a remote machine.

### 4.2.1 - TCP CONNECT/SYN Scanning

#### 4.2.1.1 - Connect Scanning

The simplest TCP port scanning technique, usually called CONNECT scanning, relies on the three-way TCP handshake mechanism. If the handshake is completed, this indicates that port is open.

Using **nc** comannd to find opent ports

> nc -nvv -w 1 -z [host IP] [port range]

<br>

> nc -nvv -w 1 -z 10.0.09 1-65535

#### 4.2.1.2 - Stealth/SYN Scanning

SYN scanning, is a TCP port scanning method that involves sending SYN packets to various ports on a target machine without completing a TCP handshake. If a TCP port is open, a SYN-ACK should be sent back from the target machine, informing us that the port is open, without the need to send a final ACK back to the target machine.

### 4.2.2 - UDP Scanning

Since UDP is stateless, and does not involve a three-way handshake, the mechanism behind UDP port scanning is different.

> nc -nv -u -z -w 1 [host IP] [port range]

<br>

> nc -nv -u -z -w 1 10.0.0.19 160-162

### 4.2.3 - Common Port Scanning Pitfalls

* UDP port scanning is often unreliable, as firewalls and routers may drop ICMP packets. This can lead to false positives in your scan, and you will regularly see UDP port scans showing all UDP ports open on a scanned machine.
* Most port scanners do not scan all available ports, and usually have a preset list of "interesting ports" that are scanned.