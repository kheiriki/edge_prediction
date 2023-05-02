import os
import pickle
import gc
roundList = ['round1', 'round2', 'round3', 'round4', 'round5', 'round6', 'round7', 'round8', 'round9', 'round10', 'round11', 'round12', 'round13', 'round14', 'round15']
currDir = '/media/EXTHDD/UnfollowData/WeeklySnapshots/round1-15/'

errorIDSet = set()
with open(os.path.join(currDir, "errorIDSet.pkl"), 'rb') as f:
    errorIDSet = pickle.load(f) 

for roundName in roundList:
    dicti = {}
    index = 0
    print("working on " + roundName)
    if os.path.isdir(os.path.join(currDir, roundName,'FriendFollowers')):
        for filename in os.listdir(os.path.join(currDir, roundName, 'FriendFollowers')):
            if filename.endswith('.csv'):
                with open(os.path.join(currDir, roundName, 'FriendFollowers', filename)) as f:
                    input = set(f.read().replace('\n', "").split(',')) - errorIDSet
                    key = int(filename.split('_')[0])
                    listLoc = 0 if filename.split('_')[1] == "friends.csv" else 1
                    #print("inserting" + filename)
                    try:
                        lst = dicti[key]
                        lst.insert(listLoc, input)
                        dicti[key] = lst
                    except KeyError:
                        dicti[key] = [input]
                    f.close()
                    if index % 10000 == 0:
                        print(index)
                        gc.collect()
                    index = index + 1


    file_name = str(roundName) + "FriendFollowers.pkl"
    open_file = open(file_name, "wb")
    pickle.dump(dicti, open_file)
    open_file.close()
