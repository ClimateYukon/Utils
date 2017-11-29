rm -r ~/src
rm -r ~/.localpython -f
mkdir ~/src
mkdir ~/.localpython
cd ~/src
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
tar xvfJ Python-3.6.3.tar.xz
cd Python-3.6.3

make clean

./configure --prefix=/home/UA/jschroder/.localpython 
export LD_LIBRARY_PATH=/home/UA/jschroder/.localpython/lib/ 
make
make install

cd ~/src
wget https://pypi.python.org/packages/d4/0c/9840c08189e030873387a73b90ada981885010dd9aea134d6de30cd24cb8/virtualenv-15.1.0.tar.gz --no-check-certificate

tar -zxvf virtualenv-15.1.0.tar.gz
cd virtualenv-15.1.0/
~/.localpython/bin/python3 setup.py install


cd ~
~/.localpython/bin/virtualenv dod --python=/home/UA/jschroder/.localpython/bin/python3


source dod/bin/activate







