## Basic Scrapefeed launch


- Stop Apache first (which runs on port 80 by default on some servers).

```bash
/etc/init.d/apache2 stop

export FLASK_APP=~/scrapefeed/scrapefeed.py

nohup flask run --host=0.0.0.0 --port=80
```

- Restart Apache server:

```bash
/etc/init.d/apache2 start
```

> Caution: This setup is good for testing but can't handle concurrent users. See included 'Launch Server - Gunicode.md' for a bit more stability.