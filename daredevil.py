import boto3
from pprint import pprint


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


def get_ec2_instances(region):

    print ''
    print "REGION: %s" % (region)
    print '-----------------------'

    ec2 = boto3.resource('ec2', region_name=region)

    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running','pending','stopped']}])
    for instance in instances:

        # nicer structures
        tag_dict = make_tag_dict(instance)
        tag_string = make_tag_string(instance)
        
        # clean the name
        if 'Name' in tag_dict:
            clean_name = tag_dict['Name']     
        else:
            clean_name = '<no-name>'
        
        # print the info    
        print "%s - %s - %s - %s - %s - %s - %s" % (instance.vpc_id, instance.subnet_id, instance.id, instance.image_id, instance.instance_type, instance.state['Name'], clean_name)#, instance.launch_time, tag_string)
        
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