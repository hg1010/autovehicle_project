#!/usr/bin/env python

import rospy
from std_msgs.msg import String

# test
if __name__=='__main__':
	try:
		rospy.init_node('hello_ros')
		p = rospy.Publisher('hello', String, queue_size=1)
		r = rospy.Rate(1)
		cnt = 0

		while not rospy.is_shutdown():
			cnt=cnt+1
			msg = 'hello ~%s' %cnt
			print(msg)
			p.publish(msg)
			r.sleep()
			

	except rospy.ROSInterruptException:
		pass


