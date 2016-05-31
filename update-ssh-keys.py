#!/usr/bin/env python
# coding=utf-8

""" update-ssh-keys.py: Downloads the public ssh-keys from api.github.com for the selected user and inserts them into .ssh/authorized_keys. """

__author__ = "Jonathan stamp Grimmtjärn"
__license__ = "MIT"

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import os, json


# Open the ssh authorized keys file
authorized_keys = open(os.path.join(os.path.expanduser('~'),'.ssh/authorized_keys'), 'a+')

def insertOrUpdateKey(key):
    authorized_keys.seek(0);

    # Check if it already exists
    for line in authorized_keys:
        try:
            # Already there, exit
            line.index(key);
            return
        except ValueError:
            # Not found, check next line
            continue;

    # Add the key
    authorized_keys.write(key);

# Download keys and go thru them
response = urlopen("https://api.github.com/users/stamp/keys")
data = json.loads(str(response.read()))
keys = []
for item in data:
    try:
        item["key"].index("ssh-")
        key = item["key"] + " " + str(item["id"])+ "@github\r\n"
        insertOrUpdateKey(key)
        keys.append(key)
    except ValueError:
        continue;

# Remove all old keys
authorized_keys.seek(0);
old_file = authorized_keys.readlines();

authorized_keys.close();
authorized_keys = open(os.path.join(os.path.expanduser('~'),'.ssh/authorized_keys'), 'w+')
authorized_keys.seek(0);
for line in old_file:
    try:
        # Check that the key is from github
        line.index("@github");

        try:
            keys.index(line);
            #Key found, everything is good
            authorized_keys.write(line);
        except ValueError:
            #Not found, remove the key
            authorized_keys.write("# " + line);
    except ValueError:
        # Skip all lines that arent from github
        authorized_keys.write(line);
        continue;

# Make sure the file permissions is correct
os.chmod(os.path.join(os.path.expanduser('~'),'.ssh/authorized_keys'), 0o600);
