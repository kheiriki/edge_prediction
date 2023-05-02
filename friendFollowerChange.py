import os
import pickle
import gc
roundList = ['round1', 'round2', 'round3', 'round4', 'round5', 'round6', 'round7', 'round8', 'round9', 'round10', 'round11', 'round12', 'round13', 'round14', 'round15']
currDir = '/media/EXTHDD/UnfollowData/WeeklySnapshots/round1-15/'
outputDir = '/media/EXTHDD/UnfollowData/WeeklySnapshots/round1-15/'

# data structure
# { userID :[ [{newFriends}, {lostFriends}], [{newFollowers}, {lostFollowers}] ] }

index = 0
while index < (len(roundList) - 1):
    count = 0
    print("working on " + roundList[index] + " and " + roundList[index + 1])

    #open the files
    with open(os.path.join(currDir, roundList[index] + 'FriendFollowers.pkl'), 'rb') as r1:
        with open(os.path.join(currDir, roundList[index + 1] + 'FriendFollowers.pkl'), 'rb') as r2:
            #load files
            firstRound = pickle.load(r1)
            secondRound = pickle.load(r2)
            #find all keys
            keySet = set(firstRound.keys()).intersection(set(secondRound.keys()))
            dicti = {}
            print("...loaded")
            for key in keySet:
                newFriend = secondRound[key][0] - firstRound[key][0]
                lostFriend = firstRound[key][0] - secondRound[key][0]
                newFollower = secondRound[key][1] - firstRound[key][1]
                lostFollower = firstRound[key][1] - secondRound[key][1]
                dicti[key] = [[newFriend, lostFriend], [newFollower, lostFollower]]

                if count % 10000 == 0:
                    print(count)
                count = count + 1

            file_name = str(roundList[index]) + str(roundList[index + 1]) + "Change.pkl"
            open_file = open(os.path.join(outputDir, "FriendFollowerChange", file_name), "wb")
            pickle.dump(dicti, open_file)
            open_file.close()
            r1.close()
            r2.close()
            gc.collect()
    index = index + 1
