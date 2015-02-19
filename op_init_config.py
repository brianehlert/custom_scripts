import sys
sys.path.insert(0,'/var/opt/citrix/sdxtools/install/scripts/lin/python')

import utils
import os
import subprocess
def op_init_config():

# not specialized to Meshblu

    utils.process_request()

    DSS_ADDR = str(utils.requestparams['dss_addr'])
    DSS_ADMIN = str(utils.requestparams['dss_admin'])
    DSS_PASSWD = str(utils.requestparams['dss_passwd'])

    config_file = "/tmp/test_securecomm.conf"
    file_write = open(config_file, 'w')
        
    file_write.write("DSS_ADDR="  + DSS_ADDR + "\n")
        file_write.write("DSS_ADMIN="  + DSS_ADMIN + "\n")
        file_write.write("DSS_PASSWD="  + DSS_PASSWD + "\n")

    if 'root_passwd' in utils.requestparams:
        ROOT_PASSWD= str(utils.requestparams['root_passwd'])
        file_write.write("ROOT_PASSWD="  + ROOT_PASSWD + "\n")
    if 'admin_passwd' in utils.requestparams:
        ADMIN_PASSWD= str(utils.requestparams['admin_passwd'])
        file_write.write("ADMIN_PASSWD="  + ADMIN_PASSWD + "\n")
    if 'time_zone' in utils.requestparams:
        tz= str(utils.requestparams['time_zone'])
        if tz != "UTC":
            tz= tz.split()[2].replace("\\","")
        file_write.write("TZ="  + tz + "\n")

    file_write.close()

    self_path = os.getcwd()
        os.chdir("/opt/websense/neti/bin/")	
    proc = subprocess.Popen(['./pamaConfigurator-citrix -f ' + config_file + ' -m sdxsecurecomm'], stderr = subprocess.PIPE, shell = True)
        proc.communicate()
        exit_code_dss = proc.returncode
        os.chdir(self_path)	

    os.system('rm -rf ' + config_file);

    if exit_code_dss == 0:
        utils.process_response("op_init_config", 0, "Done")
    else:
        utils.process_response("op_init_config", exit_code_dss, "setting pama & pe failed")


if __name__ == '__main__':
        op_init_config()
