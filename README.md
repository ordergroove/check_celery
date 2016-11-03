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
  - ```command[check_celery]=/usr/bin/sudo /usr/local/nagios/libexec/check_celery.py $ARG1$```
- Allow nagios user to run the check with sudo without requiring a password
  - Use ```visudo``` command to edit */etc/sudoers* and add following:
```
    Defaults:nagios !requiretty
    nagios    ALL=(ALL)   NOPASSWD:/usr/local/nagios/libexec/check_celery.py
```

## Command Line Parameters
- Space separated list of worker node names to check
- --service - [*optional*] - Service script used to manage celery; defaults to "celeryd"

## Example Usage
As standalone:
```
[user@host ~]# sudo ./check_celery.py atomic1 atomic2 periodic1
OK - All workers running
```

As NRPE plugin:
```
./check_nrpe -H localhost -c check_celery -a "atomic1 atomic2 periodic1 --service celeryd_scc"
```
### Sample services.cfg
```
define service{
    use                 generic-service
    hostgroup_name	    celery_hosts
    service_description Check Celery Workers
    check_command	    check_nrpe!check_celery!"atomic1 atomic2 periodic1"
}
```
