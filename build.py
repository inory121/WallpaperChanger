import os
import subprocess
from pathlib import Path
import nicegui

cmd = ['PyInstaller',
       'nicegui_win.py',
       '--name', 'WallpaperChanger',
       '--onefile',
       '--clean',
       '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui'
       ]
subprocess.call(cmd)
