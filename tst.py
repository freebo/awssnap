import boto3
import boto3.ec2

rds = boto3.client('rds')

for region in boto3.ec2.regions():
    conn = region.connect()
    if region.name != 'ap-southeast-2':
        print 'Skipping Region ',region.name
        next
    else:
        print 'Checking Region ',region.name
        print 'Done'
