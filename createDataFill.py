
import random

# Insert into profile values('JAMES1997','JAMES','SMITH','JAMES.SMITH@nyu.edu','SEMAJ7991','1997-10-5','2017-11-4 22:6:47');


# create table messages{
# 	msgID: varchar(20),
# 	fromUserID: varchar(20),
# 	toUserID: varchar(20),
# 	toGroupID: varchar(20),
# 	message: varchar(200),
# 	dateSent: timestamp,


# 400 messages 

readFriends = open("SQL/insertFriends.sql","r")
f = open("insertMessages.txt", "w+")

# Insert into friends values('JAMES1997','JOHN1995','2014-11-6','JOHN1995 has accepted your friend request.');

# for i in range(300):
	# userID1 = readLastNames.readline()

	# userID1 = userID1.split("'")[1]
	# userID1 = userID1.split("'")[0]

	# line = readFriends.readline()
	# linecut = line.split("'", 1)[1]
	# toUserID = linecut.split("'")[0]
	# lc2 = linecut.split("'", 1)[1]
	# lc3 = lc2.split("'", 1)[1]
	# fromUserID = lc3.split("'", 1)[0]

	# msgID = fromUserID + toUserID + str(random.randint(0,1000))

	# toGroupID = 'NULL'

	# message = "Welcome to the group! Thanks for joining!"


	# lineFirst = lineFirst.split(',')[0];
	# yearOfBirth = random.randint(2014,2018)
	# monthOfBirth = random.randint(1,12)
	# dayOfBirth = random.randint(1,28)
	# DOB = str(yearOfBirth) + '-' + str(monthOfBirth) + '-' + str(dayOfBirth)
	# message = userID2 + " has accepted your friend request."
	# userID = lineFirst + str(yearOfBirth)
	# email = lineFirst + "." + lineLast + "@nyu.edu"
	# password = lineFirst[::-1] + str(yearOfBirth)[::-1]

	# lastlogin = str(random.randint(2016,2018)) + '-' + str(random.randint(1,12)) + '-' + str(random.randint(1,28)) + ' ' + str(random.randint(0,23)) + ":" + str(random.randint(0,60)) + ":" + str(random.randint(0,60)) 
	# f.write("Insert into messages values('" + msgID + "','" + fromUserID + "','" + toUserID + "','" + toGroupID +  "','" + message + "','" + lastlogin + "');" '\n')

f.write("-- Inserting group messages" '\n') # add a comment in insertMessages.sql

readGroups = open("SQL/insertGroups.sql","r")

# Create group members
insertMembers = open("Extras/insertGroupMembers.txt", "w")
lines = open("SQL/insertFriends.sql").read().splitlines()

# Add members for each of the 25 groups
for i in range(25):
	# get group ID
	line = readGroups.readline()
	linecut = line.split("'", 1)[1]
	gID = linecut.split("'", 1)[0]
	lc2 = linecut.split("'", 1)[1]
	lc3 = lc2.split("'", 1)[1]
	lc4 = lc3.split("'", 1)[1]
	lc5 = lc4.split("'", 1)[1]
	limit = int(lc5.split("'", 1)[0])

	for i in range(limit - random.randint(0, limit)):
		# get a random user ID
		line = random.choice(lines)
		linecut = line.split("'", 1)[1]
		userID = linecut.split("'", 1)[0]
		if i == 0:
			insertMembers.write("Insert into groupMembership values('" + gID + "','" + userID + "','" + "Manager" + "');" '\n')
		else:
			insertMembers.write("Insert into groupMembership values('" + gID + "','" + userID + "','" + "Member" + "');" '\n')

# Insert group messages
readGroupMembers = open("SQL/insertGroupMembers.sql", "r")
GroupMembersLines = open("SQL/insertGroupMembers.sql").read().splitlines()

