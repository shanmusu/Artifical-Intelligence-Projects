#Wedding Problem By Yuchen Wang 2016
#I think this is an NP-hard question and I would like to solve it as fast as possbile, so I choose a kind of
#Greedy Algorithm
#Always put the person who has most friends in the table first.
#This way would give me one correct solution quickly, but it might not be the optimal one.
import re
from sys import argv
#import the friendlist and create a dictionary for each person
tablemaxassign = int(argv[2])
f = open(argv[1],"r")
friendlist = []
frienddic ={}
while True:
    line = f.readline()
    if line:
        line = line.strip('\n')
        friendline = line.split()
        friendnumber = len(friendline)
        for i in range(1,friendnumber):
            if friendline[0] in frienddic:
                frienddic[friendline[0]].append(friendline[i])
            else:
                frienddic[friendline[0]] = [friendline[i]]
            if friendline[i] in frienddic:
                frienddic[friendline[i]].append(friendline[0])
            else:
                frienddic[friendline[i]] = [friendline[0]]
    else:
        break

f.close()

friendnumberdic = {}

for name in frienddic:
    friendnumberdic[name] = len(frienddic[name])

#order the guests based on the number of friends
orderguestlist = sorted(friendnumberdic.iteritems(),key=lambda f:f[1],reverse=True)

tablenumber = 0
tablelist = [[]]
guestassignflag = 0
#function to check is guest is legal for the table
def checklegal(guest,table):
    if len(table) == tablemaxassign:
        return 1
    for name in table:
        if guest in frienddic[name]:
            return 1
    return 0
#put guests one by one into the table
for a in range(0,len(frienddic)):
    for b in range(0,len(tablelist)):
        if checklegal(orderguestlist[a][0],tablelist[b]) == 0:
            tablelist[b].append(orderguestlist[a][0])
            guestassignflag = 1
            break
    if guestassignflag == 0:
        tablelist.append([orderguestlist[a][0]])
    guestassignflag = 0

print str(len(tablelist)) + ' ' + ' '.join(','.join(string)for string in tablelist)


