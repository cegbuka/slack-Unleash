# slack-Unleash

This is a rudimentary configuration management tool in python

# Setting Up / Installation

- OS - Ubuntu
- Python3

## Step 1:
### Clone the project
```bash
  git clone https://github.com/cegbuka/slack-Unleash.git
```

## Step 2:
### Convert the boostrap script to execute
### Ensure to be in the home directory

``` chmod +x bootstrap. 
    ./bootstrap.sh
```


## Step 3:
### Create a Host file in the slack-Unleash directory
``` 
    vi hosts
    ## Update your ssh credentials

    
        [server_name]
        ssh_user=root
        ssh_pass=##password
        ssh_host=##ip
        ssh_port=22
```

## Step 4:
### Navigate to apache-conf directory and create your apache conf file
``` 
    cd apache-conf
    ## name your file index.conf
    ## Sample content 
        <VirtualHost *:80>
            ServerAdmin webmaster@localhost
            DocumentRoot /var/www/html

            ErrorLog ${APACHE_LOG_DIR}/error.log
            CustomLog ${APACHE_LOG_DIR}/access.log combined
        </VirtualHost>

```

## Step 5: 
### Run the main.py file to excute the various task in the task.yaml

```
    python3 main.py
```
