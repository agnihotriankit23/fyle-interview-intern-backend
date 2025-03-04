#!/bin/bash

# Reset DB Before Testing
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/

pytest -vvv -s tests/
#pytest --cov