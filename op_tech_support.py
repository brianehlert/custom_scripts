import sys
sys.path.insert(0,'/var/opt/citrix/sdxtools/install/scripts/lin/python')

import utils
import os

def op_do_tech_support():

    utils.process_request()
    sdxtools_file = '/var/opt/citrix/sdxtools/install/software_files/tech_support/'
    blu_logs = '/opt/blu/log/'
    errorcode = 0
    errormessage = 'Done'
    filename = 'blu_support.tar.gz'

    if os.path.exists(blu_logs) is True:
        # os.system('cp -f ' + blu_logs + ' ' + sdxtools_file)
        self_path = os.getcwd()
        os.chdir(blu_logs)

        os.system('tar -cvzf ' + (sdxtools_file + filename) + ' ' + blu_logs + '*.* --remove-files')

        os.chdir(self_path)
    else:
        errorcode = 1
        errormessage = 'TechSupport file not found'

    utils.responseparams["filename"] = filename
    utils.process_response("op_tech_support", errorcode, errormessage)


if __name__ == '__main__':
        op_do_tech_support()

