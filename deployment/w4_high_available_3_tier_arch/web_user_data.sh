#!/bin/bash
set -xe

# Update system packages
dnf update -y

# Install Apache and proxy module
dnf install -y httpd mod_proxy_html

# Enable and start Apache service
systemctl enable httpd
systemctl start httpd

# Create web root directory
mkdir -p /var/www/html

# Download index.html from S3                                           # EDIT <s3-bucket-name>
aws s3 cp s3://<s3-bucket-name>/index.html /var/www/html/index.html     

# Set permissions
chmod 644 /var/www/html/index.html

# Configure reverse proxy                                               # EDIT <dns-name-app-alb>
cat <<EOL >/etc/httpd/conf.d/proxy.conf
<VirtualHost *:80>
    ServerName localhost

    ProxyPreserveHost On
    ProxyPass /api/ http://<dns-name-app-alb>/
    ProxyPassReverse /api/ http://<dns-name-app-alb>/

    DocumentRoot /var/www/html
    <Directory "/var/www/html">
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
EOL

# Restart Apache
systemctl restart httpd