# Create 200 group messages: average 8 message per group.
for i in range(200):
	line = random.choice(GroupMembersLines)
	# l = readGroupMembers.readline()
	linecut = line.split("'", 1)[1]
	toGroupID = linecut.split("'", 1)[0]
	lc2 = linecut.split("'", 1)[1]
	lc3 = lc2.split("'", 1)[1]
	fromUserID = lc3.split("'", 1)[0]

	msgID = fromUserID + toGroupID + str(random.randint(0, 1000))

	toUserID = "NULL"

	message = "This is a group message " + str(i) + "."

	lastlogin = str(random.randint(2016,2018)) + '-' + str(random.randint(1,12)) + '-' + str(random.randint(1,28)) + ' ' + str(random.randint(0,23)) + ":" + str(random.randint(0,59)) + ":" + str(random.randint(0,59))
	f.write("Insert into messages values('" + msgID + "','" + fromUserID + "','" + toUserID + "','" + toGroupID +  "','" + message + "','" + lastlogin + "');" '\n')


readFriends.close()
readGroups.close()
readGroupMembers.close()
f.close()

















# clubs = ['advocacy', 'anchorage society', 'africa global', 'blockchain collective','BPM', 
# 'capoeira club', 'catholic community', 'chinese culture club', 'discovr', 'ecoherence', 'equestrian', 
# 'hackad', 'marketing', 'oh shoot!', 'paused: videogame society', 'spacious', 'strip club', 
# 'students for justice in palestine', 'design collective', 'tower of babel', 'veggie might',
# 'weSTEM', 'woodworking', 'coffee collective', 'tashan', 'outed: outdoor sig']

# desc = ['ADvocacy is a student group committed to social justice and provision of humanitarian assistance to marginalized communities throughout Abu Dhabi.',
# 'A safe place where students of all sexual orientations and gender expressions can come to teach, learn, and dialogue. Devoted to the principles of respect, social equality, and inclusion.',
# 'At Africa Global, we celebrate our wonderfully diverse mosaic of cultural identities and heritage across the continent and its diaspora, but more importantly we hope to help bring about new friendships, consolidate already existing ones and have semesters full of learning, fun and meaningful events. ',
# 'Blockchains are the future. Here at Blockchain Collective we aim to educate ourselves and get ahead with the world that is dynamically changing to adapt this innovation.',
# 'BPM is a place for members of the NYUAD community who share a passion for DJing to practice their art.',
# 'Capoeira is an Afro-Brazilian martial art which incorporates elements of dance and acrobatics.',
# 'The Catholic SIG aims to create a community that strengthens spiritual Catholic life and faith through prayer, dialogue and understanding of Catholicism, and apostolate.',
# 'This club is dedicated to promoting the Chinese culture among the NYU Abu Dhabi community.',
# 'We are a SIG devoted to learning and promoting Virtual Reality (VR) and Augmented Reality(AR) technologies through research and development. ',
# 'Ecoherence transforms the wider NYU Abu Dhabi community into agents for sustainability and environmental social justice.',
# 'We are a group of students who are passionate and fully committed to horseback-riding.',
# 'We promote sharing knowledge, learning as a community and writing beautiful, concise code.',
# 'The Marketing Society aims to create and connect marketers within Abu Dhabi and beyond. ',
# 'A group of students meeting to learn and practice archery, the ancient art of shooting with a bow and arrow, thereby developing skills of patience, focus and mental as well as physical strength',
# 'PAUSED focuses on creating a fun and exciting atmosphere where you can take a break and pause the stress in your life by playing video games and board games with others.',
# 'Spacious is a community of people who want to learn and practice mindfulness and compassion. ',
# 'We deal with almost all things animated and works that carefully combine image and text. ',
# 'The mission of SJP is to provide forums to raise awareness of Palestinian human, economic, political, social, and cultural rights.',
# 'We are a student-powered, project-driven group that seeks to institute great design in our world. ',
# 'A SIG for those of us who love linguistics and who want to learn new languages by making friends from all over the world',
# 'Veggie Might is dedicated to promoting vegan lifestyles and animal rights in the NYUAD community.',
# 'weSTEM (Women Empowered in STEM) is established in order to increase the number of girls and women pursuing degrees and careers in science, technology, engineering and mathematics ',
# 'Are you interested in learning a hard skill and working with your hands? Have you always wanted to use power tools and never had an excuse before?',
# 'The Coffee Collective is interested in coffee craft and bringing people together around coffee.',
# 'TASHAN is the South Asian SIG. We aim to spread awareness and understanding of South Asian culture and heritage in the NYUAD community.',
# 'Outed is a fun SIG for cool people to do exciting things outside.'
# ]