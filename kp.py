#!/usr/bin/env python3

# Copyright (c) 2023, Rodrigo Farinon <rfarinon@alu.ufc.br>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import time
import argparse
import subprocess
import threading
from termcolor import colored
import time

# ------------------ VARIÁVEIS -------------------- #
# tempo de compilação
update = False
time_to_compile = time.time()
total_time = time.time()
error = False
version = "0.1.9"
versionInt = int(version.replace(".", ""))

# ------------------ FUNÇÕES VARIADAS ---------------------- #


def check_new_version():
    try:
        newVersion = subprocess.check_output("timeout 0.2 curl -SsLp https://raw.githubusercontent.com/Rodriggrr/kp/main/version.txt", shell=True, text=True)
        newVersionInt = int(newVersion.replace(".", ""))

        if newVersionInt > versionInt:
            global update
            update = True
    except subprocess.CalledProcessError:
        return

# função para mostrar tempo de compilação
def show_compiling_time(file, foo=""):
    global time_to_compile
    if not error:
        compile_time = time.time() - time_to_compile
        print(f"{file}: compiled in " + colored(f'[{float(compile_time):.3f}]', "green") + f" seconds.{foo}")
        time_to_compile = time.time()

# funções de erro
def unexpected_error(code, close=True):
    if code != 0 and code != 2:
        print(colored(f"Program closed with code {code}.", "red"))
        if close:
            sys.exit(code)

def error_msg(msg, close=True):
    print(colored(msg, "red"))
    if close:
        print(colored('\nAborting. Use -h or --help for help.', "red"))
        sys.exit(1)

# -------------------- COMPILAR ---------------------- #

# compilar arquivos .cpp
def compile_cpp(args, opt='', show=True) -> int:
    hide = ""
    if show:
        print("Compiling C++ file...")
    else:
        hide = "> /dev/null 2>&1"
    code = os.system(f"g++ {opt + ' ' if opt else ''}\"{args}\" -o \"{args[:-4]}\" {hide}")
    return code


# compilar arquivos .c
def compile_c(args, show=True) -> int:
    hide = ""
    if show:
        print("Compiling C file...")
    else:
        hide = "> /dev/null 2>&1"

    code = os.system(f"gcc \"{args}\" -o \"{args[:-2]}\" {hide}")
    return code


# compilar arquivos .java
def compile_java(args, show=True) -> int:
    hide = ""
    if show:
        print("Compiling Java file...")
    else:
        hide = "> /dev/null 2>&1"

    code = os.system(f"javac \"{args}\" {hide}")
    return code

# compilar aquivos .ts
def compile_ts(args, show=True) -> int:
    hide = ""
    if show:
        print("Compiling Typescript file...")
    else:
        hide = "> /dev/null 2>&1"

    code = os.system(f"tsc \"{args}\" {hide}")
    return code



# compilar varios arquivos
def compile(args):
    if len(args) > 1:
        print("Compiling files...")
    count = 0
    show = True
    if len(args) > 1:
        show = False
    for file in args:
        code = 0
        if file.endswith(".cpp"):
            code = compile_cpp(file, '', show)
        elif file.endswith(".c"):
            code = compile_c(file, show)
        elif file.endswith(".java"):
            code = compile_java(file, show)
        elif file.endswith(".ts"):
            code = compile_ts(file, show)
        else:
            error_msg(f"{file}: File type not supported.")
            count += 1
        if code != 0:
            error_msg(f"{file}: Compilation failed.", close=False)
            count += 1
        else:
            show_compiling_time(file)

    if count > 0 and not show:
        error_msg(f"{count} files were not compiled.", close=False)


# ----------------- RODAR ---------------------- #

