# nagios-aws
## Nagios AWS CPUUtiliztion plugin

command definition
```
define  command{
        command_name    check_aws_cpu
        command_line    $USER4$/nagios_aws_cpu.py $HOSTALIAS$


```

service definition
```
define service{
        use                     email-critical-service ; Inherit values from a template
        host_name               Host
        service_description     CPU
        check_command           check_aws_cpu
        }
```
LICENSE

This source files are made available under the terms of the GNU Affero General Public License (GNU AGPLv3).
