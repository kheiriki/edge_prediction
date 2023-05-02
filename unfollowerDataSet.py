import os
import pickle
import gc
currDir = '/home/jack/unfollow_project/FriendFollowerChange'
outputDir = '/home/jack/unfollow_project'

f = open(os.path.join(outputDir, "megaUserSet.pkl"), 'rb')
userSet = pickle.load(f) # all user in set
f.close()

unfollowDataSet = set()
for i in os.listdir(os.path.join(currDir)):
    count = 0
    print("working on " + i)
    print("size of data set: " + str(len(unfollowDataSet)))
    if os.path.isfile(os.path.join(currDir, i)):
        #print("opening..." + i)
        with open(os.path.join(currDir, i), 'rb') as r:
            roundIndex = i[12:14] # the round where unfollowing takes place

            #load files
            roundDelta = pickle.load(r)
            ids = roundDelta.keys()

            for j in ids:
                lostFriends = roundDelta[j][0][1] # j unfollows them
                lostFollowers = roundDelta[j][1][1] # they unfollow j
                for num in lostFollowers:
                    if num.isnumeric() and int(num) in userSet:
                        temp = [num, "uf", j, roundIndex]
                        unfollowDataSet.add(tuple(temp))

                for num in lostFriends:
                    if num.isnumeric() and int(num) in userSet:
                        temp = [j, "uf", num, roundIndex]
                        unfollowDataSet.add(tuple(temp))
                count += 1
                #if count % 1000 == 0:
                #    print(count)


    gc.collect()

file_name = "unfollowDataSet.pkl"
open_file = open(os.path.join(outputDir, file_name), "wb")
pickle.dump(list(unfollowDataSet), open_file)
open_file.close()
f.close()
