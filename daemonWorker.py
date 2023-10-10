# script that executes the latest download

import os
import glob
import subprocess
import datetime
import time


def work(timeWait, sattelite, resLevel):

	os.chdir("\image")

	# main loop, download the image and move + rename for the webserver
	while(True):
		# download the image using slider cli
		subprocess.call("./slider-cli --satellite=" + sattelite + " --sector=full-disk --product=geocolor -i 1 -z " + resLevel + " -f png")
		
		# rename the old image with the current timestamp (yes they are offset by 10 mins)
		now = datetime.datetime.now()
		if (os.path.isfile("latest.png")):
			os.rename("latest.png", now + "_previous.png")
		
		for file in glob.glob("cira*.png"):
    		 os.rename(file, "latest.png")
		
		# wait 10 mins for the next image to come avaliable
		time.sleep(timeWait * 10)

