import psycopg2
import time
import random




def f(query):
    global currentUser

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
            if currentUser is None or currentUser == '':
                print("Please login in first using the \"login\" command")
            else:
                userid = query[1]

                search_query = "select fname, lname from profile where LOWER(userid) LIKE LOWER('%" + userid + "%');"
                cur.execute(search_query)
                rows = cur.fetchall()
                for row in rows:
                    print(" FULL NAME: " + row[0] + " " + row[1])

                message = input("What would you like to say in your request?\n[If you want a default message simply press enter to continue]\n: ")
                if message is None or message == '':
                    message = 'NULL'

                insert_query = "insert into pendingfriends values ('" + currentUser + "','" + userid + "','" + message + "');"
                # print(insert_query)
                try:
                    cur.execute(insert_query)
                    conn.commit()
                    print("Request sent successfully!")
                except Exception as e:
                    print("Request not sent. Error has occurred, please try again.")
                    print(e)


    elif query[0] == 'confirmFriendship':
        if len(query) != 1:
            print("Please enter only the command name \"confirmFriendship\" to see your pending friend requests")
        else:
            if currentUser is None or currentUser == '':
                print("Please login in first using the \"login\" command")
            else:
                # formatted number list of all friend and group requests along with the messages
                print("PENDING REQUESTS:\n")
                search_query = "select userid1, message from pendingfriends where LOWER(userid2)=LOWER('" + currentUser + "');"
                cur.execute(search_query)
                rows = cur.fetchall()
                x = 0
                for row in rows:
                    print(str(x) + ". \n")
                    print(" REQUEST FROM: " + row[0] + "\n  MESSAGE:" + row[1] + "\n")
                    x = x + 1

                #This is for group membership requests
                search_query = "select p.userid, p.gID, p.message from pendingGroupMembers p, groupMembership g where LOWER(g.userid)=LOWER('" + currentUser + "') and g.role = 'Manager' and g.gID = p.gID;"
                cur.execute(search_query)
                rowsOfGroup = cur.fetchall()
                for row in rowsOfGroup:
                    print(str(x) + ". \n")
                    print(" REQUEST FROM: " + row[0] + " TO JOIN: " + row[1] + "\n  MESSAGE:" + row[2] + "\n")
                    x = x + 1

                # prompt to have # of requests confirmed or denied and any not selected are declined and removed from pendingfriends pendinggroupmemebers
                confirmNumbers = input("Type the numbers of the requests you wish to accept\n[Press Enter to Deny All or type \"all\" to accept all]: ")
                confirmNumbers = confirmNumbers.split(' ')
                # give option to confirm or deny all
                if len(confirmNumbers) == 1 and confirmNumbers[0] == '':
                    print("Deny all")
                    counter = 0
                    counterGroup = 0
                    for tuple in range(x):
                        print(x)
                        # print(str(counter) + " confirmed and the info for that is: " + rows[counter][0] + " " + rows[counter][1])
                        if counter < len(rows):
                            delete_query = "delete from pendingfriends where LOWER(userid2)=LOWER('" + currentUser + "') and LOWER(userid1)=LOWER('" + rows[counter][0] + "');"
                            counter = counter + 1
                        else:
                            delete_query = "delete from pendingGroupMembers where LOWER(userid)=LOWER('" + rowsOfGroup[counterGroup][0] + "');"
                            counterGroup = counterGroup + 1
                        cur.execute(delete_query)
                        conn.commit()





                elif len(confirmNumbers) == 1 and confirmNumbers[0] == 'all':
                    print("Accept all")
                    counter = 0
                    counterGroup = 0
                    for tuple in range(x):
                        print(x)
                        friendshipdate = time.strftime('%Y-%m-%d')
                        message = currentUser + " has accepted your friend request."

                        if counter < len(rows):
                            insert_query = "insert into friends values ('" + rows[counter][0] + "','" + currentUser + "','" + friendshipdate + "','" + message + "');"
                            delete_query = "delete from pendingfriends where LOWER(userid2)=LOWER('" + currentUser + "') and LOWER(userid1)=LOWER('" + rows[counter][0] + "');"
                            counter = counter + 1
                        else:
                            # gID userID role
                            insert_query = "insert into groupMembership values ('" + rowsOfGroup[counterGroup][1] + "','" + rowsOfGroup[counterGroup][0] + "','Member');"
                            delete_query = "delete from pendingGroupMembers where LOWER(userid)=LOWER('" + rowsOfGroup[counterGroup][0] + "') and LOWER(gID)=LOWER('" + rowsOfGroup[counterGroup][1] + "');"
                            counterGroup = counterGroup + 1
                        cur.execute(insert_query)
                        cur.execute(delete_query)
                        conn.commit()





                else:
                    # after this move pendingfriends to friends and pendinggroupmemebrs to groupmembers
                    # friends: userid1 userid2 friendshipdate message (userid2 is accepting request from userid1)
                    # delete from pendingFriends where userid1= and userid2=
                    counter = 0
                    print(confirmNumbers)
                    for tuple in range(x):
                        print(x)
                        if str(counter) in confirmNumbers:
                            friendshipdate = time.strftime('%Y-%m-%d')
                            message = currentUser + " has accepted your friend request."
                            # print(str(x) + " confirmed and the info for that is: " + rows[counter][0] + " " + rows[counter][1])
                            if counter < len(rows):
                                insert_query = "insert into friends values ('" + rows[counter][0] + "','" + currentUser + "','" + friendshipdate + "','" + message + "');"
                                # counter = counter + 1
                            else:
                                # gID userID role
                                insert_query = "insert into groupMembership values ('" + rowsOfGroup[counter-len(rows)][1] + "','" + rowsOfGroup[counter-len(rows)][0] + "','Member');"
                                # counter = counter + 1

                            cur.execute(insert_query)


                        if counter < len(rows):
                            delete_query = "delete from pendingfriends where LOWER(userid2)=LOWER('" + currentUser + "') and LOWER(userid1)=LOWER('" + rows[counter][0] + "');"
                            # counter = counter + 1
                        else:
                            delete_query = "delete from pendingGroupMembers where LOWER(userid)=LOWER('" + rowsOfGroup[counter-len(rows)][0] + "') and LOWER(gID)=LOWER('" + rowsOfGroup[counter-len(rows)][1] + "');"
                            # counterGroup = counterGroup + 1

                        cur.execute(delete_query)
                        conn.commit()
                        counter = counter + 1


    elif query[0] == 'displayFriends': #browse user's friends AND their friends
        if len(query) != 1:
            print("Please enter only the command name \"displayFriends\" to see your friends")
        else:
            if currentUser is None or currentUser == '':
                print("Please login in first using the \"login\" command")
            else:
                search_query = "select * from friends where LOWER(userid1)=LOWER('" + currentUser + "') or LOWER(userid2)=LOWER('" + currentUser + "');"
                cur.execute(search_query)
                rows = cur.fetchall()
                print("~~~~~Friends and Friends of Friends~~~~~\n") #display friends names and their userIDs
                for row in rows:
                    if row[0] == currentUser:
                        search_query = "select * from profile where LOWER(userid)=LOWER('" + row[1] + "');"
                        cur.execute(search_query)
                        profileRows = cur.fetchall()
                        for newr in profileRows:
                            print("userID: " + newr[0] + " Name: " + newr[1] + " " + newr[2])

                            #now print the friends of this particular friend
                            search_query = "select * from friends where LOWER(userid1)=LOWER('" + newr[0] + "') or LOWER(userid2)=LOWER('" + newr[0] + "');"
                            cur.execute(search_query)
                            friendsOfFriend = cur.fetchall()
                            for rowFriends in friendsOfFriend:
                                if rowFriends[0] == newr[0]:
                                    search_query = "select * from profile where LOWER(userid)=LOWER('" + rowFriends[1] + "');"
                                    cur.execute(search_query)
                                    profileRows = cur.fetchall()
                                    for rowfromFriendsFriendProfile in profileRows:
                                        # print(rowfromFriendsFriendProfile)
                                        print("\tuserID: " + rowfromFriendsFriendProfile[0] + " Name: " + rowfromFriendsFriendProfile[1] + " " + rowfromFriendsFriendProfile[2])
                                    # print(row[1])
                                else:
                                    search_query = "select * from profile where LOWER(userid)=LOWER('" + rowFriends[0] + "');"
                                    cur.execute(search_query)
                                    profileRows = cur.fetchall()
                                    for rowfromFriendsFriendProfile in profileRows:
                                        # print(rowfromFriendsFriendProfile)
                                        print("\tuserID: " + rowfromFriendsFriendProfile[0] + " Name: " + rowfromFriendsFriendProfile[1] + " " + rowfromFriendsFriendProfile[2])



                    else:
                        search_query = "select * from profile where LOWER(userid)=LOWER('" + row[0] + "');"
                        cur.execute(search_query)
                        profileRows = cur.fetchall()
                        for newr in profileRows:
                            print("userID: " + newr[0] + " Name: " + newr[1] + " " + newr[2])

                            #now print the friends of this particular friend
                            search_query = "select * from friends where LOWER(userid1)=LOWER('" + newr[0] + "') or LOWER(userid2)=LOWER('" + newr[0] + "');"
                            cur.execute(search_query)
                            friendsOfFriend = cur.fetchall()
                            # print()
                            for rowFriends in friendsOfFriend:
                                # print("row 0: " + rowFriends[0] + " newr[0]: " + newr[0])
                                if rowFriends[0] == newr[0]:
                                    search_query = "select * from profile where LOWER(userid)=LOWER('" + rowFriends[1] + "');"
                                    cur.execute(search_query)
                                    profileRows = cur.fetchall()
                                    for rowfromFriendsFriendProfile in profileRows:
                                        # print(rowfromFriendsFriendProfile)
                                        print("\tuserID: " + rowfromFriendsFriendProfile[0] + " Name: " + rowfromFriendsFriendProfile[1] + " " + rowfromFriendsFriendProfile[2])
                                    # print(rowFriends[1])
                                else:
                                    search_query = "select * from profile where LOWER(userid)=LOWER('" + rowFriends[0] + "');"
                                    cur.execute(search_query)
                                    profileRows = cur.fetchall()
                                    for rowFromFriendsFriendProfile in profileRows:
                                        # print(rowFromFriendsFriendProfile)
                                        print("\tuserID: " + rowFromFriendsFriendProfile[0] + " Name: " + rowFromFriendsFriendProfile[1] + " " + rowFromFriendsFriendProfile[2])
                                # print(rowFriends[1])
                #retrieve another or return
                while(1):
                    print("\n")
                    #retrieve entire profile by entering their userID or exit browsing with 0
                    displayThisProfile = input("Type the userID of the profile you wish to view\n[Simply enter 0 to go back to the main menu]:")
                    if displayThisProfile == '0':
                        break;
                    else:
                        #show friend's profile when selected in formatted manner
                        try:
                            # print(displayThisProfile)
                            search_query = "select * from profile where LOWER(userid)=LOWER('" + displayThisProfile + "');"
                            cur.execute(search_query)
                            profileRows = cur.fetchall()
                            print("\n")
                            for newr in profileRows:
                                print("Name: " + newr[1] + " " + newr[2] + "\nuserID: " + newr[0] + "\nemail: " + newr[3] + "\nDOB: " + str(newr[5]) + "\nLast login: " + str(newr[6]))
                        except Exception as e:
                            print(e)
                            print("That friend's profile could not be found. Please try again.")


    elif query[0] == '3Degrees': # provide two user IDs
        if len(query) != 3:
            print("Please enter command with 2 user IDs.")
        else:
            if currentUser is None or currentUser == '':
                print("Please login in first using the \"login\" command")
            else:
                # check if userA is in any of userB's friends up to 3 degrees
                userA = query[1].upper()
                userB = query[2].upper()
                degree = 0
                found = False

                search_query = "select * from friends where LOWER(userid1)=LOWER('" + userB + "') or LOWER(userid2)=LOWER('" + userB + "');"
                cur.execute(search_query)
                rows_1 = cur.fetchall()

                # scan the 1st degree
                print("======================== Scanning 1st Degree ========================")
                for row_1 in rows_1:
                    if row_1[0].upper() == userB:
                        search_query = "select * from profile where LOWER(userid)=LOWER('" + row_1[1] + "');"
                    else:
                        search_query = "select * from profile where LOWER(userid)=LOWER('" + row_1[0] + "');"
                    
                    cur.execute(search_query)
                    profileRows_1 = cur.fetchall()
                    for prow_1 in profileRows_1:
                        print("userID: " + prow_1[0] + " Name: " + prow_1[1] + " " + prow_1[2])

                        if prow_1[0].upper() == userA: # userA found as a friend of userB
                            print("Found " + userA + " as a friend of " + row_1[0].upper() + ". Returning " + str(degree+1))
                            degree += 1
                            found = True
                            break
                    else:
                        continue
                    break
                    
                # scan the 2nd degree
                if not found:
                    print("======================== Scanning 2nd Degree ========================")
                    for row_1 in rows_1:
                        # print(row[1], userB.upper())
                        if row_1[0].upper() == userB:
                            search_query = "select * from profile where LOWER(userid)=LOWER('" + row_1[1] + "');"
                        else:
                            search_query = "select * from profile where LOWER(userid)=LOWER('" + row_1[0] + "');"
                        
                        cur.execute(search_query)
                        profileRows_1 = cur.fetchall()
                        for prow_1 in profileRows_1:
                            search_query = "select * from friends where LOWER(userid1)=LOWER('" + prow_1[0] + "') or LOWER(userid2)=LOWER('" + prow_1[0] + "');"
                            cur.execute(search_query)
                            rows_2 = cur.fetchall()
                            for row_2 in rows_2:
                                if row_2[0] == prow_1[0]:
                                    search_query = "select * from profile where LOWER(userid)=LOWER('" + row_2[1] + "');"
                                else:
                                    search_query = "select * from profile where LOWER(userid)=LOWER('" + row_2[0] + "');"
                                
                                cur.execute(search_query)
                                profileRows_2 = cur.fetchall()
                                for prow_2 in profileRows_2:
                                    print("userID: " + prow_2[0] + " Name: " + prow_2[1] + " " + prow_2[2])
                                    if prow_2[0].upper() == userA:
                                        print("Found " + userA + " as a friend of " + row_2[0].upper() + ". Returning " + str(degree+2))
                                        degree += 2
                                        found = True
                                        break
                                else:
                                    continue
                                break
                            else:
                                continue
                            break
                        else:
                            continue
                        break
                
                # scan the 3rd degree
                if not found:
                    print("======================== Scanning 3rd Degree ========================")
                    for row_1 in rows_1:
                        # print(row[1], userB.upper())
                        if row_1[0].upper() == userB:
                            search_query = "select * from profile where LOWER(userid)=LOWER('" + row_1[1] + "');"
                        else:
                            search_query = "select * from profile where LOWER(userid)=LOWER('" + row_1[0] + "');"
                        
                        cur.execute(search_query)
                        profileRows_1 = cur.fetchall()
                        for prow_1 in profileRows_1:
                            search_query = "select * from friends where LOWER(userid1)=LOWER('" + prow_1[0] + "') or LOWER(userid2)=LOWER('" + prow_1[0] + "');"
                            cur.execute(search_query)
                            rows_2 = cur.fetchall()
                            for row_2 in rows_2:
                                if row_2[0] == prow_1[0]:
                                    search_query = "select * from profile where LOWER(userid)=LOWER('" + row_2[1] + "');"
                                else:
                                    search_query = "select * from profile where LOWER(userid)=LOWER('" + row_2[0] + "');"
                                
                                cur.execute(search_query)
                                profileRows_2 = cur.fetchall()
                                for prow_2 in profileRows_2:
                                    search_query = "select * from friends where LOWER(userid1)=LOWER('" + prow_2[0] + "') or LOWER(userid2)=LOWER('" + prow_2[0] + "');"
                                    cur.execute(search_query)
                                    rows_3 = cur.fetchall()
                                    for row_3 in rows_3:
                                        if row_3[0] == prow_2[0]:
                                            search_query = "select * from profile where LOWER(userid)=LOWER('" + row_3[1] + "');"
                                        else:
                                            search_query = "select * from profile where LOWER(userid)=LOWER('" + row_3[0] + "');"
                                        
                                        cur.execute(search_query)
                                        profileRows_3 = cur.fetchall()
                                        for prow_3 in profileRows_3:
                                            print("userID: " + prow_3[0] + " Name: " + prow_3[1] + " " + prow_3[2])
                                            if prow_3[0].upper() == userA:
                                                print("Found " + userA + " as a friend of " + row_3[0].upper() + ". Returning " + str(degree+3))
                                                degree += 3
                                                found = True
                                                break
                                        else:
                                            continue
                                        break
                                    else:
                                        continue
                                    break
                                else:
                                    continue
                                break
                            else:
                                continue
                            break
                        else:
                            continue
                        break

                # print the results
                print(degree)
                if degree < 1 or degree > 3:
                    print(userA + " is not within 3 degrees of " + userB + ".")
                else:
                    print(userA + " is a " + str(degree) + "-Degree friend of " + userB + "!!!!")



    elif query[0] == 'createGroup': # provide a name, description, and membership limit
        if len(query) != 4:
            print("Please enter a group name, description, and membership limit to create a group.")
        else:
            name = query[1]
            description = query[2]
            maxUsers = query[3]
            gID = name.split(' ')[0] + random.randint(2000, 2018)
            insert_query = "insert into groups values ('" + gID + "','" + name + "','" + description + "','" + maxUsers + "');"
            cur.execute(insert_query)
            conn.commit()
    
    
    elif query[0] == 'initiateAddingGroup': # provide a user ID and a group name
        if len(query) != 3:
            print("Please enter your user ID and the group you wish to join")
        else:
            userid = query[1]
            gID = query[2]

            search_query = "select fname, lname from profile where LOWER(userid) LIKE LOWER('%" + userid + "%');"
            cur.execute(search_query)
            rows = cur.fetchall()
            for row in rows:
                print(" FULL NAME: " + row[0] + " " + row[1])

            search_query = "select name from groups where LOWER(gID) LIKE LOWER('%" + gID + "%');"
            cur.execute(search_query)
            rows = cur.fetchall()
            for row in rows:
                print("GROUP NAME: " + row[0])

            message = input("What would you like to say in your request?\n[Press enter to continue with default message]\n: ")
            if message is None or message == '':
                message = 'NULL'

            insert_query = "insert into pendingGroupMembers values ('" + gID + "','" + userid + "','" + message + "');"
            # print(insert_query)
            try:
                cur.execute(insert_query)
                conn.commit()
                print("Request sent successfully!")
            except Exception as e:
                print("Request not sent. Error has occurred, please try again.")
                print(e)
    
    
    elif query[0] == 'logout': #logout: terminate the application and update the last login time of logged in user
        if len(query) != 1:
            print("Please enter only the command name \"logout\" to logout and close the program")
        else:
            if currentUser is None or currentUser == '':
                print("Please login in first using the \"login\" command")
            else:
                #here update last login of logged in user
                newLoggedTime = time.strftime('%Y-%m-%d %H:%M:%S')
                update_query = "update profile set lastlogin='" + newLoggedTime + "' where LOWER(userid)=LOWER('" + currentUser + "')";
                cur.execute(update_query)
                conn.commit()

                global runProgram
                runProgram = False
    
    
    elif query[0] == 'topUsers': #topUsers k x
        if len(query) != 3:
            print("Please enter the number of users (k) and the amount of days to check (x):\ntopUsers k x")
        else:
            if currentUser is None or currentUser == '':
                print("Please login in first using the \"login\" command")
            else:
                print("topUsers")

    else:
        print('Please use a proper command')


# connect to the database and enter while loop
try:
    # conn = psycopg2.connect("dbname='Nick_Peter_Project2' user='postgres' ' password='MyPassword'");
    conn = psycopg2.connect(dbname="Nick_Peter_Project2", user="njw275", password="MyPassword", host="m-dclap-p302-csd.abudhabi.nyu.edu")
    print("Success")
    cur = conn.cursor()
    currentUser = ''
    runProgram = True

    while(1):

        command = input("socnyuad> ")
        commandSplit = command.split(" ")
        
        # exit/quit the program
        if commandSplit[0] == 'exit' or commandSplit[0] == 'quit':
            break

        f(commandSplit)


except Exception as e:
    print(e)
