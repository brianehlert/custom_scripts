import sys
sys.path.insert(0, '/var/opt/citrix/sdxtools/install/scripts/lin/python')

import subprocess
import utils
import psutil

# Need to get cpu and memory utilization for this VM
# use psutil as it is built-in to Python
# Be sure that it is added to the image  sudo apt-get install python-psutil  or  python3-psutil


def op_get_stat_main():
    
    utils.process_request()    

    total_memory = (int(psutil.phymem_usage().total)/1024)/1024

    used_memory = (int(psutil.phymem_usage().used)/1024)/1024
    
    free_memory = (int(psutil.phymem_usage().free)/1024)/1024
    
    memory_utilisation = float(psutil.phymem_usage().percent)
    
    cpu_utilisation = psutil.cpu_percent(2.0, True)
    # this needs to sample a bit or it returns 0.0
       
    node_stat = "off"
    mongo_stat = "off"
    redis_stat = "off"
    mb_stat = "off"
            
    for proc in psutil.process_iter():
        if proc.name() == "nodejs":
            if proc.is_running() is True:
                node_stat = "on"
        elif proc.name() == "mongod":
            if proc.is_running() is True:
                mongo_stat = "on"
        elif proc.name() == "redis_server":
            if proc.is_running() is True:
                redis_stat = "on"

    proc = subprocess.Popen(['service meshblu status'], stdout=subprocess.PIPE, shell=True)
    mb_status = proc.communicate()[0]
    
    if mb_status.find("running") is True:
        mb_stat = "on"

    # meshblu configuration needs to be returned.  UUID, token, parent URI, UUID, token, other useful things from config

    utils.responseparams["vm_memory_total_mb"] = int(total_memory)
    utils.responseparams["vm_memory_free_mb"] = int(free_memory)
    utils.responseparams["vm_memory_used_mb"] = int(used_memory)
    utils.responseparams["vm_memory_utilization_percent"] = float(memory_utilisation)
    utils.responseparams["vm_cpu_usage"] = str(cpu_utilisation)
    utils.responseparams["meshblu_status"] = mb_stat
    utils.responseparams["mongodb_status"] = mongo_stat
    utils.responseparams["redis_status"] = redis_stat
    utils.responseparams["node_status"] = node_stat
    utils.process_response("op_get_stat", 0, "Done")

if __name__ == '__main__':
        op_get_stat_main()
