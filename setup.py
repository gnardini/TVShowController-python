from cx_Freeze import setup, Executable

base = None

executables = [Executable("controller.py", base=base)]

setup(
    name = "TV Show Controller",
    options = {
        'build_exe': {
            'packages': ['flask', 'json', 'os', 'win32com', 'socket']
        }
    },
    version = "0.1",
    description = 'Control computer from your mobile phone',
    executables = executables
)