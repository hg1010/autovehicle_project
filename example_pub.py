#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def simple_pub():
	rospy.init_node('simple_pub', anonymous=True)
	pub = rospy.Publisher('hi', String, queue_size=10)
	rate = rospy.Rate(1)

	while not rospy.is_shutdown():
		str = 'hi %s' %rospy.get_time()
		pub.publish(str)
		rate.sleep()

if __name__=='__main__':
	try:
		simple_pub()
	except rospy.ROSInterruptException:
		pass
