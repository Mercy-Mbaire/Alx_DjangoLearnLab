# Deployment Guide: Securing your Django Application with HTTPS

This guide provides instructions for configuring popular web servers to support HTTPS for your Django application.

## Nginx Configuration

To secure your application with Nginx, you need to set up an SSL server block and proxy requests to your Django application (e.g., using Gunicorn).

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/mediafiles/;
    }
}
```

## Apache Configuration

For Apache, you can use the `mod_ssl` module and `mod_proxy`.

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com

    SSLEngine on
    SSLCertificateFile /path/to/your/certificate.crt
    SSLCertificateKeyFile /path/to/your/private.key

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    Alias /static /path/to/your/staticfiles
    <Directory /path/to/your/staticfiles>
        Require all granted
    </Directory>
</VirtualHost>
```

## Obtaining SSL Certificates

You can obtain free SSL certificates from [Let's Encrypt](https://letsencrypt.org/) using the `certbot` tool.

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```
