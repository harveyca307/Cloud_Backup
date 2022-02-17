"""
Usage:
    TM1_CLoud_Backup -h
    TM1_Cloud_Backup --help
    TM1_CLoud_Backup SERVERNAME SOURCE DESTINATION SEVENZIP [-fk <kn>]

Arguments:
    SERVERNAME  TM1 Instance Name
    SOURCE      TM1 Database Location
    DESTINATION Location to place backup files
    SEVENZIP    Location of 7z.exe

Options:
    -h, --help  Show this screen
    -f          Backup Feeder files
    -k <kn>     Keep <kn> number of backup files
"""
import os
import time

from docopt import docopt

from Services import BackupService


def main(args: dict) -> bool:
    try:
        backup_dict = {}
        server = args['SERVERNAME']
        source = args['SOURCE']
        destination = args['DESTINATION']
        seven = args['SEVENZIP']
        feeders = args['-f']
        keep = args['-k']
        if not os.path.exists(source):
            raise ValueError(f"Source path: {source} does not exist")
        if not os.path.exists(destination):
            raise ValueError(f"Destination path: {destination} does not exist")
        if not os.path.exists(seven):
            raise ValueError(f"Sevenzip not located at {seven}")
        backup_dict = {'Server': server,
                       'Source': source,
                       'Dest': destination,
                       'Seven': seven,
                       'Feeders': feeders,
                       'Retention': keep}
        bkp = BackupService(**backup_dict)
        bkp.backup()
        return True
    except ValueError as v:
        print(v)
        return False


if __name__ == "__main__":
    start_time = time.perf_counter()
    cmd_args = docopt(__doc__, version="TM1_Cloud_backup.exe by GL Consulting Services, 2.0")
    success = main(cmd_args)
    if success:
        end_time = time.perf_counter()
        print(f"Backup compete in {round(end_time - start_time, 2)} seconds")
    else:
        print("An error occurred.  See above errors")
        raise SystemExit
