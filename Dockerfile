# Use official Python3 supported container
FROM python:3.9
MAINTAINER Professional Service: Software Services <eos-cs-sw@arista.com>

# Configure some python settings for containers
#   Don't write .pyc files while working in the container
ENV PYTHONDONTWRITEBYTECODE 1
#   Don't buffer output while working in the container
ENV PYTHONBUFFERED 1
#   Don't store installation files in the container
ENV PIP_NO_CACHE_DIR 1

# Set the poetry version to use
ENV POETRY_VERSION 1.5.1

# Install necessary packages
RUN apt-get update \
    && apt-get -y install \
        iputils-ping \
        openvpn \
        rpm \
        sudo \
        tree \
        unzip \
        vim \
        yamllint \
    && rm -rf /var/lib/apt/lists/*

# Update pip and install the poetry package
RUN pip3 install --upgrade pip
RUN pip install poetry==${POETRY_VERSION}

# Create the /project directory and add it as a mountpoint
WORKDIR /project
COPY . .

# Allow python install to run without being root
RUN chmod 777 /usr/local/lib/python*/site-packages /usr/local/bin

# Create the user/group that will be used in the container
# Set some defaults that can be overridden in the build command
ARG UNAME=docker
ARG UPASS=docker
ARG UID
ARG GID
# Create the sudo and UNAME groups and add the sudo group to sudoers
# Create the user, add to the sudo group, and set the password to UPASS
RUN echo "%sudo   ALL=(ALL:ALL) ALL" >> /etc/sudoers \
    && groupadd -r -g $GID -o $UNAME \
    && useradd -r -m -u $UID -g $GID -G sudo -o -s /bin/bash -p $(perl -e 'print crypt($ENV{"UPASS"}, "salt")') $UNAME

# Switch to the new user for when the container is run
USER $UNAME
RUN echo "PS1='🐳  \[\033[1;36m\]\h \[\033[1;34m\]\W\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" >> /home/${UNAME}/.bashrc

# Install dependencies required by the repo
RUN poetry install --no-root

# Create an alias for activating the poetry shell
RUN echo "alias activate='source `poetry env info --path`/bin/activate'" >> /home/${UNAME}/.bashrc

# Start the container
CMD ["/bin/bash"]
