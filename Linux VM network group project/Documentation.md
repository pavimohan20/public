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
	- [Backups](#backups-cron)
- [Client configuration](#client-configuration)
___
## Setting up the VMs

**Client**: https://cdimage.kali.org/kali-2024.3/kali-linux-2024.3-virtualbox-amd64.7z

Download the file at the above link, extract all, in the extracted file double click “kali-linux-2024.3-virtualbox-amd64” (the one with a blue cube, Type “VirtualBox Machine Definition”). VirtualBox will automatically execute the file and start a Kali Linux VM

**Server**: [Get Ubuntu Server | Download](https://ubuntu.com/download/server)

VirtualBox Manager > New > ISO Image: ubuntu-24.04.1-live-server-amd64; Type: Linux

### Putting both VMs on the same network

1. VirtualBox Manager > Tools > Network > NAT Networks > Create a NAT network with DHCP activated
![](./Assets/nat%20network%20tools.png)
  
3. On each VM, Settings > Network > Attached to: NAT Network; Name: [name of the NAT network you just created]
![](./Assets/nat%20network%20hosts.png)
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
![](./Assets/client%20dns.png)

### Web server

1. Update packages:

`sudo apt update`

2. Install nginx:

`sudo apt install nginx -y`

3. Make sure nginx starts and that it will start working when you turn the server on:

`sudo systemctl start nginx`

`sudo systemctl enable nginx`

4. Go to the directory to start making your page:

`cd /etc/nginx/sites-available/`

5. Create your web page config file in this directory and start writing in it:

`sudo nano /etc/nginx/sites-available/my_website`

6. Write the config lines for the page in the nano:

```
server {
    listen 80;
    server_name your_domain_or_IP;
    root /var/www/my_website;
    index index.html index.htm;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

7. Create a directory for you webpage:

`sudo mkdir -p /var/www/my_website`

8. Give yourself the permissions to modify it and have access to it:

`sudo chown -R $USER:$USER /var/www/my_website`

`sudo chmod -R 755 /var/www/my_website`

9. Check in /var/www/my_website if the file index.html exists and if it doesn’t, create it:

`cd /var/www/my_website`

`ls`

`touch index.html`

10. Modify the index.html file with your html file:

`nano index.html`

`<html><body><h1>Hello World!</h1></body></html>`

11. Create a symbolic link to enable the new webpage:

`sudo ln -s /etc/nginx/sites-available/my_website /etc/nginx/sites-enabled/`

12. Check the nginx configuration:

`sudo ln -s /etc/nginx/sites-available/my_website /etc/nginx/sites-enabled/`

13. Restart nginx for it to work:

`sudo systemctl reload nginx`

14. To connect to the webpage:
	a. connect with you machine to the server with ssh

`ssh username@server_ip_adress`

	b. open your web navigator and type the ip address of your server as the url

15. If it is still not working:
	1. delete the default file in /var/www/
	2. delete the default file in /etc/nginx/sites-enabled/
	3. restart nginx

### Backups (cron)

#### Define Backup Requirements:

**Services to Back Up:** We focused on backing up the configuration files for the DHCP and DNS services, with plans to add Nginx later.
**Backup Destination:** We decided to use a dedicated backup directory, /mnt/backup, for storing backup files.

#### Setup the Backup Directory:

**Mounting the Backup Partition:**
You mounted a partition (like /dev/sda2) to /mnt/backup to ensure that there was enough space and separation for backup files.

You used the command:

`sudo mount /dev/sda2 /mnt/backup`

**Create the Backup Script:**

Script Creation: We created a backup script named backup_config.sh in your home directory using nano.

`nano ~/backup_config.sh`

`#!/bin/bash`

Backup destination directory

`BACKUP_DIR="/mnt/backup"`

Create a timestamp for the backup file name

`TIMESTAMP=$(date +"%Y%m%d%H%M")`

`BACKUP_FILE="$BACKUP_DIR/config_backup_$TIMESTAMP.tar.gz"`

**Ensure the backup directory exists**

```
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Backup directory $BACKUP_DIR does not exist. Please mount the partition."
    exit 1
fi
```


#### Create the backup of configuration files

Update the paths below based on your actual configuration files
`tar -czvf "$BACKUP_FILE" /etc/dhcp/dhcpd.conf /etc/bind/named.conf`

Check if the backup was successful
```
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $BACKUP_FILE"
else
    echo "Backup failed!"
    exit 1
fi
```

Save and exit

**Run the backup Script:**

`sudo ~/backup_config.sh`

**Verify the Backup**

`ls -l /mnt/backup`

**CRON:**

Cron is a time-based job scheduler in Unix-like operating systems, including Linux. It allows you to run scripts or commands automatically at specified intervals (e.g., hourly, daily, weekly). Using cron, you can schedule your backup script to run automatically without needing to manually execute it each time.

`crontab -e`

**Run the backup every Sunday at 2:00 AM, you would add the following line:**

`0 2 * * 0 /bin/bash /home/pavithra/backup_config.sh`

**Run the crontab**

`crontab -l`

By setting up a cron job, your backup script will run automatically at the specified time, ensuring that you have regular backups of your configuration files without manual intervention. 
### SSH connection
**On server**

Make sure SSH is installed

Enable and start

`sudo systemctl start ssh`

`sudo systemctl enable ssh`

`sudo systemctl status ssh`
 
Allow ssh through the firewall

`sudo ufw allow ssh`

`sudo ufw reload
`
`sudo ufw status`
 
**On client**

`ssh [user]@[ip of the ssh server]`




___
## Client configuration
  
  
  
  
  
  
___
## Online resources:

- [How to Network Two Virtual Machines With VirtualBox](https://www.makeuseof.com/how-network-two-virtual-machines-with-virtualbox/) 
- [Setting up a Bind DNS server on Ubuntu server](https://youtu.be/DuVNclBfykw)
- [How to change DNS Server on Kali Linux | Troubleshoot DNS on Kali](https://youtu.be/Ya0AZDPgvNk)
- [Linux DNS Server Configuration for Beginners](https://youtu.be/I8lawEbZKxA)
- [Linux DNS Server - YouTube](https://www.youtube.com/playlist?list=PL291a0KYQZSK6E_1j9xkkieCOi_867pyc)
- [How to add a new user on a Linux server (with SSH access)](https://youtu.be/86EYEuJWfeE)
- [How to enable SSH on Linux Ubuntu](https://youtu.be/Wlmne44M6fQ)
