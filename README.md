# Flask Security


- Login to ubuntu server v22.04
    >ssh root@'ipaddress'
    >'Enter password'
- apt update && apt upgrade
- hostnamectl set-hostname flask-server
- hostname
- nano /etc/hosts
- adduser han
- 'Create password'
- adduser han sudo

Now let's login without password authentication for better security!
-mkdir .ssh

Under win local computer, use bash to generate ssh key

    > ssh-keygen -b 4096
- Make sure file is generated under dir C:\Users\afaid\.ssh
- Transfer generated file id_rsa.pub to remote server under dir ~/.ssh folder
    > scp id_rsa.pub han@ip_addr:~/.ssh/authorized_keys


Under Linux remote server, set permission
> sudo chmod 700 ~/.ssh/

> sudo chmod 600 ~/.ssh/*

- Test if can login w/o password with ssh han@ip_addr
  - Disable root login 
    - sudo nano /etc/ssh/sshd_config 
    - set root login PermitRootLogin to no 
    - set PasswordAuthentication to no
- Save the file and restart ssh server
    >     sudo systemctl restart sshd

Let's install firewall
- sudo apt install ufw 
- sudo ufw default allow outgoing 
- sudo ufw default deny incoming 
- sudo ufw allow ssh 
- sudo ufw allow 5000 
- sudo ufw enable 
- sudo ufw status

Transfer all project workfiles from local pc to remote server, use bash, 
- scp -r D:/python/flask_security han@ip_addr:~/



