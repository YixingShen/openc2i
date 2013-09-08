#!/bin/sh

python RF_Client.py 0x158a00:0xfcf00:SENSOR_JOINED
python RF_Client.py 0x158a00:0xfcf00:ALERT:Motion,PIR1
python RF_Client.py 0x158a00:0xfcf00:SENSOR_LOCATION:3334.4924,07306.5569,0.1111
#sleep 10
python RF_Client.py 0x158a00:0xfcf11:SENSOR_JOINED
python RF_Client.py 0x158a00:0xfcf11:ALERT:Vibration,VX1
python RF_Client.py 0x158a00:0xfcf11:SENSOR_LOCATION:3334.6124,07306.10169,0.1111
#sleep 10
python RF_Client.py 0x158a00:0xfcf22:SENSOR_JOINED
python RF_Client.py 0x158a00:0xfcf22:ALERT:Vibration,VX2
python RF_Client.py 0x158a00:0xfcf22:ALERT:Motion,PIR1
python RF_Client.py 0x158a00:0xfcf22:ALERT:Vibration,VX4
python RF_Client.py 0x158a00:0xfcf22:ALERT:Motion,PIR3
python RF_Client.py 0x158a00:0xfcf22:SENSOR_LOCATION:3334.6924,07306.9969,0.1111
#sleep 10
python RF_Client.py 0x158a00:0xfcf33:SENSOR_JOINED
python RF_Client.py :ALERT:Motion,PIR2
python RF_Client.py 0x158a00:0xfcf33:SENSOR_LOCATION:3334.7924,07306.9969,0.1111
sleep 10
python RF_Client.py 0x158a00:0xfcf44:SENSOR_JOINED
python RF_Client.py 0x158a00:0xfcf44:ALERT:Motion,PIR3
python RF_Client.py 0x158a00:0xfcf44:SENSOR_LOCATION:3334.8924,07306.9969,0.1111
sleep 10
python RF_Client.py 0x158a00:0xfcf55:SENSOR_JOINED
python RF_Client.py 0x158a00:0xfcf55:ALERT:Motion,PIR4
python RF_Client.py 0x158a00:0xfcf55:SENSOR_LOCATION:3334.9924,07306.9969,0.1111
sleep 10
python RF_Client.py 0x158a00:0xfcf66:SENSOR_JOINED
python RF_Client.py 0x158a00:0xfcf66:ALERT:Motion,PIR1
python RF_Client.py 0x158a00:0xfcf66:ALERT:Motion,PIR2
python RF_Client.py 0x158a00:0xfcf66:ALERT:Motion,PIR4
sleep 10
python RF_Client.py 0x158a00:0xfcf77:SENSOR_JOINED
python RF_Client.py 0x158a00:0xfcf77:ALERT:Vibration,VX3
python RF_Client.py 0x158a00:0xfcf77:SENSOR_LOCATION:3334.1204,07306.9969,0.1111
