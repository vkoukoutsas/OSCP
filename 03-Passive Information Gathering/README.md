# Passive Information Gathering

PIG is the process of colleting information about your target using publicly available information, in other words, any act of gathering information about your target without communicating with them directly can de considered "passive". This could include services like:

* Search engine results
* **whois** information
* Background check services
* Public company information
* Forum posts

##### Te more information we manage to gather about our target, prior to our attack, the more likely we are to succeed.

Information-gathering in a penetration test is the most important phase. Knowing your target before attacking it is a proven recipe for success.

## 3.1 - Open Web Information Gathering

Once an engagement starts, it's important to first spend time browsing the web, looking for background information about the tarhet organization. 

* What do they do?
* How do they interact with the world?
* Do they have a sales department?
* Are they hiring?
* Email
* Phone
* Company structure

Sometimes, it's the smallest details that give you the most information: how well designed is the target website? How clean is their HTML code? This might give you a clue their web development budget, which may reflect on their security budget.

### 3.1.1 - Google

The Goole search engine is a security auditor's best friend.

#### 3.1.1.1 - Ennumerating with Google

Google supports the use of various search operators, wich allow a user to narrow down and pinpoint search results.

* site

> site:microsoft.com

The **site** operator will limit Google search results to a single domain. A simples search operator like this provide us with useful information.

* -site

> site:microsoft.com -site:www.microsoft.com

Remove **www** search

* filetype

> filetype:sql

* inurl

> inurl:admin.php

* intitle

> intitle: index of

* title

> title:"Admin Painel"

### 3.1.2 - Google Hacking

Using Google Hacking to find juicy information, vulnerabilities, or misconfigured websites was publicly introduced by Johnny Long in 2001. SInce then, a database of interesting searches has been compiled to enable security auditors to quickly identify numerous misconfigurations within a given domain.

#### 3.1.2.1 - Hardware with Known Vulnerabilities

Finding hardware with known vulnerabilities

> intitle:"SpeedStream Router Management Interface"

#### 3.1.2.2 - Web Accessible, Open Cisco Routers

Finding Web Accessible, Open Cisco Routers

> inurl:"level/15/exec/-/show"

#### 3.1.2.3 - Exposed Frontpage Credentials

Using Google to find exposed frontpage Credentials

> "# -FrontPage-" filetype:pwd inutl:(service | authors | adminitrators | users)"


### GHDB

The are hundreds of interesting searches that can be made, and many of them are listed in the [Google Hacking](https://www.exploit-db.com/google-hacking-database/) (GHDB) section of the Exploit Database.

### 3.1.3 - Exercicies

1. Choose an organization and use Google to gather as much information as possible about it.

> site:www.facebook.com

2. Use the Google **filetype** search operator and look for interesting documents from the target organization.

> filetype: txt

3. Re-do the exercise on your copany's domain. Can you find anu data leakage you were not aware of?

## 3.2 - Email Harvesting

##### [theHarvester](https://tools.kali.org/information-gathering/theharvester)

Email harvesting is an effective way of finding emails, and possibly usernames, belonging to an organization. These emails are useful in many ways, such as prividing us a potential list for client side attacks, revealing the naming convention used in the organization, or mapping out users in the organization.

One of the tools in Kali Linux that can perform this task is **theharvester**.

```
root@kali:~# theharvester ­‐d cisco.com	­‐b google > google.txt
root@kali:~# theharvester ­‐d cisco.com	-l 10 ­‐b bing > bing.txt
```

* Examples:
```
root@kali:~# theharvester -d microsoft.com -l 500 -b google -h myresults.html
root@kali:~# theharvester -d microsoft.com -b pgp
root@kali:~# theharvester -d microsoft -l 200 -b linkedin
root@kali:~# theharvester -d apple.com -b googleCSE -l 500 -s 300
```

### 3.2.1 - Exercicies

1. Use **theharvester** to enumerate email addresses belonging to the organization you chose in the previous exercicies.

> root@kali:~# theharvester -d example.com -b google

2. Experiment with different data sources (**-b**). Which work best for you?

> linkedin, yahoo, baidu, twitter, shodan...

<br>

> root@kali:~# theharvester -d example.com -b bing

## 3.3 - Additional Resources

### 3.3.1 - Netcraft

##### [Netcraft](https://www.netcraft.com/)

Netcraft can be used to indirectly find out information about web servers on the Internet, including the underlying operating system, web server version, and uptime graphs.

### 3.3.2 - Whois Enumeration

Whois is a name for a TCP service, a tool, and a type of database. Whois databases contain name server, registrar, and, in some cases, full contact information about a domain name. These databases are usually published by a whois server over **TCP port 43** and are accessible using **whois** client program.

```
root@kali:~# whois megacorpone.com
```