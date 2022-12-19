# Flask Security
#### References:
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04

https://www.youtube.com/watch?v=goToXTC96Co&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=13

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
- sudo ufw allow 8000 
- sudo ufw enable 
- sudo ufw status

Transfer all project workfiles from local pc to remote server, use bash, 
- scp -r D:/python/flask_security han@ip_addr:~/

## Install Anaconda
- https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-22-04

## Install Redis
- https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-22-04

## Install NGINX
> sudo apt install nginx
> 
> sudo rm /etc/nginx/sites-enabled/default
> 
> sudo nano /etc/nginx/sites-enabled/flask_security

Add code below
```
server {
        listen 80;
        server_name 139.162.44.216 myfreedomaintest.website;

        location /static {
                alias /home/han/flask_security/flaskapp/static;
        }

        location / {
                proxy_pass http://localhost:8000;
                include /etc/nginx/proxy_params;
                proxy_redirect off;
        }

}
```
Link it
> sudo ln -s /etc/nginx/sites-available/flask_security /etc/nginx/sites-enabled

Allow port 8000
> sudo ufw allow 8000
> 
> sudo ufw allow http/tcp
> 
> sudo ufw delete allow 5000 (optional)
> 
> sudo ufw enable
> 
Restart nginx
> sudo systemctl restart nginx
> 
> sudo usermod -a -G han www-data
> 
> chmod 710 /home/han
> 
> sudo nginx -t
> 
> sudo systemctl restart nginx
> 
> sudo systemctl enable nginx
> 
> sudo systemctl status -l nginx
> 
Run gunicorn for test
> gunicorn -w 3 run:app 
- should be able to view the web page from http://<ip_addr> (no port)

- create service, start and enable the service. Make sure .sock file is created.
