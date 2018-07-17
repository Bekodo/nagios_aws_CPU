#!/usr/bin/python2.7

import json, os, sys, boto3
from datetime import datetime, timedelta
from optparse import OptionParser

class Monitor(object):
    difhourmin = 10
    client = []
    instance = ''

    def __init__(self,instance):
        self.instance = instance
        self.client = boto3.client('cloudwatch',
            aws_access_key_id = os.environ.get('$AWSKEY$'),
            aws_secret_access_key = os.environ.get('$AWSSECRET$'),
            region_name = os.environ.get('$AWSREGION$')
        )

    def _setDimensions(self):
        instance = self.instance
        dimension = {
            'Namespace' : '',
            'Dimensions' : [
                {
                    'Name': '',
                    'Value': ''
                },
            ],
        }
        dimension['Namespace'] = 'AWS/EC2'
        dimension['Dimensions'][0]['Name'] = 'InstanceId'
        dimension['Dimensions'][0]['Value'] = instance
        return dimension

    def getMetric(self):
        dimension = self._setDimensions()
        response = self.client.get_metric_statistics(
            Namespace = dimension['Namespace'],
            MetricName = 'CPUUtilization',
            Dimensions = [
                {
                    'Name': dimension['Dimensions'][0]['Name'],
                    'Value': dimension['Dimensions'][0]['Value']
                },
            ],
            StartTime = datetime.now() - timedelta(minutes = (self.difhourmin + 10)),
            EndTime = datetime.now() - timedelta(minutes = (self.difhourmin + 5)),
            Period = 300,
            Statistics = ['Average'],
            Unit = 'Percent'
        )
        value = response['Datapoints'][0]['Average']
        return round(value,2)

def main():
    parser = OptionParser(usage="usage: %prog [options] instance")
    parser.add_option("-c", "--critica", dest="critical", default=60, help="Critical per cent")
    parser.add_option("-w", "--warning", dest="warning", default=40, help="Warning per cent")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    try:
        ClodWatch = Monitor(args[0])
        metric = ClodWatch.getMetric()
        if float(metric) > float(options.critical):
            print("CPU %3.2f is CRITICAL" % float(metric))
            sys.exit(2)
        if float(metric) > float(options.warning):
            print("CPU %3.2f is WARNING" % float(metric))
            sys.exit(1)
        if float(metric) < float(options.warning):
            print("CPU %3.2f is OK" % float(metric))
            sys.exit(0)
    except Exception as e:
        print("UNKNOWN")
        sys.exit(3)

if __name__ == '__main__':
    main()
