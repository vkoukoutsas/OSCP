# 4. - Active Information Gathering

##### p. 82

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
root@kali:~# host -t ns megacorpone.com
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

> root@kali:~# nc -nvv -w 1 -z [host IP] [port range]

<br>

> root@kali:~# nc -nvv -w 1 -z 10.0.09 1-65535

#### 4.2.1.2 - Stealth/SYN Scanning

SYN scanning, is a TCP port scanning method that involves sending SYN packets to various ports on a target machine without completing a TCP handshake. If a TCP port is open, a SYN-ACK should be sent back from the target machine, informing us that the port is open, without the need to send a final ACK back to the target machine.

### 4.2.2 - UDP Scanning

Since UDP is stateless, and does not involve a three-way handshake, the mechanism behind UDP port scanning is different.

> root@kali:~# nc -nv -u -z -w 1 [host IP] [port range]

<br>

> root@kali:~# nc -nv -u -z -w 1 10.0.0.19 160-162

### 4.2.3 - Common Port Scanning Pitfalls

* UDP port scanning is often unreliable, as firewalls and routers may drop ICMP packets. This can lead to false positives in your scan, and you will regularly see UDP port scans showing all UDP ports open on a scanned machine.
* Most port scanners do not scan all available ports, and usually have a preset list of "interesting ports" that are scanned.
* People often forget to scan for UDP services, and stick only to tcp scanning, thereby seeing only half of the equation.

### 4.2.4 - Port Scanning with Nmap

##### [Nmap](https://nmap.org/)

Nmap is one of the most popular, versatile, and robust port scanners to date.

#### 4.2.4.1 - Accountability for Your Traffic

A default **nmap** TCP scan will scan the 1000 most popular ports on a given machine.

##### Metasploitable vm

```
root@kali:~# nmap -sT 192.168.0.104

Starting Nmap 7.01 ( https://nmap.org ) at 2018-03-11 09:42 -04
Nmap scan report for 192.168.0.104
Host is up (0.0017s latency).
Not shown: 977 closed ports
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
23/tcp   open  telnet
25/tcp   open  smtp
53/tcp   open  domain
80/tcp   open  http
111/tcp  open  rpcbind
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
512/tcp  open  exec
513/tcp  open  login
514/tcp  open  shell
1099/tcp open  rmiregistry
1524/tcp open  ingreslock
2049/tcp open  nfs
2121/tcp open  ccproxy-ftp
3306/tcp open  mysql
5432/tcp open  postgresql
5900/tcp open  vnc
6000/tcp open  X11
6667/tcp open  irc
8009/tcp open  ajp13
8180/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 1.66 seconds
```

#### 4.2.4.2 - Network Sweeping

To deal with large volumes of hosts, or to otherwise try to conserve network traffic, we can attempt to probe these machines using **Network Sweeping** techniques. Network Sweeping is a term indicating a network wide action.

```
root@kali:~# nmap -sn 192.168.11.200-250
```

Searching for live machines using the **grep** command can give you autput that's difficult to manage. Instead, let's use Nmap's "greppable" output parameter (**-oG**) to save these results into a format that is easier to manage.

```
root@kali:~# nmap -v -sn 192.168.11.200-250 -oG ping-sweep.txt
root@kali:~# grep Up ping-sweep.txt | cut -d " " -f 2
```

Additionally, we can sweep for specific TCP or UDP ports (**-p**) across the network, probing for common services and ports with services that may be useful, or otherwise have known vulnerabilities.

```
root@kali:~# nmap -p 80 192.168.0.200-250 -oG web-sweep.txt
root@kali:~# grep open web-sweep.txt | cut -d " " -f 2
```

Using techniques such as these, we can scan across multiple IPs, probing for only a few common ports. In the command below, we are conducting a scan for the top 20 TCP ports.

```
root@kali:~# nmap -sT -A --top-ports=20 192.168.0.200-250 -oG top-ports-sweep.txt
```

Machines that prove to be rich in services, or otherwise interesting, would then be individually port scanned, using a more exhaustive port list.

### 4.2.5 - O.S Fingerprinting

Nmap has a built-in feature called **OS Fingerprinting** (**-O** parameter). This feature attempts to guss the underlying operating system, by inspecting the packets received from the target. The Nmap scanner will inspect the traffic sent and received from the target machine, and attempt to match the fingerprint to a know list.

```
root@kali:~# nmap -O 192.168.0.200
						...
Device type: general purpose
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6
OS details: Linux 2.6.9 - 2.6.33
Network Distance: 1 hop
						...
```

