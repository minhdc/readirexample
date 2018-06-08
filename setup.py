from cx_Freeze import setup, Executable

base = None
executables = [Executable("readirchangexample.py", base=base)]
includefiles = ['setttings.py']
packages = ["idna","os","win32file","win32con","setttings","utils","traceback","sys"]
options = {
    'build_exe': {
        'packages':packages,
        'include_files':includefiles,
    },
    
}

setup(
    name = "readirnew",
    options = options,
    version = "0.1",
    description = 'shit',
    executables = executables
)