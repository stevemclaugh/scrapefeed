# Gunicorn server with Flask

## Setup

```bash
sudo apt-get update
sudo apt-get install python-pip python-dev nginx -y
sudo apt-get install libxml2-dev libxslt1-dev libssl-dev -y

sudo pip install virtualenv

mkdir ~/scrapefeed
cd ~/scrapefeed

virtualenv scrapefeedenv
source scrapefeedenv/bin/activate

sudo pip install -U bs4 ftfy unidecode lxml
```

### Starting Server

- Write Flask application and and save it somewhere.

- Create wsgi.py file in the same directory to launch Flask application from Gunicorn.

- Check firewall and open port 80 if necessary.

- If you're already running an Apache server on port 80 (for instance), kill it. That might look like this:

```bash
/etc/init.d/apache2 stop
```

- Launch Gunicorn server with up to 10 concurrent users.

```bash
sudo gunicorn --workers 10 --bind 0.0.0.0:80 wsgi
```

