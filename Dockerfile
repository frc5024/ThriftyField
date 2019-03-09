from alpine:3.9
maintainer ewpratten@gmail.com

# Install needed tools
run apk add python3 git

# Get the repo
run git clone https://github.com/frc5024/ThriftyField 

# Install required python libs
run pip3 install -r ThriftyField/requirements.txt

# EXPOSE 443
expose 5000

entrypoint python3 ThriftyField/main.py && /bin/bash