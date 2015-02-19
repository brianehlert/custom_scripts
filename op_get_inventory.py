import sys
sys.path.insert(0, '/var/opt/citrix/sdxtools/install/scripts/lin/python')

import utils
import json
import subprocess
import glob


def op_do_get_inventory():

        utils.process_request()

        blu_packages = []
        # node_packages = []
        blu_configurations = []

        for name in glob.glob('/opt/blu/*/package.json'):
            blu_packages.append(name)

        blu_services = []
        for blu in blu_packages:
            json_data = open(blu)
            data = json.load(json_data)
            blu_services.append(json.dumps(data["name"]) + " : " + json.dumps(data["version"]))

        # for name in glob.glob('/opt/blu/*/node_modules/*/package.json'):
        #     node_packages.append(name)
        #
        # node_versions = []
        # for node in node_packages:
        #     json_data = open(node)
        #     data = json.load(json_data)
        #     node_versions.append(json.dumps(data["name"]) + " : " + json.dumps(data["version"]))

        for name in glob.glob('/opt/blu/*/config.js'):
            blu_configurations.append(name)

        blu_config = []
        for blu in blu_configurations:
            lines = [line.strip() for line in open(blu, 'r')]
            blu_config.append(lines)

        proc = subprocess.Popen(['mongod --version'], stdout=subprocess.PIPE, shell=True)
        mongo_version = (proc.communicate()[0]).split('\n')[0]

        proc = subprocess.Popen(['redis-server --version'], stdout=subprocess.PIPE, shell=True)
        redis_version = (proc.communicate()[0]).split(' ')

        utils.responseparams["blu services"] = blu_services
        utils.responseparams["blu configurations"] = blu_config
        utils.responseparams["MongoDB version"] = mongo_version
        utils.responseparams["Redis version"] = (redis_version[0] + ' ' + redis_version[1] + ' ' + redis_version[2])
        utils.responseparams["node module versions"] = node_versions
        utils.process_response("op_get_inventory", 0, "Done")

if __name__ == '__main__':
    op_do_get_inventory()

