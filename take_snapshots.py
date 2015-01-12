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
            do_volumes(instance.id)


#-----------------------------------------------------------------------------------------------------------
def do_volumes(id):
    volumes = conn.get_all_volumes(filters={'attachment.instance-id': id})
    for volume in volumes:
        if 'Snapshot schedule' in volume.tags:
            print '\tInstance %s Volume id [%s] Schedule (%s) ' % (id, volume.id, volume.tags['Snapshot schedule'])
            snapshots = conn.get_all_snapshots(filters={'volume-id': volume.id})
            if volume.tags['Snapshot schedule'] == 'W':
                expiry=7
            elif volume.tags['Snapshot schedule'] == 'D':
                expiry=1
            #If no snapshots exist take one
            if not snapshots:
                print 'No Snapshot'
            for snapshot in snapshots:
                limit = datetime.now() - timedelta(days=expiry)
                if parser.parse(snapshot.start_time).date() <= limit.date():
                    print '\t\tSnapshot [%s] is older than %s days limit date is %s' % (snapshot.id, expiry, limit.date())
                else:
                    print '\t\tSnapshot [%s] is newer than %s days' % (snapshot.id, expiry)
        else:
            print '\tInstance %s Volume id [%s] has no Snapshot Schedule Tag' % (id, volume.id)



                
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

