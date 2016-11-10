# check_celery

A Nagios NRPE plugin written in Python to monitor celery workers.

## Requirements
- Python 2.7
- For RHEL distros:
  - yum install nagios nagios-devel nagios-plugins nagios-plugins-nrpe nrpe

## Installation
- Copy check_celery.py to /usr/lib64/nagios/plugins
- ```chmod u+x /usr/lib64/nagios/plugins/check_celery.py```
- ```chown nagios:nagios /usr/lib64/nagios/pluginscheck_celery.py```
- Add command to *nrpe.cfg*:
  - ```command[check_celery]=/usr/bin/sudo /usr/lib64/nagios/plugins/check_celery.py $ARG1$```
- Allow nrpe user to run the check with sudo without requiring a password
  - Use ```visudo``` command to edit */etc/sudoers* and add following:
```
    Defaults:nrpe !requiretty
    nrpe    ALL=(ALL)   NOPASSWD:/usr/lib64/nagios/plugins/check_celery.py
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

In order to pass arguments to the command being executed by check_nrpe, I'd recommend creating a new command, similar to the default chec_nrpe command:
```
define command{
    command_name    check_nrpe_with_args
    command_line    $USER1$/check_nrpe -H '$HOSTADDRESS$' -c '$ARG1$' -a $ARG2$
}
```
