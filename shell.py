import os
import subprocess
import argparse

# set reputation
cmd_reputation = 1


# structure holding data of codamosa
class DataPaths:
    project_path = ""
    module_name = ""

    def __init__(self, path, module):
        self.project_path = "./test_modules/" + path
        self.module_name = module

    def get_output(self, llm_name):
        return self.project_path + "/" + self.get_module() + "/" + llm_name

    def get_module(self):
        return self.module_name.split(".")[-1]


# run script and record the result
def shell_cmd(cmd, file_name, max_count=3, tm=36000):
    # write log into "cmd.log" file
    log = open("./cmd.mlog", 'a')
    log.writelines(cmd + ": \n")
    log.close()

    i = 0
    cnt = 0
    # try to repeat
    while i < cmd_reputation and cnt < max_count + cmd_reputation:
        si = str(i)
        flag = False
        log = open("./cmd.mlog", 'a')
        os.system("rm *.log")
        try:
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, encoding="utf-8", timeout=tm)
            flag = True
        finally:
            # write result to log
            if flag:
                if p.returncode == 0:
                    success = "success " + si + ":" + str(p)
                    print(success)
                    log.writelines(success + "\n")
                    file = file_name + "-" + si

                    # collect data
                    os.mkdir(file)
                    os.system("mv *.log ./" + file)
                    os.system("mv " + file + " ./result")
                    i += 1
                else:
                    error = "error " + si + ":" + str(p)
                    print(error)
                    log.writelines(error + "\n")
            else:
                # record failure and continue
                error = "error " + si + ": is not finish"
                print(error)
                log.writelines(error + "\n")
            # retry the command
            log.close()
            cnt += 1
            continue


def read_data(path):
    data = []
    file = open(path)
    try:
        while True:
            line = file.readline()
            if line:
                data_line = line.split(",")
                data.append(DataPaths(data_line[0], data_line[1][:-1]))
            else:
                break
    finally:
        file.close()
    return data


# create the bash script
def shell(model, path, time, key):
    name = get_token(model)
    file_name = name + "_" + path.get_module()
    print(file_name)
    output_path = p.get_output(name)
    if key == "codamosa":
        cli = "run.sh"
    else:
        cli = "mosa.sh"

    # e.g. bash run.sh -p ./test_modules/typesystem
    # -o ./test_outputs/typesystem/formats/MOSA -r ./test_outputs/typesystem/formats/MOSA
    # -n deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B -t 600
    # each line are built as follow:
    cmd_0 = "bash " + cli + " -p " + path.project_path
    cmd_1 = " -o " + output_path + " -r " + output_path
    cmd_2 = " -n " + model
    cmd_3 = " -m " + path.module_name + " -t " + str(time)
    if key == "codamosa":
        cmd = cmd_0 + cmd_1 + cmd_2 + cmd_3
    else:
        cmd = cmd_0 + cmd_1 + cmd_3
    print(cmd)
    # shell_cmd(cmd, file_name)


# create file names of the result
def get_token(model):
    if model == "state-spaces/mamba-790m-hf":
        sign = "790m"
    elif model == "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B":
        sign = "1.5b"
    elif model == "stabilityai/stablelm-3b-4e1t":
        sign = "3b"
    elif model == "thesven/Mistral-7B-Instruct-v0.3-GPTQ":
        sign = "7b"
    else:
        sign = "mosa"
    return sign


# input
parser = argparse.ArgumentParser()
parser.add_argument('-k', '--key', default="list", type=str)
parser.add_argument('-l', '--llm', default="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", type=str)
parser.add_argument('-t', '--max_time', default="600", type=int)
parser.add_argument('-p', '--project', default="./test_modules/typesystem", type=str)
parser.add_argument('-d', '--data_path', default="./list.dt", type=str)
args = parser.parse_args()

option = args.key
llm = args.llm
max_time = args.max_time
proj = args.project
data = args.data_path

# Preparation
os.system("rm cmd_log")
if llm == "mosa":
    alg = "mosa"
else:
    alg = "codamosa"

if option == "list":
    for p in read_data(data):
        # print(p.project_path + "," + p.module_name)
        shell(llm, p, max_time, alg)

