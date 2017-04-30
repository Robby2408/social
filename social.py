import redis
import time
import ast
import pprint , pickle
import os
import signal

try:
	conn = redis.StrictRedis(
       host='localhost',
       port= 6379,
       db= 0)
	print conn
	conn.ping()
	print 'Connected!'
except Exception as ex:
	print 'Error:',ex
	exit('Failed to connect , terminating .')

	# basic database model for users 
users = {

	"root":{
	 	 "password":"12345",
	 	 "type":{
	 	    "project":{
	 	       "author":"ram",
	 	       "description":"this is my project!",
	 	       "teammembers":['ram','shyam'],
	 	       "likes":0,
	 	       "comments":['Nice Project!']
	 	    },
	 	    "startup":{
	 	        "ceo":"ram",
	 	       "description":"this is my startup!",
	 	       "teammembers":['ram','shyam'],
	 	       "likes":0,
	 	       "comments":['Nice Startup!']
	 	    }
	 	 }
	}


}

def likes(username):
	print "Enter name of the user whose post you want to like "
	name = raw_input()
	pkl_file = open('data.pkl', 'rb')
	users = pickle.load(pkl_file)
	pkl_file.close()
	if name in users:
		print "Enter project or startup name you want to like ?"
		ans = raw_input()
		if ans in users[name]["type"]:
			print ans
			print users[name]["type"][ans]["likes"]
			users[name]["type"][ans]["likes"] = users[name]["type"][ans]["likes"] +1
			output = open('data.pkl', 'wb')
			pickle.dump(users, output)
			output.close()
		else:
			print "Sorry project not found ! Redirecting to dashboard ....."
			dashboard(username)
	else:
		print "Sorry user not found ! Redirecting to dashboard ...."
		dashboard(username)


def comments(username):
	print "Enter name of the user whose post you want to add comment to  "
	name = raw_input()
	pkl_file = open('data.pkl', 'rb')
	users = pickle.load(pkl_file)
	pkl_file.close()
	if name in users:
		print "Enter project or startup name you want to add comment in ?"
		ans = raw_input()
		if ans in users[name]["type"]:
			print "Enter comment !"
			comment = raw_input()
			users[name]["type"][ans]["comments"].append(comment)
			output = open('data.pkl', 'wb')
			pickle.dump(users, output)
			output.close()
		else:
			print "Sorry project not found ! Redirecting to dashboard ....."
			dashboard(username)
	else:
		print "Sorry user not found ! Redirecting to dashboard ...."
		dashboard(username)

#end of users model 
def dashboard(username):
	
	print "***********************************************"
	print "YOU ARE VIEWING DASHBOARD !"
	print "***********************************************"
	pkl_file = open('data.pkl', 'rb')
	users = pickle.load(pkl_file)
	pkl_file.close()
	printall(users)
	print "***********************************************"
	print "Want to like or comment a post ? (1/0) . Reply 2 for Not !"
	print "***********************************************"
	choice = raw_input()
	if choice == '1':
		likes(username)
	elif choice == '0':
		comments(username)
	else:
		print "Opted Nothing !"



def logout():
	
	print "You are going to be logged out in 5 seconds "
	for i in range(1,5):
		print i
		time.sleep(1)
	os.kill(os.getppid(), signal.SIGHUP)

def panel(username):
	print "***********************************************"
	print "WELCOME TO THE SOCIAL PANEL !"
	print "***********************************************"
	print "Enter Choice 1)Upload Project 2)Upload StartUp 3)View Profile 4)View Dashboard   5)Logout \n"

	choice = raw_input("Choice?")
	if choice == '5':
		logout()
	else:
		update(choice,username)
		print "***********************************************\n"


def printall(users):
	for k, v in users.iteritems():
		if isinstance(v, dict):
			printall(v)
		else:
			print "{0} : {1}".format(k, v)

def editpass(username):
	pkl_file = open('data.pkl', 'rb')
	users = pickle.load(pkl_file)
	pkl_file.close()
	newpassword=raw_input("Enter new password :")
	users[username]["password"]=newpassword
	output = open('data.pkl', 'wb')
	pickle.dump(users, output)
	output.close()
	time.sleep(1)
	print "Password Successfully Changed !\n"
	panel(username)

