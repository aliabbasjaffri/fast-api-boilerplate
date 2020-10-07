# fast-api-boilerplate
fast-api boilerplate template for personal projects based on 12 factor app rules

## Setting up fastapi for Development Environment
- The development environment is managed by Docker and docker-compose file
- Update the variables in `docker-compose` file and run `docker-compose up`


## Setting up fastapi Application for Production Environment
- Launch a VM and upgrade/update it via `apt update && apt upgrade -yq`
- Install the system dependencies via `apt install -yq git python3 python3-pip nginx`
- Checkout this repository in it and move the project file to the appropriate directory
```bash
mv fast-api-boilerplate/ /opt/api
```
- Update `pip` and install python application dependencies using `python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt`
- Move the daemon service to the `systemd` path
```bash
mv /opt/api/api.service /etc/systemd/system/
```
- You can use the already created user `www-data` in the system. Alternatively you can create a new user as well.
- The advantage of user `www-data` is that you don't have to replace your user in `/etc/nginx/nginx.conf` file
```bash
# If you need to create a new user
useradd --system --user-group <USER-NAME>
chown -R <USER-NAME>:<GROUP-NAME> /opt/api
```
- Provide permissions to the api
```bash
chmod -R g+w /opt/api
```
- Create gunicorn log file and provide permissions to it
```bash
mkdir -p /var/log/gunicorn/ 
chown -R <USER-NAME>:<GROUP-NAME> /var/log/gunicorn/
```
- Reload the daemon and start it
```bash
systemctl daemon-reload
systemctl start api.service
systemctl enable api.service
systemctl status api.service
```
- If the command `systemctl status api.service` gives an error, run `journalctl -xe` for more details
- Next, setup nginx service to talk to gunicorn. Copy the contexts of `nginx.conf` in the folder to `/etc/nginx/sites-available/api` and replace the `<IP-ADDRESS>` with your server's IP address or your domain
- Execute the following steps:
```bash
# To verify if everything is okay
cat /etc/nginx/sites-available/api

# creating a link from sited available to sites enabled
ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled

# testing the service for the updated configuration
nginx -t
systemctl restart nginx && systemctl status nginx
```
- In case there is any error you can try either of the following commands to check where the issue exists
```bash
journalctl -xe
---

journalctl -u api
---

journalctl -u nginx
---

tail -30 /var/logs/nginx/error.log
```
- Allowing the system `ufw` to enable information exchange on all Nginx ports
```bash
sudo ufw allow 'Nginx Full'
```
- You can check the `netstat` if the application is responding on a respective port
```bash
netstat -lpn | grep app
```

### Setup NGINX with SSL and HTTP/2
- Generate self-signed certificates using OpenSSL. Create a Certification Authourity root certificate and generate server certificate from that CA.
- This example is with self-signed root CA authrourity. If you have a root CA for your domain, skip the step for its generation and jump directly to generating `fastapi Server CSR` and following steps.
```bash
# Generating root certificate `certificate signing request` to be used as Certification Authourity
openssl req -new -nodes -text -out fastapi.root.csr \
  -keyout fastapi.root.key -subj "/CN=<YOUR-DOMAIN>"
# Changing permissions on root certificate key
chmod og-rwx fastapi.root.key

# Generating root certificate with 10 years validity
openssl x509 -req -in fastapi.root.csr -text -days 3650 \
  -extfile /etc/ssl/openssl.cnf -extensions v3_ca \
  -signkey fastapi.root.key -out fastapi.root.crt

# Copying root certificate as root.ca.crt in ssl store
cp fastapi.root.crt /etc/ssl/root.ca.crt

# Generating CSR for fastapi server certificate
openssl req -new -nodes -text -out fastapi.server.csr \
  -keyout fastapi.server.key -subj "/CN=<YOUR-DOMAIN>"

# Changing certificate key access
chmod og-rwx fastapi.server.key

# Generating x509 certificate with 365 days validity
openssl x509 -req -in fastapi.server.csr -text -days 365 \
  -CA fastapi.root.crt -CAkey fastapi.root.key -CAcreateserial \
  -out fastapi.server.crt

# Copying fastapi.server.* certificate key pair to nginx certificate store
cp fastapi.server.{key,crt} /etc/ssl/
```
- The nginx conf file is already pointing to the generated certificate and key pair; `fastapi.server.{key,crt}`.
- To verify if the certificate is being served on secure port
```bash
openssl s_client -connect <VM-IP>:443 -showcerts
```

## API Testing
- If everything goes well, you can easily test the API at `<VM-IP-ADDRESS>:8000/docs` using swagger docs

## Supervisord as an alternative to Daemon Service
- If you are monitoring gunicorn via supervisord, you need to install it as a system dependency using `apt-get install -y supervisor`
- This would create `/etc/supervisor/conf.d` directory. Move the `supervisord.conf` to `/etc/supervisor/conf.d` via `mv supervisord.conf /etc/supervisor/conf.d`. This allows our config file to be included in the main supervisord config.
- Start the supervisor service via `systemctl start supervisor`
- You can monitor the state of the application being run using the built in web interface on `<VM-IP-ADDRESS>:9001`
- For troubleshooting, refer to the following [link](https://serversforhackers.com/c/monitoring-processes-with-supervisord)
