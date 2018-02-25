# 1. ‐ Getting Comfortable with Kali Linux

##### p.22

#### [1.1 ‐ Finding Your Way Around Kali](#11-finding-your-way-around-kali_1)
* [1.1.3 - Find, Locate, and Which](#113-find-locate-and-which)
	* [locate](#locate)
	* [which](#which)
	* [find](#find)
	* [Exercicies](#exercicies)

#### [1.2 - Managing Kali Linux Services](#12---managing-kali-linux-services-1)
* [1.2.1 - Default root Password](#121---default-root-password)
* [1.2.2 - SSH Service](#122---ssh-service)
* [1.2.3 - HTTP Service](#123-http-service)
* [Exercicies](#exercicies-1)

#### [1.3 - The Bash Environment](#13---the-bash-environment-1)

#### [1.4 - Into to Bash Scripting](#14---into-to-bash-scripting-1)
* [1.4.1 - Pratical Bash Usage - Example 1](#141---pratical-bash-usage---example-1)
* [1.4.2 - Practical Bash Usage - Example 2](#142---practical-bash-usage---example-2)
* [Exercicies](#exercicies-2)

---

## 1.1 ‐ Finding Your Way Around Kali

### 1.1.3 - Find, Locate, and Which

There are a number of Linux utilities that can be used to locate files in a Linux installation with three of the most common being find, locate, and which. All three of these utilities all have similar functions, but work and return data in different ways.

### locate

Prior to using the locate utility, we must first use the updatedb command to build a local database of all files on the filesystem. Once the database has been built, locate can be used to easily query this database when looking for local files. Before running locate, you should always update the local database using the updatedb command.

```
root@kali:~# updatedb	
root@kali:~# locate sbd.exe
/usr/share/windows-­‐binaries/backdoors/sbd.exe
```

### which

The which command searches through the directories that are defined in the **$PATH** environment variable for a given filename. If a match is found, which returns the full path to the file as shown below.
```
root@kali:~# which sbd
/usr/bin/sbd
```

### find

The find command is a more aggressive search tool than locate or which. Find is able to recursively search any given path for various files.
```
root@kali:~# find / -­‐name sbd*
/usr/share/doc/sbd 
/usr/share/windows-­‐binaries/sbd.exe  
/usr/share/windows-­‐binaries/backdoors/sbd.exe  
/usr/share/windows-­‐binaries/backdoors/sbdbg.exe  
/usr/bin/sbd  
/var/lib/dpkg/info/sbd.md5sums  
/var/lib/dpkg/info/sbd.list
```

### Exercicies

2. Determine the cloation of the file **plink.exe** in Kali
```
root@kali:~# updatedb
root@kali:~# locate plink.exe
/usr/share/windows-binaries/plink.exe
```

3. Find and read the documentation fot the [dnsenum](https://tools.kali.org/information-gathering/dnsenum) tool
```
root@kali:~# find / -name dnsenum*
/usr/bin/dnsenum
/usr/share/python-faraday/plugins/repo/dnsenum
/usr/share/dnsenum
/usr/share/doc/dnsenum
/var/lib/dpkg/info/dnsenum.list
/var/lib/dpkg/info/dnsenum.md5sums
```

## 1.2 - Managing Kali Linux Services

### 1.2.1 - Default root Password

The root password can be changed with the **passwd** command as shown below.

```
root@kali:~# passwd
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully
```

### 1.2.2 - SSH Service

The [Secure Shell](https://en.wikipedia.org/wiki/Secure_Shell) (SSH) service is most commonly used to remotely access a computer, using a secure, encrypted protocol. The **SSH** service is a TCP-based and listens by default on port **22**. To start the **SSH**service in Kali, type the following command into a Kali terminal.

```
root@kali:~# service ssh start
Starting OpenBSD Secure Shell server: sshd.
```

We can verify that the **SSH** service is running and listening on TCP port 22, using the **netstat** command and **grep** command to search the output for sshd.
```
root@kali:~# netstat -antp | grep sshd
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      493/sshd            
tcp        0      0 10.0.2.15:22            10.0.2.2:48458          ESTABLISHED 3086/sshd: root@pts 
tcp6       0      0 :::22                   :::*                    LISTEN      493/sshd
```

To have the **SSH** service start automatically at boot time, you nedd to enable it using the **update-rc.d** script. The **update-rc.d** script can be used to enable and disable most services within Kali Linux.
```
root@kali:~# update-rc.d ssh enable
update­‐rc.d: using dependency based boot sequencing
```

### 1.2.3 HTTP Service

The **HTTP** service can come in handy during a penetration test, either for hosting a site, or providing a plataform for downloading file to a victim machine.

```
root@kali:~# service apache2 start
```

```
netstat -nlpt | grep apache
tcp6       0      0 :::80                   :::*                    LISTEN      3359/apache2
```

```
root@kali:~# update-rc.d apache2 enable
update­‐rc.d: using dependency based boot sequencing
```

### Exercicies

1. Change the **root** password
```
root@kali:~# passwd
```

2. Pratice starting and stopping various Kali services.
```
root@kali:~# update-rc.d apache2 enable
root@kali:~# update-rc.d apache2 disable
```

3. Enable the **SSH** service to statr on system boot.
```
root@kali:~# update-rc.d ssh enable
```

## 1.3 - The Bash Environment

The [GNU Bourne-Again SHell](https://en.wikipedia.org/wiki/Bash_Unix_shell) (Bash) provides a powerful environment to work in, and a scripting engine that we can make use of automate procedures using existing Linux tools.

## 1.4 - Into to Bash Scripting

### 1.4.1 - Pratical Bash Usage - Example 1

Imagine you are tasked with finding all of the subdomains listed on the *cisco.com* index page, and then find their corresponding IP address. With some simple Bash commands, we can turn this into an easy taks.

We start by downloading the *cisco.com* index page using **wget** commands.

```
wget http://www.cisco.com
URL transformed to HTTPS due to an HSTS policy
--2018-02-24 15:03:17--  https://www.cisco.com/
Resolving www.cisco.com (www.cisco.com)... 23.75.128.80, 2600:1419:18:18e::b33, 2600:1419:18:188::b33
Connecting to www.cisco.com (www.cisco.com)|23.75.128.80|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Saving to: ‘index.html’

index.html              [    <=>             ]  68,72K  22,6KB/s    in 3,0s    

2018-02-24 15:03:26 (22,6 KB/s) - ‘index.html’ saved [70373]
```

Quickly loking over this file, we see entries which contain the information we need such.

```html
<li><a href="//www.cisco.com/c/en/us/about/legal/trademarks.html">Trademarks</a></li>
```

We start by using the **grep** command to extract all the lines in the file that contain the string *href=*, indicating tha this line contains a link.
```
root@kali:~# grep "href=" index.html 
```

The result is still a swamp of HTML, but notice that most of the lines have a similar structure, and can be slipt conveniently using the *"/"* character as a delimiter. To specifically extract domain names from the file, we can try using the **cut** comman with our delimeter at the 3º field.

```
root@kali:~# grep "href=" index.html | cut -d "/"  -f3
```

The output we get is far from optimal, and has probally missed quite a few links on the way, but let's continue. Our text now includes entries such as the following.

> www.cisco.com
> secure.opinionlab.com
> developer.cisco.com
> learningnetwork.cisco.com
> supportforums.cisco.com
> video.cisco.com

Next, we will clean up our list to include only domain names. Use **grep** to filter out all the lines that contain a period, to get cleaner output.

```
root@kali:~# grep "href=" index.html | cut -d "/"  -f3 | grep "\."
```

Our output is almost clean, however we now have entries that look like the following.

> learningnetwork.cisco.com">Learning Network<
> supportforums.cisco.com">Support Community<

We can clean these out by using the **cut** command again, at the first delimeter.

```
root@kali:~# grep "href=" index.html | cut -d "/"  -f3 | grep "\." | cut -d '"' -f1
```

Now we have a nice clean list, but lost of duplicates. We can clean these ou by **sort** command, with the *unique* (**-u**) option.

```
root@kali:~# grep "href=" index.html | cut -d "/"  -f3 | grep "\." | cut -d '"' -f1 | sort -u
```
> blogs.cisco.com
> com.cisco.androidcisco
> communities.cisco.com
> developer.cisco.com
> idreg.cloudapps.cisco.com
> investor.cisco.com
> jobs.cisco.com
> learninglocator.cloudapps.cisco.com
> learningnetwork.cisco.com
> locatr.cloudapps.cisco.com
> marketplace.cisco.com
> mycase.cloudapps.cisco.com
> newsroom.cisco.com
> secure.opinionlab.com
> software.cisco.com
> supportforums.cisco.com
> tools.cisco.com
> video.cisco.com
> www.cisco.com
> www.ciscolive.com

Save content.

```
root@kali:~# grep "href=" index.html | cut -d "/"  -f3 | grep "\." | cut -d '"' -f1 | sort -u > list.txt
```

An even cleaner way of doing this would be to involve a touch of regular expressions into our command, redirecting the output into a text file, as shown below:

```
root@kali:~# cat index.html | grep -o 'http://[^"]*' | cut -d "/" -f3 | sort -u
```

Now we have a nice, clean list of domain names linked from the front page of *cisco.com*. Our next step will be to use the **host** command on each domain name in the text file we created, in order to discover their corresponding IP address. We can use a Bash oneline loop to do this for us:

```
root@kali:~# for url in $(cat list.txt); do host $url; done | grep "has address" | cut -d " " -f4 | sort -u
104.105.203.206
104.105.221.88
173.36.104.10
173.36.104.11
173.36.124.49
173.37.145.8
173.37.216.11
204.93.85.56
	 ...
```

### 1.4.2 - Practical Bash Usage - Example 2

We are given an Apache HTTP server log that contains evidence of an attack. Our task is to use simple Bash commands to inspect the and discover various pieces of information, such as who the attackers were, and what exactly happened on the server.
We first use the **head** and **wc** commands to take a quick peek at the log file to understand its structure.

```
root@kali:~# head access.log
		...
root@kali:~# wc -­l access.log
1788 access.log
```

Notice that the log file is grep friendly, and different fields such as, IP address, timestamp, HTTP request, etc., all of wichare separated by spaces. We begin by searching through the **=HTTP** requests made to the server, for all the IP address recorded in this log file. We will pipe the output of **cat** into the **cut** and **sort** commands. This may give us a clue about the number of potentional attackers we will need to deal with.

```
root@kali:~# cat access.log | cut -d " " -f1 | sort -u
194.25.19.29
202.31.272.117
208.68.234.99
5.16.23.10
88.11.27.23
93.241.170.13
	...
```

Wee see that less than ten IP addresses were recorded in the log file, although this still doesn'ttell us anything about the attackers. Next, we use **uniq** and **sort** to further refine out output, and sort the data by the number of times each IP address accessed the server.

```
root@kali:~# cat access.log | cut -d " " -f1 | sort | uniq -c | sort -urn
	1038 208.68.234.99
	445  186.19.15.24
	89   194.25.19.29
	62   142.96.25.17
	56   93.241.170.13
	37   10.7.0.52
	30   127.0.0.1
	13   5.16.23.10
	10   88.11.27.23
	6    172.16.40.254    
```

A few IP addresses stand out, but we will focus on the address that has the highest access frequency first. To display and ount the resources that were  being requested by the IP ddress, the following command sequence can be used:

```
root@kali:~# cat access.log | grep '205.167.170.15' | cut -d "\"" -f2 | uniq -c
1038
GET    //admin    HTTP/1.1
```

From this output, it seems that the IP address at 208.68.234.99 was accesssing the **/admin** directory exclusively. Let's take a closer look at this:

```
root@kali:~# cat access.log | grep '208.68.234.99' | grep '/admin' | sort -u

208.68.234.99 ­‐ ­‐ [22/Apr/2013:07:51:20 ­‐0500] "GET //admin HTTP/1.1" 401 742 "­‐" "Teh    Forest    Lobster"

root@kali:~# cat access.log|grep '208.68.234.99'| grep ­‐v 
```

It seems like 208.68.234.99 has been involved in an HTTP brute force attemp against this web server. Furthermore, after about 1070 attemps, it seems like the brute force attempt succeeded, as indicated by the HTTP 200 message.

### Exercicies

1. Research bash loops and write a short script to perform a ping sweep of your current subnet.

```bash
root@kali:~# for i in {1..5};do ping -c1 127.0.0.1; done
```

2. Try to do the above exercise with a higher-level scripting language such as Python, Perl, or Ruby.

```python
import sys
import os

print("Ping in Python")

def ping(host):
    rsp = os.system("ping -c3 " + host)

    if rsp == 0:
        print("[*] Host: " + host + " is up!")
    else:
        print("[!] Host: " + host + " is down!")

ping(sys.argv[1])
```

3. Ensure you understand the difference between directing output from a command line to a file (**>**) and output form a command as input to another command (**|**)