### 4.2.6 - Banner Grabbing/Service Enumeration

Nmap can also help identify services on specific ports, by banner grabbing, and running several enumeration scripts (**-sV** and **-A** parameters).

```
root@kali:~# nmap -sV -sT 192.168.0.200

Starting Nmap 7.01 ( https://nmap.org ) at 2018-03-11 10:15 -04
Nmap scan report for 192.168.0.104
Host is up (0.0017s latency).
Not shown: 977 closed ports
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.3.4
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
23/tcp   open  telnet      Linux telnetd
25/tcp   open  smtp        Postfix smtpd
53/tcp   open  domain      ISC BIND 9.4.2
80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)
111/tcp  open  rpcbind     2 (RPC #100000)
139/tcp  open  netbios-ssn Samba smbd 3.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.X (workgroup: WORKGROUP)
512/tcp  open  exec        netkit-rsh rexecd
513/tcp  open  login
514/tcp  open  tcpwrapped
1099/tcp open  rmiregistry GNU Classpath grmiregistry
1524/tcp open  shell       Metasploitable root shell
2049/tcp open  nfs         2-4 (RPC #100003)
2121/tcp open  ftp         ProFTPD 1.3.1
3306/tcp open  mysql       MySQL 5.0.51a-3ubuntu5
5432/tcp open  postgresql  PostgreSQL DB 8.3.0 - 8.3.7
5900/tcp open  vnc         VNC (protocol 3.3)
6000/tcp open  X11         (access denied)
6667/tcp open  irc         Unreal ircd
8009/tcp open  ajp13       Apache Jserv (Protocol v1.3)
8180/tcp open  http        Apache Tomcat/Coyote JSP engine 1.1
Service Info: Hosts:  metasploitable.localdomain, localhost, irc.Metasploitable.LAN; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.46 seconds
```

### 4.2.7 - Nmap Scripting Engine (NSE)

The Nmap Scripting Engine (NSE) is a recent addition to Nmap, wich allows users to write simple scripts, in order to automate various networking tasks. The scripts include a broad range of utilities, form DNS enumeration scripts, brute force attack scripts, and even vulnerability identification scripts.
All NSE scripts can be found in the **/usr/share/nmap/scripts** directory.

