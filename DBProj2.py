import psycopg2
import time



def f(query):
    if query[0] == 'createUser':     #first, last name, email address, password, and date of birth,
        if len(query) != 6:
            print("Please enter a First Name, Last Name, email, password, and DOB to create a user")
        else:
            first_name = query[1]
            last_name = query[2]
            email = query[3]
            password = query[4]
            dob = query[5]
            userid = first_name + dob.split('/')[2]
            lastlogin = time.strftime('%Y-%m-%d %H:%M:%S')
            print("Your userid is: " )
            print("User created!")
            insert_query = "insert into profile values ('" + userid + "','" + first_name + "','" + last_name + "','" + email + "','" + password + "','" + dob + "','" + lastlogin + "');"
            cur.execute(insert_query)
            conn.commit()
    elif query[0] == 'login': #userID and password login else make an error message
        if len(query) != 3:
            print("Please enter your userID and password")
        else:
            userID = query[1]
            password = query[2]
            # email = query[3]
            search_query = "select userid, password from profile where LOWER(userid)=LOWER('" + userID + "');"
            cur.execute(search_query)
            rows = cur.fetchall()
            if rows[0][1] == password:
                print("Correct userID and password! Logged in!")
                currentUser = rows[0][0]
            else:
                print("User name or password incorrect.")
            # print(rows[0][1])
            # for row in rows:
            #     print(row)
            # return
    elif query[0] == 'searchForUser': #searchForUser userid fname lname email for substring
        if len(query) != 2:
            print("Please enter the substring you want to search")
        else:
            substring = query[1]

            search_query = "select userid, fname, lname, email from profile where LOWER(userid) LIKE LOWER('%" + substring + "%') OR LOWER(email) LIKE LOWER('%"+ substring +"%') OR LOWER(fname) LIKE LOWER('%" + substring + "%') OR LOWER(lname) LIKE LOWER('%" + substring + "%');"
            cur.execute(search_query)
            rows = cur.fetchall()
            for row in rows:
                print("USERID: " + row[0] + " FULL NAME: " + row[1] + " " + row[2] + " EMAIL: " + row[3])
            # if rows[0][1] == password:
            #     print("Correct userID and password! Logged in!")
            #     currentUser = rows[0][0]
            # else:
            #     print("User name or password incorrect.")
            # print(rows[0][1])
            # for row in rows:
            #     print(row)
            # return
    elif query[0] == 'initiateFriendship': #initiateFriendship userID
        if len(query) != 2:
            print("Please enter the userID of the friend you would like to add")
        else:
            userid = query[1]


            #display full name of user its going to then ask for a personalized message
            #user needs a confirmation for making the request into pendingFriends relation (success or failure feedback)

            search_query = "select userid, fname, lname, email from profile where LOWER(userid) LIKE LOWER('%" + substring + "%') OR LOWER(email) LIKE LOWER('%"+ substring +"%') OR LOWER(fname) LIKE LOWER('%" + substring + "%') OR LOWER(lname) LIKE LOWER('%" + substring + "%');"
            cur.execute(search_query)
            rows = cur.fetchall()
            for row in rows:
                print("USERID: " + row[0] + " FULL NAME: " + row[1] + " " + row[2] + " EMAIL: " + row[3])
            # if rows[0][1] == password:
            #     print("Correct userID and password! Logged in!")
            #     currentUser = rows[0][0]
            # else:
            #     print("User name or password incorrect.")
            # print(rows[0][1])
            # for row in rows:
            #     print(row)
            # return
    else:
        print('Please use a proper command')

try:
    # conn = psycopg2.connect("dbname='Nick_Peter_Project2' user='postgres' ' password='MyPassword'");
    conn = psycopg2.connect(dbname="Nick_Peter_Project2", user="njw275", password="MyPassword", host="m-dclap-p302-csd.abudhabi.nyu.edu")
    print("Success")
    cur = conn.cursor()

    while(1):





        command = raw_input("socnyuad> ")
        commandSplit = command.split(" ");
        # print(commandSplit)
        f(commandSplit)
        # print(query)
        #

except Exception, e:
    print(e)
