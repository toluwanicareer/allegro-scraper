from cx_Freeze import setup, Executable

base = None

executables = [Executable("fe.py", base=base)]

packages = ["idna","core","webbrowser","tkinter", "csv","requests","pandas", "numpy","time"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "allegro_search",
    options = options,
    version = "1",
    description = 'something here',
    executables = executables
)