# compilar e rodar arquivos
def compile_and_run(args, opt=''):
    global time_to_compile
    if args.file[0].endswith(".py"):
        time_to_compile = time.time()
        run_py(args.file[0])

    elif args.file[0].endswith(".js"):
        print("Running Javascript file...")
        run(args.file[0], 3, ext=".js", run="node ", remove=False)

    elif args.file[0].endswith(".ts"):
        code = compile_ts(args.file[0])
        if code != 0:
            unexpected_error(code)
        show_compiling_time(args.file[0], foo="\n")
        run(args.file[0], 3, ext=".js", run="node ")

    elif args.file[0].endswith(".cpp"):
        code = compile_cpp(args.file[0], opt=opt)
        if code != 0:
            unexpected_error(code)
        show_compiling_time(args.file[0], foo="\n")
        run(args.file[0], 4)

    elif args.file[0].endswith(".c"):
        code = compile_c(args.file[0])
        if code != 0:
            unexpected_error(code)
        show_compiling_time(args.file[0], foo="\n")
        run(args.file[0], 2)

    elif args.file[0].endswith(".java"):
        code = compile_java(args.file[0])
        if code != 0:
            unexpected_error(code)
        show_compiling_time(args.file[0], foo="\n")
        run(args.file[0], 5, ext="", run="java ", remove=False)
        os.system(f"rm \"{args.file[0][:-5]}.class\"")

    else:
        error_msg("File type not supported.")


# rodar arquivos
def run(args, erase, ext="", run="./", remove=True):
    code = os.system(f"{run}\"{args[:-erase]}\"{ext}")
    if remove:
        os.system(f"rm \"{args[:-erase]}\"{ext}")
    if code != 0:
        unexpected_error(code)

# rodar arquivos .py
def run_py(args):
    print("Running Python file...")
    code = os.system(f"python3 \"{args}\"")
    if code != 0 or error:
        unexpected_error(code)


# ----------------- ARGPARSE ---------------------- #
parser = argparse.ArgumentParser(description="Compile and run:\nC, C++, Java, Python, Javascript and Typescript files.")
parser.add_argument("file", help="File to compile and run.", nargs="*")
parser.add_argument("-c", "--compile", help="Compile multiple files.", action="store_true")
parser.add_argument("-u", "--update", help="Update kp.", action="store_true")
parser.add_argument("-a", "--args", help="Pass arguments to the program.", action="append", type=str)
parser.add_argument("-e", "--execution-time", help="Show program total execution time.", action="store_true")
parser.add_argument("-v", "--version", help="Show version.", action="store_true")
args = parser.parse_args()


# ----------------- MAIN ---------------------- #
thread = threading.Thread(target=check_new_version)
thread.start()

if args.version:
    print(f"Version {version}")
    sys.exit(0)

if args.update:
    print("Updating kp...")
    os.system(f"echo Your version: {version}")
    newVersion = subprocess.check_output("curl -SsL https://raw.githubusercontent.com/Rodriggrr/kp/main/version.txt", shell=True, text=True)
    print(f"Current version: {newVersion}")
    newVersionInt = int(newVersion.replace(".", ""))

    if newVersionInt > versionInt:
        print("kp will be updated.")
        os.system("sh -c \"$(curl -fsSL https://raw.githubusercontent.com/Rodriggrr/kp/main/tools/install.sh)\"")
        print("kp updated.")
    
    sys.exit(0)
    


# file not found
try:
    if not os.path.exists(args.file[0]):
        error_msg(f"File \"{args.file[0]}\" does not exist.")
except IndexError:
    error_msg("No file specified.")

if args.compile:
    compile(args.file)

else:
    compile_and_run(args, opt=args.args[0] if args.args else '')
# print program closed and time of execution.
endTime = float(time.time() - total_time)
print("\nProgram closed in " + colored(f"[{endTime:.3f}]", "green") + " seconds.")

startTime = float(time.time() - time_to_compile)
if args.execution_time:
    print("Total execution time: " + colored(f"[{(startTime):.5f}]", "blue") + " seconds.")

if update:
    print(colored("kp tem uma nova atualização, use kp -u para atualizar.", "yellow"))

thread.join()
