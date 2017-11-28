#!/bin/bash
mkdir ~/src
mkdir ~/.localpython
cd ~/src
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz

tar xvfJ Python-3.6.3.tar.xz

cd Python-3.6.3

​
make clean
./configure --prefix=/home/UA/jschroder/.localpython --enable-shared
make
make install
​
#2) Install virtualenv
cd ~/src
wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-15.1.0.tar.gz --no-check-certificate
tar -zxvf virtualenv-15.1.0.tar.gz
cd virtualenv-15.1.0/
~/.localpython/bin/python setup.py install
​
#3) Create a virtualenv using your local python
cd ~
~/.localpython/bin/virtualenv dod --python=/home/UA/jschroder/.localpython/bin/python3
​
#4) Activate the environment
​
source venv2/bin/activate