```
root@kali:~# ls /usr/share/nmap/scripts/
acarsd-info.nse                         ike-version.nse
address-info.nse                        imap-brute.nse
afp-brute.nse                           imap-capabilities.nse
afp-ls.nse                              informix-brute.nse
afp-path-vuln.nse                       informix-query.nse
afp-serverinfo.nse                      informix-tables.nse
afp-showmount.nse                       ip-forwarding.nse
ajp-auth.nse                            ip-geolocation-geobytes.nse
ajp-brute.nse                           ip-geolocation-geoplugin.nse
ajp-headers.nse                         ip-geolocation-ipinfodb.nse
ajp-methods.nse                         ip-geolocation-maxmind.nse
ajp-request.nse                         ip-https-discover.nse
allseeingeye-info.nse                   ipidseq.nse
amqp-info.nse                           ipv6-node-info.nse
asn-query.nse                           ipv6-ra-flood.nse
auth-owners.nse                         irc-botnet-channels.nse
auth-spoof.nse                          irc-brute.nse
backorifice-brute.nse                   irc-info.nse
backorifice-info.nse                    irc-sasl-brute.nse
bacnet-info.nse                         irc-unrealircd-backdoor.nse
banner.nse                              iscsi-brute.nse
bitcoin-getaddr.nse                     iscsi-info.nse
bitcoin-info.nse                        isns-info.nse
bitcoinrpc-info.nse                     jdwp-exec.nse
bittorrent-discovery.nse                jdwp-info.nse
bjnp-discover.nse                       jdwp-inject.nse
broadcast-ataoe-discover.nse            jdwp-version.nse
broadcast-avahi-dos.nse                 knx-gateway-discover.nse
broadcast-bjnp-discover.nse             knx-gateway-info.nse
broadcast-db2-discover.nse              krb5-enum-users.nse
broadcast-dhcp6-discover.nse            ldap-brute.nse
broadcast-dhcp-discover.nse             ldap-novell-getpass.nse
broadcast-dns-service-discovery.nse     ldap-rootdse.nse
broadcast-dropbox-listener.nse          ldap-search.nse
broadcast-eigrp-discovery.nse           lexmark-config.nse
broadcast-igmp-discovery.nse            llmnr-resolve.nse
broadcast-listener.nse                  lltd-discovery.nse
broadcast-ms-sql-discover.nse           maxdb-info.nse
broadcast-netbios-master-browser.nse    mcafee-epo-agent.nse
broadcast-networker-discover.nse        membase-brute.nse
broadcast-novell-locate.nse             membase-http-info.nse
broadcast-pc-anywhere.nse               memcached-info.nse
broadcast-pc-duo.nse                    metasploit-info.nse
broadcast-pim-discovery.nse             metasploit-msgrpc-brute.nse
broadcast-ping.nse                      metasploit-xmlrpc-brute.nse
broadcast-pppoe-discover.nse            mikrotik-routeros-brute.nse
broadcast-rip-discover.nse              mmouse-brute.nse
broadcast-ripng-discover.nse            mmouse-exec.nse
broadcast-sonicwall-discover.nse        modbus-discover.nse
broadcast-sybase-asa-discover.nse       mongodb-brute.nse
broadcast-tellstick-discover.nse        mongodb-databases.nse
broadcast-upnp-info.nse                 mongodb-info.nse
broadcast-versant-locate.nse            mrinfo.nse
broadcast-wake-on-lan.nse               msrpc-enum.nse
broadcast-wpad-discover.nse             ms-sql-brute.nse
broadcast-wsdd-discover.nse             ms-sql-config.nse
broadcast-xdmcp-discover.nse            ms-sql-dac.nse
cassandra-brute.nse                     ms-sql-dump-hashes.nse
cassandra-info.nse                      ms-sql-empty-password.nse
cccam-version.nse                       ms-sql-hasdbaccess.nse
citrix-brute-xml.nse                    ms-sql-info.nse
citrix-enum-apps.nse                    ms-sql-query.nse
citrix-enum-apps-xml.nse                ms-sql-tables.nse
citrix-enum-servers.nse                 ms-sql-xp-cmdshell.nse
citrix-enum-servers-xml.nse             mtrace.nse
couchdb-databases.nse                   murmur-version.nse
couchdb-stats.nse                       mysql-audit.nse
creds-summary.nse                       mysql-brute.nse
cups-info.nse                           mysql-databases.nse
cups-queue-info.nse                     mysql-dump-hashes.nse
cvs-brute.nse                           mysql-empty-password.nse
cvs-brute-repository.nse                mysql-enum.nse
daap-get-library.nse                    mysql-info.nse
daytime.nse                             mysql-query.nse
db2-das-info.nse                        mysql-users.nse
dhcp-discover.nse                       mysql-variables.nse
dict-info.nse                           mysql-vuln-cve2012-2122.nse
distcc-cve2004-2687.nse                 nat-pmp-info.nse
dns-blacklist.nse                       nat-pmp-mapport.nse
dns-brute.nse                           nbstat.nse
dns-cache-snoop.nse                     ncp-enum-users.nse
dns-check-zone.nse                      ncp-serverinfo.nse
dns-client-subnet-scan.nse              ndmp-fs-info.nse
dns-fuzz.nse                            ndmp-version.nse
dns-ip6-arpa-scan.nse                   nessus-brute.nse
dns-nsec3-enum.nse                      nessus-xmlrpc-brute.nse
dns-nsec-enum.nse                       netbus-auth-bypass.nse
dns-nsid.nse                            netbus-brute.nse
dns-random-srcport.nse                  netbus-info.nse
dns-random-txid.nse                     netbus-version.nse
dns-recursion.nse                       nexpose-brute.nse
dns-service-discovery.nse               nfs-ls.nse
dns-srv-enum.nse                        nfs-showmount.nse
dns-update.nse                          nfs-statfs.nse
dns-zeustracker.nse                     nje-node-brute.nse
dns-zone-transfer.nse                   nping-brute.nse
docker-version.nse                      nrpe-enum.nse
domcon-brute.nse                        ntp-info.nse
domcon-cmd.nse                          ntp-monlist.nse
domino-enum-users.nse                   omp2-brute.nse
dpap-brute.nse                          omp2-enum-targets.nse
drda-brute.nse                          omron-info.nse
drda-info.nse                           openlookup-info.nse
duplicates.nse                          openvas-otp-brute.nse
eap-info.nse                            oracle-brute.nse
enip-info.nse                           oracle-brute-stealth.nse
epmd-info.nse                           oracle-enum-users.nse
eppc-enum-processes.nse                 oracle-sid-brute.nse
fcrdns.nse                              ovs-agent-version.nse
finger.nse                              p2p-conficker.nse
firewalk.nse                            path-mtu.nse
firewall-bypass.nse                     pcanywhere-brute.nse
flume-master-info.nse                   pgsql-brute.nse
freelancer-info.nse                     pjl-ready-message.nse
ftp-anon.nse                            pop3-brute.nse
ftp-bounce.nse                          pop3-capabilities.nse
ftp-brute.nse                           pptp-version.nse
ftp-libopie.nse                         qconn-exec.nse
ftp-proftpd-backdoor.nse                qscan.nse
ftp-vsftpd-backdoor.nse                 quake1-info.nse
ftp-vuln-cve2010-4221.nse               quake3-info.nse
ganglia-info.nse                        quake3-master-getservers.nse
giop-info.nse                           rdp-enum-encryption.nse
gkrellm-info.nse                        rdp-vuln-ms12-020.nse
gopher-ls.nse                           realvnc-auth-bypass.nse
gpsd-info.nse                           redis-brute.nse
hadoop-datanode-info.nse                redis-info.nse
hadoop-jobtracker-info.nse              resolveall.nse
hadoop-namenode-info.nse                reverse-index.nse
hadoop-secondary-namenode-info.nse      rexec-brute.nse
hadoop-tasktracker-info.nse             rfc868-time.nse
hbase-master-info.nse                   riak-http-info.nse
hbase-region-info.nse                   rlogin-brute.nse
hddtemp-info.nse                        rmi-dumpregistry.nse
hnap-info.nse                           rmi-vuln-classloader.nse
hostmap-bfk.nse                         rpcap-brute.nse
hostmap-ip2hosts.nse                    rpcap-info.nse
hostmap-robtex.nse                      rpc-grind.nse
http-adobe-coldfusion-apsa1301.nse      rpcinfo.nse
http-affiliate-id.nse                   rsync-brute.nse
http-apache-negotiation.nse             rsync-list-modules.nse
http-auth-finder.nse                    rtsp-methods.nse
http-auth.nse                           rtsp-url-brute.nse
http-avaya-ipoffice-users.nse           s7-info.nse
http-awstatstotals-exec.nse             samba-vuln-cve-2012-1182.nse
http-axis2-dir-traversal.nse            script.db
http-backup-finder.nse                  servicetags.nse
http-barracuda-dir-traversal.nse        sip-brute.nse
http-brute.nse                          sip-call-spoof.nse
http-cakephp-version.nse                sip-enum-users.nse
http-chrono.nse                         sip-methods.nse
http-cisco-anyconnect.nse               skypev2-version.nse
http-coldfusion-subzero.nse             smb-brute.nse
http-comments-displayer.nse             smb-enum-domains.nse
http-config-backup.nse                  smb-enum-groups.nse
http-cors.nse                           smb-enum-processes.nse
http-cross-domain-policy.nse            smb-enum-sessions.nse
http-csrf.nse                           smb-enum-shares.nse
http-date.nse                           smb-enum-users.nse
http-default-accounts.nse               smb-flood.nse
http-devframework.nse                   smb-ls.nse
http-dlink-backdoor.nse                 smb-mbenum.nse
http-dombased-xss.nse                   smb-os-discovery.nse
http-domino-enum-passwords.nse          smb-print-text.nse
http-drupal-enum.nse                    smb-psexec.nse
http-drupal-enum-users.nse              smb-security-mode.nse
http-enum.nse                           smb-server-stats.nse
http-errors.nse                         smb-system-info.nse
http-exif-spider.nse                    smbv2-enabled.nse
http-favicon.nse                        smb-vuln-conficker.nse
http-feed.nse                           smb-vuln-cve2009-3103.nse
http-fetch.nse                          smb-vuln-ms06-025.nse
http-fileupload-exploiter.nse           smb-vuln-ms07-029.nse
http-form-brute.nse                     smb-vuln-ms08-067.nse
http-form-fuzzer.nse                    smb-vuln-ms10-054.nse
http-frontpage-login.nse                smb-vuln-ms10-061.nse
http-generator.nse                      smb-vuln-regsvc-dos.nse
http-git.nse                            smtp-brute.nse
http-gitweb-projects-enum.nse           smtp-commands.nse
http-google-malware.nse                 smtp-enum-users.nse
http-grep.nse                           smtp-open-relay.nse
http-headers.nse                        smtp-strangeport.nse
http-huawei-hg5xx-vuln.nse              smtp-vuln-cve2010-4344.nse
http-icloud-findmyiphone.nse            smtp-vuln-cve2011-1720.nse
http-icloud-sendmsg.nse                 smtp-vuln-cve2011-1764.nse
http-iis-short-name-brute.nse           sniffer-detect.nse
http-iis-webdav-vuln.nse                snmp-brute.nse
http-joomla-brute.nse                   snmp-hh3c-logins.nse
http-litespeed-sourcecode-download.nse  snmp-info.nse
http-ls.nse                             snmp-interfaces.nse
http-majordomo2-dir-traversal.nse       snmp-ios-config.nse
http-malware-host.nse                   snmp-netstat.nse
http-methods.nse                        snmp-processes.nse
http-method-tamper.nse                  snmp-sysdescr.nse
http-mobileversion-checker.nse          snmp-win32-services.nse
http-ntlm-info.nse                      snmp-win32-shares.nse
http-open-proxy.nse                     snmp-win32-software.nse
http-open-redirect.nse                  snmp-win32-users.nse
http-passwd.nse                         socks-auth-info.nse
http-phpmyadmin-dir-traversal.nse       socks-brute.nse
http-phpself-xss.nse                    socks-open-proxy.nse
http-php-version.nse                    ssh2-enum-algos.nse
http-proxy-brute.nse                    ssh-hostkey.nse
http-put.nse                            sshv1.nse
http-qnap-nas-info.nse                  ssl-ccs-injection.nse
http-referer-checker.nse                ssl-cert.nse
http-rfi-spider.nse                     ssl-date.nse
http-robots.txt.nse                     ssl-dh-params.nse
http-robtex-reverse-ip.nse              ssl-enum-ciphers.nse
http-robtex-shared-ns.nse               ssl-google-cert-catalog.nse
http-server-header.nse                  ssl-heartbleed.nse
http-shellshock.nse                     ssl-known-key.nse
http-sitemap-generator.nse              ssl-poodle.nse
http-slowloris-check.nse                sslv2.nse
http-slowloris.nse                      sstp-discover.nse
http-sql-injection.nse                  stun-info.nse
http-stored-xss.nse                     stun-version.nse
http-svn-enum.nse                       stuxnet-detect.nse
http-svn-info.nse                       supermicro-ipmi-conf.nse
http-title.nse                          svn-brute.nse
http-tplink-dir-traversal.nse           targets-asn.nse
http-trace.nse                          targets-ipv6-map4to6.nse
http-traceroute.nse                     targets-ipv6-multicast-echo.nse
http-unsafe-output-escaping.nse         targets-ipv6-multicast-invalid-dst.nse
http-useragent-tester.nse               targets-ipv6-multicast-mld.nse
http-userdir-enum.nse                   targets-ipv6-multicast-slaac.nse
http-vhosts.nse                         targets-ipv6-wordlist.nse
http-virustotal.nse                     targets-sniffer.nse
http-vlcstreamer-ls.nse                 targets-traceroute.nse
http-vmware-path-vuln.nse               targets-xml.nse
http-vuln-cve2006-3392.nse              teamspeak2-version.nse
http-vuln-cve2009-3960.nse              telnet-brute.nse
http-vuln-cve2010-0738.nse              telnet-encryption.nse
http-vuln-cve2010-2861.nse              tftp-enum.nse
http-vuln-cve2011-3192.nse              tls-nextprotoneg.nse
http-vuln-cve2011-3368.nse              tor-consensus-checker.nse
http-vuln-cve2012-1823.nse              traceroute-geolocation.nse
http-vuln-cve2013-0156.nse              unittest.nse
http-vuln-cve2013-7091.nse              unusual-port.nse
http-vuln-cve2014-2126.nse              upnp-info.nse
http-vuln-cve2014-2127.nse              url-snarf.nse
http-vuln-cve2014-2128.nse              ventrilo-info.nse
http-vuln-cve2014-2129.nse              versant-info.nse
http-vuln-cve2014-8877.nse              vmauthd-brute.nse
http-vuln-cve2015-1427.nse              vnc-brute.nse
http-vuln-cve2015-1635.nse              vnc-info.nse
http-vuln-misfortune-cookie.nse         voldemort-info.nse
http-vuln-wnr1000-creds.nse             vuze-dht-info.nse
http-waf-detect.nse                     wdb-version.nse
http-waf-fingerprint.nse                weblogic-t3-info.nse
http-webdav-scan.nse                    whois-domain.nse
http-wordpress-brute.nse                whois-ip.nse
http-wordpress-enum.nse                 wsdd-discover.nse
http-wordpress-users.nse                x11-access.nse
http-xssed.nse                          xdmcp-discover.nse
iax2-brute.nse                          xmlrpc-methods.nse
iax2-version.nse                        xmpp-brute.nse
icap-info.nse                           xmpp-info.nse
```

