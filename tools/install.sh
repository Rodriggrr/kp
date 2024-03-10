#!/bin/bash

# Install python3-pip
sudo apt-get install python3-pip

# Install the termcolor package
pip install termcolor


# Set the installation directory
INSTALL_DIR=~/.local/bin

# Check the installation directory
if [ ! -d $INSTALL_DIR ]; then
    mkdir -p $INSTALL_DIR
fi

# download kp
curl -fsSL https://raw.githubusercontent.com/Rodriggrr/kp/main/kp.py > $INSTALL_DIR/kp

# CHMOD the file
chmod +x $INSTALL_DIR/kp

# Check for PATH
amarelo='\033[0;33m'
vermelho='\033[0;31m'
reset='\033[0m'
answer=""

status=$(echo $PATH | grep -o '/.local/bin' | wc -l)

if [ $status = "0" ]; then
	echo "${vermelho}ATENÇÃO: ${INSTALL_DIR} não existe na varíavel PATH. Deseja adicionar? Será necessário reiniciar o terminal. (caso escolha não, o programa não irá funcionar) [Y/n]${reset}"
    read answer

    if [ $answer = "Y" ] || [ $answer = "y" ]; then
        echo "export PATH=\$PATH:${INSTALL_DIR}" >> ~/.bashrc
        echo "export PATH=\$PATH:${INSTALL_DIR}" >> ~/.zshrc
    fi
fi 

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "Program $PROGRAM installed successfully in $INSTALL_DIR"
else
    echo "An error occurred while installing the $PROGRAM program"
fi
