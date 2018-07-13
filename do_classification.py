import os
import sys
import win32file
import win32con
import traceback
import setttings
import logging

from utils import do_the_classification_job_for_single_eml_file,get_target_list_from_folder
from displayutils import printProgressBar

logging.basicConfig(filename='do_classification.log',level=logging.INFO)
print("inited logger")
try:

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

    while 1:
        target_list = get_target_list_from_folder(setttings.LIST_OF_TARGET)
        results = win32file.ReadDirectoryChangesW(
            hDir,
            102400000,
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
        
        #eml_counts = 0
        #try:
        completed = len(results)
        #except ZeroDivisionError:

        index = 0
        printProgressBar(index,completed,prefix="Tiến độ:",length=50)
        for action, each_file in results:
            full_filename = os.path.join(path_to_watch,each_file)             
            if "eml" in each_file and os.path.isfile(full_filename):
                if ACTIONS.get(action,"Unknown") == 'Created' or ACTIONS.get(action,"Unknown") == 'Updated':
                    do_the_classification_job_for_single_eml_file(os.path.join(path_to_watch,each_file),target_list)       
            else:
                print("The followin isnt an eml file:",full_filename,ACTIONS.get(action,"Unknown")) 
            index += 1
            printProgressBar(index,completed,prefix="Tiến độ:",length=50)
            
        print(r"---------------------------------------------------------------")
        print(r"  _____ ____  __  __ _____  _      ______ _______ ______ _____")
        print(r"/ ____// __ \|  \/  |  __ \| |    |  ____|__   __|  ____|  __\\")
        print(r"| |   | |  | | \  / | |__) | |    | |__     | |  | |__  | |  | |")
        print(r"| |   | |  | | |\/| |  ___/| |    |  __|    | |  |  __| | |  | |")
        print(r"| |___| |__| | |  | | |    | |____| |____   | |  | |____| |__| |")
        print(r" \_____\____/|_|  |_|_|    |______|______|  |_|  |______|_____/ ")
        print(r"---------------------------------------------------------------")     
        #print("\n\nNhấn phím bất kỳ để thoát...\n\n")
        #input()
         
        #print("received %r eml file(s)"%(eml_counts))
except Exception as e:
    print(e)            
    traceback.print_exc(file=sys.stdout)
    logging.error('[ERROR] '+str(e))
    logging.traceback.print_stack()
    #input()