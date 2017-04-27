import redis
import time

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
#end of users model 
def dashboard():
	users = conn.hgetall("users")
	printall(users)



def printall(users):
	for k, v in users.iteritems():
		if isinstance(v, dict):
			printproject(v)
		else:
			print "{0} : {1}".format(k, v)



def update(ans,username):
	users = conn.hgetall("users")
	if ans == 1:
		print "**** POST INCOMPLETE PROJECT ****"
		projectname=raw_input("Enter project name prefixed by word project ")
		author = raw_input('Author ?')
		description = raw_input('Description ?')
		teammembers = raw_input('Enter team members separated by comma (,) :')
		teammembers=teammembers.split(",");
		likeinproject=0
		commentinproject = []
		
		print "Adding Your Project ....... \n"
		users[username]["type"].update({projectname:{
			 "author":author,
			 "description":description,
			 "teammembers":teammembers,
			 "likes":likeinproject,
			 "comments":commentinproject
			}})
		conn.hmset("users",users)
		time.sleep(1)
		print "Project successfully added !"

        # users[username]["type"]["project"]["author"]=author
        # users[username]["type"]["project"]["description"]=description
        # users[username]["type"]["project"]["teammembers"]=teammembers
        # users[username]["type"]["project"]["likes"]=likeinproject
        # users[username]["type"]["project"]["comments"]=commentinproject	    
	elif ans== 2:
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
		conn.hmset("users",users)
		time.sleep(1)
		print "Startup idea successfully added !\n"
        # users[username]["type"]["startup"]["author"]=author
        # users[username]["type"]["startup"]["description"]=description
        # users[username]["type"]["startup"]["teammembers"]=teammembers
        # users[username]["type"]["startup"]["likes"]=likeinstartup
        # users[username]["type"]["startup"]["comments"]=commentinstartup
	elif ans == 3:
		print "****",username,"'s Profile !! **** \n"
		

		print "**** Your Project and Startup idea Details along with password details are \n ****"

		for key, value in users.iteritems():
			if username in key:
				for k,v in users[username].iteritems():
					print k,v
					print "\n"
		# if(users[username]["type"]["project"]==""):
		# 	print "No Projects to show !"
		# else:
		# 	print "Author : ",users[username]["type"]["project"]["author"]
  #           print "Description : ",users[username]["type"]["project"]["description"]
  #           print "Team-members : ",users[username]["type"]["project"]["teammembers"]
  #           print "Likes : ",users[username]["type"]["project"]["likes"]
  #           print "Comments : ",users[username]["type"]["project"]["comments"]
        
  #       print "**** Your Startup idea Details ****"
		# if(users[username]["type"]["startup"]==""):
		# 	print "No Startup Idea to show !"
		# else:
		# 	print "CEO : ",users[username]["type"]["startup"]["ceo"]
  #           print "Description : ",users[username]["type"]["startup"]["description"]
  #           print "Team-members : ",users[username]["type"]["startup"]["teammembers"]
  #           print "Likes : ",users[username]["type"]["startup"]["likes"]
  #           print "Comments : ",users[username]["type"]["startup"]["comments"]


        # print "Your Password :",users[username]["password"]
		print "Edit password ?\n"
		ans = raw_input("1/0 ?")
		if ans == 1:
			newpassword=raw_input("Enter new password :")
			users[username]["password"]=password
			conn.hmset("users",users)
			time.sleep(1)
			print "Password Successfully Changed !\n"
	elif ans==4:
		print "Redirecting to dashboard............\n"
		time.sleep(1)
		dashboard()




def signin():
	print "Enter username: \n"
	username = raw_input()
	print "Enter password : \n"
	password = raw_input()
	# currentuser = conn.get(username)
	users = conn.hgetall("users")
	if username in users:
		if password == users[username]["password"]:
			print "You have Successfully signed up !\n"
			print "Enter Choice 1)Upload Project 2)Upload StartUp 3)View Profile 4)View Dashboard \n"
			choice = raw_input("Choice?")
			update(choice,username)
		else:
			print "Incorrect Password ! Please Login again !\n"
			signin()
	else:
		print "Not Registered ! Go for Signup !\n"
		signup()
	


def signup():
	print "Enter username: \n"
	username = raw_input()
	print "Enter password : \n"
	password = raw_input()
	print "Signing Up...\n"
	# conn.set(username,password)
	users[username]={}
	users[username]["password"]=password
	time.sleep(1)
	conn.hmset("users",users)
	print "Signed Up successfully !!\n"
	print "Going for signin !\n"

	signin()


# def dashboard():



signup()


     