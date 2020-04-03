import sys
import subprocess
import os

def bashc(cmd): #function which will execute a bash command.
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')

def help(): #display the help menu if the arguments are incorrect
	print("This tool uses the apache2 webserver to communicate with a device through the network.") 
	print("It is in plain text and one way. Super simple code and not the most secure.")
	print("Usage: ", sys.argv[0], " [command to send to other system]")
	sys.exit(0)

if __name__ == '__main__': #main function
	
	if os.geteuid() != 0: #perform a user check to see if the script is run as root.
    		exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
	
	if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) == 1:
		help()

	commandArray = []
	i = 0
	while i < (len(sys.argv) - 1):
		try:
			commandArray.append(sys.argv[i + 1])
			commandArray.append(" ")
		except Exception as e:
			print(e)
		i += 1

	commandArray[len(commandArray) - 1] = ""
	commandWord = "".join(commandArray)
	print("Commands to be written are: ", commandWord)
	bashc('cd / && touch /var/www/html/commands.txt')
	print("DEBUG: changed directory to / and made sure commands.txt was available.")
	bashc('service apache2 start')
	print("DEBUG: started the apache2 web server")
	
	with open("/var/www/html/commands.txt", 'w') as file:
		try:
			file.write(commandWord)
		except Exception as e:
			print("ERROR: unable to write commands to local file: /var/www/html/commands.txt")
			print(e)
			sys.exit(0)
	print("DEBUG: successfully wrote commands to text file.")
