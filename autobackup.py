# Autobackup.py - zip a files seen in $HOME/Documents and upload to dropbox
# https://dropbox-sdk-python.readthedocs.io/en/master/moduledoc.html

import os, sys, shutil, dropbox, configparser
from pathlib import Path
from datetime import datetime
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

credpath = str(Path.home()) + '/credentials.txt'
creds = configparser.ConfigParser()
creds.read(credpath)
TOKEN = creds['dropbox']['token']


def backup(db, ff, ft):
    with open(ff, 'rb') as f:
        print("Uploading to Dropbox:" + ft)
        # TODO duplicate file check / dropbox versioning
        try:
            db.files_upload(f.read(), ft, mode=WriteMode('overwrite'))
        except ApiError as err:
            print(err)
            sys.exit()


def zipfiles():
    path = str(Path.home()) + '/Desktop/test'
    filename = 'AutoBackup-Documents-' + str(datetime.date(datetime.now())) + '.zip'
    # return zip folder
    return filename, shutil.make_archive(filename, 'zip', path)


def main():
    if len(TOKEN) == 0:
        sys.exit('ERROR: DropBox Access Token not provided')

    print("Confirming files to upload..")
    filename, zippedfiles = zipfiles()
    uploadlocation = '/DGAutoBackup/' + filename
    print('Zip to upload: ' + filename)
    print('Dropbox upload location: ' + uploadlocation)
    print("Initiating Dropbox Client..")
    with dropbox.Dropbox(TOKEN, scope=['files.content.read', 'files.metadata.read', 'files.content.write']) as dbclient:
        try:
            # Auth check
            dbclient.users_get_current_account()
        except AuthError:
            sys.exit('ERROR: Bad Access Token provided')

    backup(dbclient, zippedfiles, uploadlocation)
    print('Upload Successful: ' + 'https://www.dropbox.com/home' + uploadlocation)


if __name__ == '__main__':
    main()
