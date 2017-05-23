"""FileMonitor
modified by http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
only on windows
Usage:
  file_monitor [--no-dump]
  file_monitor <watch-path>... [--no-dump]

Options:
  watch-path  default ["C:\\WINDOWS\\Temp", tempfile.gettempdir()]
  --no-dump   not dump modified file content

"""
__version__ = '1.0'
import os
import signal
import tempfile
import threading

import cchardet as chardet
from docopt import docopt
from minghu6.etc.version import iswin

if iswin():
    dirs_to_monitor = ["C:\\WINDOWS\\Temp", tempfile.gettempdir()]
else:
    dirs_to_monitor = [tempfile.gettempdir()]

# file modification constants
FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5


def start_monitor_win(path_to_watch, no_dump=False):
    import win32file
    import win32con
    # we create a thread for each monitoring run
    FILE_LIST_DIRECTORY = 0x0001

    h_directory = win32file.CreateFile(
        path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None)

    while True:
        try:
            results = win32file.ReadDirectoryChangesW(
                h_directory,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
            )

            for action, file_name in results:
                full_filename = os.path.join(path_to_watch, file_name)

                if action == FILE_CREATED:
                    print("[ + ] Created %s" % full_filename)
                elif action == FILE_DELETED:
                    print("[ - ] Deleted %s" % full_filename)
                elif action == FILE_MODIFIED:
                    print("[ * ] Modified %s" % full_filename)

                    if os.path.isfile(full_filename) and not no_dump:  # dump out the file contents
                        print("[vvv] Dumping contents...")

                        try:
                            fd = open(full_filename, "rb")
                            contents = fd.read()
                            fd.close()

                            encoding = chardet.detect(contents)['encoding']
                            contents = contents.decode(encoding, errors='ignore')

                            print(contents)
                            print("[^^^] Dump complete.")
                        except:
                            print("[!!!] Failed.")

                elif action == FILE_RENAMED_FROM:
                    print("[ > ] Renamed from: %s" % full_filename)
                elif action == FILE_RENAMED_TO:
                    print("[ < ] Renamed to: %s" % full_filename)
                else:
                    print("[???] Unknown: %s" % full_filename)
        except:
            pass


def monitor_loop(dirs_to_monitor=dirs_to_monitor, no_dump=False):
    if iswin():
        start_monitor = start_monitor_win
    else:
        raise NotImplementedError

    for path in dirs_to_monitor:
        monitor_thread = threading.Thread(target=start_monitor, args=(path, no_dump), daemon=True)
        print("Spawning monitoring thread for path: %s" % os.path.abspath(path))
        monitor_thread.start()

    def handler_kill(signum, frame):
        raise SystemExit

    signal.signal(signal.SIGINT, handler_kill)
    while True:  # for main thread can catch signal
        pass


def cli():
    arguments = docopt(__doc__, version=__version__)
    if arguments['<watch-path>'] is not None:
        monitor_loop(arguments['<watch-path>'], arguments['--no-dump'])
    else:
        monitor_loop(arguments['--no-dump'])


if __name__ == '__main__':
    cli()
