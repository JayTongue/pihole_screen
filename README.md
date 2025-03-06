# Pihole Screen
---------------------------
This is some quick and easy CircuitPython code for displaying PiHole stats on an LCD1602 display with the Adafruit character LCD library. 

![](screen_demo.jpg)

Stats are obtained via using the PiHole's API and authenticating with the password. The given session ID and CSRF tokens are then used to grab data from relevant endpoints. This is easy to call from a cronjob at your desired interval. 

The PiHole image is made by creating four custom characters which are defined by a binary pattern. 
