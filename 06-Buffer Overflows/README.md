# 6. - Buffer Overflow

##### p. 132

When discussing buffer overflows, some of the questions that rise are **"How are these bugs found?"** and **"How did you know X bytes in the Y command would crash the application and result in a buffer overflow?"**.

There are three main ways of identifying flaws in application. If the source course of the application is available, then source code review is probably the easiesty way to identify bugs. If the application is closed source, you can use reverse engineering techniques, or fuzzing, to find bugs.

## 6.1 - Fuzzing

Fuzzing involves sending malformed data into application input and watching for unexpected crashes. An unexpected crash indicates that application might not filter certain input correctly. This could lead to discovering an exploitable vulnerability.

### 6.1.1 - Vulnerability History

The following example will demonstrate simplified fuzzing in order to find a known buffer overflow vulnerability in the [**SLMail 5.5 Mail Server**](https://www.exploit-db.com/apps/12f1ab027e5374587e7e998c00682c5d-SLMail55_4433.exe) software.

The buffer overflow was found back in 2005 and affected the POP3 **PASS** command, which is provided during user login. This makes the vulnerability a pre-authentication buffer overflow, as an attacker would not need to know any credentials, in order to trigger this vulnerability.

The SLMail software was not compiled with **Data Execution Prevention ([DEP](http://en.wikipedia.org/wiki/Data_Execution_Prevention))**, or **Address Space Layout Randomization ([ASLR](http://en.wikipedia.org/wiki/ASLR))** support, which makes the explotation process similar, as we will not have to bypass these internal security mechanisms.

### 6.1.2 - A Word About **DEP** and **ASLR**

#### DEP

**DEP** is a set of hardware, and software, tachnologies that perform additional checks on memory, to help prevent malicious code from running on a system. The primary benefit pf DEP is to help prevent code execution from data pages, by raising an exception, when execution occurs.

**ASLR** randomizes the base addresses of loaded applications, and DLLs, every time the Operating System is booted.

### 6.1.3 - Interacting with the POP3 Protocol

Earlier, we saw an example of this when we conversed with a POP3 server using **netcat**. To reproduce the netcat connection usage performed earlier in the course using a Python script.

##### [connect.py](https://github.com/cdojo/OSCP/blob/master/06-Buffer%20Overflows/scripts/slmail/connect.py)

Taking this simple script and modifying it to fuzz the password field during the login process is easy.

##### [fuzzer.py](https://github.com/cdojo/OSCP/blob/master/06-Buffer%20Overflows/scripts/slmail/fuzzer.py)

Running this script against your SLMail instance.

```
root@kali:~# ./fuzzer.py 10.0.0.1
Fuzzing PASS with 1 bytes
					...
Fuzzing PASS with 2700 bytes
Fuzzing PASS with 2900 bytes
```

When our **PASS** buffer reaches approximately 2700 bytes in length, the debugger presents us with the following information.

![Execution Halted in OllyDbg](https://preview.ibb.co/jwKeN7/im_dbg.png)

###### Execution Halted in OllyDbg

The screenshot suggests that the Extended Instruction Pointer (**[EIP](http://en.wikipedia.org/wiki/EIP_register#32-­bit)**) register has been overwritten with our input buffer of *A*'s (**\x41** in hex). This is of particular interest to us, as the EIP register also controls the execution flw of the application. This means that if we craft our exploit buffer carefully, we mught be able to divert the execution of the program to a place of our choosing, such as a into the memory were we can introduce some recever shell code, as part of our buffer.

One other Address worth noting in this specific window, is the value of the Extended Stack Pointer (**[ESP](https://en.wikipedia.org/wiki/Stack_register)**)

## Exercicies

1. Fuzz SLMail and replicate the crash.

> [fuzzer.py](https://github.com/cdojo/OSCP/blob/master/06-Buffer%20Overflows/scripts/slmail/fuzzer.py)

2. Examine the memory in the stack, when SLMail crashes. What does it look like? Consider how this might be useful.

> ...