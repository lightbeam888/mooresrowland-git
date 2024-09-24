#!/bin/sh

# start api with gunicorn
/usr/src/Wagtail-CRX/virtualenv/bin/gunicorn mysite.wsgi -b 0.0.0.0:8000 --chdir=/usr/src/Wagtail-CRX
