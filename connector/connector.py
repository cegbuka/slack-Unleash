import os
import logging
import paramiko


class sshconnection():
    def __init__(self, username, password, serverip, port):
        self.user = username
        self.password = password
        self.port = port
        self.server_ip = serverip
        self.connection = paramiko.SSHClient()
        self.logger = logging.getLogger(__name__)
        self.logger.propagate = False

    def connect(self):
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connection.connect(hostname=self.server_ip, port=self.port, username=self.user, password=self.password)
        #print("***** Connected to Server ********")
    
    def execute_command(self, command):
        stdin, stdout, stderr = self.connection.exec_command(command)
        output = stdout.readlines()
        error = stderr.readlines()
        return output, error

    def sftp(self, destination, src, user_id=None, group_id=None):
        sftp=self.connection.open_sftp()
        #output, err = sftp.put(src, os.path.join(destination, filename))
        output = sftp.put(os.path.join(os.getcwd(), '/'+src), destination)
        #sftp.chown(dest,int(uid),int(gid))
        if user_id != None and group_id != None:
            output = self.chown(sftp=sftp, user_id=user_id, group_id=group_id, destination=destination)
        
        sftp.close()

    
    # def test_connection(self, server:dict):
    #     #self.connection.connect(hostname=server['ssh_pass'], port=server['ssh_port'], username=server['ssh_user'], password=server['ssh_password'])
    #     self.connection.connect(hostname=server['ssh_host'], port=server['ssh_port'], username=server['ssh_user'], password=server['ssh_password'])
    #     print(f"Connected to {server['name']}")


    def chown(self, sftp, user_id, group_id, destination) -> any:
        output = sftp.chown(destination, int(user_id), int(group_id))
        return output

    def close(self):
        if self.connection is not None: 
            self.connection.close()


# if __name__ == "__main__":
#     ssh = sshconnection(username='jerry', password='8iu7*IU&', serverip='63.35.224.83')
#     ssh.connect()
#     ssh.sftp()
#     exec, err = ssh.execute_command("ls -l /tmp")
#     print(''.join(exec))
#     print(''.join(err))
    
  
#     ssh.close()


