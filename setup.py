import os
import logging
from connector.connector import sshconnection
import yaml
from task.task import Task
from termcolor import colored


logger = logging.getLogger(__name__)
class Setup():
    def __init__(self, username:str, password:str, serverip:str, port:int=22):
        #self.command = 'sudo apt-get -y'
        self.username=username, 
        self.password=password, 
        self.serverip=serverip
        self.port=port

    def read_yaml(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(current_dir, 'task.yaml')
        with open(filename, "r") as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as exc:
                return None
        

    def installation(self, content, task):
        runner = Task()
        # check if there are prograns to install
        ssh = sshconnection(username=content['ssh_user'], password=content['ssh_pass'], serverip=content['ssh_host'], port=content['ssh_port'])
        ssh.connect()
        commands, title = runner.checker(task)
        
        ##commands = runner.remove_file(task)
        for index, command in enumerate(commands):
            #print("your command", command)
            #output, err = ssh.execute_command(command=command)
            print("TASK  ",title[index],"..................................................................................")
            if 'copy' in commands[index]:
                destination=command['copy']['dest']
                #dest = destination.split("/")
                src = os.path.join(os.getcwd(), command['copy']['src'])
                output, err = ssh.execute_command(f"[ -f {destination} ] && echo 'present' || echo 'not-present'")
                if err:
                    failed = colored('failed=1', 'red')
                else:
                    failed = 'failed=0'
                if output:
                    if "present\n" ==''.join(output):
                        changed = 'changed=0'
                    elif "not-present\n" == ''.join(output):
                        changed = colored('changed=1', 'yellow')

                if 'owner' in command['copy'].keys() and 'group' in command['copy'].keys():
                    stdout, err = ssh.execute_command("getent passwd " + command['copy']['owner'])
                    user_id = stdout[0].split(":")[2]
                    stdout, err = ssh.execute_command("getent group " + command['copy']['group'])
                    group_id = stdout[0].split(":")[2]
                    ssh.sftp(destination=destination, src=src, user_id=user_id, group_id=group_id)
                else:
                    ssh.sftp(destination=destination, src=src)

                
                if 'perms' in command['copy'].keys():
                    dest =f"chmod {command['copy']['perms']} " + destination
                    output, err = ssh.execute_command(dest)
                    
                    logger.info(err)
                print(f"{content['ssh_host']}        ",colored(':ok=0', 'green'),"      ",changed,"       ",failed,"\n\n")
                

                
            elif 'write' in commands[index]:
                file = command['write']['file']
                content = command['write']['content'].replace('"','\"')
                outp, error = ssh.execute_command(command=f"cat {file}")
                output, err = ssh.execute_command(f"echo -e '{content}' > {file}")
                
                if "No such file" in ''.join(error):
                    if err:
                        print(f"{content['ssh_host']}        ",colored(':ok=0', 'green'),"       changed=0       ",colored('failed=1', 'red'),"\n\n")
                    else:
                        print(f"{content['ssh_host']}       ",colored(':ok=0', 'green'),"       ",colored('changed=1', 'yellow'),"      ",colored('failed=1', 'red'),"\n\n")
                elif outp:
                    outp.pop()
                    if len(''.join(outp)) == len(content):
                        print(f"{content['ssh_host']}         ",colored(':ok=0', 'green'),"       changed=0       failed=0\n\n")
                    else:
                        print(f"{content['ssh_host']}         ",colored(':ok=0', 'green'),"       ",colored('changed=1', 'yellow'),"      failed=0\n\n")
                else:
                    print(f"{content['ssh_host']}         ",colored(':ok=0', 'green'),"       changed=0      failed=0\n\n")
                        
            else:
                output, err = ssh.execute_command(command=command)
                if err:
                    #print(err)
                    if 'apt' in command and 'WARNING:' in ''.join(err).strip("\n"):
                        failed = 'failed=0'
                    else:
                        failed = colored('failed=1', 'red')
                else:
                    failed = 'failed=0'
                
                if output:
                    samp = output[len(output) - 1]
                    # if '0 upgraded' in samp  and '0 newly installed' in samp:
                    #     print(f"1246757757        ",colored(':ok=0', 'green'),"       changed=0       ",failed,"\n\n")
                    if "present\n" == ''.join(output):
                        print(f"{content['ssh_host']}         :ok=0        changed=0       ",failed,"\n\n")
                    elif "not-present\n" == ''.join(output):
                        print(f"{content['ssh_host']}         ",colored(':ok=0', 'green'),"       ",colored('changed=1', 'yellow'),"      ",failed,"\n\n")
                    elif 'linked' in ''.join(output):
                        if "File exists" in ''.join(err):
                            print(f"{content['ssh_host']}        ",colored(':ok=0', 'green'),"       changed=0       ",failed,"\n\n")
                        else:
                            print(f"{content['ssh_host']}         :ok=0       ",colored('changed=1', 'yellow'),"      ",failed,"\n\n")
                    elif 'alreadylink' in ''.join(output):
                        print(f"{content['ssh_host']}        ",colored(':ok=0', 'green'),"       changed=0       ",failed,"\n\n")
                    elif 'systemctl start' in command:
                        if '(running)' in ''.join(output):
                            print(f"{content['ssh_host']}         ",colored(':ok=0', 'green'),"       ",colored('changed=1', 'yellow'),"      ",failed,"\n\n")
                        elif '(dead)' in ''.join(output):
                            print(f"{content['ssh_host']}        ",colored(':ok=0', 'green'),"       changed=0       ",colored('failed=1', 'red'),"\n\n")
                    elif 'systemctl stop' in command:
                        if '(dead)' in ''.join(output):
                            print(f"{content['ssh_host']}         ",colored(':ok=0', 'green'),"       ",colored('changed=1', 'yellow'),"      ",failed,"\n\n")
                        else:
                            print(f"{content['ssh_host']}        ",colored(':ok=0', 'green'),"       changed=0       ",colored('failed=1', 'red'),"\n\n")
                    elif 'remove' in command and 'Removing' in ''.join(output) :
                        changes = 0
                        for item in output:
                            if item.startswith('Removing'):
                                changes = changes+1
                        if changes != 0:
                            print(f"{content['ssh_host']}         ",colored(':ok=0', 'green'),"       ",colored(f'changed={changes}', 'yellow'),"      ",failed,"\n\n")
                        else:
                            print(f"{content['ssh_host']}        ",colored(':ok=0', 'green'),"       changed=0       ",failed,"\n\n")

                    elif 'upgrade' in command or 'install' in command:
                        changes = 0
                        for command in command.split():
                            if '-y' != command and 'install' != command and 'upgrade' != command and 'apt' != command and 'apt-get' != command:
                                if f"Setting up {command}" in ''.join(output):
                                    changes = changes+1
                        if changes != 0:
                            print(f"{content['ssh_host']}         ",colored(':ok=0', 'green'),"       ",colored(f'changed={changes}', 'yellow'),"      ",failed,"\n\n")
                        else:
                            print(f"{content['ssh_host']}        ",colored(':ok=0', 'green'),"       changed=0       ",failed,"\n\n")

                    else:
                        print(f"{content['ssh_host']}        ",colored(':ok=0', 'green'),"       changed=0       ",failed,"\n\n")
                


                #print(command['copy']['src'])
                #print(command['copy']['dest'])
                #print("output", ''.join(output))
                #print('\n\n\nerror', ''.join(err))
        # check if there are programs to
       

        
       # print(commands)




