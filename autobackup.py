# Autobackup.py - zip a files seen in $HOME/Documents and upload to dropbox
# https://dropbox-sdk-python.readthedocs.io/en/master/moduledoc.html

import os, sys, shutil, dropbox
from pathlib import Path
from datetime import datetime
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

TOKEN = ''


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
    path = str(Path.home()) + '/Documents'
    folders, files = [], []
    # Confirm folders/files to be zipped
    for entry in os.scandir(path):
        if entry.is_dir():
            folders.append(entry)
        elif entry.is_file():
            files.append(entry)
    # print("Folders: - {}".format(folders)) // AutoBackup-Documents-2021-01-11.zip
    filename = 'AutoBackup-Documents-' + str(datetime.date(datetime.now())) + '.zip'
    # return zip folder
    return filename, shutil.make_archive(filename, 'zip', path)


def main():
    if len(TOKEN) == 0:
        sys.exit('ERROR: DropBox Access Token not provided')

    print("Confirming files to upload..")
    filename, file_from = zipfiles()
    file_to = '/DGAutoBackup/' + filename
    print('Zip to upload: ' + filename)
    print('DropBox upload location: ' + file_to)
    print("Initiating DropBox Client..")
    with dropbox.Dropbox(TOKEN, scope=['files.content.read', 'files.metadata.read', 'files.content.write']) as dbclient:
        try:
            # Auth check
            dbclient.users_get_current_account()
        except AuthError:
            sys.exit('ERROR: Bad Access Token provided')

    backup(dbclient, file_from, file_to)
    print('Upload Successful: ' + 'https://www.dropbox.com/home' + file_to)


if __name__ == '__main__':
    main()
