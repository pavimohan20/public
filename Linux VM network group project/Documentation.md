# Linux VM network - DOCUMENTATION

*Henri Hubert, Pavithra Mohan, Tom Macdonald*

*As part of a 7-month training program at BeCode, we undertook a group project to create a network composed of two virtual machines (VMs): a Kali Linux client with LibreOffice, Gimp and Mullvad browser installed and a Linux server providing DHCP, DNS, web server, and SSH connection services.*
___
**Table of contents**
- [Setting up the VMs](#setting-up-the-vms)
- [Server configuration](#server-configuration)
	- [DHCP](#dhcp)
	- [DNS](#dns----resolves-our-webpage-forwards-for-external-resources)
	- [Web server](#web-server)
- [Client configuration](#client-configuration)
___
## Setting up the VMs

**Client**: https://cdimage.kali.org/kali-2024.3/kali-linux-2024.3-virtualbox-amd64.7z

Download the file at the above link, extract all, in the extracted file double click “kali-linux-2024.3-virtualbox-amd64” (the one with a blue cube, Type “VirtualBox Machine Definition”). VirtualBox will automatically execute the file and start a Kali Linux VM

**Server**: [Get Ubuntu Server | Download](https://ubuntu.com/download/server)

VirtualBox Manager > New > ISO Image: ubuntu-24.04.1-live-server-amd64; Type: Linux

### Putting both VMs on the same network:

[How to Network Two Virtual Machines With VirtualBox](https://www.makeuseof.com/how-network-two-virtual-machines-with-virtualbox/)

1. VirtualBox Manager > Tools > Network > NAT Networks > Create a NAT network with DHCP activated
![](./Assets/nat%20network%20tools.png)
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfWSO1LGth3zFoBk4i8aJtPa6LwYW1RjWyu7710NeNkSNT5uP2sW0dvm2kKyR4uXNkv5Vqs8NeG2IS36DH8f4ZE520YvalHbn41nsL66u4B11wkQ_VVV4vpVfVL2EZ1sYqavX7CnZIjKqO98eQhEHpMb3dD?key=PV6ni2H3hUc-OvwgPjFkQ3mK)
  
3. On each VM, Settings > Network > Attached to: NAT Network; Name: [name of the NAT network you just created]
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXceDAzbti459SpQc6lI3cXE_FZiNhfeNUdKfCUpvqaccw0OpdSOchFI-6XYCGg4JGhEDz7GLNljzOCqTP-s3Nyyo0cRZs8PvtpSWwAf3OnJ1EfAYCx68R46q8mg-ZXdyijSpVhyz8oXmvxJD-6VkVSFEA?key=PV6ni2H3hUc-OvwgPjFkQ3mK)
___
## Server configuration

### DHCP


### DNS -- resolves our webpage, forwards for external resources

**On the server**

Install bind and net-tools

`sudo apt-get install bind9`

`sudo apt-get install net-tools`

Check the IP of the server thanks to net-tools

`ifconfig`

After using the command `sudo nano /etc/bind/named.conf.options`, setup forwarders (google 8.8.8.8 and google backup 8.8.4.4):

```
forwarders {

8.8.8.8;

8.8.4.4;

};
```

Enable firewall and allow bind9

`sudo ufw enable`

`sudo ufw status`

`sudo ufw allow bind9`

`sudo ufw reload`

`sudo ufw status`

Status should indicate “active” and Bind9: “ALLOW”

Restart service and check if it worked

`sudo systemctl reload bind9`

`sudo systemctl status bind9`

Active section should indicate “active (running)” and Status section: “running”

**On the client**

Right click on the Connections icon (top right corner) > Edit connections… > Wired connection 1 > IPv4 Settings > Additional DNS servers: 10.0.2.15 (the default IP that is automatically assigned to a VM, you can check the IP of the server with `ifconfig` on the CLI of the server)
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdf7SqP2xGDF2Yi-xowwDLaM0f091vKWNs1YJDfvxpoK8yLIpMmCB9LSfs72Re-dOzmBuBCK59BBr9lXuNDI0zMlu5TCy1xAVoXmffQNZxNH3PPWduiznBb7NC9M7o0caJmSeqKIUmL_tHEPZ2I79nsNe2o?key=PV6ni2H3hUc-OvwgPjFkQ3mK)

### Web server


___
## Client configuration
  
  
  
  
  
  
___
## Online resources:

- [How to Network Two Virtual Machines With VirtualBox](https://www.makeuseof.com/how-network-two-virtual-machines-with-virtualbox/) 
- [Setting up a Bind DNS server on Ubuntu server](https://youtu.be/DuVNclBfykw)
- [How to change DNS Server on Kali Linux | Troubleshoot DNS on Kali](https://youtu.be/Ya0AZDPgvNk)
- [Linux DNS Server Configuration for Beginners](https://youtu.be/I8lawEbZKxA)
- [Linux DNS Server - YouTube](https://www.youtube.com/playlist?list=PL291a0KYQZSK6E_1j9xkkieCOi_867pyc)
- 
