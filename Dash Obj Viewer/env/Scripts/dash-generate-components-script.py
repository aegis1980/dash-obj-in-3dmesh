#!"C:\Users\rob59265\source\repos\Dash Obj Viewer\Dash Obj Viewer\env\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'dash==1.5.1','console_scripts','dash-generate-components'
__requires__ = 'dash==1.5.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('dash==1.5.1', 'console_scripts', 'dash-generate-components')()
    )
