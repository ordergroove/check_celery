# check_celery

A Nagios NRPE plugin written in Python to monitor celery workers.

## Requirements
- Python 2.7
- Functioning NRPE setup
  - http://www.tecmint.com/how-to-add-linux-host-to-nagios-monitoring-server/ for instructions

## Installation
- Copy check_supervisord.py to /usr/local/nagios/libexec/
- ```chmod u+x /usr/local/nagios/libexec/check_celery.py```
- ```chown nagios:nagios /usr/local/nagios/libexec/check_celery.py```
- Add command to *nrpe.cfg*:
  - ```command[check_celery]=/usr/bin/sudo /usr/local/nagios/libexec/check_celery.py```
- Allow nagios user to run the check with sudo without requiring a password
  - Use ```visudo``` command to edit */etc/sudoers* and add following:
```
    Defaults:nagios !requiretty
    nagios    ALL=(ALL)   NOPASSWD:/usr/local/nagios/libexec/check_celery.py
```

## Command Line Parameters

## Example Usage

### Sample services.cfg
