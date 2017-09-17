#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class ABCNode:
    
    def __init__(self):
        rospy.init_node('ABC')
        rospy.loginfo("ABC init")
        rospy.Subscriber("/cmd_vel", Twist, self.cmdVelCb)
        self.cmd_vel = [0, 0]
        
    def spin(self):
        r = rospy.Rate(20)
        while not rospy.is_shutdown():
            rospy.loginfo_throttle(1, "abc running")
            r.sleep()
            
    def cmdVelCb(self, req):
        x = req.linear.x
        th = req.angular.z
        ## send cmd to gpio here
        logstr =  "get x, z:" + str(x) + ", " + str(th)
        rospy.loginfo_throttle(1, logstr)
            
if __name__ == '__main__':
    try:
        robot = ABCNode()
        robot.spin()
    except rospy.ROSInterruptException:
        pass
