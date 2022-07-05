import logging

class Task():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        #self.logger.disabled = True

    def checker(self, tasks) -> list:
        commands = []
        title = []
        for task in tasks:
                
            if  'apt' in task.keys() and 'name' in task['apt'].keys():
                self.logger.info("Package Manager is apt")
                if 'state' in task['apt'].keys() and task['apt']['state'] == 'latest':
                    package = f'apt upgrade -y %s' % task['apt']['name']
                elif 'state' in task['apt'].keys() and task['apt']['state'] == 'remove':
                    package = f'apt remove -y %s' % task['apt']['name']
                elif 'state' in task['apt'].keys() and task['apt']['state'] == 'install':
                    package = f'apt-get -y %s' % task['apt']['name']
                title.append(task['name'])
                commands.append(package) 
            
            if  'apt' in task.keys() and 'autoremove' in task['apt'].keys():
                if task['apt']['autoremove'] == True:
                    package = f'apt autoremove -y'
                title.append(task['name'])
                commands.append(package)

            if  'service' in task.keys() and 'name' in task['service'].keys():
                response = self.service(task)
                title.append(task['name'])
                commands.append(response)
            
            if  'symlink' in task.keys() and 'src' in task['symlink'].keys() and 'dest' in task['symlink'].keys():
                response = self.symlink(task)
                title.append(task['name'])
                commands.append(response)
            
            if  'copy' in task.keys() and 'src' in task['copy'].keys() and 'dest' in task['copy'].keys():
                response = self.copy(task)
                title.append(task['name'])
                commands.append(response)
            
            if  'write' in task.keys() and 'file' in task['write'].keys() and 'content' in task['write'].keys():
                response = self.write(task)
                title.append(task['name'])
                commands.append(response)

            if 'file' in task.keys() and 'remove' in task['file'].keys():
                package = f"[ -f {task['file']['remove']} ] && (rm -f {task['file']['remove']}; echo 'removed') || echo 'not-present'"
                title.append(task['name'])
                commands.append(package)

        return commands, title
    
    def write(self, task) -> dict:
        command = { "write" : {}}
        command['write']['file'] = task['write']['file']
        command['write']['owner'] = task['write']['owner']
        command['write']['group'] = task['write']['group']
        command['write']['perms'] = task['write']['perm']
        command['write']['content'] = task['write']['content']

        return command

    def service(self, task) -> str:
        command = ''
        if 'state' in task['service'].keys() and task['service']['state'] == 'started':
            command = f'systemctl start %s' % task['service']['name'] + f' && systemctl status %s ' % task['service']['name'] + "| grep Active"
        elif 'state' in task['service'].keys() and task['service']['state'] == 'stop':
            command = f'systemctl stop %s' % task['service']['name'] + f' && systemctl status %s ' % task['service']['name'] + "| grep Active"
        elif 'state' in task['service'].keys() and task['service']['state'] == 'restart':
            command = f'systemctl restart %s' % task['service']['name'] + f' && systemctl status %s ' % task['service']['name'] + "| grep Active"
        
        return command
    
    def symlink(self, task) -> str:
        link = 'ln -s '+task['symlink']['src']+ " "+task['symlink']['dest']
        command = f"[ -L {task['symlink']['dest']} ] && [ -e {task['symlink']['dest']} ] && echo 'alreadylink' || ({link}; echo 'linked')"
        return command

    
    def copy(self, task) -> dict:
        command = { "copy" : {}}
        command['copy']['src'] = task['copy']['src']
        command['copy']['dest'] = task['copy']['dest']
        command['copy']['owner'] = task['copy']['owner']
        command['copy']['group'] = task['copy']['group']
        command['copy']['perms'] = task['copy']['perms']
        # elif 'copy' in task.keys() and 'src' in task['copy'].keys() and 'dest' in task['copy'].keys():
        return command

            
    def remove_file(self, tasks) -> list:
        commands = []
        for task in tasks:
            if 'file' in task.keys() and 'remove' in task['file'].keys():
                package = f'rm -f %s' % task['file']['remove']
                commands.append(package)
        return commands
            

