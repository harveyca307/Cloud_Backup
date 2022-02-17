import datetime
import os
import subprocess
from pathlib import Path


class BackupService:

    def __init__(self, **kwargs):
        self.server = kwargs['Server']
        self.source = kwargs['Source']
        self.dest = kwargs['Dest']
        self.seven = kwargs['Seven']
        self.feeders = kwargs['Feeders']
        self.keep = int(kwargs['Retention'])
        date = datetime.datetime.now()
        self.tmst = date.strftime('%Y%m%d%H%M%S')
        # Source
        self.source = Path(self.source)
        self.source = '"{}"'.format(self.source)
        self.source = Path(self.source)
        # Dest
        self.zipfile = Path(self.dest)
        self.zipfile = self.zipfile / ''.join([self.server + '_Backup_' + self.tmst + '.7z'])
        self.zipfile = '"{}"'.format(self.zipfile)
        self.zipfile = Path(self.zipfile)
        # 7-zip
        self.seven = Path(self.seven)
        self.seven = '"{}"'.format(self.seven)
        self.seven = Path(self.seven)
        # print directions
        print(f"Server Name: {self.server}")
        print(f"Source path {self.source} found.")
        print(f"Destination path {self.dest} found.")
        print(f"7-zip path {self.seven} confirmed.")
        print(f"Backup file to be generated: {self.zipfile}")
        if self.feeders:
            print("Feeders will be backed up")
            self.cmd = fr'{self.seven} a {self.zipfile} -t7z -mmt -mx=1 -- {self.source}'
        else:
            print("Feeders will be ignored")
            self.cmd = fr'{self.seven} a {self.zipfile} -t7z -mmt -mx=1 -xr!FEEDERS -- {self.source}'
        if self.keep:
            print(f"Backup file retention {self.keep}")
        else:
            print("All backup files will be retained.")

    def clean_dir(self):
        print(f"Beginning clean of folder: {self.dest}")
        _keep = int(self.keep)
        for file in sorted(os.listdir(self.dest))[:-_keep]:
            f = os.path.join(self.dest, file)
            os.remove(f)
        print("Cleaning complete")

    def backup(self):
        print("Backup starting...")
        no_window = 0X08000000
        subprocess.call(self.cmd, creationflags=no_window)
        if self.keep:
            self.clean_dir()
