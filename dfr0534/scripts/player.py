#!/usr/bin/env python

import rospy
from std_msgs.msg import String

"""
    @brief Function sends given message to ''sound_listener' topic
    @param[in] message: Given message of type string
"""

def send_message(message):
    pub = rospy.Publisher('sound_listener', String, queue_size=10) 
    rospy.loginfo('Sending message: %s', message)
    pub.publish(message)
"""
    @brief Main function of program, getting input from console and sending it further
"""

if __name__ == '__main__':
    message = ""
    rospy.init_node('sound_player', anonymous=True) 
    send_message('')
    while(message != 'q'):
        try:
            print('Sound player for DFR0534')    
            message = raw_input("Choose an option (type help for more info) ")
    
            if(message[0] == 'h'):
                print('\n type:')
                print('p* -- to play sound where * is track number')
                print('v* -- to set volume, where * is volume level[0, 30]')
                print('s -- to stop playback')
                print('q -- to quit \n')
            elif(message[0] == 'q'):
                pass
            else:
                send_message(message)
        except:
            print('Something went wrong!')