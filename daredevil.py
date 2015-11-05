import boto3
from pprint import pprint
from datetime import datetime
import time

def make_tag_dict(ec2_object):
    """Given an tagable ec2_object, return dictionary of existing tags."""
    tag_dict = {}
    if ec2_object.tags is None: return tag_dict
    for tag in ec2_object.tags:
        tag_dict[tag['Key']] = tag['Value']
    return tag_dict


def make_tag_string(ec2_object):
    """Given an tagable ec2_object, return string of existing tags."""
    tag_string = ''
    if ec2_object.tags is None: return tag_string
    for tag in ec2_object.tags:
        tag_string = tag_string + tag['Key'] + "=" + tag['Value'] + " "
    return tag_string

def time_difference(the_time):
    
        # convert to timestamp
        the_time_ts = time.mktime(the_time.timetuple())
        
        # current time as timestamp
        now = datetime.utcnow()
        now_ts = time.mktime(now.timetuple())
    
        # find the difference in days (how many days the instance has been up)
        difference_ts = now_ts-the_time_ts
        return ( difference_ts/60/60/24 ) 
        
        
def get_ec2_instances(region):

    print ''
    print "REGION: %s" % (region)
    print '-----------------------'

    ec2 = boto3.resource('ec2', region_name=region)

    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:

        # nicer structures
        tag_dict = make_tag_dict(instance)
        tag_string = make_tag_string(instance)
        
        # clean the name
        if 'Name' in tag_dict:
            clean_name = tag_dict['Name']     
        else:
            clean_name = '<no-name>'

        # find out how many days the EC2 has been running
        days_running = time_difference(instance.launch_time)
        days_running = round(days_running,2)
        
        # print the info    
        print "%s - %s - %s - %s - %s - %s - %s - %s days running" % (instance.vpc_id, instance.subnet_id, instance.id, instance.image_id, instance.instance_type, instance.state['Name'], clean_name, days_running)#, instance.launch_time, tag_string)


        #pprint (instance.__dict__)
        #print "this is the {id} ".format(**instance.__dict__)
    
def lambda_handler(event, context):
    print '-------------------------'
    print '----- start -----'
    print ''
    
    # regions = ['us-east-1','us-west-2','us-west-1','eu-west-1','eu-central-1','ap-southeast-1','ap-southeast-2','ap-northeast-1','sa-east-1']
    
    # quicker
    regions = ['ap-southeast-2','ap-northeast-1']

    for region in regions: get_ec2_instances(region)

    print ''
    print '----- end -----'
    print '-------------------------' 
    return 'foo'
    