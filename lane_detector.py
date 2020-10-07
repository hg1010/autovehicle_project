#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import os, rospkg
import json

from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridgeError
from std_msgs.msg import Float64

class IMGParser:
	def __init__(self):
		rospy.init_node('lane_detector', anonymous=True)	
		#self.image_sub = rospy.Subscriber("/usb_cam/image_raw/compressed", CompressedImage, self.callback)

		self.offset_pub = rospy.Publisher('/offset', Float64, queue_size=1)
		self.image_sub = rospy.Subscriber("/image_jpeg/compressed", CompressedImage, self.callback)
		
		self.offset_msg = Float64()
		self.offset = None

		self.img_wlane = None
	
		self.point_weight = None
		self.point_height = None

		self.left_weight_circle = None
		self.left_height_circle = None

		self.right_weight_circle = None
		self.right_height_circle = None
		self.center_weight = None

		self.img_bgr = None

		rate = rospy.Rate(20)

		while not rospy.is_shutdown():
			if self.img_wlane is not None:

				self.offset_pub.publish(self.offset_msg)
				
				cv2.circle(self.img_bgr, (self.left_weight_circle,self.left_height_circle),3,(255,255,0),5)
				cv2.circle(self.img_bgr, (self.right_weight_circle,self.right_height_circle),3,(255,0,255),5)
				cv2.circle(self.img_bgr, (self.center_weight,self.right_height_circle),3,(0,255,255),5)

				cv2.imshow("canvas", self.img_bgr)
				cv2.waitKey(1)

			rate.sleep()

	def callback(self, msg):
		np_arr=np.fromstring(msg.data, np.uint8)
		self.img_bgr=cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

		height = self.img_bgr.shape[0]
		weight = self.img_bgr.shape[1]

		self.point_weight = weight / 2
		self.point_height = height * 4/5

		img_gray = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2GRAY)
		
		ret, self.img_wlane = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		
		#self.img_wlane[height][weight]

		while self.point_weight > 0:
			if self.img_wlane[self.point_height][self.point_weight] == 0:
				self.point_weight = self.point_weight - 1
			else:
				break

		self.left_height_circle = self.point_height
		self.left_weight_circle = self.point_weight

		self.point_weight = weight / 2

		while self.point_weight < weight:
			if self.img_wlane[self.point_height][self.point_weight] == 0:
				self.point_weight = self.point_weight + 1
			else:
				break
			
		self.right_height_circle = self.point_height
		self.right_weight_circle = self.point_weight

		self.center_weight = (self.right_weight_circle + self.left_weight_circle) / 2

		self.offset_msg.data = (weight/2) - self.center_weight

if __name__ == '__main__':
	try:
		image_parser = IMGParser()
	except rospy.ROSInterruptException:
		pass



