# sets up my web servers for the deployment of web_static

exec { 'deploy':
  provider => shell,
  command  => "apt-get -y update ; apt-get -y install nginx ; service nginx start ; mkdir -p /data/web_static/shared/ ; mkdir -p /data/web_static/releases/test/ ; echo 'Alx School' > /data/web_static/releases/test/index.html ; ln -sf /data/web_static/releases/test/ /data/web_static/current ; chown -R ubuntu:ubuntu /data/ ; sed -i '41i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n' /etc/nginx/sites-available/default ; service nginx restart"
}
