#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from sensor_msgs.msg import RegionOfInterest
from geometry_msgs.msg import PointStamped
from image_recognition_msgs.srv import Recognize
from image_recognition_msgs.msg import Recognition
from wire_msgs.msg import WorldEvidence
from rgbd.srv import Project2DTo3D
from beginner_tutorials.srv import *

srv = None
srv2 = None
srv3 = None
pub = None

def callback(data):

    try:
        # transforms the image to an ROIs
        resp = srv(image=data)
        # initialize time that is needed to transform a 2D roi to a 3D point 
        # because it also uses the depth info of the kinect image at 
        # the time that the roi is send.
        time = rospy.get_rostime()
        a=[]
        # to make a list of all ROIs
        for test in resp.recognitions:
            a.append(test.roi)
        
        # 2D roi to 3D point service    
        resp2 = srv2(time, a)
        point=resp2.points

        # from a 3D point to a message in WorldEvidence format --> 
        # a format that wire can use for the PMHA.
        resp3 = srv3(point)
        pub.publish(resp3.ev)
    except IndexError, e:
        print e
        rospy.logerr("Service call failed: %s" % e)

    return 1
    
def listener():
    # define all services, subscribers and publishers
    global srv
    global srv2
    global srv3
    global pub

    rospy.init_node('listener', anonymous=True)
    rospy.wait_for_service('/recognize')
    rospy.wait_for_service('project_2d_to_3d')
    rospy.wait_for_service('geometry_to_world_evidence')

    rospy.Subscriber("/camera/rgb/image_rect_color", Image, callback, queue_size=1, buff_size=999999999)

    srv = rospy.ServiceProxy('/recognize', Recognize)
    srv2 = rospy.ServiceProxy('project_2d_to_3d', Project2DTo3D)
    srv3 = rospy.ServiceProxy('geometry_to_world_evidence', Geometry_msgs_to_world_evidence)

    pub = rospy.Publisher("/world_evidence", WorldEvidence, queue_size=10)

    rospy.spin()

if __name__ == '__main__':
    listener()
