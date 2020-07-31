#!/usr/bin/env python

import rospy
import serial

from std_msgs.msg import String
import subprocess
import os
"""
Folder w ktorym uruchamiany jest skrypt
"""
path = os.path.dirname(os.path.abspath(__file__))
 
"""
Poszukaj adresu konwertera USB 
 """
port_def = subprocess.check_output([path +"/find_usb.bash"], shell=True)
port_def = port_def.strip()

while(port_def==""):
    print("USB UART not found! Press enter to search again")
    raw_input('')
    port_def = subprocess.check_output([path +"/find_usb.bash"], shell=True)
    port_def = port_def.strip()
print("Found USB UART converter on port: " + port_def)   
rospy.loginfo('Starting node') 
    
    
"""
    @brief Funkcja zwrotna, która wysyła komendę do odtwarzacza DFR0534
    @param[in] message: Otrzymana wiadomos typu String
    p*:odtwarzaj dzwiek gdzie * to ID dzwieku
    v*: ustaw glosnosc, gdzie * to poziom glosci [0,30]
    s: zatrzymaj odtwarzanie
    @param[in] port: Port USB UART do ktorego podlaczony jest konwerter
"""
def callback(message, port = port_def):
    code = ""
    ser = serial.Serial(port)  # open serial port
    message = str(message)
    message = message.replace('data: "', '')
    message = message.replace('"', '')
    try:
        if(message[0] == 'p'):
            code = bytearray([0xAA, 0x07, 0x02, 0x00, int(message[1:]), int(message[1:])+0xB3])
            rospy.loginfo('Playing sound: %s on port: %s', message[1:], port)   
            pass
        if(message[0] == 'v'):
            code = bytearray([0xAA, 0x13, 0x01, int(message[1:]), int(message[1:])+0xBE])
            rospy.loginfo('Setting volume to: %s on port: %s', message[1:], port)
        if(message[0] == 's'):
            code = bytearray([0xAA, 0x04, 0x00, 0xAE])
            rospy.loginfo('Stopping sound on port: %s', port)
    except: 
        print('Unknown command')
    ser.write(code)
    ser.close()

"""
    @brief Funkcja nasłuchujaca inicjujaca node ''listener' i tworzaca topic 'sound_listener'
"""
def listener():
    rospy.Subscriber('sound_listener', String, callback)
    rospy.init_node('listener', anonymous=True)
    rospy.spin()

if __name__ == '__main__':
    listener()