One such script is **smb-os-discovery**, which attempts to connect to the SMB service on a target system, and determine its operating system version.

```
root@kali:~# nmap 192.168.0.104 --script smb-os-discovery.nse
Host script results:
| smb-os-discovery: 
|   OS: Unix (Samba 3.0.20-Debian)
|   NetBIOS computer name: 
|   Workgroup: WORKGROUP
|_  System time: 2018-02-16T22:23:16-05:00

Nmap done: 1 IP address (1 host up) scanned in 2.50 seconds
```

Another useful script is the DNS zone transfer NSE script, wich can be invoked in the following way:

```
root@kali:~# nmap --script=dns-zone-transfer -p 53 ns2.example.com
```

### 4.2.8 - Exericies

1. Use **nmap** to conduct a ping sweep for your target IP range and save the output to a file, so that you can grep for hosts that are online.

```
root@kali:~# nmap -sn 192.168.0.1-150 -oG ping-sweep.txt
root@kali:~# grep Up ping-sweep.txt | cut -d" " -f2 >> hosts.txt
```

2. Scan the IPs you found in exercise 1 for open webserver ports. Use **nmap** to find the web sever and operating system version.

```
root@kali:~# sudo nmap -iL hosts.txt -p 80 -O
[sudo] password for zero: 

Starting Nmap 7.01 ( https://nmap.org ) at 2018-03-11 10:32 -04
Nmap scan report for 192.168.0.1
Host is up (0.0053s latency).
PORT   STATE SERVICE
80/tcp open  http
MAC Address: C8:3A:35:4D:3A:78 (Tenda Technology)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Wind River VxWorks
OS CPE: cpe:/o:windriver:vxworks
OS details: VxWorks
Network Distance: 1 hop

Nmap scan report for 192.168.0.104
Host is up (0.00024s latency).
PORT   STATE SERVICE
80/tcp open  http
MAC Address: 08:00:27:3B:13:69 (Oracle VirtualBox virtual NIC)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6
OS details: Linux 2.6.9 - 2.6.33
Network Distance: 1 hop

Nmap scan report for 192.168.0.105
Host is up (0.000046s latency).
PORT   STATE  SERVICE
80/tcp closed http
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6
OS details: Linux 2.6.14 - 2.6.34, Linux 2.6.17, Linux 2.6.17 (Mandriva)
Network Distance: 0 hops

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 4 IP addresses (3 hosts up) scanned in 7.90 seconds

```

