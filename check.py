#!/usr/bin/env python

URL = "{{ app_url }}"
app_name = "{{ app_name }}"
app_file = "{{ app_file }}"

# ----------------------------------------------------------------------------
# no need to edit below this line
# ----------------------------------------------------------------------------
import hashlib
import os
import requests
import shutil
import sqlite3
import tarfile
from datetime import datetime
from subprocess import call


def md5(fname):
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

r = requests.head(URL)

etag = r.headers.get('etag', False)
if not etag:
    print "URL/Etag not found %s" % URL
    exit(1)

if etag.startswith('"') and etag.endswith('"'):
    etag = etag[1:-1]

conn = sqlite3.connect('etags.db')
c = conn.cursor()
conn.execute("CREATE TABLE IF NOT EXISTS etags (etag text, cdate date)")
c.execute("SELECT etag FROM etags WHERE etag =?", (etag, ))
value = c.fetchone()
if not value:
    today = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # set a new dist_dir for every update
    dist_dir = "/arena/%s/releases/%s" % (app_name, today)

    print "ETAG not found, updating..."

    """ getting file """
    r = requests.get(URL, stream=True)

    """ save on tmp file very checksum and overwrite """
    with open("%s.tmp" % app_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    """ verify md5 == etag """
    if md5("%s.tmp" % app_file) != etag:
        print "WARNING md5 not matching"

    """ extract the contents of the compressed file to dist """
    with tarfile.open("%s.tmp" % app_file) as tar:
        tar.extractall(path=dist_dir)
        tar.close()

    """ add etag to local db """
    c.execute("INSERT INTO etags VALUES(?, ?)", (etag, datetime.utcnow()))
    conn.commit()

    service_dir = "/service/%s" % app_name
    """ remove old service and link to the new one """
    if os.path.exists(service_dir):
        if os.path.islink(service_dir):
            os.unlink(service_dir)
        else:
            shutil.rmtree(service_dir)

    """ update home link """
    current_link = "/arena/%s/current" % app_name
    if os.path.islink(current_link):
        os.unlink(current_link)
    elif os.path.exists(current_link):
        shutil.rmtree(current_link)

    """ link dist_dir to current """
    os.symlink(dist_dir, current_link)

    """ start the service """
    os.symlink("/arena/%s/runit" % app_name, service_dir)

    """ restart service """
    call(["sv", "restart", service_dir])
    exit(0)

print "ETAG found not updating, doing some cleaning..."
os.chdir("/arena/%s/releases" % app_name)
releases = sorted(filter(os.path.isdir, os.listdir('.')), key=os.path.getmtime)
for k in releases[3:]:
    shutil.rmtree(k)
exit(0)
