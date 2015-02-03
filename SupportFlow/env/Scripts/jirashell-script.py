#!"C:\Users\mwillis\Documents\Visual Studio 2013\Projects\SupportFlow\SupportFlow\env\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'jira==0.32','console_scripts','jirashell'
__requires__ = 'jira==0.32'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('jira==0.32', 'console_scripts', 'jirashell')()
    )
