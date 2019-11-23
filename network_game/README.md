# Network based multi-players bounce game
The project extends the bounce game program to a network multi-players game

# How to test
## Run both server and clients locally on the same computer

### Run server
```shell
python server.py
```
or:
```shell
python server.py 127.0.0.1
```

### Run clients
```shell
python bounce.py 127.0.0.1 my_cool_name
```

Note that you can start multiple clients in different consoles

## Run both server and client in a local network on the different computers
### Find the IP address of the computer you are going to run the server progra
```shell
ipconfig
```
You may get the output similar to the following:

```shell

Windows IP Configuration


Ethernet adapter Ethernet:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :

Wireless LAN adapter Local Area Connection* 1:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :

Wireless LAN adapter Local Area Connection* 2:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :

Wireless LAN adapter Wi-Fi:

   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : fe80::9c5a:538d:ec8e:163d%13
   IPv4 Address. . . . . . . . . . . : 192.168.1.28
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.1.1

Ethernet adapter Bluetooth Network Connection:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
```

In this case, your IP address of the computer is "192.168.1.28" shown in the line "IPv4 Address". The following examples uses "192.168.1.28", you'd replace the IP address with what you get from ipconfig command.

### Run server
```shell
python server.py 192.168.1.28
```

### Run clienta
On the same computer as your server computer or different computer, start the bounce game clients by:
```shell
python bounce.py 192.168.1.28 my_cool_name
```
Note that you can start multiple clients on different computers
