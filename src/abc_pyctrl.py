#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

import RPi.GPIO as GPIO
FORWARD_IN = 16
BACKWARD_IN = 18
LEFT_IN = 24
RIGHT_IN = 22
FORWARD_OUT = 11
BACKWARD_OUT = 7
LEFT_OUT = 5
RIGHT_OUT = 3

class ABCNode:
    
    def __init__(self):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(FORWARD_IN,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(BACKWARD_IN,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(LEFT_IN,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(RIGHT_IN,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	GPIO.setup(FORWARD_OUT,GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(BACKWARD_OUT,GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(LEFT_OUT,GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(RIGHT_OUT,GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

        rospy.init_node('ABC')
        rospy.loginfo("ABC init")
        rospy.Subscriber("/cmd_vel", Twist, self.cmdVelCb)
        self.cmd_vel = [0, 0]
        
    def spin(self):
        r = rospy.Rate(20)
        while not rospy.is_shutdown():
            rospy.loginfo_throttle(1, "abc running")
	    forward_in =  GPIO.input(FORWARD_IN)
	    backward_in = GPIO.input(BACKWARD_IN)
	    left_in = GPIO.input(LEFT_IN)
	    right_in = GPIO.input(RIGHT_IN)
	    infostr = "get input: " + str(forward_in) + ", " + str(backward_in) + ", " + str(left_in) + ", " + str(right_in)
	    rospy.loginfo_throttle(1, infostr)
            r.sleep()
            
    def cmdVelCb(self, req):
        x = req.linear.x
        th = req.angular.z
        ## send cmd to gpio here
	if x > 0:
	    GPIO.output(BACKWARD_OUT,False)
	    GPIO.output(FORWARD_OUT,True)
	elif x < 0:
	    GPIO.output(FORWARD_OUT,False)
	    GPIO.output(BACKWARD_OUT,True)
	else:
	    GPIO.output(FORWARD_OUT,False)
	    GPIO.output(BACKWARD_OUT,False)

	if th > 0:
	    GPIO.output(RIGHT_OUT,False)
	    GPIO.output(LEFT_OUT,True)
	elif th < 0:
	    GPIO.output(LEFT_OUT,False)
	    GPIO.output(RIGHT_OUT,True)
	else:
	    GPIO.output(LEFT_OUT,False)
	    GPIO.output(RIGHT_OUT,False)	

        logstr =  "get x, z:" + str(x) + ", " + str(th)
        rospy.loginfo_throttle(1, logstr)
            
if __name__ == '__main__':
    try:
        robot = ABCNode()
        robot.spin()
    except rospy.ROSInterruptException:
        pass
