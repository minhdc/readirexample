import os 
from cx_Freeze import setup, Executable

base = None
executables = [Executable("do_classification.py", base=base),Executable("get_excel_report.py", base=base)]
includefiles = ['setttings.py']
packages = ["idna","os","win32file","win32con","setttings","utils","traceback","sys","xlsxwriter","datetime","pandas","pathlib","csvhandle","displayutils","numpy","time","logging"]
options = {
    'build_exe': {
        'packages':packages,
        'include_files':includefiles,        
    },
    
}

os.environ['TCL_LIBRARY'] = r'C:\Users\Ladygaga\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Ladygaga\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

setup(
    name = "email_classification",
    options = options,
    version = "0.6",
    description = 'updated with report generator',
    executables = executables
)