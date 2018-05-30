import os
import win32file
import win32con

import setttings

from utils import do_the_classification_job_for_single_eml_file

ACTIONS = {
    1 : "Created",
    2 : "Deleted",
    3 : "Updated",
    4 : "Renamed from something",
    5 : "Renamed to something",
}

FILE_LIST_DIRECTORY = 0x0001

path_to_watch = setttings.SRC_DIR

hDir = win32file.CreateFile(
    path_to_watch,
    FILE_LIST_DIRECTORY,
    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
    None,
    win32con.OPEN_EXISTING,
    win32con.FILE_FLAG_BACKUP_SEMANTICS,
    None
)
try:
    while 1:

        results = win32file.ReadDirectoryChangesW(
            hDir,
            1024000,
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
        
        for action, each_file in results:
            full_filename = os.path.join(path_to_watch,each_file)
            print(full_filename,ACTIONS.get(action,"Unknown"))  
            if ACTIONS.get(action,"Unknown") == 'Created' or ACTIONS.get(action,"Unknown") == 'Updated':
                do_the_classification_job_for_single_eml_file(os.path.join(path_to_watch,each_file))
except Exception as e:
    print(e)            
    input()