def update(ans,username):
	
	pkl_file = open('data.pkl', 'rb')
	users = pickle.load(pkl_file)
	pkl_file.close()
	print "hello"
	
	print "hello"
	if ans == '1':
		print "hello"
		print "**** POST INCOMPLETE PROJECT ****"
		projectname=raw_input("Enter project name prefixed by word project ")
		author = raw_input('Author ?')
		description = raw_input('Description ?')
		teammembers = raw_input('Enter team members separated by comma (,) :')
		teammembers=teammembers.split(",");
		likeinproject=0
		commentinproject = []
		
		print "Adding Your Project ....... \n"
		print users[username]

		users[username]["type"].update({projectname:{
			 "author":author,
			 "description":description,
			 "teammembers":teammembers,
			 "likes":likeinproject,
			 "comments":commentinproject
			}})
		
		output = open('data.pkl', 'wb')
		pickle.dump(users, output)
		output.close()
		time.sleep(1)
		print "Project successfully added !"
		panel(username)

        	    
	elif ans== '2':
		print "**** POST STARTUP IDEA ****"
		startupname=raw_input("Enter startup name prefixed by word startup ")
		ceo = raw_input('Ceo ?')
		description = raw_input('Description ?')
		teammembers = raw_input('Enter team members separated by comma (,) :')
		teammembers=teammembers.split(",");
		likeinstartup=0
		commentinstartup = []
		
		print "Adding Your Startup idea ....... \n"
		users[username]["type"].update({startupname:{
			 "ceo":ceo,
			 "description":description,
			 "teammembers":teammembers,
			 "likes":likeinstartup,
			 "comments":commentinstartup
			}})
		
		output = open('data.pkl', 'wb')
		pickle.dump(users, output)
		output.close()
		time.sleep(1)
		print "Startup idea successfully added !\n"
		panel(username)
        
	elif ans == '3':
		print "****",username,"'s Profile !! **** \n"
		
        
		print " Your Project and Startup idea Details along with password details are \n "
		for key, value in users.iteritems():
			if username in key:
				for k,v in users[username].iteritems():
					if isinstance(v, dict):
						for k,v in users[username]["type"].iteritems():
							print "{0} => {1}".format(k, v)
					else:
						print "{0} => {1}".format(k, v)


					
		
		print "Edit password ?\n"
		passans = raw_input("1/0 ?")
		if passans == '1':
			editpass(username)
		else:
			panel(username)
			

	elif ans=='4':
		print "Redirecting to dashboard............\n"
		time.sleep(1)
		dashboard(username)
		panel(username)
	else:
		print "Invalid choice!"




def signin():
	print "***********************************************"
	print "WELCOME TO THE SIGN-IN !"
	print "***********************************************"
	print "Enter username: \n"
	username = raw_input()
	print "Enter password : \n"
	password = raw_input()
	
	pkl_file = open('data.pkl', 'rb')
	users = pickle.load(pkl_file)
	
	if username in users:
		print username
		if password == users[username]["password"]:
			print "You have Successfully signed up !\n"
			panel(username)
		else:
			print "Incorrect Password ! Please Login again !\n"
			signin()
	else:
		print "Not Registered ! Go for Signup !\n"
		signup()
	pkl_file.close()
	


def signup():
	print "***********************************************"
	print "WELCOME TO THE SOCIAL PANEL !"
	print "***********************************************"
	print "WELCOME TO THE SIGNUP !"
	print "***********************************************"
	print "Enter username: \n"
	username = raw_input()
	print "Enter password : \n"
	password = raw_input()
	print "Signing Up...\n"
	pkl_file = open('data.pkl', 'rb')
	users = pickle.load(pkl_file)
	pkl_file.close()
	
	
	users.update({username:{}})
	
	
	users[username]["type"]={}
	
	users[username]["password"]=password
	time.sleep(1)
	
	
	
	output = open('data.pkl', 'wb')
	pickle.dump(users, output)
	output.close()
	print "Signed Up successfully !!\n"
	print "Going for signin !\n"

	signin()


def start():
	print "***********************************************"
	print "WELCOME TO THE SOCIAL !"
	print "***********************************************"
	print "Already registered (1) or New User (0) ?"
	ans = raw_input()
	if ans == '1':
		signin()
	elif ans == '0':
		signup()
	else:
		print "Invalid Option!"


start()
