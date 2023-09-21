#!/bin/bash

# Install python3-pip
sudo apt-get install python3-pip

# Install the termcolor package
pip install termcolor


# Set the installation directory
INSTALL_DIR=~/.local/bin

# download kp
wget https://raw.githubusercontent.com/Rodriggrr/kp/main/kp.py > /dev/null 2>&1

# Mv the file
mv kp.py $INSTALL_DIR/
mv $INSTALL_DIR/kp.py $INSTALL_DIR/kp
chmod +x $INSTALL_DIR/kp

# Check for PATH
amarelo='\033[0;33m'
vermelho='\033[0;31m'
reset='\033[0m'

status=$(echo $PATH | grep -o '/.local/bin' | wc -l)

if [ $status = "0" ]; then
	echo "${vermelho} ATENÇÃO: Considere adicionar ${INSTALL_DIR} à variável PATH, caso contrário o programa não irá funcionar.${reset}"
fi 



# move the program file to the installation directory
mv $PROGRAM $INSTALL_DIR

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "Program $PROGRAM installed successfully in $INSTALL_DIR"
else
    echo "An error occurred while installing the $PROGRAM program"
fi
