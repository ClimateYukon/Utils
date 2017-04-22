# ALFRESCO post processing quick Python environment install
The following describes how to easily set up a python 2.7 environment to use [ALFRESCO post processing](https://github.com/ua-snap/alfresco_postprocessing)
## Anaconda 3

Anaconda 3 installs a lot of useful packages by default in the main environment


1. Download the last anaconda package for the last python 3 :

`wget https://repo.continuum.io/archive/Anaconda3-4.3.1-Linux-x86_64.sh`

2. Install the python 3 version of Anaconda (Python 2.7 is still accessible from Anaconda 3):

`bash Anaconda3-4.3.1-Linux-x86_64.sh`

Answer Yes to every questions, it will create a base repository name anaconda3

3. Refresh the bashrc so conda command are recognized

`source ~/.bashrc` 

4. Create a new virtualenvironment

`conda create --name ALFPP27 python=2.7 ipython numpy scipy rasterio`

5. Activate the newly created environment

`source activate ALFPP27`

6. Install the Alfresco Post processing package

`pip install git+git://github.com/ua-snap/alfresco_postprocessing.git`



## Miniconda 3

Miniconda 3 install only the essentials packages in the main environment, faster and lighter installation

1. Download the Miniconda package for the last Python 3 :

`wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh`

2. Install the python 3 version of Anaconda (Python 2.7 is still accessible from Miniconda 3):

`bash Miniconda3-latest-Linux-x86_64.sh`

Answer Yes to every questions, it will create a base repository name miniconda3

3. Refresh the bashrc so conda command are recognized

`source ~/.bashrc` 

4. Create a new virtualenvironment

`conda create --name ALFPP27 python=2.7 ipython numpy scipy rasterio`

5. Activate the newly created environment

`source activate ALFPP27`

6. Install the Alfresco Post processing package

`pip install git+git://github.com/ua-snap/alfresco_postprocessing.git`

