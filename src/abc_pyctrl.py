#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def abc_control():
    rospy.init_node('abc_pyctrl', anonymous=True)
    pub = rospy.Publisher('test', String, queue_size=10)
    
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        abc_control()
    except rospy.ROSInterruptException:
        pass
