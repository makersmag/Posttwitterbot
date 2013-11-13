#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep
import os
import picamera
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


# Define Email function...
def emailme():
   # Define these once; use them twice!
		from_string = 'Home <myhouse@gmail.com>' # change this to the email address you want your messages sent from
		to_string = 'you@yourdomain.com' # change this to the email address attached to your IFTTT account

		# Create the root message and fill in the from, to, and subject headers
		root_message = MIMEMultipart('related')
		root_message['Subject'] = 'You have post!'
		root_message['From'] = from_string
		root_message['To'] = to_string
		root_message.preamble = 'This is a multi-part message in MIME format.'

		# Encapsulate the plain and HTML versions of the message body in an
		# 'alternative' part, so message agents can decide which they want to display.
		alternative_message = MIMEMultipart('Post, post, post.')
		root_message.attach(alternative_message)

		message_text = MIMEText('You have post')
		alternative_message.attach(message_text)

		# We reference the image in the IMG SRC attribute by the ID we give it below
		message_text = MIMEText('<b>Woo!</b> <br><br><img src="cid:image1">', 'html')
		alternative_message.attach(message_text)

		# identifying that we want to use 'post.jpg' as our image.
		fp = open('post.jpg', 'rb')
		message_image = MIMEImage(fp.read())
		fp.close()

		# Define the image's ID as referenced above
		message_image.add_header('Content-ID', '<image1>')
		root_message.attach(message_image)

		# Send the email
		username = 'myhouse@gmail.com'
		password = 'password'
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(username,password)
		server.sendmail(from_string, to_string, root_message.as_string())
		server.quit()
		print "Email Sent!"


# Setting up the microswitch
letterPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(letterPin,GPIO.IN) # Set this pin to an INPUT (a switch is an input, we are waiting for it to do something. An LED would be an output, we are telling it to do something)


#Script is set up and ready to go...
print "Waiting for post"
while True:
		if ( GPIO.input(letterPin) == False ): # if the switch is pressed....
				print "Button Pressed..."
				print "Waiting one minute for the postperson to put the letters through"
				sleep(60) # Wait for the postperson to put the letters through
				while True:
						if ( GPIO.input(letterPin) == True ): # if the switch is now unpressed
								print "Button released..."
								sleep(2) # wait for 2 seconds to give the postperson a chance to get the letter through the letterbox, and for the letter to land
								os.system("raspistill -w 600 -h 450 -o /home/pi/Raspberry-Pi-Twitter-Postbox/post.jpg") # take a photo and save it as 'post.jpg' in the Raspberry-Pi-Twitt$
								print "Photo taken.."
								emailme() # call the email function
								break
