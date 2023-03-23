#!/usr/bin/env python3
import time
import os
import sys
import termcolor

# variáveis globais
total_time = time.time()
time_to_compile = time.time()
speed = False

# mensagem de ajuda
help_msg = '''
Usage: kp <option> <file>
Example: kp -s main.cpp (runs main.cpp with speed option) | kp main.cpp (runs main.cpp)
Supports: 
    .c, .cpp, .py, .java, .ts, .js

Options:
    -h, --help      Show this help message.
    -s, --speed     Show total running time of the program at its end. (Not supported for non-compiled languages)
'''

# --------------------------------- FUNÇÕES -----------------------------------
# função para mostrar tempo de compilação
def show_compiling_time():
    global time_to_compile
    time_to_compile = time.time() - time_to_compile
    print("Compiled in " + termcolor.colored(f'[{float(time_to_compile):.3f}]', "green") + " seconds, running.\n")

# funções de erro
def unexpected_error(code):
    print(termcolor.colored(f"Program closed with code {code}.", "red"))
    sys.exit(1)

def error_msg(msg):
    print(termcolor.colored(msg + '\nAborting. Use -h or --help for help.', "red"))
    sys.exit(1)

# rodar arquivos .cpp
def run_cpp(args):
    print("Compiling C++ file...")
    code = os.system(f"g++ \"{args}\" -o \"{args[:-4]}\"")
    if code != 0:
        unexpected_error(code)

    show_compiling_time()
    
    os.system(f"./\"{args[:-4]}\"")
    os.system(f"rm \"{args[:-4]}\"")

# rodar arquivos .c
def run_c(args):
    print("Compiling C file...")
    code = os.system(f"gcc \"{args}\" -o \"{args[:-2]}\"")
    if code != 0:
        unexpected_error(code)

    show_compiling_time()
    
    os.system(f"./\"{args[:-2]}\"")
    os.system(f"rm \"{args[:-2]}\"")

# rodar arquivos .java
def run_java(args):
    print("Compiling Java file...")
    code = os.system(f"javac \"{args}\"")
    if code != 0:
        unexpected_error(code)

    show_compiling_time()

    os.system(f"java \"{args[:-5]}\"")
    os.system(f"rm \"{args[:-5]}.class\"")

# rodar arquivos .py
def run_py(args):
    print("Running Python file...")
    code = os.system(f"python3 \"{args}\"")
    if code != 0:
        unexpected_error(code)

#rodar arquivos .ts
def run_ts(args):
    print("Running TypeScript file...")

    # check if tsc is installed, if not, install it.
    if  os.system("tsc -v \"$@\" > /dev/null 2") != 0:
        print(termcolor.colored("TypeScript is not installed ", "red") + "installing...")
        os.system("npm install -g typescript")
        print("TypeScript installed.")
    
    code = os.system(f"npx tsc \"{args}\"")
    if code != 0:
        unexpected_error(code)

    show_compiling_time()

    os.system(f"node \"{args[:-3]}.js\"")
    os.system(f"rm \"{args[:-3]}.js\"")

# rodar arquivos .js
def run_js(args):
    print("Running JavaScript file...")
    code = os.system(f"node \"{args}\"")
    if code != 0:
        unexpected_error(code)



# --------------------------------- MAIN --------------------------------------

# checar quantidade de argumentos de entrada
if len(sys.argv) == 1:
    error_msg("No arguments passed.")
elif len(sys.argv) == 2 and (sys.argv[1].startswith('-s') or sys.argv[1].startswith('--speed')):
    error_msg("No file supplied.")

args = sys.argv[1]

# checar argumentos de entrada
if args == '-h' or args == '--help':
    print(help_msg)
    sys.exit(0)
elif (args == '-s' or args == '--speed') and not sys.argv[2].endswith(".py"):
    args = sys.argv[2]
    speed = True
elif args == '-s' or args == '--speed':
    error_msg("Python files are not supported for this option.")

# checar se arquivo existe
if not os.path.exists(args):
    error_msg(f"File \"{args}\" does not exist.")

# checar tipo de arquivo e executar
if args.endswith(".cpp"):
    run_cpp(args)
elif args.endswith(".c"):
    run_c(args)
elif args.endswith(".py"):
    run_py(args)
elif args.endswith(".java"):
    run_java(args)
elif args.endswith(".ts"):
    run_ts(args)
elif args.endswith(".js"):
    run_js(args)
else:
    error_msg("File type is not supported.")

# tempo total
print("\nFinished in " + termcolor.colored('[' + "{:.3f}".format(time.time() - total_time) + ']', "green") + " seconds.")

# tempo de execução
if speed:
    elapsed_time = time.time() - total_time - time_to_compile
    print("Program executed in " + termcolor.colored(f'[{float(elapsed_time):.5f}]', "blue") + " seconds.")