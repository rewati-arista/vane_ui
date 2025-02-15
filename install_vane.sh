#!/bin/bash

# Declare global variables

# Check if destination folder has been passed as parameter
if [ ! $# -eq 0 ]; then
    DESTINATION_FOLDER=$1
    last_char="${DESTINATION_FOLDER: -1}"
    if [ ! "$last_char" = "/" ]; then
        DEFAULT="/"
    fi
fi
DEFAULT+="vane"
DESTINATION_FOLDER+=$DEFAULT

PACKAGE_MANAGER=""
PYTHON_VERSION="3.9"
INSTALL_OPTION=""

# Function to install Homebrew (macOS) if not already installed
function install_homebrew() {
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
}

# Function to setup package manager to be used to install commands needed
function set_up_package_manager() {

    # Determine the package manager based on the system's OS and implement initial configuration

    # Debian based Linux distribution
    if command -v apt-get &>/dev/null; then
        echo "Using apt-get as found Linux Subsystem"
        PACKAGE_MANAGER="apt-get"
        INSTALL_OPTION="-y"
        apt update
    # CentOS and older versions
    elif command -v yum &>/dev/null; then
        echo "Using yum as found CentOS"
        PACKAGE_MANAGER="yum"
        INSTALL_OPTION="-y"
        path=$(pwd)
        cd /etc/yum.repos.d/
        sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
        sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
        cd "$path"
        yum install -y glibc-langpack-en
    # For MacOs
    elif command -v brew &>/dev/null; then
        echo "Using brew as found MacOS"
        PACKAGE_MANAGER="brew"
        INSTALL_OPTION="--force"
    else
	    # Install Homebrew on macOS
    	if [[ "$OSTYPE" =~ ^darwin ]]; then
            install_homebrew
	        PACKAGE_MANAGER="brew"
            INSTALL_OPTION="--force"
	    else
            # Add support for other package managers if needed, like chocolatey for Windows
            echo "Error: Package manager not found."
            exit 1
        fi
    fi
}

# (1) Set up package manager
set_up_package_manager

# (2) Check if Git is installed
if command -v git &>/dev/null; then
    echo "Git is installed."
else
    echo "Git is not installed. Installing Git"
    $PACKAGE_MANAGER install $INSTALL_OPTION git
fi

# (3) Download Vane repo into current directory
echo "Cloning Vane Repo"
git clone https://github.com/aristanetworks/vane.git $DESTINATION_FOLDER

# Exit the script if cloning fails
if [ $? -eq 0 ]; then
    echo "Repository cloned successfully."
else
    echo "Failed to clone repository. Exiting script."
    exit 1  # Exit the script with a non-zero status
fi

# (4) Install Python 3.9 if version does not exist
if ! command -v python3.9 &>/dev/null; then
    echo "Python 3.9 not found. Installing Python 3.9"
    if [ "$PACKAGE_MANAGER" = "brew" ]; then
        brew install $INSTALL_OPTION python@3.9
    elif [ "$PACKAGE_MANAGER" = "apt-get" ]; then
        apt install $INSTALL_OPTION software-properties-common
        add-apt-repository $INSTALL_OPTION ppa:deadsnakes/ppa
        apt install $INSTALL_OPTION python3.9
        apt-get install $INSTALL_OPTION python3-pip
    else
        $PACKAGE_MANAGER install $INSTALL_OPTION python3.9
    fi
else
    echo "Python 3.9 is already installed."
fi

# (5) Check if Poetry is installed using pip3
if pip3 show poetry &>/dev/null; then
    echo "Poetry is installed."
else
    echo "Poetry is not installed. Installing Poetry 1.4.2"
    pip3 install poetry==1.4.2
fi

# (6) Set up virtual environment in downloaded vane folder
cd $DESTINATION_FOLDER
echo "cd $DESTINATION_FOLDER"
path=$(pwd)
poetry config virtualenvs.path "$path"
python=$(command -v python3.9)
poetry env use "$python"
poetry install 

# (7) Activate poetry environment within the root folder
poetry shell