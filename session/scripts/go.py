#!/usr/bin/env python3


from cmath import atan
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


x = 5.544445
y = 5.544445
theta = 0
beta = rospy.get_param("/beta")
x_goal = rospy.get_param("/x_goal")
y_goal = rospy.get_param("/y_goal")
phai = rospy.get_param("/phai")




def pose_callback(data):

	global x, y, theta
	x = data.x
	y = data.y
	theta = data.theta
	

def go():
	global x, y, theta, x_goal, y_goal
	pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
	rospy.init_node('veloctiy', anonymous=True)
	rate = rospy.Rate(10) 
	rospy.Subscriber("/turtle1/pose", Pose, pose_callback)
	print("Controller has been initialized")
	
	while not rospy.is_shutdown():
		delta_x = x_goal - x
		delta_y = y_goal - y
		vel = Twist()
		vel_x = (beta * math.sqrt((delta_x ** 2) + (delta_y ** 2)))
		vel_z = (phai * ( (-theta) + math.atan2(delta_y , delta_x)))
		vel.linear.x = vel_x
		vel.linear.y = 0
		vel.linear.z = 0
		vel.angular.x= 0
		vel.angular.y = 0
		vel.angular.z = vel_z
		
		if abs(delta_x) < 0.01 and abs(delta_y) < 0.01:
			vel.linear.x = 0
			vel.angular.z = 0
			print("Turtle has reached its destination")
			pub.publish(vel)
			print("Type F if you want to exit the controller")
			x_goal = (input('Entered desired x goal coordinate  '))
			if x_goal == 'F' or x_goal == 'f':
				exit()
			x_goal = float(x_goal)	
			y_goal = float(input('Entered desired y goal coordinate  '))
			


		pub.publish(vel)	
		rate.sleep()



if __name__ == '__main__':
	try:
		go()
	except rospy.ROSInterruptException:
		pass


