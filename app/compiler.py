# !/usr/bin/python3
# -*- coding:utf8 -*-
# author: suntangji 2018-01-19 14:54:49

import os
import subprocess
import global_var

# t = str((time.time()) / random.randint(100, 1000))
# t = time.time()


def get_file_name(lang, t):
    fpath = get_file_path()
    if lang == 'python2' or lang == 'python3':
        fname = os.path.join(fpath, '%s.py' % t)
    elif lang == 'c':
        fname = os.path.join(fpath, '%s.c' % t)
    elif lang == 'cpp':
        fname = os.path.join(fpath, '%s.cc' % t)
    elif lang == 'java':
        fname = os.path.join(fpath, '%s.java' % t)
    elif lang == 'php':
        fname = os.path.join(fpath, '%s.php' % t)
    elif lang == 'go':
        fname = os.path.join(fpath, '%s.go' % t)
    return fname


def get_file_path():
    path = "/tmp/compiler/"
    if not os.path.exists(path):
        os.mkdir(path)
    # temp_dir = tempfile.mkdtemp(suffix="_test", prefix=time, dir=None)
    return path


def generate_file(code, lang, file_name):
    # fpath = get_file_name(lang)
    fpath = file_name
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(code)
    # with open(fpath, 'r', encoding='utf-8') as f:
    # file = f.read()
    # print(file)


def process_switch(file_name, lang, user_input):
    if lang == 'python2':
        # cmd = "python2 %s" % file_name
        cmd = ['python2', file_name]
    elif lang == 'python3':
        # cmd = "python3 %s" % file_name
        cmd = ['python3', file_name]
    elif lang == 'c' or lang == 'cpp':
        # cmd1 = "g++ {file} -o {file}.out".format(file=file_name)
        # cmd2 = "%s.out" % file_name
        # cmd = cmd1 + "&&" + cmd2
        cmd = ['g++', file_name, '-o', file_name + '.out']
        # file_name + '.out'
        proc = subprocess.Popen(cmd, shell=False, stderr=subprocess.PIPE)
        err_out = proc.stderr.read()
        # out_prem, err_prem = proc.communicate()
        proc.stderr.close()
        # proc.stdout.close()
        err_out = err_out.decode('utf-8')
        # print(err_out)
        if err_out == '':
            cmd = [file_name + '.out']
            # print(cmd)
        else:
            return err_out
    # obj = subprocess.getoutput(cmd)
    # print(cmd)
    proc = subprocess.Popen(
        cmd,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    # proc.stdin.write(user_input.encode('utf-8'))
    # user_input = global_var.get_global()
    userinput = user_input.encode('utf-8')
    # proc.stdin.write(userinput)
    try:
        out_value, err_value = proc.communicate(userinput, 10)
        out = out_value.decode('utf-8')
        err = err_value.decode('utf-8')
    except subprocess.TimeoutExpired:
        err = 'timeout!'
        proc.kill()

    if err == '':
        return out
    else:
        return err


def remove_file(file_name, lang):
    if lang == "python2" or lang == "python3":
        os.remove(file_name)
    elif lang == "c" or lang == "cpp":
        # file_name_excu = os.path.join(file_name,".out")
        if os.path.exists(file_name + ".out"):
            os.remove(file_name + ".out")
        os.remove(file_name)
    # shutil.rmtree(file_name)


def action(code, lang, user_input, time):
    file_name = get_file_name(lang, time)
    generate_file(code, lang, file_name)
    ret = process_switch(file_name, lang, user_input)
    remove_file(file_name, lang)
    return ret