3. Use the NSE scripts to scan the servers in the labs wich are running the SMB service.

```
root@kali:~# nmap -v -Pn --script smb-* 192.168.0.104
```

4. Explore the various command line options that nmap offers while scanning an online host you discovered within your target IP range. Monitor the bandwidth usage changes for the different options. Weigh the use of collecting as much informations possible against the resources it takes to gather it.

[nmap-cheat-sheet](#)

## 4.3 - SMB Enumeration

##### [SMB wiki](https://en.wikipedia.org/wiki/Server_Message_Block)

The Server Message Block (SMB) protocol's security track record has been poor for over a decade, due to its complex implementation, and open nature. From unauthenticated SMB null sessions in Windows 2000 and XP, to a plethora of SMB bugs and vulnerabilities over the years, SMB has seen its fair share of action.

* SMB version numbers, and their related Windows Operating system versions:
	* **SMB1** - Windows 2000, XP and Windows 2003
	* **SMB2** - Windows Vista SP1 and Windows 2008
	* **SMB2.1** - Windows 7 and Windows 2008 R2
	* **SMB3** - Windows 8 and Windows 2012

### 4.3.1 - Scanning for the NetBIOS Service

##### [NetBIOS wiki](https://en.wikipedia.org/wiki/NetBIOS)

The SMB NetBIOS service listens on TCP ports 139 and 445, as well as several UDP ports. These can be scanned with tools, such as **nmap**, using syntax similar to the following:

```
root@kali:~# nmap -v -p 138,445 -oG smb.txt 192.168.11.200-254
```

There are other, more specialized, tools for specifically identifying NetBIOS information, such as **nbtscan** as shown below.

```
root@kali:~# nbtscan -r 192.168.11.0/24
```

## 4.3.2 - Null Session Enumeration

##### [enum4linux](https://tools.kali.org/information-gathering/enum4linux)

A null session refers to an unauthenticated NetBIOS session betwee two computers. This feature exists to allow unauthenticated machines to obtain browse lists from other Microsoft servers. A null session also allows unauthenticated hackers to obtain large amounts of information about the machine, such as password polices, usernames, group names, machine names, user and host SIDs.
A useful tool for this is **enum4linux**, present in Kali. It is written in Perl and is basically a wrapper around the [Samba](http://www.samba.org/) tools **smbclient**, **rpcclient**, **net** and **nmblookup**.

```
root@kali:~# enum4linux -a 192.168.11.227
```

###### For more information about **enum4linux**, check out the examples available on the [Portcullis Labs website](http://labs.portcullis.co.uk/tools/enum4linux/)

### 4.3.3 - Nmap SMB NSE Scripts

##### [NSE scripts](https://nmap.org/nsedoc/)

Nmap contains many useful NSE scripts that can be used to discover and enumerate SMB services. These scripts can be found in the **/usr/share/nmap/scripts** directory.

```
root@kali:~# ls /usr/share/nmap/scripts/smb*
/usr/share/nmap/scripts/smb-brute.nse
/usr/share/nmap/scripts/smb-enum-domains.nse
/usr/share/nmap/scripts/smb-enum-groups.nse
/usr/share/nmap/scripts/smb-enum-processes.nse
/usr/share/nmap/scripts/smb-enum-sessions.nse
/usr/share/nmap/scripts/smb-enum-shares.nse
/usr/share/nmap/scripts/smb-enum-users.nse
/usr/share/nmap/scripts/smb-flood.nse
/usr/share/nmap/scripts/smb-ls.nse
/usr/share/nmap/scripts/smb-mbenum.nse
/usr/share/nmap/scripts/smb-os-discovery.nse
/usr/share/nmap/scripts/smb-print-text.nse
/usr/share/nmap/scripts/smb-psexec.nse
/usr/share/nmap/scripts/smb-security-mode.nse
/usr/share/nmap/scripts/smb-server-stats.nse
/usr/share/nmap/scripts/smb-system-info.nse
/usr/share/nmap/scripts/smbv2-enabled.nse
/usr/share/nmap/scripts/smb-vuln-conficker.nse
/usr/share/nmap/scripts/smb-vuln-cve2009-3103.nse
/usr/share/nmap/scripts/smb-vuln-ms06-025.nse
/usr/share/nmap/scripts/smb-vuln-ms07-029.nse
/usr/share/nmap/scripts/smb-vuln-ms08-067.nse
/usr/share/nmap/scripts/smb-vuln-ms10-054.nse
/usr/share/nmap/scripts/smb-vuln-ms10-061.nse
/usr/share/nmap/scripts/smb-vuln-regsvc-dos.nse
```

We can see thtat several interesting Nmap SMB NSE scripts exist, such as OS discovery and enumeration of various pieces of information from the protocol.

```
root@kali:~# nmap -v -p 139, 445 --script=smb-os-discovery 192.168.11.227
```

To check for known SMB protocol vulnerabilities, you can invoke the **nmap** <b>*smb-check-vulns*</b> script as shown below.

```
root@kali:~# nmap -v -p 139,445 --script=smb-check-vulns --script-args=unasafe=1 192.168.11.201
```

In this case, **nmap** identifies that the specific SMB service is missing at least one critical patch for the [MS08-067](https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2008/ms08-067) vulnerability.

### 4.3.4 - Exercises

1. Use Nmap to make a list of which SMB servers in the lab are running Windows.

2. Use NSE scripts to scan these systems for SMB vulnerabilities.

```
root@kali:~# nmap -v -p 139,445 --script=smb-check-vulns --script-args=unasafe=1 192.168.11.201
```

3. Use **nbtscan** and **enum4linux** against these systems and identify the kinds of data you can obtain from different versions of Windows.

## 4.4 - SMTP Enumeration

##### [SMTP](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol)

In certain vulnerable configurations, mail servers can also be used to gather information about a host or network. SMTP supports several important commands, such as **VRFY** and **EXPN**. A **VRFY** request asks the server to verify an email address, while **EXPN** asks the server for the membership of a mailing list.

Example:

```
root@kali:~# nc -nv 192.168.0.104 25
Connection to 192.168.0.104 25 port [tcp/*] succeeded!
220 metasploitable.localdomain ESMTP Postfix (Ubuntu)
VRFY root
252 2.0.0 root
VRFY idontexist
550 5.1.1 <idontexist>: Recipient address rejected: User unknown in local recipient table
```

Notice the difference in the message received when a user is present on the system. The SMTP server happily verifies that the user exists. This procedure can be used to help guess valid usernames.

[smtp-vrfy.py](#)

### 4.4.1 - Exercise

1. Search your target network range, and see if you can identify any systems that respond to the SMTP *VRFY* command.

## 4.5 - SNMP Enumeration

##### [SNMP](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol)

Over the years, we have often found that Simple Network Management Protocol (SNMP) is a poorly understood protocol by many network administrators. This often results in SNMP misconfigurations, which can result in a dramatic information leakage. SNMP is based on UDP, a simple, stateless protocol, and is therefore susceptible to IP spoofing, and replay attacks. In a addition, the commonly used SNMP protocols 1, 2 and 2c offer no traffic encryption, meaning SNMP information and credentials can be easily intercepted over a local network. Traditional SNMP protocols also have weak authentication schemes, and are commonly left configured with default public and private community strings.
<br>
Now, consider that all of the above applies to a protocol, which by definition is meant to "Manege the Network".

### 4.5.1 - MIB Tree

The SNMP Management Information Base ([MIB](https://en.wikipedia.org/wiki/Management_information_base)) is a databse containing information usually related to network management. The database is organized like a tree, where branches represent different organizations or network functions. The leaves of the tree (final endpoints) correspond to specific variable values that can then be accessed, and probed, by an external user.

For example, the following MIB values corresponf to specific Microsoft Windows SNMP parameters.

| - | - |
| - | - |
| 1.3.6.1.2.1.25.1.6.0  | System Processes |
| 1.3.6.1.2.1.25.4.2.1.2 | Running Programs |
| 1.3.6.1.2.1.25.4.2.1.4 | Processes Path |
| 1.3.6.1.2.1.25.2.3.1.4 | Storage Units |
| 1.3.6.1.2.1.25.6.3.1.2 | Software Name |
| 1.3.6.1.4.1.77.1.2.25 | User Accounts |
| 1.3.6.1.2.1.6.13.1.3	| TCP Local Ports |

### 4.5.2 - Scanning for SNMP

To scan open SNMP ports, we can use **nmap** with syntax similar to:

```
root@kali:~# nmap -sU --open -p 161 192.168.11.200-254 -oG mega-snmp.txt
```

Alternatively, we can use a toll such as **onesixtyone**, wich will check for given community strings against an IP list, allowing us to brute force various community strings.

```
root@kali:~# echo public > community
root@kali:~# echo private >> community
root@kali:~# echo manager >> community
root@kali:~# for ip in $(seq 200 254);do echo 192.168.11.$ip;done > ips
root@kali:~# onesixtyone -c community -i ips
```

Once these SNMP services are found, we can start querying them for specific MIB data that misght be interesting to us.

### 4.5.3 - Windows SNMP Enumeration Example

We can probe and query SNMP values using a tool such as **snmpwalk** provide we at least know the SNMP read-only community string, wich in most cases is "<b>*public*</b>". Using some of the MIB values provided above, we could attemp to enumerate their corresponding values.

#### Enumerating the Entire MIB Tree:

```
root@kali:~# snmpwalk -c public -v1 192.168.11.204 1.3.6.1.4.1.77.1.2.25
```

#### Enumerating Windows Users:

```
root@kali:~# snmpwalk -c public -v1 192.168.11.204 1.3.6.1.2.1.25.4.2.1.2
```

#### Enumerating Running Windows Processes:

```
root@kali:~# snmpwalk -c public -v1 192.168.11.204 1.3.6.1.2.1.6.13.1.3
```

#### Enumerating Open TCP Ports:

```
root@kali:~# snmpwalk -c public -v1 192.168.11.204 1.3.6.1.2.1.6.13.1.3
```

#### Enumerating Installed Software:

```
root@kali:~# snmpwalk -c public -v1 192.168.11.204 1.3.6.1.2.1.25.6.3.1.2
```

### 4.5.4 - Exercicies

1. Scan yout target network with **onesixtyone**. Identify any SNMP servers.

2. Use **snmpwalk** and **snmpcheck** to gather information about the discovered targets.