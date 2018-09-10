import paramiko
import argparse
import sys

def LTP_parse(content):

    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())#第一次登录的认证信息
    # 连接服务器
    ssh.connect(hostname='210.72.13.22', port=22, username='root', password='!r@o#o$t@olm.com.cn')
    # 执行命令
    cmd = 'curl -d "s='+content+'&f=xml&t=all" http://127.0.0.1:12306/ltp'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # 获取命令结果
    res,err = stdout.read(),stderr.read()
    result = res if res else err
    print(result.decode())
    # 关闭连接
    ssh.close()

def LTP_parse_file(args):
    content = ""
    for line in args.file:
        content += line.strip()
    LTP_parse(content)

def LTP_parse_content(args):
    content = args.content
    LTP_parse(content)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='LTP 工具， 制作者David_狄')

    parser.add_argument('-c', '--content', help="content to analyze by LTP")
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), help="Path to file")

    ARGS = parser.parse_args()
    # print(ARGS)
    if ARGS.file is None and ARGS.content is not None:
        LTP_parse_content(ARGS)
    elif ARGS.file is not None and ARGS.content is None:
        LTP_parse_file(ARGS)
    else:
        parser.print_help()
        sys.exit(1)