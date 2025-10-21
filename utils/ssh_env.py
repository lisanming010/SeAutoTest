import paramiko
import re, os, hashlib, sys
from pathlib import Path

class sshToEnv:
    '''
    ssh连接操作类
    
    :hostname : 远程连接名
    :username : 登录名，默认为root
    :passwd : 登录密码
    :port : 登录端口，默认为22
    '''
    def __init__(self, hostname, passwd, username='root',port=22):
        self.hostname = hostname
        self.username =username
        self.passwd = passwd
        self.port = port
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def _close_ssh(func):
        '''
        ssh连接回收装饰器
        '''
        def wrapper(*args, **kwarges):
            try:
                return func(*args, **kwarges)
            except Exception as e:
                raise e
            finally:
                if kwarges.get('close_ssh', True):
                    args[0].ssh.close()
                    print(f'{func.__qualname__}方法调用ssh链接关闭,func params:{args}')
                else:
                    pass
        return wrapper

    def ssh_client(slef) -> paramiko:
        '''
        ssh连接方法
        '''
        slef.ssh.connect(slef.hostname, slef.port, slef.username, slef.passwd)

    @_close_ssh
    def exec_cmd(self, cmd:str, ssh_client:paramiko='', get_pty=False, close_ssh=True) -> tuple:
        '''
        ssh自定义命令执行方法

        :cmd: 自定义命令
        :ssh_clinet: paramiko实例对象，决定是否复用外部connect
        :get_pty: 是否需要pty，一般执行sudo命令时需要，默认为false
        :close_ssh: 是否自动关闭ssh连接，默认为Ture，自动关闭 

        -> (stdout, stderr)
        '''
        if ssh_client == '':
            self.ssh_client()
        print(f'exec cmd: {cmd}')
        _, stdout, stderr = self.ssh.exec_command(cmd, get_pty=get_pty)
        return stdout.read().decode(), stderr.read().decode()
    
    @staticmethod
    def local_md5sum(file_full_path, bufsize=8192) -> dict:
        '''
        计算MD5，若传递值为文件则直接计算文件md5,若为文件夹则递归计算文件夹下所有文件md5

        :file_full_path: 路径
        '''
        print(f'------------------{file_full_path} md5sum start-----------------------')
        root = Path(file_full_path)
        if not root.exists():
            raise FileNotFoundError(root)

        def _walk(current: Path, base: Path):
            try:
                for p in sorted(current.iterdir()):
                    rel = str(p)
                    if p.is_file():
                        h = hashlib.md5()
                        with p.open('rb') as f:
                            for chunk in iter(lambda: f.read(bufsize), b''):
                                h.update(chunk)
                        yield rel, h.hexdigest()
                    elif p.is_dir():
                        yield from _walk(p, base)
            except NotADirectoryError as e: #捕获到目录名称无效，但已有文件存在校验所以进入次逻辑可能是因为传递的是文件名而非一个路径
                h = hashlib.md5()
                with current.open('rb') as f:
                    for chunk in iter(lambda: f.read(bufsize), b''):
                        h.update(chunk)
                yield str(current), h.hexdigest()
        print(f'------------------{file_full_path} md5sum end-----------------------')
        return dict(_walk(root, root))

    @_close_ssh
    def _md5_check(self, local_file_full_path, remote_file_path, ssh_client:paramiko='', close_ssh=True) -> tuple:
        """
        文件md5校验

        :local_file_full_path: 本地文件路径
        :remote_file_path: 远程文件路径
        :close_ssh: 调用结束后是否需要自动关闭ssh连接
        -> (run_code, 本地文件md5, 远程文件md5)
        """
        run_code = True
        local_file_md5 = self.local_md5sum(local_file_full_path)
        remote_file_md5, stderr = self.exec_cmd(f'md5sum {remote_file_path}', ssh_client=ssh_client, close_ssh=close_ssh)

        if stderr != '':
            print(stderr)
            sys.exit()
        if local_file_md5[local_file_full_path] in remote_file_md5:
            pass
        else:
            run_code = False
        return run_code, local_file_md5, remote_file_md5

    def close_ssh(self):
        """
        手动关闭连接
        """
        self.ssh.close()

    @_close_ssh
    def sftp_file(self, local_file_path, remote_file_path, 
                  local_file_name, remote_file_name, ssh_client:paramiko='', flow_direction='upload', close_ssh=True):
        '''
        sftp文件上传/下载方法

        :local_file_path: 本地文件路径
        :remote_file_path: 远程文件路径
        :close_ssh: 是否自动关闭ssh连接，默认为Ture，自动关闭 
        '''
        print(f'{local_file_name} {flow_direction} start!')
        if ssh_client == '':
            self.ssh_client()

        local_file_full_path = Path(local_file_path).joinpath(local_file_name)
        remote_file_full_path = remote_file_path + '/' + remote_file_name
        
        if flow_direction == 'upload':
            if not local_file_full_path.exists():
                raise FileExistsError(f'{local_file_full_path}不存在')
        elif flow_direction == 'download':
            if not Path(local_file_path).exists():
                raise FileExistsError(f'{local_file_full_path}不存在')

        with self.ssh.open_sftp() as sftp:
            if flow_direction == 'upload':
                sftp.put(local_file_full_path, remote_file_full_path)
            elif flow_direction == 'download':
                sftp.get(remote_file_full_path, local_file_full_path)
            
            md5_check_result, local_file_md5, remote_file_md5 = self._md5_check(str(local_file_full_path), remote_file_full_path, 
                                                                                self.ssh, close_ssh=False)
            if md5_check_result:
                print(f'{remote_file_full_path} {flow_direction}成功！\n本地文件MD5:{local_file_md5}\n远程文件MD5:{remote_file_md5}')
            else:
                print(f'{remote_file_full_path} {flow_direction}失败！\n本地文件MD5:{local_file_md5}\n远程文件MD5:{remote_file_md5}')
                raise RuntimeError(f'{remote_file_full_path} {flow_direction}失败！\n本地文件MD5:{local_file_md5}\n远程文件MD5:{remote_file_md5}')