# VTK Python Setup (Ubuntu 18.04)
*Created on March 06, 2020 by Edwin Sarver*

## Install Python 3 ##
```bash
sudo apt update
sudo apt install python3 python3-pip
```

## Installing Dependencies ##
After installing Python 3, there are two ways to work with dependencies: 
    1. Install them system-wide
    2. Install them as part of a virtual environment
    
### System Wide ###
```bash
pip3 install vtk # other dependencies can be added here as well
```

### Virtual Environment ###
Using virtual environments helps to keep your system clean of 
all the libraries for all your projects. Instead each virtual environment 
will be self-contained. Incorporating PipFiles makes it easier to put your
project on any equipped computer. 

There are multiple ways to setup virtual environments. The one the I have tried is using `pipenv`
because is simplifies the workflow by including pip.

**To install:**
```bash
pip3 install --user pipenv
```

After installing pipenv, navigate to your project root and do the following to set it up:
```bash
pipenv install
pipenv shell
pipenv install vtk #add any other dependencies here as well.
```
## Development ##
I personally love Microsoft's Visual Studio Code. It generally handles Python code very well, 
however I haven't had much luck when trying to get code-completions for VTK (something that is 
very desirable for such a large library). 

I therefore suggest using JetBrains' PyCharm, which is super easy to install using 
any Linux distribution that has snapd. I also found that it has code-completions 
ready to go for VTK in my `pipenv` environment. 

```bash
sudo snap install pycharm-community --classic
```    

## Resources ##
VTK has a bunch of examples online for all the language-bindings they support.
The examples for Python can be found at https://lorensen.github.io/VTKExamples/site/Python/. 
