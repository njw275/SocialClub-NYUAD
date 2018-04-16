
create table profile (
	userID     varchar(20),
	fname      varchar(15),
	lname      varchar(20),
	email      varchar(30),
	password   varchar(15),
	DOB        date,
	lastlogin  timestamp,
	primary key(userID)
);

create table friends (
	userID1         varchar(20),
	userID2         varchar(20),
	friendshipDate  date,
	message         char(200),
	foreign key(userID1) references profile,
	foreign key(userID2) references profile,
	primary key(userID1,userID2)
);

create table pendingFriends (
	userID1 varchar(20),
	userID2 varchar(20),
	message char(200),
	foreign key(userID1) references profile,
	foreign key(userID2) references profile,
	primary key(userID1,userID2)
);

create table groups (
	gID          varchar(20),
	name         varchar(40),
	maxUsers     integer,
	description  varchar(200),
	primary key(gID)
);

create table groupMembership (
	gID     varchar(20),
	userID  varchar(20),
	role    varchar(15) not null,
	foreign key(gID) references groups,
	foreign key(userID) references profile,
	primary key(gID,userID)
);

create table pendingGroupMembers (
	gID     varchar(20),
	userID  varchar(20),
	message varchar(200),
	foreign key(gID) references groups,
	foreign key(userID) references profile,
	primary key(gID,userID)
);

create table messages (
	msgID       varchar(20),
	fromUserID  varchar(20),
	toUserID    varchar(20) default NULL,
	toGroupID   varchar(20) default NULL,
	message     varchar(200),
	dateSent    timestamp,
	primary key(msgID),
	foreign key(toUserID) references profile,
	foreign key(fromUserID) references profile,
	foreign key(toGroupID) references groups
);

create table messageRecipient (
	msgID     varchar(20),
	toUserID  varchar(20),
	foreign key(msgID) references messages,
	foreign key(toUserID) references profile,
	primary key(msgID,toUserID)
);


--1. profile
--no triggers needed (?)

--2. friends
--no triggers needed (?)

--3. pendingFriends
--alert userID2 that a friend request has been sent to them?
--trigger into friends when friendship is confirmed

--4. messages
--Note that the default values for toUserID/toGroupID are NULL. 

--5. messageRecipient
--no triggers needed (?)

--6. groups
--no triggers needed (?)

--7. groupMembership
--no triggers needed (?)

--8. pendingGroupMembers
--when request sent, alert the manager of the group

--check the maxUsers on the group before accepting new memeber
--trigger the groupMembership update when membership is confirmed

