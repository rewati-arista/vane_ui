# Use official Python3 supported container
FROM python:3
MAINTAINER Professional Service: Software Services <eos-cs-sw@arista.com>

# Install necessary packages
RUN apt-get update \
    && apt-get -y install vim sudo \
    && rm -rf /var/lib/apt/lists/*

# Create the /project directory and add it as a mountpoint
WORKDIR /project
VOLUME ["/project"]

# Install python modules required by the repo
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r /tmp/requirements.txt \
    && pip3 install --upgrade pip

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

CMD ["/bin/sh"]
