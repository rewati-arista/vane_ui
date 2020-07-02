# Project: VANE

Network Certification Tool

## Description

A weather vane is an instrument used for showing the direction of the wind.
Just like a weather vane, Vane is a network certification tool that shows a
network's readiness for production based on validation tests.

## Installation

Let user know how to install

## Development

Contributed pull requests are gladly welcomed for this project.

### Build Docker Container

The docker container approach for development can be used to ensure that
everybody is using the same development environment while still being flexible
enough to use the repo you are making changes in. You can inspect the
Dockerfile to see what packages have been installed. Note that specifying the
build arguments allows you to run the container as your user-id and not as the
default user docker.

```
    $ docker build -t repo-name . --build-arg UID=$(id -u) --build-arg GID=$(id -g) --build-arg UNAME=$(id -un)
```

### Run the Docker Container

Start up the docker container from the root of the repo directory with the
following command.

```
    $ docker run -it --volume "$(pwd):/repo-name" repo-name
```

## Contributing	
	
Contributing pull requests are gladly welcomed for this repository.	
Please note that all contributions that modify the library behavior	
require corresponding test cases otherwise the pull request will be	
rejected.

## License

Copyright (c) 2020, Arista Networks EOS+
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the Arista nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
