#!/usr/bin/python
import boto
import boto.ec2

#-----------------------------------------------------------------------------------------------------------
def get_instances():
    reservations = conn.get_all_instances()
    for reservation in reservations:
        for instance in reservation.instances: 
            if 'Name' in instance.tags:
                print "%s (%s) [%s]" % (instance.tags['Name'], instance.id, instance.state)
            else:
                print "Instance %s [%s] has no Name tag" % (instance.id, instance.state)
                question = "Assign a Name Tag? "
                if get_answer(question) == "Yes":
                    tag_instance(instance.id,instance)
        volumes = conn.get_all_volumes(filters={'attachment.instance-id': instance.id})
        for volume in volumes:
            print 'Volume id [%s] size %s ' % (volume.id, volume.size )


#-----------------------------------------------------------------------------------------------------------
def tag_instance(id,instance):
    print "Please enter name for instance [%s] " % (id)
    instance_name = raw_input(prompt)
    question = "Write Name tag [%s] to instance_name [%s]" % (instance_name, id)
    if get_answer(question) == "Yes":
        instance.add_tag("Name",instance_name)
        print "Instance tagged"
#-----------------------------------------------------------------------------------------------------------
def get_answer(question):
    while True:
        print question
        answer = raw_input(prompt)
        if answer.lower() == "y":
            return "Yes"
            break
        elif answer.lower() == "n":
            return "No"
            break
        else:
            print "Please answer Y or N"

#MAIN-------------------------------------------------------------------------------------------------------

prompt = '=> '
for region in boto.ec2.regions():
    #print ("%s "  % region.name )
    conn = region.connect()
    if region.name == 'ap-southeast-1' or region.name == "cn-north-1" or region.name == "us-gov-west-1":
        print "Skipping Region ",region.name
        next
    else:
        print "Checking Region ",region.name
        get_instances()
print "Done"

