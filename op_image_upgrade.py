import sys
sys.path.insert(0,'/var/opt/citrix/sdxtools/install/scripts/lin/python')

import utils
import subprocess
import os
import shutil

def op_do_image_upgrade():

    utils.process_request()
    # upgrade_filename = str(utils.requestparams['filename'])
    upgrade_filename = 'meshblu-server-1.1.1.tgz'
    image_file = '/var/opt/citrix/sdxtools/install/software_files/images/' + upgrade_filename
    config_file = '/opt/blu/meshblu/config.js'

    os.system('chmod +x ' + image_file)

    # copy the current config file
    shutil.copy(config_file, '/var/opt/citrix/sdxtools/install/software_files/config/meshblu_conf.js')

    # stop the meshblu service
    proc = subprocess.Popen(['service meshblu status'], stdout=subprocess.PIPE, shell=True)
    mb_status = proc.communicate()[0]

    if mb_status.find("running") is True:
        proc = subprocess.Popen(['service meshblu stop'], stdout=subprocess.PIPE, shell=True)
        proc.communicate()[0]

    # install the update
    update_log = open('/opt/blu/log/meshblu_update.log', 'w+')

    proc = subprocess.Popen(['npm install ' + image_file + ' --production'], cwd='/opt/blu/meshblu', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    for line in proc.stdout:
        sys.stdout.write(line)
        update_log.write(line)

    proc.wait()

    # copy the config back
    if os.path.exists(config_file):
        os.remove(config_file)
    shutil.copy('/var/opt/citrix/sdxtools/install/software_files/config/meshblu_conf.js', config_file)

    rc = proc.returncode

    if rc == 0:
        utils.process_response("op_image_upgrade", 0, "reboot")
    else:
        utils.process_response("op_image_upgrade", rc, "Cannot upgrade the instance")


if __name__ == '__main__':
        op_do_image_upgrade()

