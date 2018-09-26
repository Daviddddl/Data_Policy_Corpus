import paramiko
import argparse
import sys, re
import subprocess
import xml.etree.ElementTree as ET


def LTP_parse(content):
    # 开启远程服务
    # sudo docker run -d -p 12306:12345 ltp/ltp /ltp_server --last-stage all
    # 创建SSH对象
    # ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 第一次登录的认证信息
    # 连接服务器
    # ssh.connect(hostname='54.169.197.230', port=22, username='david', password='123@nus')
    # 执行命令
    cmd = 'curl -d "s=' + content + '&f=xml&t=all" http://127.0.0.1:12306/ltp'
    # print(cmd)
    # stdin, stdout, stderr = ssh.exec_command(cmd)
    # 获取命令结果
    # res, err = stdout.read(), stderr.read()
    # result = res if res else err
    # print(result.decode())
    # 关闭连接
    # ssh.close()

    # return result.decode()

    result = subprocess.check_output(cmd, shell=True)

    return result


def LTP_parse_file(file):
    f = open(file, 'r')
    content = ""
    for line in f:
        content += line.strip()
    return LTP_parse(content)


def LTP_parse_file_type(file, type, out_file):
    data_types = 'title,context'.split(',')

    with open(file, 'r') as f:
        con_dict = eval(f.read())

        for t in data_types:
            # print(con_dict[t], type)
            out_file_type = re.sub(".txt", '_', out_file) + t + '.txt'
            print(out_file_type)
            types = type.split(',')
            for each_type in types:
                res = LTP_parse_content(con_dict[t], each_type)
                # print(res)
                if out_file is not None:
                    with open(out_file_type, 'w+') as out_f:
                        for each_w in res[each_type]:
                            out_f.write(str(each_w) + ' ')
                        out_f.write('\n')


def LTP_parse_content(content, type):
    tree = ET.fromstring(LTP_parse(content))

    res = {}
    docs = []
    global_paras = []
    global_sents = []
    global_words = []
    global_words_id = []
    global_words_cont = []
    global_words_pos = []
    global_words_ne = []
    global_words_parent = []
    global_words_relate = []
    for doc in tree.findall('doc'):
        paras = []
        for para in doc.findall('para'):
            sents = []
            for sent in para.findall('sent'):
                words = []
                for word in sent.findall('word'):
                    each_word = {}

                    each_word_id = int(word.attrib['id'])
                    each_word['id'] = each_word_id
                    global_words_id.append(each_word_id)

                    each_word_cont = str(word.attrib['cont'])
                    each_word['cont'] = each_word_cont
                    global_words_cont.append(each_word_cont)

                    each_word_pos = str(word.attrib['pos'])
                    each_word['pos'] = each_word_pos
                    global_words_pos.append(each_word_pos)

                    each_word_ne = str(word.attrib['ne'])
                    each_word['ne'] = each_word_ne
                    global_words_ne.append(each_word_ne)

                    each_word_parent = int(word.attrib['parent'])
                    each_word['parent'] = each_word_parent
                    global_words_parent.append(each_word_parent)

                    each_word_relate = str(word.attrib['relate'])
                    each_word['relate'] = each_word_relate
                    global_words_relate.append(each_word_relate)

                    args = []
                    for arg in word.findall('arg'):
                        each_arg = {}
                        each_arg['id'] = int(arg.attrib['id'])
                        each_arg['type'] = str(arg.attrib['type'])
                        each_arg['beg'] = int(arg.attrib['beg'])
                        each_arg['end'] = int(arg.attrib['end'])
                        args.append(each_arg)
                    each_word['args'] = args
                    words.append(each_word)
                sents.append(words)
                global_words.append(words)
            paras.append(sents)
            global_sents.append(sents)
        global_paras.append(paras)
        docs.append(paras)

    type_list = type.split(',')
    if 'doc' in type_list:
        res['doc'] = docs
    if 'paras' in type_list:
        res['paras'] = global_paras
    if 'sents' in type_list:
        res['sents'] = global_sents
    if 'words' in type_list:
        res['words'] = global_words
    if 'words_id' in type_list:
        res['words_id'] = global_words_id
    if 'words_cont' in type_list:
        res['words_cont'] = global_words_cont
    if 'words_pos' in type_list:
        res['words_pos'] = global_words_pos
    if 'words_ne' in type_list:
        res['words_ne'] = global_words_ne
    if 'words_parent' in type_list:
        res['words_parent'] = global_words_parent
    if 'words_relate' in type_list:
        res['words_relate'] = global_words_relate

    # print(res)
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LTP 工具， 制作者David_狄')

    parser.add_argument('-c', '--content', help="content to analyze by LTP")
    parser.add_argument('-f', '--file', help="Path to the input file")
    parser.add_argument('-t', '--type', help="get the special type list from the LTP result")
    parser.add_argument('-p', '--parser', type=bool, help='get the raw result of the LTP')
    parser.add_argument('-o', '--output', help="Path to the output file")
    ARGS = parser.parse_args()

    if ARGS.file is None and ARGS.content is not None:
        if ARGS.parser is not None:
            res = LTP_parse(ARGS.content)
            print(res)
            if ARGS.output is not None:
                with open(ARGS.output, 'w+') as out:
                    out.write(res)
        if ARGS.type is not None:
            res = LTP_parse_content(ARGS.content, ARGS.type)
            print(res)
            types = ARGS.type.split(',')
            if ARGS.output is not None:
                with open(ARGS.output, 'w+') as out_f:
                    for each_t in types:
                        for each_w in res[each_t]:
                            out_f.write(str(each_w) + ' ')
                        out_f.write('\n')
        else:
            parser.print_help()
            sys.exit(1)
    elif ARGS.file is not None and ARGS.content is None:
        if ARGS.parser is not None:
            res = LTP_parse_file(ARGS.file)
            print(res)
            if ARGS.output is not None:
                with open(ARGS.output, 'w+') as out:
                    out.write(res)
        if ARGS.type is not None:
            out_file = None if ARGS.output is None else ARGS.output
            LTP_parse_file_type(ARGS.file, ARGS.type, out_file)

        else:
            out_file = None if ARGS.output is None else ARGS.output
            res = LTP_parse_file(ARGS.file)
            print(res)
            if ARGS.output is not None:
                with open(ARGS.output, 'w+') as out:
                    out.write(res)

    else:
        parser.print_help()
        sys.exit(1)
