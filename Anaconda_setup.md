###ALFRESCO post processing quick install
## ANACONDA3
Anaconda comes with a lot of useful packages pre installed to install :



#download the last anaconda package for the last python 3 :
`wget https://repo.continuum.io/archive/Anaconda3-4.3.1-Linux-x86_64.sh`

#install the python 3 version of Anaconda, there is still possibility to set up py27 environment easily after that
#Answer Yes to every questions, it will create a base repository name anaconda3
`bash Anaconda3-4.3.1-Linux-x86_64.sh`

#Refresh the bashrc so conda command are recognized
source ~/.bashrc 

#Create a new virtualenvironment through conda just asking it to install ipython for debugging
conda create --name ALFPP27 python=2.7 ipython

#to activate it :
source activate ALFPP27

#install the Alfresco Post processing package (see package github for this step)
pip install git+git://github.com/ua-snap/alfresco_postprocessing.git

########################################################################################################################
########################################################################################################################
#############################################    Miniconda 3   #########################################################
########################################################################################################################
########################################################################################################################
#If not wanting the full array of anaconda +> Miniconda just ships with essential package for the main environment:

#download the last miniconda package for the last python 3 :
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

#install the python 3 version of Anaconda, there is still possibility to set up py27 environment easily after that
#Answer Yes to every questions, it will create a base repository name miniconda3
bash Miniconda3-latest-Linux-x86_64.sh

#Refresh the bashrc so conda command are recognized
source ~/.bashrc 

#Create a new virtualenvironment through conda just asking it to install ipython for debugging
conda create --name ALFPP27 python=2.7 ipython

#to activate it :
source activate ALFPP27

#install the Alfresco Post processing package (see package github for this step)
pip install git+git://github.com/ua-snap/alfresco_postprocessing.git




#Keep that in case the setup.py from alfpp is missing some package :
#conda create --name ALFPP27 python=2.7 --file /workspace/Shared/Users/jschroder/Github/Utils/ALF.txt
