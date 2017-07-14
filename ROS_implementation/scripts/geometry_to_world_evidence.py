#!/usr/bin/env python

# this is the service to transform a 3D point to a WorldEvidence 
# message
import rospy
from beginner_tutorials.srv import *
from wire_msgs.msg import WorldEvidence
from wire_msgs.msg import ObjectEvidence
from wire_msgs.msg import Property


def callback(data):
    
    worldev = WorldEvidence()
    worldev.header.stamp = rospy.Time.now()
    # set the worldevidence frame to the camera frame to see
    # the visualization from the perspective of the Kinect.
    worldev.header.frame_id = "camera_rgb_optical_frame"

    list_objev = []

    # make a list of all object evidences. One object evidence has 
    # two properties a position with covariance and a class label 
    # with a discrete probability. 

    # This class label is not used here but is added for proper use 
    # in the future.

    for point_seq in data.points:
        objev = ObjectEvidence()
        obj_props = Property()
        obj_props.attribute = "position"
        obj_props.pdf.type = 1
        obj_props.pdf.dimensions = 3
        obj_props.pdf.data = [1.0, point_seq.point.x, 
        point_seq.point.y, point_seq.point.z, 
        0.01, 0.0, 0.0, 0.01, 0.0, 0.01]
        obj_props2 = Property()
        obj_props2.attribute = "class_label"
        obj_props2.pdf.type = 5
        obj_props2.pdf.dimensions = 1
        obj_props2.pdf.domain_size = -1
        obj_props2.pdf.values = ["face"]
        obj_props2.pdf.probabilities = [1]

        objev.properties = [obj_props, obj_props2]
        list_objev.append(objev)

    worldev.object_evidence = list_objev

    return Geometry_msgs_to_world_evidenceResponse(worldev)

def geometry_to_world_evidence():
    rospy.init_node('geometry_test_server')
    rospy.Service('geometry_to_world_evidence', 
    	Geometry_msgs_to_world_evidence, callback) 

    print "Starting"
    rospy.spin()

if __name__ == "__main__":
    geometry_to_world_evidence()

