#!/usr/bin/python
import boto
import boto.ec2
from datetime import timedelta, datetime 
from dateutil import parser
import pytz

#-----------------------------------------------------------------------------------------------------------
def get_instances():
    reservations = conn.get_all_instances()
    for reservation in reservations:
        for instance in reservation.instances: 
            print
            if 'Name' in instance.tags:
                print 'Instance %s [%s] (%s)' % (instance.tags['Name'], instance.id, instance.state)
            else:
                print 'Instance %s [%s] has no Name tag' % (instance.id, instance.state)
                question = 'Assign a Name Tag? '
                if get_answer(question) == 'Yes':
                    tag_instance(instance.id,instance)
        get_volumes(instance.id)


#-----------------------------------------------------------------------------------------------------------
def get_volumes(id):
    volumes = conn.get_all_volumes(filters={'attachment.instance-id': id})
    for volume in volumes:
        if 'Snapshot schedule' in volume.tags:
            print '\tVolume id [%s] Schedule (%s) ' % (volume.id, volume.tags['Snapshot schedule'])
        else:
            print '\tVolume id [%s] has no Snapshot Schedule Tag' % (volume.id)
            question = 'Assign a Snapshot Scedule? '
            if get_answer(question) == 'Yes':
                print "Please Select (W)eekly or (D)aily"
                schedule = raw_input(prompt)
                volume.add_tag('Snapshot schedule', schedule)
            else:
                break

        snapshots = conn.get_all_snapshots(filters={'volume-id': volume.id})

        if volume.tags['Snapshot schedule'] == 'W':
            expiry=7
        elif volume.tags['Snapshot schedule'] == 'D':
            expiry=1

        for snapshot in snapshots:
            limit = datetime.now() - timedelta(days=expiry)
            if parser.parse(snapshot.start_time).date() <= limit.date():
                print 'Snapshot [%s] is older than %s days' % (snapshot.id, expiry)
                
#-----------------------------------------------------------------------------------------------------------
def tag_instance(id,instance):
    print 'Please enter name for instance [%s] ' % (id)
    instance_name = raw_input(prompt)
    question = 'Write Name tag [%s] to instance_name [%s]' % (instance_name, id)
    if get_answer(question) == 'Yes':
        instance.add_tag('Name',instance_name)
        print 'Instance tagged %s' % (instance_name)
#-----------------------------------------------------------------------------------------------------------
def get_answer(question):
    while True:
        print question
        answer = raw_input(prompt)
        if answer.lower() == 'y':
            return 'Yes'
            break
        elif answer.lower() == 'n':
            return 'No'
            break
        else:
            print 'Please answer Y or N'

#MAIN-------------------------------------------------------------------------------------------------------

#today = datetime.date.today()

prompt = '=> '
for region in boto.ec2.regions():
    conn = region.connect()
    #if region.name == 'ap-southeast-1' or region.name == 'cn-north-1' or region.name == 'us-gov-west-1':
    if region.name != 'ap-southeast-2':
        print 'Skipping Region ',region.name
        next
    else:
        print 'Checking Region ',region.name
        get_instances()
print 'Done'

