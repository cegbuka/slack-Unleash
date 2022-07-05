from setup import Setup
from connector.connector import sshconnection
from multiprocessing.pool import ThreadPool
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

# instantiate
config = ConfigParser(allow_no_value=True)

# parse existing file



servers = []

def testing_connection(server):
    print ("Establishing a connection to  %s" %server["ssh_host"])
    try:
        ssh = sshconnection(username=server["ssh_user"], password=server["ssh_pass"], serverip=server["ssh_host"], port=server["ssh_port"])
        ssh.connect()
        ssh.close()
        print ("\n\nConnected to  %s" %server["ssh_host"])
        return server
    except Exception as e:
        print("Connection lost : %s "%e)


if __name__ == "__main__":
    config.read('hosts')
    
    config.sections()
    for item in config.sections():
        if item != 'DEFAULT':
            servers.append({ "name": item, "ssh_user" : config.get(item, 'ssh_user'), "ssh_pass" : config.get(item, 'ssh_pass'), "ssh_host" : config.get(item, 'ssh_host'), "ssh_port" : int(config.get(item, 'ssh_port'))})

    # if servers:
    print (f"TESTING SERVER CONNECTION ------------------------")
    #     for server in servers:
    #         testing_connection(server)
    pool = ThreadPool(len(servers))       
    result = pool.map(testing_connection, servers)

    for content in result:
        
        if  content:
            sd = Setup(username=content['ssh_user'], password=content['ssh_pass'], port=content['ssh_port'], serverip=content['ssh_host'])
            
            playbook = sd.read_yaml()
            for tasks in playbook:
                if tasks['tasks']:
                    sd.installation(content, task=tasks['tasks'])
            #print(sd.read_yaml())