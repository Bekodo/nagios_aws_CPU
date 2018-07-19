# nagios-aws
## Nagios AWS CPUUtiliztion plugin

command definition
```
define  command{
        command_name    check_aws_cpu
        command_line    $USER4$/nagios_aws_cpu.py -k $USER7$ -s $USER8$ -r $USER9$ $HOSTALIAS$
}
```

service definition
```
define service{
        use                     local-service ; Inherit values from a template
        host_name               Host
        service_description     CPU
        check_command           check_aws_cpu
        }
```

host definition
```
define host{
        use                     [Template_host]
        host_name               [Host_tag]
        alias                   [InstanceId]
        address                 [IP]
}
```

Keys setup: on file: resource.cfg
```
$USER7$=[KEY]
$USER8$=[SECRET]
$USER9$=[REGION]
```

LICENSE

This source files are made available under the terms of the GNU Affero General Public License (GNU AGPLv3).
