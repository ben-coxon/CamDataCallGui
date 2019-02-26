#!/bin/bash

source venv/bin/activate

export FLASK_APP=notes_blog.py

## Allows email debug (currently not working!)
export MAIL_SERVER=smtp.googlemail.com
export MAIL_PORT=587
export MAIL_USE_TLS=1
export MAIL_USERNAME='benstechnotes@gmail.com'
export MAIL_PASSWORD='!Volcalogue'

flask run