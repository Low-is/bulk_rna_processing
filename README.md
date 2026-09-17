# bulk_rna_processing

## WSL and Ubuntu Installation
```
# WindowsPowerShell

wsl --install
wsl --install -d Ubuntu
```

## Run Ubuntu
```
# WindowsPowerShell
wsl -d Ubuntu

# Will ask to create user name and password...
# Press `ENTER` for username
# Create simple password, nothing will appear on the screen, no dots or asterisks. This is normal for Linux
```

## Install the tools needed to build STAR
```
# Bash

sudo apt update
sudo apt install -y wget tar make g++

# May ask for Linux password
```


## Clone Repository
```
# Bash  

git clone https://github.com/Low-is/bulk_rna_processing.git
cd bulk_rna_processing
```

## Create Python venv
```
# Bash

python -m venv venv
source venv/Scripts/activate # Git Bash command
```


## Run bulk RNA-seq processing
```
# Bash

python bulk_rna_processing.py
```
